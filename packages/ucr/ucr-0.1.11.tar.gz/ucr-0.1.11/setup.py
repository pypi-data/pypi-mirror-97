# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ucr',
 'ucr.core',
 'ucr.core.architecture',
 'ucr.core.architecture.backbone',
 'ucr.core.architecture.head',
 'ucr.core.architecture.neck',
 'ucr.core.architecture.transform',
 'ucr.core.dataloader',
 'ucr.core.postprocess',
 'ucr.core.preprocess',
 'ucr.core.preprocess.text_image_aug',
 'ucr.inference',
 'ucr.inference.torch',
 'ucr.utils']

package_data = \
{'': ['*'], 'ucr.utils': ['dict/*', 'fonts/*']}

install_requires = \
['geos>=0.2.3,<0.3.0',
 'imgaug>=0.4.0,<0.5.0',
 'numpy<1.20.0',
 'opencv-python>=4.1.0,<5.0.0',
 'torchvision>=0.9.0,<0.10.0',
 'tqdm>=4.40,<5.0',
 'wandb>=0.8.18,<0.9.0']

setup_kwargs = {
    'name': 'ucr',
    'version': '0.1.11',
    'description': 'Universal Character Recognizer (UCR): Simple, Intuitive, Extensible, Multi-Lingual OCR engine',
    'long_description': '',
    'author': 'Abhigyan Raman',
    'author_email': 'abhigyan@docyard.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
