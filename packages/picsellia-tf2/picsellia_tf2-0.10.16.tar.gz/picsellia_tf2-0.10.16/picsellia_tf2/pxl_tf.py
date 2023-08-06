from PIL import Image, ImageDraw, ExifTags
import io
import numpy as np 

def tf_vars_generator(
    dict_annotations, train_list, train_list_id, eval_list, 
    eval_list_id, label_map=None,  ensemble='train', annotation_type="polygon"
    ):
        """THIS FUNCTION IS MAINTAINED FOR TENSORFLOW 1.X
        Generator for variable needed to instantiate a tf example needed for training.

        Args :
            label_map (tf format)
            ensemble (str) : Chose between train & test
            annotation_type: "polygon", "rectangle" or "classification"

        Yields :
            (width, height, xmins, xmaxs, ymins, ymaxs, filename,
                   encoded_jpg, image_format, classes_text, classes, masks)

        Raises:
            ResourceNotFoundError: If you don't have performed your trained test split yet
                                   If images can't be opened

        """
        if annotation_type not in ["polygon", "rectangle", "classification"]:
            raise ValueError("Please select a valid annotation_type")

        if label_map is None and annotation_type != "classification":
            raise ValueError("Please provide a label_map dict loaded from a protobuf file when working with object detection")

        if annotation_type == "classification":
            label_map = {v: int(k) for k, v in label_map.items()}

        if ensemble == "train":
            path_list = train_list
            id_list = train_list_id
        else:
            path_list = eval_list
            id_list = eval_list_id

        if annotation_type == "rectangle":
            for ann in dict_annotations["annotations"]:
                for an in ann["annotations"]:
                    if "polygon" in an.keys():
                        annotation_type = "rectangle from polygon"
                        break

        print(f"annotation type used for the variable generator: {annotation_type}")

        for path, ID in zip(path_list, id_list):
            xmins = []
            xmaxs = []
            ymins = []
            ymaxs = []
            classes_text = []
            classes = []
            masks = []

            internal_picture_id = ID

            image = Image.open(path)
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if exif[orientation] == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif exif[orientation] == 6:
                    image = image.transpose(Image.ROTATE_270)
                elif exif[orientation] == 8:
                    image = image.transpose(Image.ROTATE_90)

            except (AttributeError, KeyError, IndexError):
                # cases: image don't have getexif
                pass

            encoded_jpg = io.BytesIO()
            image.save(encoded_jpg, format="JPEG")
            encoded_jpg = encoded_jpg.getvalue()

            width, height = image.size
            filename = path.encode('utf8')
            image_format = path.split('.')[-1]
            image_format = bytes(image_format.encode('utf8'))

            if annotation_type == "polygon":
                for image_annoted in dict_annotations["annotations"]:
                    if internal_picture_id == image_annoted["internal_picture_id"]:
                        for a in image_annoted["annotations"]:
                            try:
                                if "polygon" in a.keys():
                                    geo = a["polygon"]["geometry"]
                                    poly = []
                                    for coord in geo:
                                        poly.append([[coord["x"], coord["y"]]])
                                    poly = np.array(poly, dtype=np.float32)
                                    mask = np.zeros((height, width), dtype=np.uint8)
                                    mask = Image.fromarray(mask)
                                    ImageDraw.Draw(mask).polygon(poly, outline=1, fill=1)
                                    maskByteArr = io.BytesIO()
                                    mask.save(maskByteArr, format="JPEG")
                                    maskByteArr = maskByteArr.getvalue()
                                    masks.append(maskByteArr)

                                    x, y, w, h = cv2.boundingRect(poly)
                                    x1_norm = np.clip(x / width, 0, 1)
                                    x2_norm = np.clip((x + w) / width, 0, 1)
                                    y1_norm = np.clip(y / height, 0, 1)
                                    y2_norm = np.clip((y + h) / height, 0, 1)

                                    xmins.append(x1_norm)
                                    xmaxs.append(x2_norm)
                                    ymins.append(y1_norm)
                                    ymaxs.append(y2_norm)
                                    classes_text.append(a["label"].encode("utf8"))
                                    label_id = label_map[a["label"]]
                                    classes.append(label_id)

                            except Exception:
                                pass

                yield (width, height, xmins, xmaxs, ymins, ymaxs, filename,
                       encoded_jpg, image_format, classes_text, classes, masks)

            if annotation_type == "rectangle from polygon":
                for image_annoted in dict_annotations["annotations"]:
                    if internal_picture_id == image_annoted["internal_picture_id"]:
                        for a in image_annoted["annotations"]:
                            if "polygon" in a.keys():
                                geo = a["polygon"]["geometry"]
                                poly = []
                                for coord in geo:
                                    poly.append([[coord["x"], coord["y"]]])

                                poly = np.array(poly, dtype=np.float32)

                                x, y, w, h = cv2.boundingRect(poly)
                                x1_norm = np.clip(x / width, 0, 1)
                                x2_norm = np.clip((x + w) / width, 0, 1)
                                y1_norm = np.clip(y / height, 0, 1)
                                y2_norm = np.clip((y + h) / height, 0, 1)

                                xmins.append(x1_norm)
                                xmaxs.append(x2_norm)
                                ymins.append(y1_norm)
                                ymaxs.append(y2_norm)
                                classes_text.append(a["label"].encode("utf8"))
                                label_id = label_map[a["label"]]
                                classes.append(label_id)

                            elif 'rectangle' in a.keys():
                                xmin = a["rectangle"]["left"]
                                ymin = a["rectangle"]["top"]
                                w = a["rectangle"]["width"]
                                h = a["rectangle"]["height"]
                                xmax = xmin + w
                                ymax = ymin + h
                                ymins.append(np.clip(ymin / height, 0, 1))
                                ymaxs.append(np.clip(ymax / height, 0, 1))
                                xmins.append(np.clip(xmin / width, 0, 1))
                                xmaxs.append(np.clip(xmax / width, 0, 1))

                                classes_text.append(a["label"].encode("utf8"))
                                label_id = label_map[a["label"]]
                                classes.append(label_id)

                yield (width, height, xmins, xmaxs, ymins, ymaxs, filename,
                       encoded_jpg, image_format, classes_text, classes)

            elif annotation_type == "rectangle":
                for image_annoted in dict_annotations["annotations"]:
                    if internal_picture_id == image_annoted["internal_picture_id"]:
                        for a in image_annoted["annotations"]:
                            try:
                                if 'rectangle' in a.keys():
                                    xmin = a["rectangle"]["left"]
                                    ymin = a["rectangle"]["top"]
                                    w = a["rectangle"]["width"]
                                    h = a["rectangle"]["height"]
                                    xmax = xmin + w
                                    ymax = ymin + h
                                    ymins.append(np.clip(ymin / height, 0, 1))
                                    ymaxs.append(np.clip(ymax / height, 0, 1))
                                    xmins.append(np.clip(xmin / width, 0, 1))
                                    xmaxs.append(np.clip(xmax / width, 0, 1))
                                    classes_text.append(a["label"].encode("utf8"))
                                    label_id = label_map[a["label"]]
                                    classes.append(label_id)
                            except Exception:
                                print(f"An error occured with the image {path}")

                yield (width, height, xmins, xmaxs, ymins, ymaxs, filename,
                       encoded_jpg, image_format, classes_text, classes)

            if annotation_type == "classification":
                for image_annoted in dict_annotations["annotations"]:
                    if internal_picture_id == image_annoted["internal_picture_id"]:
                        for a in image_annoted["annotations"]:
                            classes_text.append(a["label"].encode("utf8"))
                            label_id = label_map[a["label"]]
                            classes.append(label_id)

                yield (width, height, filename, encoded_jpg, image_format,
                       classes_text, classes)