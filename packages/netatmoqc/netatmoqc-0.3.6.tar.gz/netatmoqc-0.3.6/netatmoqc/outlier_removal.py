#!/usr/bin/env python3
"""Code related to outlier removal functionality."""
import logging
import time

import numpy as np
from numba import njit, prange
from sklearn.neighbors import LocalOutlierFactor

logger = logging.getLogger(__name__)


# Routines related to the "iterative" outlier removal method
@njit(cache=True)
def _trim_np_array(array, perc, min_size=3):
    """Remove extreme values from both sides of an array.

    Takes an array and removes the "50*perc %" largest and
    "50*perc %" smallest elements, provided that the resulting
    trimmed array has a length no smaller tyan min_size

    Args:
        array (numpy.array): Input array.
        perc (float): Proportion of the array elements to be removed. Should be
            between 0 and 1.
        min_size (int): Size below which the array does not get truncated.
            (Default value = 3)

    Returns:
        numpy.array: Truncated array.

    """
    len_array = len(array)
    n_rm_each_side = int(abs(perc) * 0.5 * len_array)
    truncated_size = len_array - 2 * n_rm_each_side
    if (truncated_size != len_array) and (truncated_size >= min_size):
        array.sort()
        array = array[n_rm_each_side:-n_rm_each_side]
    return array


@njit(cache=True, parallel=True)
def _truncated_means_and_stds(df, perc, min_size=3):
    """Return truncated means and stdevs for all columns in the dataframe df.

    Takes a numpy version "df" of a pandas dataframe (obtained by
    calling the ".to_numpy" method on the original dataframe) and

    Args:
        df (numpy.ndarray): The input data.
        perc (float): Proportion of the array elements to be removedi for the
            truncation used in the calculation of the stds and means. Should be
            between 0 and 1.
        min_size (int): Size below which the data column arrays don't get
            truncated in the calculation of the stds and means.
            (Default value = 3)

    Returns:
        {
            numpy.array: Truncated means calculated for each column in the
                input data.
            numpy.array: Truncated stds for each column in the data.
        }

    """
    ncols = df.shape[1]
    means = np.zeros(ncols)
    stds = np.zeros(ncols)
    for icol in prange(ncols):
        array = _trim_np_array(df[:, icol], perc, min_size)
        means[icol] = np.mean(array)
        stds[icol] = np.std(array)
    return means, stds


@njit(cache=True, parallel=True)
def _filter_outliers_iterative_one_iter(
    df, max_n_stdev_around_mean, truncate, weights
):
    """Execute one iteration of the _filter_outliers_iterative function.

    Args:
        df (numpy.ndarray): Matrix (obtained from a dataframe) containing
            clustering info. The cluster labels are assumed to have been
            stored in the last column of df.
        max_n_stdev_around_mean (float): Max allowed number of stdevs around
            the mean for an observation to be considered acceptable.
        truncate (float): Proportion of array elements to be removed for the
            calculation of the truncated stds and means. Should lie between
            0 and 1.
        weights (numpy.array): Weights chosen for each observation parameter.

    Returns:
        numpy.ndarray: Input matrix with cluster labels for outlier obs
            reassigned to -2.

    """
    unique_labels = np.unique(df[:, -1])
    for label in unique_labels[unique_labels > -1]:
        indices_for_label = np.transpose(np.argwhere(df[:, -1] == label))[0]

        cols_taken_into_acc = []
        for icol in range(df.shape[1] - 1):
            if icol in [0, 1]:
                if weights[0] < 1e-3:
                    continue
            elif weights[icol - 1] < 1e-3:
                continue
            cols_taken_into_acc.append(icol)
        cols_taken_into_acc = np.array(cols_taken_into_acc)

        df_subset = df[indices_for_label, :][:, cols_taken_into_acc]
        means, stds = _truncated_means_and_stds(df_subset, truncate)
        tol = max_n_stdev_around_mean * stds[:]
        for irow in indices_for_label:
            for icol in cols_taken_into_acc:
                if np.abs(df[irow, icol] - means[icol]) > tol[icol]:
                    # Use "-2" as a "removed by refining methods" flag
                    df[irow, -1] = -2
                    break

    return df


def _filter_outliers_iterative(
    df,
    max_num_iter=100,
    max_n_stdev_around_mean=2.0,
    trunc_perc=0.0,
    weights=None,
):
    """Detect & assign new labels to obs where abs(obs[i]-obs_mean)>tolerance.

    Helper function for the filter_outliers_iterative routine.

    Args:
        df (pandas.Dataframe): Dataframe containing clustering info.
        max_num_iter (int): Max number of iterations performed.
            (Default value = 100).
        max_n_stdev_around_mean (float): Max allowed number of stdevs around
            the mean for an observation to be considered acceptable.
            (Default value = 2.0).
        trunc_perc (float): Proportion of array elements to be removed for the
            calculation of the truncated stds and means. Should lie between
            0 and 1. (Default value = 0.0).
        weights (numpy.array): Weights chosen for each observation parameter.
            If None is passed, then all obs will have the same weight.
            (Default value = None).

    Returns:
        numpy.array: Array with clustering labels for each row in the input
            data. Entries considered to be outliers by this routine will be
            assigned the integer cluster label "-2".

    """
    used_cols = [
        "lat",
        "lon",
        "alt",
        "mslp",
        "pressure",
        "temperature",
        "humidity",
        "sum_rain_1",
        "cluster_label",
    ]
    df = df.loc[:, df.columns.intersection(used_cols)].to_numpy()
    if weights is None:
        # (lat, lon) -> geodist weight; remove "cluster_label" from weights
        weights = np.ones(
            len([_ for _ in df.columns if _ not in ["lat", "cluster_label"]])
        )
    # Set any negative weight value to zero
    weights = np.where(weights < 0, 0.0, weights)

    n_removed_tot = 0
    verbose = (logger.getEffectiveLevel() == logging.DEBUG,)
    for i in range(max_num_iter):
        if verbose:
            print("    > Refining scan, iteration ", i + 1, ": ", end=" ")
            start_time = time.time()
        # We use "-2" as a "removed by refining methods" flag
        n_removed_old = np.count_nonzero(df[:, -1] == -2)
        df = _filter_outliers_iterative_one_iter(
            df, max_n_stdev_around_mean, truncate=trunc_perc, weights=weights,
        )
        n_removed_new = np.count_nonzero(df[:, -1] == -2)
        n_removed_this_iter = n_removed_new - n_removed_old
        n_removed_tot = n_removed_tot + n_removed_this_iter
        if verbose:
            print("* rm ", n_removed_this_iter, end=" ")
            print(" stations, ", n_removed_tot, " so far. ", end=" ")
            print("Took ", time.time() - start_time, "s")
        if n_removed_this_iter == 0:
            break
    return df[:, -1]


def filter_outliers_iterative(
    df,
    skip,
    weights,
    trunc_perc=0.25,
    max_num_refine_iter=1000,
    max_n_stdev_around_mean=2.0,
):
    """Filter outliers using an iterative method.

    For each obs type (column) in the dataframe, calculate the mean value
    and standard deviation. Remove rows for which any observation has a value
    lying more than "max_n_stdev_around_mean" stdevs from the corresponding
    column's mean. Repeat the process untill either no data is removed or
    the max number of iterations is reached.

    Args:
        df (pandas.Dataframe): Dataframe containing clustering info.
        skip (list): List of names of columns in the df to be skipped (i.e.,
            not taken into account in the filtering).
        weights (numpy.array): Weights chosen for each observation parameter.
            If None is passed, then all obs will have the same weight.
        trunc_perc (float): Proportion of array elements to be removed for the
            calculation of the truncated stds and means. Should lie between
            0 and 1. (Default value = 0.25).
        max_num_refine_iter (int): Max number of iterations performed.
            (Default value = 1000).
        max_n_stdev_around_mean (float): Max allowed number of stdevs around
            the mean for an observation to be considered acceptable.
            (Default value = 2.0).

    Returns:
        pandas.Dataframe: Copy of input data, with clustering labels reassigned
            such that outliers are marked with integer label "-2".

    """
    df["cluster_label"] = _filter_outliers_iterative(
        df.drop(list(skip), axis=1),
        max_num_iter=max_num_refine_iter,
        max_n_stdev_around_mean=max_n_stdev_around_mean,
        trunc_perc=trunc_perc,
        weights=weights,
    ).astype(int)
    return df


# GLOSH outlier removal method
def filter_outliers_glosh(df, outlier_scores):
    """Detect outliers using the GLOSH method.

    Args:
        df (pandas.Dataframe): Input data with clustering info.
        outlier_scores (numpy.array): GLOSH outlier scores for each row
            in the input dataframe.

    Returns:
        pandas.Dataframe: Copy of input data, with clustering labels reassigned
            such that outliers are marked with integer label "-2".

    """
    df["GLOSH"] = outlier_scores
    threshold = min(0.25, df[df["cluster_label"] > -1]["GLOSH"].quantile(0.75))
    outliers_index = (df["cluster_label"] > -1) & (df["GLOSH"] > threshold)
    # Use "-2" as a "removed by refining methods" flag
    df.at[outliers_index, "cluster_label"] = -2
    return df


# Routines related to the LOF outlier removal method
def get_local_outlier_factors(df, distance_matrix, calc_per_cluster=False):
    """Calculate local outlier factors (LOF) for entries in the input data.

    Args:
        df (pandas.Dataframe): Input data with clustering info.
        distance_matrix (netatmoqc.metrics.HollowSymmetricMatrix): Distance
            matrix consistent with the input data.
        calc_per_cluster (bool): Calculate the LOF scores in a per-cluster
            basis (True) or using the dataset as a whole (False).
            (Default value = False).

    Returns:
        numpy.array: Local outlier factors (LOF) for every row of the
            input data.

    """
    # See <https://scikit-learn.org/stable/modules/generated/
    # sklearn.neighbors.LocalOutlierFactor.html#>
    unique_labels = df["cluster_label"].unique()
    all_lof_values = np.empty(len(df.index))
    all_lof_values[:] = np.nan
    # Is it better to do this in a per-cluster basis or
    # with the dataset as a whole? Maybe, with such a small
    # n_neighbors, the results won't change much.
    if calc_per_cluster:
        for label in unique_labels:
            if label < 0:
                continue
            indices = df.index[df["cluster_label"] == label]
            clf = LocalOutlierFactor(
                n_neighbors=min(3, len(indices)), metric="precomputed"
            )
            clf.fit_predict(distance_matrix.subspace(indices))
            all_lof_values[indices] = clf.negative_outlier_factor_
    else:
        indices = df.index[df["cluster_label"] > -1]
        clf = LocalOutlierFactor(n_neighbors=3, metric="precomputed")
        clf.fit_predict(distance_matrix.subspace(indices))
        all_lof_values[indices] = clf.negative_outlier_factor_
    return all_lof_values


def filter_outliers_lof(df, distance_matrix):
    """Filter outliers based on LOF scores.

    Args:
        df (pandas.Dataframe): Input data with clustering info.
        distance_matrix (netatmoqc.metrics.HollowSymmetricMatrix): Distance
            matrix consistent with the input data.

    Returns:
        pandas.Dataframe: Copy of input data, with clustering labels for
        outlier observations reassigned with integer label "-2".

    """
    df["LOF"] = get_local_outlier_factors(df, distance_matrix)
    outliers_index = (df["cluster_label"] > -1) & (df["LOF"] < -1.5)
    # Use "-2" as a "removed by refining methods" flag
    df.at[outliers_index, "cluster_label"] = -2
    return df


# Higher-level outlier removal routine calling the specific ones defined above
def filter_outliers(df, db, outlier_rm_method, distance_matrix, **kwargs):
    """Filter outliers according to specified outlier detection method.

    Args:
        df (pandas.Dataframe): Input data with clustering info.
        db (obj): Output of clustering method.
        outlier_rm_method (str): Outlier detection method of choice.
        distance_matrix (netatmoqc.metrics.HollowSymmetricMatrix): Distance
            matrix consistent with the input data.
        **kwargs: Passed on to internalm wrapped routines.

    Returns:
        pandas.Dataframe: Copy of input data, with clustering labels for
        outlier observations reassigned with integer label "-2".

    """
    tstart = time.time()
    logger.debug(
        '    > Running outlier removal method "%s" with kwargs=%s',
        outlier_rm_method,
        kwargs,
    )
    # Copy original cluster labels to a new column, so we can keep track
    # of where the removed obs came from
    df["original_cluster_label"] = df["cluster_label"]
    if outlier_rm_method == "glosh":
        rtn = filter_outliers_glosh(df, outlier_scores=db.outlier_scores_)
    elif outlier_rm_method == "lof":
        rtn = filter_outliers_lof(df, distance_matrix=distance_matrix)
    elif outlier_rm_method == "reclustering":
        func = kwargs.pop("reclustering_function")
        rtn = func(df, distance_matrix, **kwargs)
    else:
        rtn = filter_outliers_iterative(df, **kwargs)
    logger.debug(
        "      * Done with outlier removal. Elapsed: %.1fs",
        time.time() - tstart,
    )

    return rtn
