import json
import tensorflow as tf
tf.get_logger().setLevel('INFO')

from PIL import Image, ImageDraw
import os
import numpy as np 
import cv2
import functools
import sys
from IPython.display import display
import random

from object_detection.utils import dataset_util
from object_detection.utils import config_util
from object_detection.utils import label_map_util
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from object_detection.builders import dataset_builder
from object_detection.builders import graph_rewriter_builder
from object_detection.builders import model_builder
from object_detection.legacy import trainer
from object_detection.legacy import evaluator
from object_detection import exporter
from object_detection.utils import ops as utils_ops
from object_detection.utils import visualization_utils as vis_util
from object_detection import exporter_lib_v2
from object_detection.protos import pipeline_pb2
from object_detection import model_lib_v2
from tensorflow.python.summary.summary_iterator import summary_iterator
from google.protobuf import text_format
from object_detection.protos import optimizer_pb2

def create_record_files(dict_annotations, train_list, train_list_id, eval_list, 
                        eval_list_id, label_path, record_dir, tfExample_generator, annotation_type):
    '''
        Function used to create the TFRecord files used for the training and evaluation.
        
        TODO: Shard files for large dataset


        Args:
            label_path: Path to the label map file.
            record_dir: Path used to write the records files.
            tfExample_generator: Use the generator from the Picsell.ia SDK by default or provide your own generator.
            annotation_type: "polygon" or "rectangle", depending on your project type. Polygon will compute the masks from your polygon-type annotations. 
    '''
    label_map = label_map_util.load_labelmap(label_path)
    label_map = label_map_util.get_label_map_dict(label_map) 
    datasets = ["train", "eval"]
    
    for dataset in datasets:
        output_path = os.path.join(record_dir, dataset+".record")
        writer = tf.compat.v1.python_io.TFRecordWriter(output_path)
        print(f"Creating record file at {output_path}")
        for variables in tfExample_generator(dict_annotations, train_list, train_list_id, eval_list, 
                            eval_list_id, label_map, ensemble=dataset, annotation_type=annotation_type):
            if isinstance(variables, ValueError):
                print("Error", variables)
            elif annotation_type=="polygon":
                (width, height, xmins, xmaxs, ymins, ymaxs, filename,
                     encoded_jpg, image_format, classes_text, classes, masks) = variables
            
                tf_example = tf.train.Example(features=tf.train.Features(feature={
                    'image/height': dataset_util.int64_feature(height),
                    'image/width': dataset_util.int64_feature(width),
                    'image/filename': dataset_util.bytes_feature(filename),
                    'image/source_id': dataset_util.bytes_feature(filename),
                    'image/encoded': dataset_util.bytes_feature(encoded_jpg),
                    'image/format': dataset_util.bytes_feature(image_format),
                    'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
                    'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
                    'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
                    'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
                    'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
                    'image/object/class/label': dataset_util.int64_list_feature(classes),
                    'image/object/mask': dataset_util.bytes_list_feature(masks)
                }))               
                
            elif annotation_type=="rectangle":
                (width, height, xmins, xmaxs, ymins, ymaxs, filename,
                        encoded_jpg, image_format, classes_text, classes) = variables

                tf_example = tf.train.Example(features=tf.train.Features(feature={
                    'image/height': dataset_util.int64_feature(height),
                    'image/width': dataset_util.int64_feature(width),
                    'image/filename': dataset_util.bytes_feature(filename),
                    'image/source_id': dataset_util.bytes_feature(filename),
                    'image/encoded': dataset_util.bytes_feature(encoded_jpg),
                    'image/format': dataset_util.bytes_feature(image_format),
                    'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
                    'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
                    'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
                    'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
                    'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
                    'image/object/class/label': dataset_util.int64_list_feature(classes)
                    }))
                    
            writer.write(tf_example.SerializeToString())    
        writer.close()
        print('Successfully created the TFRecords: {}'.format(output_path))

def update_num_classes(config_dict, label_map):
    ''' 
    Update the number of classes inside the protobuf configuration dictionnary depending on the number of classes inside the label map.

        Args :
            config_dict:  A configuration dictionnary loaded from the protobuf file with config_util.get_configs_from_pipeline_file().
            label_map: Protobuf label_map loaded with label_map_util.load_labelmap()
        Raises:
            ValueError if the backbone architecture isn't known.
    '''
    model_config = config_dict["model"]
    n_classes = len(label_map.item)
    meta_architecture = model_config.WhichOneof("model")
    if meta_architecture == "faster_rcnn":
        model_config.faster_rcnn.num_classes = n_classes
    elif meta_architecture == "ssd":
        model_config.ssd.num_classes = n_classes
    else:
        raise ValueError("Expected the model to be one of 'faster_rcnn' or 'ssd'.")



def check_batch_size(config_dict):
    model_config = config_dict["model"]
    meta_architecture = model_config.WhichOneof("model")
    batch_size = config_dict["train_config"].batch_size
    if meta_architecture == "faster_rcnn":
        image_resizer = model_config.faster_rcnn.image_resizer
    elif meta_architecture == "ssd":
        image_resizer = model_config.ssd.image_resizer
    else:
        raise ValueError("Unknown model type: {}".format(meta_architecture))

    if image_resizer.HasField("keep_aspect_ratio_resizer") and batch_size>1:
        print("Please be careful, your image resizer is keep_aspect_ratio_resizer and your batch size is >1.")
        print("This mean that all your images should have the same shape. If not then set batch size to 1 or change the image resizer to a fixed_shape_resizer.")
        
    #image_resizer.HasField("fixed_shape_resizer"):

def configure_learning_rate(configs, learning_rate=None, parameters={}):
    keys = parameters.keys()

    if 'lr_type' in keys:
        lr_type = parameters['lr_type']
    else:
        lr_type = 'constant'
    if 'decay_steps' in keys:
        decay_steps = parameters['decay_steps']
    else:
        decay_steps = None
    if 'decay_factor' in keys:
        decay_factor = parameters['decay_factor']
    else:
        decay_factor = None
    if 'staircase' in keys:
        staircase = parameters['staircase']
    else:
        staircase = True
    if 'warmup_lr' in keys:
        warmup_lr = parameters['warmup_lr']
    else:
        warmup_lr = None
    if 'warmup_steps' in keys:
        warmup_steps = parameters['warmup_steps']
    else:
        warmup_steps = None
    if 'total_steps' in keys:
        total_steps = parameters['total_steps']
    else:
        total_steps = None
    if 'momentum' in keys:
        momentum = parameters['momentum']
    else:
        momentum = 0.9
    if 'optimizer' in keys:
        optimizer = parameters['optimizer']
        if optimizer == "rms_prop":
            optimizer_type = "rms_prop_optimizer"
        elif optimizer == "momentum":
            optimizer_type = "momentum_optimizer"
        elif optimizer == "adam":
            optimizer_type = "adam_optimizer"
        else:
            raise TypeError("Optimizer %s is not supported." % optimizer)
    else:
        optimizer_type = configs["train_config"].optimizer.WhichOneof("optimizer")

    if optimizer_type == "rms_prop_optimizer":
        optimizer_config = configs["train_config"].optimizer.rms_prop_optimizer
    elif optimizer_type == "momentum_optimizer":
        optimizer_config = configs["train_config"].optimizer.momentum_optimizer
    elif optimizer_type == "adam_optimizer":
        optimizer_config = configs["train_config"].optimizer.adam_optimizer
    else:
        raise TypeError("Optimizer %s is not supported." % optimizer_type)
    
    if optimizer_type == "rms_prop_optimizer" or optimizer_type == "momentum_optimizer":
        optimizer_config.momentum_optimizer_value = min(max(0.0, momentum), 1.0)

    if lr_type == "constant":
        optimizer_config.learning_rate.constant_learning_rate.learning_rate = learning_rate
    elif lr_type == "exponential_decay":
        if decay_steps != None and decay_factor != None:
            optimizer_config.learning_rate.exponential_decay_learning_rate.initial_learning_rate = learning_rate
            optimizer_config.learning_rate.exponential_decay_learning_rate.decay_steps = decay_steps
            optimizer_config.learning_rate.exponential_decay_learning_rate.decay_factor = decay_factor
            optimizer_config.learning_rate.exponential_decay_learning_rate.staircase = staircase
    elif lr_type == "manual_step":
        optimizer_config.learning_rate.manual_step_learning_rate.initial_learning_rate = learning_rate
        steps = []
        lrs = []
        for k in parameters.keys():
            if k[:-1] == 'step_':
                step = int(k[-1])
                if 'lr_' + str(step) in parameters.keys():
                    steps.append(parameters[k])
                    lrs.append(parameters['lr_' + str(step)])
        zipped = zip(steps, lrs)
        schedules = sorted(zipped, key = lambda x: x[0]) 
        for i, schedule in enumerate(schedules):
            print(schedule)
            sched = optimizer_config.learning_rate.manual_step_learning_rate.schedule
            print(sched)
            # sched.step = schedule[0]
            sched.learning_rate = schedule[1]
            optimizer_config.learning_rate.manual_step_learning_rate.schedule.append(sched)
            # optimizer_config.learning_rate.manual_step_learning_rate.schedule.step = schedule[0]
            # optimizer_config.learning_rate.manual_step_learning_rate.schedule.learning_rate = schedule[1]
        print(optimizer_config)
    elif lr_type == "cosine_decay":
        optimizer_config.learning_rate.cosine_decay_learning_rate.learning_rate_base = learning_rate
        optimizer_config.learning_rate.cosine_decay_learning_rate.total_steps = total_steps
        optimizer_config.learning_rate.cosine_decay_learning_rate.warmup_learning_rate = warmup_lr
        optimizer_config.learning_rate.cosine_decay_learning_rate.warmup_steps = warmup_steps
    print(optimizer_config)

def set_image_resizer(config_dict, shape):
    '''
        Update the image resizer shapes.

        Args:
            config_dict:  A configuration dictionnary loaded from the protobuf file with config_util.get_configs_from_pipeline_file().
            shape: The new shape for the image resizer. 
                    [max_dimension, min_dimension] for the keep_aspect_ratio_resizer (default resizer for faster_rcnn backbone). 
                    [width, height] for the fixed_shape_resizer (default resizer for SSD backbone)

        Raises: 
            ValueError if the backbone architecture isn't known.
    '''

    model_config = config_dict["model"]
    meta_architecture = model_config.WhichOneof("model")
    if meta_architecture == "faster_rcnn":
        image_resizer = model_config.faster_rcnn.image_resizer
    elif meta_architecture == "ssd":
        image_resizer = model_config.ssd.image_resizer
    else:
        raise ValueError("Unknown model type: {}".format(meta_architecture))
    
    if image_resizer.HasField("keep_aspect_ratio_resizer"):
        image_resizer.keep_aspect_ratio_resizer.max_dimension = shape[1]
        image_resizer.keep_aspect_ratio_resizer.min_dimension = shape[0]

    elif image_resizer.HasField("fixed_shape_resizer"):
        image_resizer.fixed_shape_resizer.height = shape[1]
        image_resizer.fixed_shape_resizer.width = shape[0]

def edit_eval_config(config_dict, annotation_type, eval_number):
    '''
        Update the eval_config protobuf message from a config_dict.
        Checks if the metrics_set is the right one then update the evaluation number. 

        Args:
            config_dict: A configuration dictionnary loaded from the protobuf file with config_util.get_configs_from_pipeline_file().
            annotation_type: Should be either "rectangle" or "polygon". Depends on your project type. 
            eval_number: The number of images you want to run your evaluation on. 
        
        Raises:
            ValueError Wrong annotation type provided. If you didn't provide the right annotation_type
            ValueError "eval_number isn't an int". If you didn't provide a int for the eval_number.
    '''


    eval_config = config_dict["eval_config"]
    eval_config.num_visualizations = 0
    if annotation_type=="rectangle":
        eval_config.metrics_set[0] = "coco_detection_metrics"
    elif annotation_type=="polygon":
        eval_config.metrics_set[0] = "coco_mask_metrics"
    else:
        raise ValueError("Wrong annotation type provided")
    if isinstance(eval_number, int):
        eval_config.num_examples = eval_number
    else: 
        raise ValueError("eval_number isn't an int")


def update_different_paths(config_dict, ckpt_path, label_map_path, train_record_path, eval_record_path):
    '''
        Update the different paths required for the whole configuration.

    Args: 
        config_dict: A configuration dictionnary loaded from the protobuf file with config_util.get_configs_from_pipeline_file().
        ckpt_path: Path to your checkpoint. 
        label_map_path: Path to your label map.
        train_record_path: Path to your train record file.
        eval_record_path: Path to your eval record file.

    '''
    config_dict["train_config"].fine_tune_checkpoint = ckpt_path
    config_util._update_label_map_path(config_dict, label_map_path)
    config_util._update_tf_record_input_path(config_dict["train_input_config"], train_record_path)
    config_util._update_tf_record_input_path(config_dict["eval_input_config"], eval_record_path)


def edit_masks(config_dict, mask_type="PNG_MASKS"):
    """
        Update the configuration to take into consideration the right mask_type. By default we record mask as "PNG_MASKS".

        Args:
            config_dict: A configuration dictionnary loaded from the protobuf file with config_util.get_configs_from_pipeline_file().
            mask_type: String name to identify mask type, either "PNG_MASKS" or "NUMERICAL_MASKS"
        Raises:
            ValueError if the mask type isn't known.
    """

    config_dict["train_input_config"].load_instance_masks = True
    config_dict["eval_input_config"].load_instance_masks = True
    if mask_type=="PNG_MASKS":
        config_dict["train_input_config"].mask_type = 2
        config_dict["eval_input_config"].mask_type = 2
    elif mask_type=="NUMERICAL_MASKS":
        config_dict["train_input_config"].mask_type = 1
        config_dict["eval_input_config"].mask_type = 1
    else:
        raise ValueError("Wrong Mask type provided")


def set_variable_loader(config_dict, incremental_or_transfer, FromSratch=False):
    '''
        Choose the training type. If incremental then all variables from the checkpoint are loaded, used to resume a training.
    Args:
        config_dict: A configuration dictionnary loaded from the protobuf file with config_util.get_configs_from_pipeline_file().
        incremental_or_transfer: String name to identify use case "transfer" of "incremental".
    Raises:
        ValueError
    '''
    if not FromSratch:
        config_dict["train_config"].from_detection_checkpoint = True



def edit_config(model_selected, input_config_dir, output_config_dir, num_steps, label_map_path, 
                record_dir, eval_number, annotation_type, batch_size=None, learning_rate=None, 
                parameters={}, resizer_size=None, incremental_or_transfer="transfer"):
    '''
        Wrapper to edit the essential values inside the base configuration protobuf file provided with an object-detection/segmentation checkpoint.
        This configuration file is what will entirely define your model, pre-processing, training, evaluation etc. It is the most important file of a model with the checkpoint file and should never be deleted. 
        This is why it is saved in almost every directory where you did something to keep redondancy but also to be sure to have the right config file used at this moment.
        For advanced users, if you want to dwell deep inside the configuration file you should read the proto definitions inside the proto directory of the object-detection API.

        Args: 
            Required:
                model_selected: The checkpoint you want to resume from.
                config_output_dir: The path where you want to save your edited protobuf configuration file.
                num_steps: The number of steps you want to train on.
                label_map_path: The path to your label_map.pbtxt file.
                record_dir: The path to the directory where your TFRecord files are saved.
                eval_number: The number of images you want to evaluate on.
                annotation_type: Should be either "rectangle" or "polygon", depending on how you annotated your images.

            Optional:
                batch_size: The batch size you want to use. If not provided it will use the previous one. 
                learning_rate: The learning rate you want to use for the training. If not provided it will use the previous one. 
                                Please see config_utils.update_initial_learning_rate() inside the object_detection folder for indepth details on what happens when updating it.
                resizer_size: The shape used to update your image resizer. Please see set_image_resizer() for more details on this. If not provided it will use the previous one.            

    '''

    
    file_list = os.listdir(model_selected)
    ckpt_ids = []
    for p in file_list:
        if "index" in p:
            if "-" in p:
                ckpt_ids.append(int(p.split('-')[1].split('.')[0]))
    if len(ckpt_ids)>0:
        ckpt_path = os.path.join(model_selected,"ckpt-{}".format(str(max(ckpt_ids))))
    
    else:
        ckpt_path = os.path.join(model_selected, "ckpt")

    configs = config_util.get_configs_from_pipeline_file(os.path.join(input_config_dir,'pipeline.config'))
    label_map = label_map_util.load_labelmap(label_map_path)

    config_util._update_train_steps(configs, num_steps)
    update_different_paths(configs, ckpt_path=ckpt_path, 
                            label_map_path=label_map_path, 
                            train_record_path=os.path.join(record_dir, "train.record"), 
                            eval_record_path=os.path.join(record_dir,"eval.record"))

    if learning_rate is not None:
        configure_learning_rate(configs, learning_rate, parameters)
    if batch_size is not None:
        config_util._update_batch_size(configs, batch_size)
    check_batch_size(configs)

    if annotation_type=="polygon":
        edit_masks(configs, mask_type="PNG_MASKS")
   
    if resizer_size is not None:
        set_image_resizer(configs, resizer_size)

    if incremental_or_transfer is not None:
        set_variable_loader(configs, incremental_or_transfer)
    
    edit_eval_config(configs, annotation_type, eval_number)
    update_num_classes(configs, label_map)
    config_proto = config_util.create_pipeline_proto_from_configs(configs)
    config_util._update_batch_size(configs, batch_size)
    config_util.save_pipeline_config(config_proto, directory=output_config_dir)
    print(f"Configuration successfully edited and saved at {output_config_dir}")


def train(ckpt_dir='', config_dir='', train_steps=None, use_tpu=False, checkpoint_every_n=100,
          record_summaries=True):

    if config_dir.endswith('.config'):
        if not os.path.isfile(config_dir):
            raise FileNotFoundError('No config file found at {}'.format(config_dir))
        else:
            config = config_dir
    else:
        if os.path.isdir(config_dir):
            files = os.listdir(config_dir)
            file_found = False
            for f in files:
                if not file_found:
                    if f.endswith('.config'):
                        config = os.path.join(config_dir,f)
                        file_found = True 
    if not file_found:
        raise FileNotFoundError('No config file found in this directory {}'.format(config_dir))

    tf.config.set_soft_device_placement(True)
    strategy = tf.compat.v2.distribute.MirroredStrategy()

    with strategy.scope():
      model_lib_v2.train_loop(
          pipeline_config_path=config,
          model_dir=ckpt_dir,
          train_steps=train_steps,
          use_tpu=use_tpu,
          checkpoint_every_n=checkpoint_every_n,
          record_summaries=record_summaries)
# def train(master='', save_summaries_secs=30, task=0, num_clones=1, clone_on_cpu=False, worker_replicas=1, ps_tasks=0, 
#                     ckpt_dir='', conf_dir='', train_config_path='', input_config_path='', model_config_path=''):   
   

#     pipeline_config_path = os.path.join(conf_dir,"pipeline.config")
#     configs = config_util.get_configs_from_pipeline_file(pipeline_config_path)

#     tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
#     assert ckpt_dir, '`ckpt_dir` is missing.'
#     if task == 0: tf.compat.v1.gfile.MakeDirs(ckpt_dir)
#     if pipeline_config_path:
#         configs = config_util.get_configs_from_pipeline_file(pipeline_config_path)
#         if task == 0:
#             tf.compat.v1.gfile.Copy(pipeline_config_path,
#                           os.path.join(ckpt_dir, 'pipeline.config'),
#                           overwrite=True)
#     else:
#         configs = config_util.get_configs_from_multiple_files(
#                         model_config_path=model_config_path,
#                         train_config_path=train_config_path,
#                         train_input_config_path=input_config_path)
#         if task == 0:
#             for name, config in [('model.config', model_config_path),
#                                 ('train.config', train_config_path),
#                                 ('input.config', input_config_path)]:
#                 tf.compat.v1.gfile.Copy(config, os.path.join(ckpt_dir, name),
#                             overwrite=True)

#     model_config = configs['model']
#     train_config = configs['train_config']
#     input_config = configs['train_input_config']

#     model_fn = functools.partial(
#         model_builder.build,
#         model_config=model_config,
#         is_training=True)

#     def get_next(config):
#         return dataset_builder.make_initializable_iterator(
#             dataset_builder.build(config)).get_next()

#     create_input_dict_fn = functools.partial(get_next, input_config)

#     env = json.loads(os.environ.get('TF_CONFIG', '{}'))
#     cluster_data = env.get('cluster', None)
#     cluster = tf.train.ClusterSpec(cluster_data) if cluster_data else None
#     task_data = env.get('task', None) or {'type': 'master', 'index': 0}
#     task_info = type('TaskSpec', (object,), task_data)

#     # Parameters for a single worker.
#     ps_tasks = 0
#     worker_replicas = 1
#     worker_job_name = 'lonely_worker'
#     task = 0
#     is_chief = True
#     master = ''

#     if cluster_data and 'worker' in cluster_data:
#     # Number of total worker replicas include "worker"s and the "master".
#         worker_replicas = len(cluster_data['worker']) + 1
#     if cluster_data and 'ps' in cluster_data:
#         ps_tasks = len(cluster_data['ps'])

#     if worker_replicas > 1 and ps_tasks < 1:
#         raise ValueError('At least 1 ps task is needed for distributed training.')

#     if worker_replicas >= 1 and ps_tasks > 0:
#     # Set up distributed training.
#         server = tf.train.Server(tf.train.ClusterSpec(cluster), protocol='grpc',
#                                 job_name=task_info.type,
#                                 task_index=task_info.index)
#         if task_info.type == 'ps':
#             server.join()
#             return

#         worker_job_name = '%s/task:%d' % (task_info.type, task_info.index)
#         task = task_info.index
#         is_chief = (task_info.type == 'master')
#         master = server.target

#     graph_rewriter_fn = None
#     if 'graph_rewriter_config' in configs:
#         graph_rewriter_fn = graph_rewriter_builder.build(
#             configs['graph_rewriter_config'], is_training=True)

#     trainer.train(
#         create_input_dict_fn,
#         model_fn,
#         train_config,
#         master,
#         task,
#         num_clones,
#         worker_replicas,
#         clone_on_cpu,
#         ps_tasks,
#         worker_job_name,
#         is_chief,
#         ckpt_dir,
#         graph_hook_fn=graph_rewriter_fn)

def evaluate(metrics_dir='', config='', ckpt_dir=''):
    '''
        Function used to evaluate your trained model. 

        Args: 
            Required:               
                eval_dir: The directory where the tfevent file will be saved.
                config: The protobuf configuration file or directory.
                checkpoint_dir: The directory where the checkpoint you want to evaluate is.
            
            Optional:
                eval_training_data: Is set to True the evaluation will be run on the training dataset.

        Returns:
            A dictionnary of metrics ready to be sent to the picsell.ia platform.
    '''
    if config.endswith('.config'):
        if not os.path.isfile(config):
            raise FileNotFoundError('No config file found at {}'.format(config)) 
    else:
        if os.path.isdir(config):
            files = os.listdir(config)
            file_found = False
            for f in files:
                if not file_found:
                    if f.endswith('.config'):
                        config = os.path.join(config,f)
                        file_found = True 
    if not file_found:
        raise FileNotFoundError('No config file found in this directory {}'.format(config))

    tf.config.set_soft_device_placement(True)
    model_lib_v2.eval_continuously(
        pipeline_config_path=config,
        model_dir=metrics_dir,
        train_steps=None,
        sample_1_of_n_eval_examples=1,
        sample_1_of_n_eval_on_train_examples=(1),
        checkpoint_dir=ckpt_dir,
        wait_interval=4, timeout=5)


def tf_events_to_dict(path, type=''):
    '''Get a dictionnary of scalars from the tfevent inside the training directory.

        Args: 
            path: The path to the directory where a tfevent file is saved or the path to the file.
        
        Returns:
            A dictionnary of scalars logs.
    '''
    log_dict = {}
    if path.startswith('events.out'):
        if not os.path.isfile(path):
            raise FileNotFoundError('No tfEvent file found at {}'.format(path)) 
    else:
        if os.path.isdir(path):
            files = os.listdir(path)
            file_found = False
            for f in files:
                if not file_found:
                    if f.startswith('events.out'):
                        path = os.path.join(path,f)
                        file_found = True 
    if not file_found:
        raise FileNotFoundError('No tfEvent file found in this directory {}'.format(path))
    for summary in summary_iterator(path):
        for v in summary.summary.value:
            if not 'image' in v.tag:
                key = '-'.join(v.tag.split('/'))
                if v.tag in log_dict.keys():
                    decoded = tf.compat.v1.decode_raw(v.tensor.tensor_content, tf.float32)
                    log_dict[v.tag]["steps"].append(str(len(log_dict[v.tag]["steps"])+1))
                    log_dict[v.tag]["values"].append(str(tf.cast(decoded, tf.float32).numpy()[0]))
                else:
                    decoded = tf.compat.v1.decode_raw(v.tensor.tensor_content, tf.float32)
                    if type=='train':
                        scalar_dict = {"steps": [0], "values": [str(tf.cast(decoded, tf.float32).numpy()[0])]}
                        log_dict[v.tag] = scalar_dict
                    if type=='eval':
                        log_dict[v.tag] = str(tf.cast(decoded, tf.float32).numpy()[0])

    return log_dict

def export_graph(ckpt_dir, exported_model_dir, config_dir,
    config_override='', input_type="image_tensor", use_side_inputs=False,
    side_input_shapes='', side_input_types='', side_input_names=''):
    ''' Export your checkpoint to a saved_model.pb file
        Args:
            Required:
                ckpt_dir: The directory where your checkpoint to export is located.
                exported_model_dir: The directory where you want to save your model.
                pipeline_çonfig_path: The directory where you protobuf configuration is located.

    '''
    pipeline_config_path = os.path.join(config_dir,"pipeline.config")
    pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
    with tf.io.gfile.GFile(pipeline_config_path, 'r') as f:
        text_format.Merge(f.read(), pipeline_config)
    text_format.Merge(config_override, pipeline_config)
    exporter_lib_v2.export_inference_graph(
        input_type, pipeline_config, ckpt_dir,
        exported_model_dir, use_side_inputs, side_input_shapes,
        side_input_types, side_input_names)
        

def infer(path, exported_model_dir, label_map_path, results_dir, disp=True, num_infer=5, min_score_thresh=0.7, from_tfrecords=False):
    ''' Use your exported model to infer on a path list of images. 

        Args:
            Required:
                path_list: A list of images paths to infer on. Or the path to the TFRecord directory if infering from TFRecords files.
                exported_model_dir: The path used to saved your model.
                label_mapt_path: The path to your label_map file.
                results_dir: The directory where you want to save your infered images.

            Optional:
                disp: Set to false if you are not in an interactive python environment. Will display image in the environment if set to True.
                num_infer: The number of images you want to infer on. 
                min_score_tresh: The minimal confidence treshold to keep the detection.

    '''
    saved_model_path = os.path.join(exported_model_dir, "saved_model")
    model = tf.saved_model.load(saved_model_path)
    if not from_tfrecords:
        path_list = path
        random.shuffle(path_list)
        
    elif from_tfrecords:
        eval_path = os.path.join(path, "eval.record")
        path_list = []
        for example in tf.compat.v1.python_io.tf_record_iterator(eval_path):
            tf_examp = tf.train.Example.FromString(example)
            for key in tf_examp.features.feature:
                if key=="image/filename":
                    path_list.append(tf_examp.features.feature[key].bytes_list.value[0].decode("utf-8"))
    path_list = path_list[:num_infer]
    category_index = label_map_util.create_category_index_from_labelmap(label_map_path)
    counter=0
    for img_path in path_list:
        try:
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_tensor = np.expand_dims(img, 0)
            result = model(img_tensor)
            label_id_offset = 0
            print(result['detection_classes'][0])
            if 'detection_masks' in result:
                # we need to convert np.arrays to tensors
                detection_masks = tf.convert_to_tensor(result['detection_masks'][0])
                detection_boxes = tf.convert_to_tensor(result['detection_boxes'][0])

                # Reframe the the bbox mask to the image size.
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                            detection_masks, detection_boxes,
                            img.shape[1], img.shape[2])
                detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5,
                                                    tf.uint8)
                result['detection_masks_reframed'] = detection_masks_reframed.numpy()


            vis_util.visualize_boxes_and_labels_on_image_array(
                img,
                (result['detection_boxes'][0]).numpy(),
                (result['detection_classes'][0]).numpy().astype(int),
                (result['detection_scores'][0]).numpy(),
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=200,
                min_score_thresh=.30,
                agnostic_mode=False,
                instance_masks=result.get('detection_masks_reframed', None),
                line_thickness=8)

            img_name = img_path.split("/")[-1]
            Image.fromarray(img).save(os.path.join(results_dir,img_name))
            
            if disp == True:
                display(Image.fromarray(img))

        except:
            counter+=1
            continue
    if counter>0:
        print(f"{counter} weren't infered")

def run():
    pass