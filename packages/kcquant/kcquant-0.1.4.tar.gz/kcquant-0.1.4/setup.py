# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kcquant']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0',
 'imutils>=0.5.4,<0.6.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'opencv-python>=4.5.1,<5.0.0',
 'pandas>=1.2.2,<2.0.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'kcquant',
    'version': '0.1.4',
    'description': 'Color quantization toolkit for exploratory data analysis of images.',
    'long_description': '# kcquant\n\nThis package enables you to perform exploratory data analysis on images, as well as\neasily quantize the colors of an image to be used for machine learning applications.\n\nTo install this package, use\n\n```bash\npip install kcquant\n```\n\n![image](https://raw.githubusercontent.com/kbkus/kcquant/main/kcquant/Images/get_colors.png?token=AME4SBXQAWML7AMDXM34FMDAGRBT2)\n',
    'author': 'kbkus',
    'author_email': 'kacikus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kbkus/kcquant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
