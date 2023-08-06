# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['showergel', 'showergel.rest']

package_data = \
{'': ['*'], 'showergel': ['www/*']}

install_requires = \
['Paste>=3.5.0,<4.0.0',
 'bottle-sqlalchemy>=0.4.3,<0.5.0',
 'bottle>=0.12.19,<0.13.0',
 'click>=7.1.2,<8.0.0',
 'sqlalchemy>=1.3.19,<2.0.0']

entry_points = \
{'console_scripts': ['showergel = showergel:main',
                     'showergel_install = showergel.install:main']}

setup_kwargs = {
    'name': 'showergel',
    'version': '0.1.3',
    'description': 'Companion application for a Liquidsoap radio',
    'long_description': "=========\nShowergel\n=========\n\nShowergel is made to live aside Liquidsoap_:\nwhile a Liquidsoap script creates a radio stream,\nShowergel provides complementary features like logging or occasional scheduling,\nwith a (minimalist) Web interface.\nIt is made to run on a Linux box (with systemd) dedicated to your radio stream.\n\n**This is work in progress!** We'll welcome both contributions\nand comments, feel free to start a disucssion in the Issues tab.\n\nNews\n====\n\nRight after the 0.1.0 release, \nShowergel has been presented at Liquidshop_1.0_, \nthe very first Liquidsoap workshop !\nYou can watch the 15-minutes presentation on Youtube_,\nslides are in the repository's ``doc`` folder.\n\nInstall\n=======\n\nInstall the program by the running ``pip install showergel``.\n\nRun the interactive installer by calling ``showergel_install``.\nIt will explain on the terminal what is happening and what to do from here.\nIf you stick to defaults, the installer will:\n\n* create a database (``showergel.db``)\n  and a configuration file (``showergel.ini``) in the current directory,\n* create a systemd user service called ``showergel`` ;\n  in other words you can ``systemctl --user status|start|stop|restart showergel``.\n* enable the service and systemd's lingering_ so Showergel will start automatically at boot time.\n* after installation Showergel will be available at http://localhost:2345/.\n\nThe installer's questions allow you to:\n\n* change the name of the systemd service and the DB/configuration files' names.\n  This is useful if you want to run multiple instances of showergel because you're\n  broadcasting multiple programs from the same machine.\n  For example, responding ``radio`` will create ``radio.db``, ``radio.ini`` and a ``radio`` service.\n* skip the service creation, if you prefer to launch Showergel yourself.\n* create another systemd user service for your Liquidsoap script,\n  so systemd will automatically launch everything (this is recommanded).\n  Note that in that case, the installer creates two systemd services with the\n  same basename: for example,\n  ``radio_gel`` (showergel service associated to ``radio``)\n  and ``radio_soap`` (the Liquidsoap script you provided for ``radio``).\n\n\nConfigure\n=========\n\nSee comments in the ``.ini`` file created by the installer.\n\n\nDevelop\n=======\n\nDepencencies, installation and packing is done by Poetry_.\nOnce Poetry is installed,\ncreate a Python3 environment,\nactivate it, and run ``poetry install`` from a clone of this repository.\n\nWhen developping, your Liquidsoap script and Showergel should be launched manually.\nRun ``showergel_install --dev`` to create an empty database (``showergel.db``)\nand a basic configuration file (``showergel.ini``)\nin the current folder.\nRead (and edit, maybe) ``showergel.ini``,\nlaunch Liqudisoap, then run ``showergel showergel.ini``.\nYou'll likely want to enable the detailed log by setting ``level=DEBUG``\nin the ``logger_root`` section of the ini file.\n\nTest with ``pytest``.\n\nA font-end is coming up for v 0.2.0, see front/README.md \n\nDesign\n======\n\nShowergel is a light program made to run permanently along your Liqudidsoap instance.\nIt communicates with Liqudidsoap via its telnet server,\nand with the outside world via HTTP.\n\nWe assume that most of the program time should be handled by your Liquidsoap script,\ntypically with the ``random`` operator over a music folder\nor a ``switch`` scheduling regular pre-recorded shows.\n\nIn other words you still have to write yourself the Liquidsoap script that will fit your radio.\nWe only provides a few examples,\ncovering Liquidsoap's basics and Showgel's integration.\n\nShowergel is meant for community and benevolent radios.\nTherefore we'll keep it small and simple:\n\n* Showergel is intended to run on the same machine as Liquidsoap.\n* The REST/Web interface is served by the Bottle_ framework,\n  because it's enough and allows keeping everything in a single process.\n* Showergel's data is stored in SQLite_ because a database backing a radio stream\n  usually weights a few dozen megabytes.\n* Scheduling is delegated to APScheduler_ ... who also needs SQLAlchemy_ to\n  access SQLite, so we use SQLAlchemy too.\n* Showergel will not hold your music and shows collection.\n  For that matter we suggest Beets_,\n  you can find examples of its integration with Liquidsoap in\n  `Liquidsoap documentation <https://www.liquidsoap.info/doc-dev/beets.html>`_.\n\nShowergel have only been tested under Linux.\n\nLicense: GPL3_.\n\n\n.. _Liquidsoap: https://www.liquidsoap.info/\n.. _GPL3: https://www.gnu.org/licenses/gpl-3.0.html\n.. _Poetry: https://python-poetry.org/\n.. _APScheduler: https://apscheduler.readthedocs.io/en/stable/\n.. _SQLite: https://sqlite.org/\n.. _Beets: http://beets.io\n.. _SQLAlchemy: https://www.sqlalchemy.org/\n.. _lingering: https://www.freedesktop.org/software/systemd/man/loginctl.html\n.. _Bottle: https://bottlepy.org/docs/dev/\n.. _Liquidshop_1.0: http://www.liquidsoap.info/liquidshop/\n.. _Youtube: https://www.youtube.com/watch?v=9U2xsAhz_dU\n",
    'author': 'Martin Kirchgessner',
    'author_email': 'martin.kirch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/martinkirch/showergel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
