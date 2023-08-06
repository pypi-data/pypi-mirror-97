# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redisbench_admin',
 'redisbench_admin.compare',
 'redisbench_admin.export',
 'redisbench_admin.export.common',
 'redisbench_admin.export.ftsb_redisearch',
 'redisbench_admin.export.memtier_benchmark',
 'redisbench_admin.export.redis_benchmark',
 'redisbench_admin.extract',
 'redisbench_admin.run',
 'redisbench_admin.run.ftsb_redisearch',
 'redisbench_admin.run.redis_benchmark',
 'redisbench_admin.run_local',
 'redisbench_admin.run_remote',
 'redisbench_admin.utils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'boto3>=1.13.24,<2.0.0',
 'humanize>=2.4.0,<3.0.0',
 'jsonpath_ng>=1.5.2,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy==1.15',
 'pandas>=1.0.4,<2.0.0',
 'paramiko>=2.7.2,<3.0.0',
 'py_cpuinfo>=5.0.0,<6.0.0',
 'pysftp>=0.2.9,<0.3.0',
 'python_terraform>=0.10.1,<0.11.0',
 'redis-py-cluster>=2.1.0,<3.0.0',
 'redis>=3.5.3,<4.0.0',
 'redistimeseries>=1.4.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'toml>=0.10.1,<0.11.0',
 'tqdm>=4.46.1,<5.0.0']

entry_points = \
{'console_scripts': ['redisbench-admin = redisbench_admin.cli:main']}

setup_kwargs = {
    'name': 'redisbench-admin',
    'version': '0.1.48',
    'description': 'Redis benchmark run helper. A wrapper around Redis and Redis Modules benchmark tools ( ftsb_redisearch, memtier_benchmark, redis-benchmark, aibench, etc... ).',
    'long_description': '[![codecov](https://codecov.io/gh/RedisLabsModules/redisbench-admin/branch/master/graph/badge.svg)](https://codecov.io/gh/RedisLabsModules/redisbench-admin)\n![Actions](https://github.com/RedisLabsModules/redisbench-admin/workflows/Run%20Tests/badge.svg?branch=master)\n![Actions](https://badge.fury.io/py/redisbench-admin.svg)\n\n# [redisbench-admin](https://github.com/RedisLabsModules/redisbench-admin) \n\nRedis benchmark run helper can help you with the following tasks:\n- Setup abd teardown of benchmarking infrastructure specified on [RedisLabsModules/testing-infrastructure](https://github.com/RedisLabsModules/testing-infrastructure)\n- Setup and teardown of an Redis and Redis Modules DBs for benchmarking\n- Management of benchmark data and specifications across different setups\n- Running benchmarks and recording results\n- Exporting performance results in several formats (CSV, RedisTimeSeries, JSON)\n- [SOON] Comparing performance results\n- [SOON] Finding performance problems by attaching telemetry probes\n\nCurrent supported benchmark tools:\n- [redisgraph-benchmark-go](https://github.com/RedisGraph/redisgraph-benchmark-go)\n- [ftsb_redisearch](https://github.com/RediSearch/ftsb)\n- [redis-benchmark](https://github.com/redis/redis)\n- [SOON][memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark)\n- [SOON][aibench](https://github.com/RedisAI/aibench)\n\n## Installation\n\nInstallation is done using pip, the package installer for Python, in the following manner:\n\n```bash\npython3 -m pip install redisbench-admin\n```\n\n## Development\n\n### Running tests\n\nA simple test suite is provided, and can be run with:\n\n```sh\n$ poetry run pytest\n```\n\n## License\n\nredisbench-admin is distributed under the BSD3 license - see [LICENSE](LICENSE)\n',
    'author': 'filipecosta90',
    'author_email': 'filipecosta.90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
