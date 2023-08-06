# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py3status_cpu_governor']

package_data = \
{'': ['*']}

install_requires = \
['py3status>=3.34,<4.0']

entry_points = \
{'py3status': ['module = py3status_cpu_governor.cpu_governor']}

setup_kwargs = {
    'name': 'py3status-cpu-governor',
    'version': '0.1.2',
    'description': 'py3status monitor to show the state of your cpu governor',
    'long_description': '# py3status-cpu-governor\nPython module for py3status to show the cpu_governor state in i3\n\nThis is handy if you manage your governor manually with something like\n\n``` bash\nalias performance_mode=\'echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor\'\nalias powersave_mode=\'echo powersave | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor\'\nalias schedutil_mode=\'echo schedutil | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor\'\nalias cpu_frequency_watch=\'watch -n.5 "cat /proc/cpuinfo | grep \\"^[c]pu MHz\\""\'\n```\n\n## Screenshot\n![py3status cpu_governor](https://raw.githubusercontent.com/mcgillij/py3status-cpu-governor/main/images/cpu_governor.png)\n\n## Pre-reqs\n* i3\n* py3status\n\n## Installation\n### From Git\n``` bash\ngit clone https://github.com/mcgillij/py3status-cpu-governor.git\nmkdir -p ~/.i3/py3status && cd ~/.i3/py3status\nln -s <PATH_TO_CLONED_REPO>/src/py3status-cpu-governor/cpu_governor.py ./\n```\n\n### With Pip\n``` bash\npip install py3status-cpu-governor\n```\n\n### Building From AUR (Arch)\n``` bash\ngit clone https://aur.archlinux.org/py3status-cpu-governor.git\ncd py3status-cpu-governor.git\nmakechrootpkg -c -r $HOME/$CHROOT\n```\n\n### Installing Arch package\n``` bash\nsudo pacman -U --asdeps py3status-cpu-governor-*-any.pkg.tar.zst\n```\n\n## Configuration\n\nadd the following line to your *~/.config/i3/i3status.conf*\n\n``` bash\norder += "cpu_governor"\n```\n\nAnd restart your i3 session.\n',
    'author': 'mcgillij',
    'author_email': 'mcgillivray.jason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcgillij/py3status-cpu-governor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
