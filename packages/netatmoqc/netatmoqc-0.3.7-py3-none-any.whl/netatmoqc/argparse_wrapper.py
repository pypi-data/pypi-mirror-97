#!/usr/bin/env python3
"""Wrappers for argparse functionality."""
import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path

from . import __version__
from .commands_functions import (
    cluster_obs_single_dtg,
    csv2obsoul,
    select_stations,
    show,
    thin_data_from_csv_files,
)


class StoreDictKeyPair(argparse.Action):
    """Enable args="key1=val1, ..., keyN=valN" in command line args."""

    # Source: <https://stackoverflow.com/questions/29986185/
    #          python-argparse-dict-arg/42355279>

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """Initialise nargs."""
        self._nargs = nargs
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Get a key/value dict from passed string."""
        my_dict = {}
        for k_v in values:
            key, val = k_v.split("=")
            my_dict[key] = val
        setattr(namespace, self.dest, my_dict)


def get_parsed_args(program_name):
    """Get parsed command line arguments.

    Args:
        program_name (str): The name of the program.

    Returns:
        argparse.Namespace: Parsed command line arguments.

    """
    # Define main parser and general options
    parser = argparse.ArgumentParser(
        prog=program_name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    try:
        fpath = Path(os.getenv("NETATMOQC_CONFIG_PATH", "config.toml"))
        default_conf_path = fpath.resolve(strict=True)
    except FileNotFoundError:
        default_conf_path = (
            Path(os.getenv("HOME")) / ".netatmoqc" / "config.toml"
        )
    parser.add_argument(
        "--version", "-v", action="version", version="%(prog)s v" + __version__
    )
    parser.add_argument(
        "-config_file",
        metavar="CONFIG_FILE_PATH",
        default=default_conf_path,
        type=Path,
        help=(
            "Path to the config file. The default is whichever of the "
            + "following is first encountered: "
            + "(i) The value of the 'NETATMOQC_CONFIG_PATH' envvar or "
            + "(ii) './config.toml'. If both (i) and (ii) are missing, "
            + "then the default will become "
            + "'"
            + str(Path("$HOME/.netatmoqc/config.toml"))
            + "'"
        ),
    )
    parser.add_argument(
        "-loglevel",
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "notset"],
        help="What type of info should be printed to the log",
    )
    parser.add_argument(
        "--mpi",
        action="store_true",
        help=(
            "Enable MPI parallelisation in some parts of the code. "
            + "Requires that the code be installed with support to MPI."
        ),
    )

    # Configure the main parser to handle the commands
    # From python v3.7, add_subparsers accepts a 'required' arg. We
    # could use required=True in the definition below, but, since we
    # want to be able to use python >= 3.6.10, we won't. The requirement
    # of having a command passed will be enforced in the main.py file.
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        description=(
            "Valid commands for {0} (note that commands also accept their "
            + "own arguments, in particular [-h]):"
        ).format(program_name),
        help="command description",
    )

    ##############################################
    # Configure parser for the "cluster" command #
    ##############################################
    parser_cluster = subparsers.add_parser(
        "cluster", help="Run cluster on NetAtmo obs for a single DTG"
    )
    parser_cluster.add_argument(
        "-dtg",
        type=lambda s: datetime.strptime(s, "%Y%m%d%H"),
        default=None,
        help="""
        If not passed, then the first DTG in the config file will be used.
        """,
    )
    parser_cluster.add_argument(
        "--show",
        action="store_true",
        help="Open a browser window to show results on a map",
    )
    parser_cluster.add_argument(
        "--savefig",
        action="store_true",
        help="Save an html file showing results on a map",
    )
    parser_cluster.set_defaults(func=cluster_obs_single_dtg)

    #############################################
    # Configure parser for the "select" command #
    #############################################
    parser_select = subparsers.add_parser(
        "select",
        help=(
            "Go over a list of DTGs and use clustering to select NetAtmo "
            + "stations that are reliable throughout the survey"
        ),
    )
    parser_select.add_argument(
        "--save-obsoul",
        action="store_true",
        help="Re-read the input NetAtmo files and save parsed data in OBSOUL "
        + "format, keeping only data related to the the accepted stations",
    )
    parser_select.set_defaults(func=select_stations)

    #################################################
    # Configure parser for the "csv2obsoul" command #
    #################################################
    parser_csv2obsoul = subparsers.add_parser(
        "csv2obsoul",
        help="Convert data from NetAtmo CSV files into OBSOUL format",
    )
    parser_csv2obsoul.add_argument(
        "--rm-duplicate-stations",
        action="store_true",
        help="Remove duplicates of station reports within same DTG. It keeps "
        + "the one whose obs time is closest to the asismilation time",
    )
    parser_csv2obsoul.add_argument(
        "--rm-moving-stations",
        action="store_true",
        help="Remove stations that change any of (lat, lon, alt) within the "
        + "selected asismilation windows",
    )
    parser_csv2obsoul.add_argument(
        "--dropna",
        action="store_true",
        help="Drop NA (NaN, not a number) values",
    )
    parser_csv2obsoul.add_argument(
        "--fillna",
        # 0.1699999976e39 is obsoul's sentinel value
        default=0.1699999976e39,
        action=StoreDictKeyPair,
        nargs="+",
        metavar="data_column=fillna_value_for_col",
    )
    parser_csv2obsoul.add_argument(
        "--selected-stations-fpath",
        metavar="STATIONS_FILE_PATH",
        default=None,
        type=Path,
        help=(
            "Path to the optional selected stations file. If specified, "
            + "then only these stations are kept."
        ),
    )

    parser_csv2obsoul.set_defaults(func=csv2obsoul)

    ###########################################
    # Configure parser for the "thin" command #
    ###########################################
    parser_thin = subparsers.add_parser(
        "thin",
        help=(
            "Thin data from input file(s) using the thinning configs "
            "specified for the adopted domain."
        ),
    )
    parser_thin.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=list(Path(".").glob("*.csv")),
        help=(
            "Path(s) to input CSVs containing at least (lon, lat) data. "
            "Directory paths are also accepted, in which case they will be "
            "recursively searched for CSV files."
        ),
    )
    parser_thin.set_defaults(func=thin_data_from_csv_files)

    ###########################################
    # Configure parser for the "apps" command #
    ###########################################
    parser_apps = subparsers.add_parser(
        "apps",
        help=(
            "Start a server for the provided Dash apps. "
            + "N.B.: The apps are meant to be used for tests only."
        ),
    )
    parser_apps.set_defaults(
        func=lambda args: subprocess.run(
            [
                Path(__file__).parent.resolve() / "bin" / "start_apps",
                args.config_file.resolve(),
            ],
            check=True,
        )
    )

    ###########################################
    # Configure parser for the "show" command #
    ###########################################
    parser_show = subparsers.add_parser(
        "show",
        help="Display results from netatmoqc output files, as well as configs",
    )
    parser_show.add_argument(
        "file_list",
        nargs="*",
        type=Path,
        default=list(Path(".").glob("*.csv")),
        help="List of files the results should be read from",
    )
    parser_show.add_argument(
        "--config",
        action="store_true",
        help="Dump the used configs, including defaults, in TOML format",
    )
    parser_show.add_argument(
        "--domain",
        action="store_true",
        help="Open a browser window and show the configured domain",
    )
    parser_show.set_defaults(func=show)

    args = parser.parse_args()

    return args
