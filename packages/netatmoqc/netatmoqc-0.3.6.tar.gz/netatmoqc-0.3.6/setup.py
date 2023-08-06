# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netatmoqc',
 'netatmoqc.apps',
 'netatmoqc.apps.clustering',
 'netatmoqc.apps.scattergeo_timeseries']

package_data = \
{'': ['*'],
 'netatmoqc': ['bin/*'],
 'netatmoqc.apps.clustering': ['assets/*'],
 'netatmoqc.apps.scattergeo_timeseries': ['assets/*']}

install_requires = \
['attrs>=20.2.0,<21.0.0',
 'dash-daq>=0.5.0,<0.6.0',
 'dash>=1.13.4,<2.0.0',
 'dotmap>=1.3.17,<2.0.0',
 'flask-caching>=1.9.0,<2.0.0',
 'hdbscan>=0.8.26,<0.9.0',
 'humanize>=2.6.0,<3.0.0',
 'importlib-metadata>=1.7.0,<2.0.0',
 'joblib>=0.15.1,<0.16.0',
 'llvmlite==0.33',
 'numba>=0.50.1,<0.51.0',
 'numpy>=1.19.0,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'plotly>=4.8.2,<5.0.0',
 'psutil>=5.7.0,<6.0.0',
 'pyproj>=2.6.1,<3.0.0',
 'pytz>=2020.1,<2021.0',
 'redis>=3.5.3,<4.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'toml>=0.10.1,<0.11.0']

extras_require = \
{':sys_platform != "darwin"': ['tbb>=2020.0.133,<2021.0.0'],
 'mpi': ['mpi4py>=3.0.3,<4.0.0']}

entry_points = \
{'console_scripts': ['netatmoqc = netatmoqc.main:main']}

setup_kwargs = {
    'name': 'netatmoqc',
    'version': '0.3.6',
    'description': 'Use machine learning clustering methods to perform quality control over NetAtmo data',
    'long_description': '# NetAtmoQC\n\n\n**Table of Contents**\n\n[[_TOC_]]\n\n\n### About\n\n`netatmoqc` is a python package that uses Machine Learning Clustering methods to\nquality-control observations collected from [NetAtmo](https://www.netatmo.com/en-gb)\nweather stations. It has so far been developed at [SMHI](https://www.smhi.se/en)\nas part of the [iObs](https://wiki.neic.no/wiki/IOBS) project.\n\nPlease note that this package is still in its development/implementation stage.\nAs such, it may (certainly does) contain (hopefully minor) bugs and lack on\ndocumentation. If you wish to collaborate, suggest features or report issues,\nplease contact [Paulo Medeiros (SMHI)](mailto:paulo.medeiros@smhi.se).\n\nA note about this file: We have used the\n[Markdown format](https://docs.gitlab.com/ee/user/markdown.html) throughout.\nYou should, however, be able to read it reasonably well with your plain text\nprocessor of choice. Please disregard the formatting marks in this case.\n\nSee also the [project\'s Wiki](https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc/-/wikis/home) for more information.\n\n### System Requirements\n\n* python >=3.6.10\n* A C compiler\n\n* **Optional**: Ability to compile and run MPI applications.\n\n    The system needs to have a working installation of an MPI library. Having\n    [Open MPI](https://www.open-mpi.org/) should be fine, but there are other\n    options.\n\n    This requirement is usually already fulfilled in HPC facilities, although,\n    in some cases, you might need to load a module (e.g., `module load openmpi`).\n    Please check with your HPC support if you have doubts about this.\n\n    **NB.:** If this requirement is not fulfilled, you won\'t be able to run\n    `netatmoqc` using MPI, even if you manage to follow the MPI-related\n    installation instructions presented later on in this file.\n\n    If you don\'t have a working MPI library installed in your system but use,\n    for instance, [conda](https://docs.conda.io/projects/conda/en/latest/glossary.html#anaconda-glossary)\n    to manage your environments/source packages, then running the following\n    commands should get it working:\n\n        conda install -c conda-forge openmpi\n        conda install gxx_linux-64\n\n* **Only for\n[Developer-Mode Installtion](#developer-mode-installation):**\n\n    * [`poetry`](https://python-poetry.org), which can be installed by running\n\n            curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3\n\n\n### Installation\n\nBefore proceeding, please make sure that your system fulfils the appropriate\n[system requirements](#system-requirements). If you plan to just use the code\nwithout modifying it, please follow one of the installation methods presented\nin the [Regular Installation section](#regular-installation). However, if you\nneed/wish to modify the code in any way, then please proceed as indicated in the\n[Developer-Mode Installtion section](#developer-mode-installation).\n\n**N.B.:** In any case, you will be presented with instructions for installation\nwith and without MPI support. *You only need to follow one such set of\ninstructions*. Mind, however, the extra [system requirements](#system-requirements)\nthat apply if you choose to install `netatmoqc` with MPI support.\n\n\n#### Regular Installation\n##### Regular Installation from PyPi\n:point_right: Easiest method if you just want to use the code and don\'t want to\nlook at the source code at all.\n\n* Install *without* MPI support:\n\n        pip install netatmoqc\n\n* Install with MPI support:\n\n        pip install netatmoqc[mpi]\n\n\n##### Regular Installation Directly From The Git Repo\n\n:point_right: Similar to a [regular installation from PyPi](#regular-installation-from-pypi),\nbut retrieves the code from the git repo instead (which is usually updated more\noften).\n\n* Install *without* MPI support:\n\n        pip install "git+https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc"\n\n* Install with MPI support:\n\n        pip install "netatmoqc[mpi] @ git+https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc"\n\n\n##### Regular Installation From Downloaded Source\n\n:point_right: For those who have `netatmoqc`\'s source code in a local directory,\nwish to install it from there, but also don\'t want to modify any code.\n\n* Install *without* MPI support:\n\n        pip install .\n\n* Install with MPI support:\n\n        pip install ".[mpi]"\n\n#### Developer Mode Installation\n\n:point_right: For those who need/wish to make changes to `netatmoqc`\'s\nsource code, or use code from a different branch than `master`.\n\n* Install *without* MPI support:\n\n        poetry install\n\n* Install with MPI support:\n\n        poetry install --extras "mpi"\n\nInstalling in "developer mode" means that changes made in any of the package\'s\nsource files become visible as soon as the package is reloaded.\n\n:wrench: **Recommendation to contributors:** Before making your first commit to\nthe repo, please also run the following:\n\n    pre-commit install\n\nThis sets up the git hook scripts defined in the\n[.pre-commit-config.yaml](.pre-commit-config.yaml) file and only needs to be run\n(i) before the first commit, and (ii) after having modified the\n[.pre-commit-config.yaml](.pre-commit-config.yaml) file. The\n[pre-commit](https://pre-commit.com) package is installed when you run any of\nthe `poetry install` commands listed above.\n\n\n### After Installation: Configuration File\n\nAfter successful installation, a `netatmoqc` command will become available in\nyour environment. However, before you can use `netatmoqc` (apart from the `-h`\noption), you will need a configuration file written in the\n[TOML](https://en.wikipedia.org/wiki/TOML) format.\n\nPlease take a look at the\n[docs/minimal_config_example.toml](docs/minimal_config_example.toml) and\n[docs/more_complete_config_example.toml](docs/more_complete_config_example.toml)\nfiles, as well as the [project\'s Wiki](https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc/-/wikis/home), for more information about the configuration file.\n\n\n`netatmoqc` assumes that one of the following (whichever is first encountered)\nis your configuration file :\n\n1. A *full file path* specified via the `NETATMOQC_CONFIG_PATH` envvar\n2. A `config.toml` file located in the directory where `netatmoqc` is called\n3. `$HOME/.netatmoqc/config.toml`\n\n\n### Usage\nAfter completing the setup, you should be able to run\n\n    netatmoqc [opts] SUBCOMMAND [subcommand_opts]\n\nwhere `[opts]` and `[subcommand_opts]` denote optional command line arguments\nthat apply, respectively, to `netatmoqc` in general and to `SUBCOMMAND`\nspecifically.\n\n**Please run `netatmoqc -h` for information** about the supported subcommands\nand general `netatmoqc` options. For info about specific subcommands and the\noptions that apply to them only, **please run `netatmoqc SUBCOMMAND -h`** (note\nthat the `-h` goes after the subcommand in this case).\n\n**N.B.:** When using the (preferred and default) clustering method\n[HDBSCAN](https://hdbscan.readthedocs.io/en/latest/index.html), a typical\n`netatmoqc` run (~40000 unique station IDs per DTG) needs ca. **6 GB** RAM and\ntakes between 1 and 2 minutes to complete (on a machine equipped with Intel(R)\nXeon(R) CPU E5-2640 v3 @ 2.60GHz, 16 physical cores). Other implemented\nclustering strategies have more modest RAM requirements, but:\n  * [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)\n  results are not as good as HDBSCAN\'s in our context\n  * [OPTICS](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html)\n  produces similar results as HDBSCAN but runs *much* slower\n\n\n#### Parallelism (single-host or MPI)\n\nThe `select` subcommand supports parallelism over DTGs. How to activate it\ndepends on whether you wish to run `netatmoqc` on a single host or if you wish\nto distribute computations over different computers (e.g. on an HPC cluster).\n\n  * If you are running `netatmoqc` in a single host, then you can export the\n    environment variable `NETATMOQC_MAX_PYTHON_PROCS` to any value larger\n    than 0 and run the code as usual.\n\n  * If you wish to run `netatmoqc` with MPI, then you must have installed it\n    with MPI support. Assuming this is the case, you can then run the code as\n\n        mpiexec -n 1 [-usize N] netatmoqc --mpi [opts] select [subcommand_opts]\n\n    Notice that:\n    * Arguments between square brackets are optional\n    * The `--mpi` switch must come before any subcommand\n    * **The value "1" in `-n 1` is mandatory.** The code will always start with one\n      "manager" task which will dynamically spawn new worker tasks as needed\n      (up to a maximum number).\n    * If `-usize N` is passed, then `N` should be an integer greater than zero.\n      `N` defines the maximum number of extra workers that the manager task is\n      allowed to spawn if necessary.\n    * If `-usize N` is not passed, then:\n      * If the run is part of a submitted job managed by SLURM or PBS, then `N`\n        will be automatically determined from the options passed to the\n        scheduler (e.g. `--nnodes`, `--ntasks`, `--mem-per-cpu`, etc for SLURM).\n      * If the run is running interactive: `N` will take the value of the\n        environment variable `NETATMOQC_MAX_PYTHON_PROCS` if set, or, otherwise,\n        will be set to 1.\n    * No more than `length(DTGs)` new worker tasks will be spawn\n\nLast, but not least: Please keep in mind the RAM requirements discussed in the\n[usage](#usage) section.\n',
    'author': 'Paulo V. C. Medeiros',
    'author_email': 'paulo.medeiros@smhi.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.10,<4.0.0',
}


setup(**setup_kwargs)
