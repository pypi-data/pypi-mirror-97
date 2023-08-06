# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autobisect',
 'autobisect.evaluators',
 'autobisect.evaluators.browser',
 'autobisect.evaluators.browser.tests',
 'autobisect.evaluators.js',
 'autobisect.tests']

package_data = \
{'': ['*'],
 'autobisect.tests': ['mock-firefoxci/api/index/v1/task/*',
                      'mock-firefoxci/api/queue/v1/task/BfFeMY14Qyu_rMA2pxfZZg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/BfFeMY14Qyu_rMA2pxfZZg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/DYaFBxzITgCwBUp48Bugtw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/DYaFBxzITgCwBUp48Bugtw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/EYhOnvRFQd-rMlW2oAl10A/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/EYhOnvRFQd-rMlW2oAl10A/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/FnPonlT1QVSw-B0M0KcotQ/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/FnPonlT1QVSw-B0M0KcotQ/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/H5Dl5ijpSpOPwMLEEWx_bA/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/H5Dl5ijpSpOPwMLEEWx_bA/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HFsFsbogQ0O-sFZoYDmAZw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HFsFsbogQ0O-sFZoYDmAZw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HNaxi6w_RQeXGb4fYQFtwA/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HNaxi6w_RQeXGb4fYQFtwA/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HPE2LlTUQU62unXX8GvNGA/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HPE2LlTUQU62unXX8GvNGA/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HX3oSg_SRTq5-Mc5D0PPHg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HX3oSg_SRTq5-Mc5D0PPHg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/Hq2DMUk6QP26axMV8fDi9w/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/Hq2DMUk6QP26axMV8fDi9w/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/JucwusRxQHKQwDUPoOJIhQ/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/JucwusRxQHKQwDUPoOJIhQ/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/NKFp2FPpQ06E8C7N30JPdw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/NKFp2FPpQ06E8C7N30JPdw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/O1Sh28LhQC62SfLAi0orxg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/O1Sh28LhQC62SfLAi0orxg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/R2zRDt-ATf-zE-hYXR8kEw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/R2zRDt-ATf-zE-hYXR8kEw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/SDAzDRggRPOPYHEQC4WDEw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/SDAzDRggRPOPYHEQC4WDEw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/Tp5LesydQWyPNqpMThZLyg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/Tp5LesydQWyPNqpMThZLyg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/TxMd0rIfQKucR6p0gkaMSw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/TxMd0rIfQKucR6p0gkaMSw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/UXVT--1qQfeaGtNICDKx3w/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/UXVT--1qQfeaGtNICDKx3w/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/WLcjhVjtTLW0A_ued1Io-Q/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/WLcjhVjtTLW0A_ued1Io-Q/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/Zb_1byPDSTyhUkZeCg-PZg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/Zb_1byPDSTyhUkZeCg-PZg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/cRT3ROAzReG2wv7PW08JMg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/cRT3ROAzReG2wv7PW08JMg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/cSP0vuVWTX6JspZ2VTtDdg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/cSP0vuVWTX6JspZ2VTtDdg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/fXYHDLC_RkWNtOv01aB8wQ/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/fXYHDLC_RkWNtOv01aB8wQ/artifacts/public/build/*',
                      'mock-hg/mozilla-central/*']}

install_requires = \
['black>=19.10b0,<20.0',
 'fuzzfetch>=1.0.4,<2.0.0',
 'grizzly-framework>=0.11.1,<0.12.0',
 'lithium-reducer>=0.3.3,<0.4.0',
 'toml>=0.9,<0.10']

entry_points = \
{'console_scripts': ['autobisect = autobisect.main:main']}

setup_kwargs = {
    'name': 'autobisect',
    'version': '0.8.5',
    'description': 'Automatic bisection utility for Mozilla Firefox and SpiderMonkey',
    'long_description': "Autobisect\n==========\n[![Build Status](https://travis-ci.com/MozillaSecurity/autobisect.svg?branch=master)](https://travis-ci.org/MozillaSecurity/autobisect)\n[![codecov](https://codecov.io/gh/MozillaSecurity/autobisect/branch/master/graph/badge.svg)](https://codecov.io/gh/MozillaSecurity/autobisect)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nAutobisect is a python module that automates bisection of Mozilla Firefox and SpiderMonkey bugs.\n\nInstallation\n------------\n\n```bash\ngit clone git@github.com:MozillaSecurity/autobisect.git\ncd autobisect\npoetry install\n```\n\nUsage\n-----\nFirefox bug bisection supports the following arguments:\n\n```\npython -m autobisect firefox --help\n\npositional arguments:\n  testcase              Path to testcase\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nLauncher Arguments:\n  -e EXTENSION, --extension EXTENSION\n                        Install an extension. Specify the path to the xpi or\n                        the directory containing the unpacked extension. To\n                        install multiple extensions specify multiple times\n  --launch-timeout LAUNCH_TIMEOUT\n                        Number of seconds to wait before LaunchError is raised\n                        (default: 300)\n  --log-limit LOG_LIMIT\n                        Log file size limit in MBs (default: 'no limit')\n  -m MEMORY, --memory MEMORY\n                        Browser process memory limit in MBs (default: 'no\n                        limit')\n  -p PREFS, --prefs PREFS\n                        prefs.js file to use\n  --soft-asserts        Detect soft assertions\n  --xvfb                Use Xvfb (Linux only)\n\nReporter Arguments:\n  --ignore IGNORE [IGNORE ...]\n                        Space separated ignore list. ie: log-limit memory\n                        timeout (default: nothing)\n\nReplay Arguments:\n  --any-crash           Any crash is interesting, not only crashes which match\n                        the original signature.\n  --idle-timeout IDLE_TIMEOUT\n                        Number of seconds to wait before polling testcase for\n                        idle (default: 60)\n  --idle-threshold IDLE_THRESHOLD\n                        CPU usage threshold to mark the process as idle\n                        (default: 25)\n\nTarget:\n  --target {firefox,js}\n                        Specify the build target. (default: firefox)\n  --os {Android,Darwin,Linux,Windows}\n                        Specify the target system. (default: Linux)\n  --cpu {AMD64,ARM64,aarch64,arm,arm64,i686,x64,x86,x86_64}\n                        Specify the target CPU. (default: x86_64)\n\nBuild:\n  --build DATE|REV|NS   Specify the build to download, (default: latest)\n                        Accepts values in format YYYY-MM-DD (2017-01-01)\n                        revision (57b37213d81150642f5139764e7044b07b9dccc3) or\n                        TaskCluster namespace (gecko.v2....)\n\nBranch:\n  --inbound             Download from mozilla-inbound\n  --central             Download from mozilla-central (default)\n  --release             Download from mozilla-release\n  --beta                Download from mozilla-beta\n  --esr-stable          Download from esr-stable\n  --esr-next            Download from esr-next\n  --try                 Download from try\n\nBuild Arguments:\n  -d, --debug           Get debug builds w/ symbols (default=optimized).\n  -a, --asan            Download AddressSanitizer builds.\n  -t, --tsan            Download ThreadSanitizer builds.\n  --fuzzing             Download --enable-fuzzing builds.\n  --coverage            Download --coverage builds. This also pulls down the\n                        *.gcno files\n  --valgrind            Download Valgrind builds.\n\nTest Arguments:\n  --tests  [ ...]       Download tests associated with this build. Acceptable\n                        values are: gtest, common, reftests\n  --full-symbols        Download the full crashreport-symbols.zip archive.\n\nMisc. Arguments:\n  -n NAME, --name NAME  Specify a name (default=auto)\n  -o OUT, --out OUT     Specify output directory (default=.)\n  --dry-run             Search for build and output metadata only, don't\n                        download anything.\n\nNear Arguments:\n  If the specified build isn't found, iterate over builds in the specified\n  direction\n\n  --nearest-newer       Search from specified build in ascending order\n  --nearest-older       Search from the specified build in descending order\n\nBoundary Arguments (YYYY-MM-DD or SHA1 revision):\n  --start START         Start build id (default: earliest available build)\n  --end END             End build id (default: latest available build)\n\nBisection Arguments:\n  --timeout TIMEOUT     Maximum iteration time in seconds (default: 60)\n  --repeat REPEAT       Number of times to evaluate testcase (per build)\n  --config CONFIG       Path to optional config file\n  --find-fix            Identify fix date\n\n```\n\nSimple Bisection\n----------------\n```\npython -m autobisect firefox trigger.html --prefs prefs.js --asan --end 2017-11-14\n```\n\nBy default, Autobisect will cache downloaded builds (up to 30GBs) to reduce bisection time.  This behavior can be modified by supplying a custom configuration file in the following format:\n```\n[autobisect]\nstorage-path: /home/ubuntu/cached\npersist: true\n; size in MBs\npersist-limit: 30000\n```\n\nDevelopment\n-----------\nAutobisect includes a pre-commit hook for [black](https://github.com/psf/black) and [flake8](https://flake8.pycqa.org/en/latest/).  To install the pre-commit hook, run the following.  \n```bash\npre-commit install\n```\n\nFurthermore, all tests should be executed via tox.\n```bash\npoetry run tox\n```\n\n",
    'author': 'Jason Kratzer',
    'author_email': 'jkratzer@mozilla.com',
    'maintainer': 'Mozilla Fuzzing Team',
    'maintainer_email': 'fuzzing@mozilla.com',
    'url': 'https://github.com/MozillaSecurity/autobisect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
