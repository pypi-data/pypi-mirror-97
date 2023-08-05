# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stacki3']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['stacki3 = stacki3:main']}

setup_kwargs = {
    'name': 'stacki3',
    'version': '1.0.0',
    'description': 'Stack layout for i3/sway wm.',
    'long_description': "# stacki3\n\nSimple stack layout for i3/sway wm.\n\n## How it works\n\nThe main idea is this - I only want max two columns on the screen.\nMore windows should be spawn vertically.\n\n![Preview](./preview.gif)\n\n(proportion set with `stacki3 45`)\n\n_stacki3_ does only 3 things:\n\n- when there is only **one** window set split to `horizontal`\n- when there are exactly **two** windows set split to `vertical` on both windows\n- _optionally_ when proportion is set with `width` argument (like in preview) resize the right window\n\nThat's it!\n\n## Instalation\n\n1. Install the package\n\n```bash\npip install --user stacki3\n```\n\n2. Inside your i3/sway config add\n\n```i3\n# Default with splitting 50:50\nexec stacki3\n# OR\n# Split first two windows 55:45\nexec stacki3 45\n```\n\n3. Log out and log back in\n\n## Inspiration\n\n[i3-master-stack](https://github.com/windwp/i3-master-stack)\n[autotiling](https://github.com/nwg-piotr/autotiling)\n",
    'author': 'Viliam Valent',
    'author_email': 'stacki3@viliamvalent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/stacki3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
