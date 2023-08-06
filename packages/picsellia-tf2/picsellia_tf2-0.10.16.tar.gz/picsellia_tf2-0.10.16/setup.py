"""Setup script for object_detection with TF2.0."""
import os
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'tensorflow==2.3.1',
    'ipython>=7.16.1',
    'avro-python3==1.9.2.1',
    'apache-beam==2.27.0',
    'pillow==7.2.0',
    'lxml==4.6.2',
    'matplotlib==3.3.4',
    'Cython==0.29.21',
    'contextlib2==0.6.0.post1',
    'tf-slim==1.1.0',
    'six== 1.15.0',
    'pycocotools==2.0.2',
    'lvis==0.5.3',
    'scipy==1.4.1',
    'pandas<=1.1.5',
    'tf-models-official==2.3.0',
    'absl-py==0.10.0',
]

setup(
    name='picsellia_tf2',
    version='0.10.16',
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    packages=(
        [p for p in find_packages(where='.')]),
    package_dir={
        'datasets': os.path.join('slim', 'datasets'),
        'nets': os.path.join('slim', 'nets'),
        'preprocessing': os.path.join('slim', 'preprocessing'),
        'deployment': os.path.join('slim', 'deployment'),
        'scripts': os.path.join('slim', 'scripts'),
    },
    description='Tensorflow Object Detection Library',
    python_requires='>=3.6.9',
)
