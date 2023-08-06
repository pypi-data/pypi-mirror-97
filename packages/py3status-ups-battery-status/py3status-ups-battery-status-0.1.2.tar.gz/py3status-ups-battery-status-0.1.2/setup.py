# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py3status_ups_battery_status']

package_data = \
{'': ['*']}

install_requires = \
['py3status>=3.34,<4.0']

entry_points = \
{'py3status': ['module = py3status_ups_battery_status.ups_battery_status']}

setup_kwargs = {
    'name': 'py3status-ups-battery-status',
    'version': '0.1.2',
    'description': 'py3status module to show the status of a UPS battery',
    'long_description': '# py3status-ups-battery-status\nPython module for py3status to monitor my UPS battery status\n\n## Screenshot\n![py3status-ups-batter-status](https://raw.githubusercontent.com/mcgillij/py3status-ups-battery-status/main/images/ups_battery_status.png)\n\n## Installation\n\n### From Git\n``` bash\ngit clone https://github.com/mcgillij/py3status-ups-battery-status.git\nmkdir -p ~/.i3/py3status && cd ~/.i3/py3status\nln -s <PATH_TO_CLONED_REPO>/src/py3status-ups-battery-status/ups-battery-status.py ./\n```\n\n### Building From AUR (Arch)\n``` bash\ngit clone https://aur.archlinux.org/py3status-ups-battery-status.git\ncd py3status-ups-battery-status\nmakechrootpkg -c -r $HOME/$CHROOT\n```\n\n### Installing Arch package\n``` bash\nsudo pacman -U --asdeps py3status-ups-battery-status-*-any.pkg.tar.zst\n```\n\n## Dependencies\n\nThis module depends on the Network UPS Tools(nut) package. And having already configured your battery with it.\nIt assumes that you\'ve named your battery *battery*. If you\'ve named it something else you can change it in the module itself.\n\nDependency installation on Arch:\n``` bash\npacman -S nut\n```\n\nDependency installation on Debian:\n``` bash\napt install nut\n```\n\n## Usage\nAdd the module to your list of configured py3status modules\n\n*~/.config/i3status.conf*\n``` bash\n...\norder += "arch_updates"\norder += "volume_status"\norder += "ups_battery_status"\n...\n\n```\n\nAnd then just restart your i3 session.\n',
    'author': 'mcgillij',
    'author_email': 'mcgillivray.jason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcgillij/py3status-ups-battery-status',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
