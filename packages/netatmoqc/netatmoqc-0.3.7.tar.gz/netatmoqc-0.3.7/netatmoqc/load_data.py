#!/usr/bin/env python3
"""Routines, classes and definitions employed to load NetAtmo data."""
import logging
import time
from datetime import datetime
from pathlib import Path

import humanize
import numpy as np
import pandas as pd
from pytz import timezone

from .dtgs import Dtg, epoch2datetime

logger = logging.getLogger(__name__)


class DataNotFoundError(Exception):
    """Exeption to be raised when data has not been found."""


class DataFrameWithDtgMetadata(pd.DataFrame):
    """Pandas DataFrame with added "metadata_dict" attribute."""

    # See <https://pandas.pydata.org/pandas-docs/stable/development/
    #      extending.html#define-original-properties>
    # Define _internal_names and _internal_names_set for temporary properties
    # which WILL NOT be passed to manipulation results.
    # Define _metadata for normal properties which will be passed to
    # manipulation results.
    # See also:
    # <https://stackoverflow.com/a/23200907>
    # <https://github.com/pandas-dev/pandas/issues/6927#issuecomment-41086742>

    # temporary properties
    _internal_names = pd.DataFrame._internal_names + ["temp_property"]
    _internal_names_set = set(_internal_names)

    # normal properties
    _metadata = pd.DataFrame._metadata + ["metadata_dict"]

    def __init__(self, *args, **kwargs):
        """Initialise pandas DataFrame and then add "metadata_dict" attr."""
        self.metadata_dict = {}
        super().__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return DataFrameWithDtgMetadata

    def __finalize__(self, other, method=None, **kwargs):
        for name in self._metadata:
            if name == "metadata_dict":
                # Sometimes "other" is actually an iterable. We'll make it
                # so the final dict merge works with the iterable "others"
                try:
                    _ = other.metadata_dict
                    # Has metadata_dict attr. Let's use it as "others"
                    others = [other]
                except AttributeError:
                    try:
                        # "other" has "objs" attr. Let "objs" become "others".
                        others = other.objs
                    except AttributeError:
                        # No "objs" attr. Assume "other" is itself iterable and
                        # allow TypeError to be raised later otherwise (because
                        # then we don't know what "other" is)
                        others = other

                # Compare metadata dicts and keep only common keys/vals
                md_dicts_to_combine = [getattr(_, name, {}) for _ in others]
                self_md_dict = getattr(self, name, {})
                if self_md_dict:
                    md_dicts_to_combine.append(self_md_dict)

                common_keys = set()
                for dic in md_dicts_to_combine:
                    if dic == {}:
                        # If any dict is empty, then there will be no
                        # common keys at all.
                        common_keys = set()
                        break
                    common_keys = common_keys.union(set(dic))

                combined_md_dict = {}
                for key in common_keys:
                    val = np.unique([dic[key] for dic in md_dicts_to_combine])
                    if len(val) == 1:
                        combined_md_dict[key] = val[0]

                object.__setattr__(self, name, combined_md_dict)
            else:
                object.__setattr__(self, name, getattr(other, name, None))

        return self


@np.vectorize
def mslp2sp_coeff(alt):
    """Coeff to convert mean sea-level pressure to pressure at altitude alt.

    Args:
        alt: Altitude in meters.

    Returns:
        float: Which multiplies by the mslp to give the surface pressure at alt

    """
    return 1.0 / (
        int(round(100000 / ((288 - 0.0065 * alt) / 288) ** 5.255)) / 100000
    )


@np.vectorize
def shorten_stat_id(stat_id):
    """Shorten station ID to length 8."""
    if not isinstance(stat_id, str):
        return stat_id
    return stat_id[-8:]


def read_netatmo_csv(
    path,
    dropna=True,
    fillna=None,
    recover_pressure_from_mslp=False,
    drop_mslp=None,
):
    """Read CSV files with NetAtmo observation data.

    Args:
        path (pathlib.Path): Full path to the csv file.
        dropna (bool): Whether or not to exclude NaNs (Default value = True).
        fillna (dict): Dictionary having data parameters as keys and the fill
            values (which will replace NaNs) as dict values. The filling of
            NaNs is performed prior to dropping NaNs. (Default value = None).
        recover_pressure_from_mslp (bool): The netatmo csv files are assumed to
            contain mslp data instead of surface pressure. This flag controls
            whether surface pressure should also be included in the read data.
            If True. then a new column "pressure" will be added with surface
            pressure calculated from altitude and mslp.
            (Default value = False)
        drop_mslp (bool): Whether ot not to drop the original mslp after
            having created a new "pressure" column with surface pressure.
            If None is used, then drop_mslp takes the value of the
            recover_pressure_from_mslp parameter.
            (Default value = None)

    Returns:
        pandas.Dataframe: Data read from the input netatmo csv file.

    Raises:
        ValueError: If drop_mslp evaluates to True while
            recover_pressure_from_mslp evaluates to False.

    """
    if drop_mslp is None:
        drop_mslp = recover_pressure_from_mslp
    if drop_mslp and not recover_pressure_from_mslp:
        raise ValueError(
            "Cannot have drop_mslp=True and recover_pressure_from_mslp=False"
        )

    # Set fillna to default value if None passed.
    # Do this here instead of having a dict default because dict is mutable,
    # and default args are created at function definition time.
    if fillna is None:
        fillna = dict(sum_rain_1=0.0)

    data = pd.read_csv(path)
    # Replacing/removing invalid data (NaNs)
    if fillna:
        # fillna may be a key:val map (dict), in which case NaNs in col "key"
        # will be filled with value "val". Fill NaNs before dropping!
        data = data.fillna(fillna)
    if dropna:
        data = data.dropna()

    # Drop the 'enc:16:' stat id prefix and shorten them to 8 chars
    data["id"] = shorten_stat_id(data["id"])

    # The netatmo data I got from Norway has mean sea-level pressure
    # instead of pressure, but the label is "pressure" there. Fix this.
    data = data.rename(columns={"pressure": "mslp"})
    pressure_cols = ["mslp"]
    if recover_pressure_from_mslp:
        data["pressure"] = mslp2sp_coeff(data["alt"]) * data["mslp"]
        pressure_cols += ["pressure"]
    # Make sure columns 'id', 'time_utc', 'lat' and 'lon' appear
    # first AND in this order
    data = data[
        ["id", "time_utc", "lat", "lon", "alt"]
        + pressure_cols
        + ["temperature", "humidity", "sum_rain_1"]
    ]
    if drop_mslp:
        data = data.drop(["mslp"], axis=1)

    data["time_utc"] = epoch2datetime(data["time_utc"])

    return data.sort_values(by="time_utc").reset_index(drop=True)


def gen_netatmo_fpaths_for_dates(dates, rootdir):
    """Generate netatmo file paths for dates.

    NetAtmo CSV files are assumed to have full paths following the pattern
    "rootdir/%Y/%m/%d/%Y%m%dT%H%M%SZ.csv"

    Args:
        dates (list): List of datetime.datetime objects. Only year, month, and
            day are used.
        rootdir (pathlib.Path): Path to the top-level directory where the
            netatmo input csv files are stored.

    Yields:
        libpath.Path: Paths to files be read in order to get data for date=dt

    """
    try:
        date_iter = iter(dates)
    except TypeError:
        date_iter = [dates]
    rootdir = Path(rootdir).resolve()
    for date in sorted(date_iter):
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        for fpath in sorted((rootdir / year / month / day).glob("*.csv")):
            yield fpath


def read_netatmo_data_for_dates(dates, rootdir, **kwargs):
    """Read netatmo data for passed dates.

    Args:
        dates (list): List of datetime.datetime objects. Only year, month, and
            day are used.
        rootdir (pathlib.Path): Path to the top-level directory where the
            netatmo input csv files are stored.
        **kwargs: Passed to read_netatmo_csv

    Returns:
        pandas.Dataframe: Data read from csv files for the dates passed
            as input.

    Raises:
        DataNotFoundError: If data for the selected dates cannot be found.

    """
    data_from_all_files = {}
    for fpath in gen_netatmo_fpaths_for_dates(dates, rootdir):
        data_from_all_files[fpath.stem] = read_netatmo_csv(fpath, **kwargs)

    if len(data_from_all_files) == 0:
        raise DataNotFoundError(
            "Could not find data for date(s)={} under dir '{}'".format(
                dates, rootdir
            )
        )

    return pd.concat(data_from_all_files, ignore_index=True)


def _datetime_of_netatmo_file(fpath, fmt="%Y%m%dT%H%M%SZ.csv"):
    """Get the datetime from csv file path."""
    dt = datetime.strptime(fpath.name, fmt)
    return dt.replace(tzinfo=timezone("utc"))


# Reading data for a given DTG instead of date
def gen_netatmo_fpaths_for_time_window(start, end, rootdir):
    """Generate NetAtmo csv file paths for datetimes within [start, end].

    Returns a generator of paths leading to NetAtmo files whose names
    correspond to timestamps lying within the closed interval [start, end].

    Args:
        start (datetime.datetime): Start date.
        end (datetime.datetime): End date.
        rootdir (pathlib.Path): Path to the top-level directory
            where the netatmo input csv files are stored.

    Yields:
        pathlib.Path: NetAtmo csv file paths.

    """
    start, end = sorted((start, end))
    dates = pd.date_range(start.date(), end.date(), freq="1d")
    for fpath in gen_netatmo_fpaths_for_dates(dates, rootdir):
        date_time = _datetime_of_netatmo_file(fpath)
        if start <= date_time <= end:
            yield fpath


def gen_netatmo_fpaths_for_dtg(dtg, rootdir):
    """Paths to NetAtmo files that are likely to contain data for DTG=dtg.

    Args:
        dtg (netatmoqc.dtgs.Dtg): Data assimilation DTG.
        rootdir (pathlib.Path): Path to the top-level directory
            where the netatmo input csv files are stored.

    Returns:
        generator: Generator of the NetAtmo csv file paths

    """
    # Add a few minutes to the assimilation window, as
    # netatmo data is gathered every ~10 minutes
    start = dtg.cycle_start - pd.Timedelta("15 minutes")
    end = dtg.cycle_end + pd.Timedelta("15 minutes")
    return gen_netatmo_fpaths_for_time_window(start, end, rootdir=rootdir)


def rm_moving_stations(df):
    """Remove stations that change (lon, lat, alt) from the data.

    Args:
        df (pandas.Dataframe): Input data.

    Returns:
        {
            'pandas.Dataframe': Copy of input df, but with
                moving stations removed,
            'pandas.Dataframe': The moving stations.
        }

    """
    df_grouped_by_id = df.groupby(["id"], as_index=False, sort=False)
    df_temp = df_grouped_by_id[["lat", "lon", "alt"]].agg(["max", "min"])
    inconsistent_stations = df_temp[
        (abs(df_temp["lat"]["max"] - df_temp["lat"]["min"]) >= 1e-4)
        | (abs(df_temp["lon"]["max"] - df_temp["lon"]["min"]) >= 1e-4)
        | (abs(df_temp["alt"]["max"] - df_temp["alt"]["min"]) >= 1e-2)
    ].index.values
    df_ok = df[~df["id"].isin(inconsistent_stations)].reset_index(drop=True)
    df_inconsistent = df[df["id"].isin(inconsistent_stations)].reset_index(
        drop=True
    )
    return df_ok, df_inconsistent


def rm_overlapping_stations(df):
    """Remove from df the stations that have the same (lon, lat).

    Args:
        df (pandas.Dataframe): Input data.

    Returns:
        'pandas.Dataframe': Copy of input df, but with the
            overlapping stations removed.

    """
    overlapping_stations = (
        df[["id", "lat", "lon"]]
        .round(6)
        .groupby(["lat", "lon"], as_index=False, sort=False,)
        .filter(lambda grp: len(grp["id"].unique()) != 1)["id"]
        .unique()
    )
    return df[~df["id"].isin(overlapping_stations)].reset_index(drop=True)


def remove_duplicates_within_cycle(df, dtg):
    """Remove duplicate station reports within DTG.

    Remove duplicates for each station by keeping the one closest to DTG

    If a station reports data multiple times within the time window,
    then keep the one closest to the passed DTG and discard the rest.

    Args:
        df (pandas.Dataframe): Input data.
        dtg (netatmoqc.dtgs.Dtg): The picked assimilation DTG.

    Returns:
        'pandas.Dataframe': Copy of input df, where only one station
            report is kept for each DTG.

    """
    # It seems that using groupby followed by "apply" with a custom
    # function is about 20x slower.
    # Sort using df.loc is better than adding a new col to sort by it. See
    # <stackoverflow.com/questions/39525928/pandas-sort-lambda-function>
    df = df.loc[(abs(df["time_utc"] - dtg)).sort_values().index]
    # We don't need sorting with groupby. HDBSCAN clustering, however,
    # seems to be sensitive to the order in which the rows appear (but
    # not very much so). This seems to be knwon, see, e.g.,
    # <https://github.com/scikit-learn-contrib/hdbscan/issues/265>
    station_groups = df.groupby(["id"], as_index=False, sort=False)
    n_stations_with_duplicates = (station_groups.size()["size"] > 1).sum()
    if n_stations_with_duplicates > 0:
        orig_nobs = len(df.index)
        df = station_groups.first()
        new_nobs = len(df.index)
        msg = "Multiple reports from %d stations in DTG=%s. "
        msg += "Keeping only the one closest to the DTG: "
        msg += "%s obs now became %s"
        logger.debug(
            msg, n_stations_with_duplicates, dtg, orig_nobs, new_nobs,
        )
    return df


def read_netatmo_data_for_dtg(dtg, rootdir, **kwargs):
    """Read NetAtmo data corresponding to the selected DTG.

    Args:
        dtg (netatmoqc.dtgs.Dtg): The picked assimilation DTG.
        rootdir (pathlib.Path): Path to the top-level directory where the
            netatmo input csv files are stored.
        **kwargs: Passed to read_netatmo_csv

    Returns:
        pandas.Dataframe: Data read from csv files for the input DTG.

    Raises:
        DataNotFoundError: If data for the selected DTGs cannot be found.

    """
    t_start = time.time()
    logger.debug("Reading data for DTG=%s...", dtg)

    # Make sure the input DTG behaves as expected
    dtg = Dtg(dtg)

    data_from_all_files = {}
    for fpath in gen_netatmo_fpaths_for_dtg(dtg, rootdir=rootdir):
        data_from_all_files[fpath.stem] = read_netatmo_csv(fpath, **kwargs)
    if len(data_from_all_files) == 0:
        raise DataNotFoundError(
            "Could not find data for DTG={} under dir '{}'".format(
                dtg, rootdir
            )
        )

    df = pd.concat(data_from_all_files, ignore_index=True)
    # Remove DTGs that do not belong to the assimilation time window
    if dtg.assimilation_window.closed_left:
        mask_left = df["time_utc"] >= dtg.assimilation_window.left
    else:
        mask_left = df["time_utc"] > dtg.assimilation_window.left
    if dtg.assimilation_window.closed_right:
        mask_right = df["time_utc"] <= dtg.assimilation_window.right
    else:
        mask_right = df["time_utc"] < dtg.assimilation_window.right
    df = df[mask_left & mask_right]

    # Add DTG metadata, for a future reference of how the data was collated
    df = DataFrameWithDtgMetadata(df)
    df.metadata_dict["dtg"] = dtg

    logger.debug(
        "Dataframe has obs from %d stations, with a memsize=%s",
        len(df.index),
        humanize.naturalsize(df.memory_usage(deep=True).sum()),
    )

    logger.debug(
        "Done reading data for DTG=%s. Elapsed: %.1fs",
        dtg,
        time.time() - t_start,
    )

    return df


def remove_irregular_stations(
    df, moving=True, duplicates=True, overlapping=True
):
    """Remove obs from irregular stations (moving, duplicates or overlaps).

    This is a wrapper for the following routines:
        * rm_moving_stations
        * remove_duplicates_within_cycle
        * rm_overlapping_stations

    Args:
        df (pandas.Dataframe): Input data.
        moving (bool): Whether or not to remove moving stations.
            (Default value = True)
        duplicates (bool): Whether or not to remove duplicate sttaion reports.
            Default value = True)
        overlapping (bool): Whether or not to remove overlapping stations.
            Default value = True)

    Returns:
        {
            'pandas.Dataframe': Copy of input df, but with the
                irregular. stations removed,
            'pandas.Dataframe': Dataframe containing removed movind stations.
        }

    """
    dtg = df.metadata_dict["dtg"]
    if moving:
        # Remove stations that change (lat, lon, alt) within cycle
        df, df_moving_stations = rm_moving_stations(df)
        if len(df_moving_stations.index) > 0:
            logger.debug(
                'Removed %d obs from %d "moving" stations in DTG=%s',
                len(df_moving_stations.index),
                len(df_moving_stations["id"].unique()),
                dtg,
            )
    else:
        df_moving_stations = pd.DataFrame.empty
        logger.warning("Not checking for moving stations")

    if duplicates:
        # Remove duplicate data for stations within cycle by keeping
        # the data reported for the timestamp closest to the passed DTG
        df = remove_duplicates_within_cycle(df, dtg)
    else:
        logger.warning("Not removing duplicate stations")

    if overlapping:
        df = rm_overlapping_stations(df)

    df.metadata_dict["dtg"] = dtg

    return df, df_moving_stations
