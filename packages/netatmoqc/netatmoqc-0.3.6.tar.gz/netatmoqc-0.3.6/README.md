# NetAtmoQC


**Table of Contents**

[[_TOC_]]


### About

`netatmoqc` is a python package that uses Machine Learning Clustering methods to
quality-control observations collected from [NetAtmo](https://www.netatmo.com/en-gb)
weather stations. It has so far been developed at [SMHI](https://www.smhi.se/en)
as part of the [iObs](https://wiki.neic.no/wiki/IOBS) project.

Please note that this package is still in its development/implementation stage.
As such, it may (certainly does) contain (hopefully minor) bugs and lack on
documentation. If you wish to collaborate, suggest features or report issues,
please contact [Paulo Medeiros (SMHI)](mailto:paulo.medeiros@smhi.se).

A note about this file: We have used the
[Markdown format](https://docs.gitlab.com/ee/user/markdown.html) throughout.
You should, however, be able to read it reasonably well with your plain text
processor of choice. Please disregard the formatting marks in this case.

See also the [project's Wiki](https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc/-/wikis/home) for more information.

### System Requirements

* python >=3.6.10
* A C compiler

* **Optional**: Ability to compile and run MPI applications.

    The system needs to have a working installation of an MPI library. Having
    [Open MPI](https://www.open-mpi.org/) should be fine, but there are other
    options.

    This requirement is usually already fulfilled in HPC facilities, although,
    in some cases, you might need to load a module (e.g., `module load openmpi`).
    Please check with your HPC support if you have doubts about this.

    **NB.:** If this requirement is not fulfilled, you won't be able to run
    `netatmoqc` using MPI, even if you manage to follow the MPI-related
    installation instructions presented later on in this file.

    If you don't have a working MPI library installed in your system but use,
    for instance, [conda](https://docs.conda.io/projects/conda/en/latest/glossary.html#anaconda-glossary)
    to manage your environments/source packages, then running the following
    commands should get it working:

        conda install -c conda-forge openmpi
        conda install gxx_linux-64

* **Only for
[Developer-Mode Installtion](#developer-mode-installation):**

    * [`poetry`](https://python-poetry.org), which can be installed by running

            curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3


### Installation

Before proceeding, please make sure that your system fulfils the appropriate
[system requirements](#system-requirements). If you plan to just use the code
without modifying it, please follow one of the installation methods presented
in the [Regular Installation section](#regular-installation). However, if you
need/wish to modify the code in any way, then please proceed as indicated in the
[Developer-Mode Installtion section](#developer-mode-installation).

**N.B.:** In any case, you will be presented with instructions for installation
with and without MPI support. *You only need to follow one such set of
instructions*. Mind, however, the extra [system requirements](#system-requirements)
that apply if you choose to install `netatmoqc` with MPI support.


#### Regular Installation
##### Regular Installation from PyPi
:point_right: Easiest method if you just want to use the code and don't want to
look at the source code at all.

* Install *without* MPI support:

        pip install netatmoqc

* Install with MPI support:

        pip install netatmoqc[mpi]


##### Regular Installation Directly From The Git Repo

:point_right: Similar to a [regular installation from PyPi](#regular-installation-from-pypi),
but retrieves the code from the git repo instead (which is usually updated more
often).

* Install *without* MPI support:

        pip install "git+https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc"

* Install with MPI support:

        pip install "netatmoqc[mpi] @ git+https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc"


##### Regular Installation From Downloaded Source

:point_right: For those who have `netatmoqc`'s source code in a local directory,
wish to install it from there, but also don't want to modify any code.

* Install *without* MPI support:

        pip install .

* Install with MPI support:

        pip install ".[mpi]"

#### Developer Mode Installation

:point_right: For those who need/wish to make changes to `netatmoqc`'s
source code, or use code from a different branch than `master`.

* Install *without* MPI support:

        poetry install

* Install with MPI support:

        poetry install --extras "mpi"

Installing in "developer mode" means that changes made in any of the package's
source files become visible as soon as the package is reloaded.

:wrench: **Recommendation to contributors:** Before making your first commit to
the repo, please also run the following:

    pre-commit install

This sets up the git hook scripts defined in the
[.pre-commit-config.yaml](.pre-commit-config.yaml) file and only needs to be run
(i) before the first commit, and (ii) after having modified the
[.pre-commit-config.yaml](.pre-commit-config.yaml) file. The
[pre-commit](https://pre-commit.com) package is installed when you run any of
the `poetry install` commands listed above.


### After Installation: Configuration File

After successful installation, a `netatmoqc` command will become available in
your environment. However, before you can use `netatmoqc` (apart from the `-h`
option), you will need a configuration file written in the
[TOML](https://en.wikipedia.org/wiki/TOML) format.

Please take a look at the
[docs/minimal_config_example.toml](docs/minimal_config_example.toml) and
[docs/more_complete_config_example.toml](docs/more_complete_config_example.toml)
files, as well as the [project's Wiki](https://source.coderefinery.org/iOBS/wp2/task-2-3/netatmoqc/-/wikis/home), for more information about the configuration file.


`netatmoqc` assumes that one of the following (whichever is first encountered)
is your configuration file :

1. A *full file path* specified via the `NETATMOQC_CONFIG_PATH` envvar
2. A `config.toml` file located in the directory where `netatmoqc` is called
3. `$HOME/.netatmoqc/config.toml`


### Usage
After completing the setup, you should be able to run

    netatmoqc [opts] SUBCOMMAND [subcommand_opts]

where `[opts]` and `[subcommand_opts]` denote optional command line arguments
that apply, respectively, to `netatmoqc` in general and to `SUBCOMMAND`
specifically.

**Please run `netatmoqc -h` for information** about the supported subcommands
and general `netatmoqc` options. For info about specific subcommands and the
options that apply to them only, **please run `netatmoqc SUBCOMMAND -h`** (note
that the `-h` goes after the subcommand in this case).

**N.B.:** When using the (preferred and default) clustering method
[HDBSCAN](https://hdbscan.readthedocs.io/en/latest/index.html), a typical
`netatmoqc` run (~40000 unique station IDs per DTG) needs ca. **6 GB** RAM and
takes between 1 and 2 minutes to complete (on a machine equipped with Intel(R)
Xeon(R) CPU E5-2640 v3 @ 2.60GHz, 16 physical cores). Other implemented
clustering strategies have more modest RAM requirements, but:
  * [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
  results are not as good as HDBSCAN's in our context
  * [OPTICS](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html)
  produces similar results as HDBSCAN but runs *much* slower


#### Parallelism (single-host or MPI)

The `select` subcommand supports parallelism over DTGs. How to activate it
depends on whether you wish to run `netatmoqc` on a single host or if you wish
to distribute computations over different computers (e.g. on an HPC cluster).

  * If you are running `netatmoqc` in a single host, then you can export the
    environment variable `NETATMOQC_MAX_PYTHON_PROCS` to any value larger
    than 0 and run the code as usual.

  * If you wish to run `netatmoqc` with MPI, then you must have installed it
    with MPI support. Assuming this is the case, you can then run the code as

        mpiexec -n 1 [-usize N] netatmoqc --mpi [opts] select [subcommand_opts]

    Notice that:
    * Arguments between square brackets are optional
    * The `--mpi` switch must come before any subcommand
    * **The value "1" in `-n 1` is mandatory.** The code will always start with one
      "manager" task which will dynamically spawn new worker tasks as needed
      (up to a maximum number).
    * If `-usize N` is passed, then `N` should be an integer greater than zero.
      `N` defines the maximum number of extra workers that the manager task is
      allowed to spawn if necessary.
    * If `-usize N` is not passed, then:
      * If the run is part of a submitted job managed by SLURM or PBS, then `N`
        will be automatically determined from the options passed to the
        scheduler (e.g. `--nnodes`, `--ntasks`, `--mem-per-cpu`, etc for SLURM).
      * If the run is running interactive: `N` will take the value of the
        environment variable `NETATMOQC_MAX_PYTHON_PROCS` if set, or, otherwise,
        will be set to 1.
    * No more than `length(DTGs)` new worker tasks will be spawn

Last, but not least: Please keep in mind the RAM requirements discussed in the
[usage](#usage) section.
