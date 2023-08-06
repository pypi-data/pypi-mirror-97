#!/usr/bin/env python3
"""Calculation of custom metrics used in the code."""
import atexit
import logging
import time

import numba
import numpy as np
from numba import njit, prange

from .hollow_symmetric_matrix import (
    HollowSymmetricMatrix,
    _data_index_to_matrix_index,
)

logger = logging.getLogger(__name__)


@njit(cache=True)
def haversine_distance(point1, point2):
    """Return the Haversine distance between point1 and point2."""
    lat1 = np.deg2rad(point1[0])
    lat2 = np.deg2rad(point2[0])
    dlat = lat2 - lat1
    dlon = np.deg2rad(point2[1] - point1[1])
    param_a = (
        np.sin(dlat * 0.5) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon * 0.5) ** 2
    )
    # earth_mean_diameter = 12742.0176 Km
    rtn = 12742.0176 * np.arcsin(np.sqrt(param_a))
    return rtn


@njit(cache=True)
def get_obs_norm_factors(obs_values):
    """Return multiplicative factor to normalise obs_values."""
    stdev = np.std(obs_values)
    obs_mean = np.mean(obs_values)
    if (
        (abs(obs_mean) > 1e-5 and abs(stdev / obs_mean) < 1e-5)
        or abs(obs_mean) <= 1e-5
        and stdev < 1e-7
    ):  # pylint: disable=chained-comparison
        rtn = 0.0
    else:
        rtn = 1.0 / stdev
    return rtn


@njit("f4[:](f8[:, :], f8[:])", parallel=True, cache=True)
def calc_distance_matrix_numba(df, weights):
    """Calculate distance matrix using python+numba.

    Args:
        df (numpy.ndarray): Multidimensional numpy array containing the data
            entries, obtained from a pandas dataframe (numba doesn't work with
            pandas datafames).
        weights (numpy.array): Weights chosen for each observation parameter.
            The weigts determine the relative importance of the observation
            parameters w.r.t. each other.

    Returns:
        numpy.ndarray: Distance matrix.

    """
    nrows, ncols = df.shape

    # Get normalisation factors so that observations in different
    # scales have comparable diff values
    # Remember: The first entry in weights refers to geo_dist and
    #           the first two columns of df are (lat, lon)
    obs_norm_factors = np.ones(ncols - 1, dtype=np.float32)
    for i in range(1, len(obs_norm_factors)):
        obs_norm_factors[i] = get_obs_norm_factors(df[:, i + 1])

    # weights can be used by the users to give extra or
    # lower weight to a given observation type. The weights
    # are applied to the normalised values of the obd diffs
    #
    # We are not normalising geodists. Therefore, the normalised obs
    # dists should have the same units as the geodists (km).
    # Let's assign 10 km/normalized_obs_unit_diff by default
    # This unit conversion is highly arbitrary...

    weights_internal = weights
    # Set any negative weight value to zero
    weights_internal = np.where(weights_internal < 0, 0.0, weights_internal)
    weights_internal *= obs_norm_factors

    n_dists = (nrows * (nrows - 1)) // 2
    rtn = np.zeros(n_dists, dtype=np.float32)
    # For better parallel performance, loop over single idist instead of doing
    # a nested "for i in prange(nrows): for j in range(i+1, nrows):".
    # If one wishes to reverse this, then use func _matrix_index_to_data_index
    # or note that idist = i*nrows - i*(i+1)//2 + (j - i - 1)
    # NB.: Initialising i and j as integers, otherwise numba v0.50.1 fails
    # silently and gives wrong results in python 3.8 with "parallel=True".
    # Strangely, the results are correct without initialisation when using
    # python 3.6 or when setting parallel=False.
    i, j = np.zeros(2, dtype=np.int64)
    for idist in prange(n_dists):  # pylint: disable=not-an-iterable
        i, j = _data_index_to_matrix_index(nrows, idist, check_bounds=False)
        rtn[idist] = weights_internal[0] * haversine_distance(
            df[i], df[j]
        ) + np.sum(
            np.sqrt((weights_internal[1:] * (df[j, 2:] - df[i, 2:])) ** 2)
        )

    return rtn


def calc_distance_matrix(df, weights, optimize_mode, num_threads=-1):
    """Calculate distance matrix between obs in dataframe df.

    Args:
        df (pandas.Dataframe): Input data.
        weights (numpy.array): Weights chosen for each observation parameter.
            The weigts determine the relative importance of the observation
            parameters w.r.t. each other.
        optimize_mode: How the distance matrix is to be calculated and stored.
            This is passed onto the constructor for the class
            netatmoqc.hollow_symmetric_matrix.HollowSymmetricMatrix.
        num_threads: Max number of threads used for the computation.
            (Default value = -1)

    Returns:
        netatmoqc.hollow_symmetric_matrix.HollowSymmetricMatrix: The distance
            matrix.

    """
    logger.debug("    > Calculating distance matrix...")
    tstart = time.time()

    if num_threads > 0:
        original_nthreads = numba.get_num_threads()
        numba.set_num_threads(num_threads)
        atexit.register(numba.set_num_threads, original_nthreads)

    rtn = HollowSymmetricMatrix(
        data=calc_distance_matrix_numba(df.to_numpy(), weights=weights),
        optimize_mode=optimize_mode,
    )

    logger.debug(
        "      * Done calculating distance matrix. Elapsed: %.1fs",
        time.time() - tstart,
    )
    return rtn
