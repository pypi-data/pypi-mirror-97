#!/usr/bin/env python3
"""Routines related to clustering."""
import logging
import time
from functools import wraps

import numpy as np
import pandas as pd
from hdbscan import HDBSCAN, RobustSingleLinkage
from sklearn import metrics
from sklearn.cluster import DBSCAN, OPTICS

from .config_parser import UndefinedConfigValue
from .domains import Domain
from .metrics import calc_distance_matrix
from .outlier_removal import filter_outliers

logger = logging.getLogger(__name__)


def sort_df_by_cluster_size(df):
    """Return a version of df with data sorted by cluster_size.

    Sort df so that clusters with more members are put at the top of the
    dataframe. The exception if the "-1" label, which, if present, will
    always remain at the top. Handy if results are to be plotted.

    Args:
        df (pandas.DataFrame): Dataframe with clustering info.

    Returns:
        pandas.DataFrame: Copy of input df sorted by cluster size.

    """
    # The labels may have been reassigned if the df was passed through
    # an outlier removal routine. Let's keep track of the original ones.
    # This will help keeping obs removed from a cluster by the outlier
    # removed routine close to their origin cluster.
    original_cluster_label_col = "cluster_label"
    if "original_cluster_label" in df.columns:
        original_cluster_label_col = "original_cluster_label"

    # Temporarily add a column with cluster sizes for sorting
    unique_labels, member_counts = np.unique(
        df[original_cluster_label_col], return_counts=True
    )
    label2count_dict = dict(zip(unique_labels, member_counts))
    df["parent_cluster_size"] = [
        label2count_dict[label] for label in df[original_cluster_label_col]
    ]
    # Sort dataframe according to frequency, but keep -1 at the top
    df = pd.concat(
        [
            df[df["cluster_label"] == -1],
            df[df["cluster_label"] == -3],
            df[df["cluster_label"] == -4],
            df[~df["cluster_label"].isin([-1, -3, -4])].sort_values(
                [
                    "parent_cluster_size",
                    original_cluster_label_col,
                    "cluster_label",
                ],
                ascending=[False, True, False],
            ),
        ]
    )

    # Reassign labels so that fewer members leads to larger labels.
    # Note that the df unique method does not sort, so this method won't
    # mess up the sorting performed above.
    unique_labels = df[original_cluster_label_col].unique()
    _labels_old2new = {
        old: new
        for new, old in enumerate(lab for lab in unique_labels if lab >= 0)
    }

    @np.vectorize
    def labels_old2new(old):
        if old < 0:
            return old
        return _labels_old2new[old]

    for col in ["cluster_label", "original_cluster_label"]:
        try:
            df[col] = labels_old2new(df[col])
        except KeyError:
            pass

    return df.drop("parent_cluster_size", axis=1).reset_index(drop=True)


def weights_dict_to_np_array(
    df, pairwise_diff_weights=None, skip=("id", "time_utc"), default=1
):
    """Convert pairwise_diff_weights into a numpy array.

    Takes a pandas dataframe and a {column_name:weight} dictionary and returns
    an array of weights to be passed to the routine that calculates the
    distance matrix.

    Columns "lat" and "lon" in df are treated specially, in that they are
    not assigned a weight individually, but rather a single weight gets
    assigned to the "geo_dist" property.

    Args:
        df (pandas.Dataframe): Dataframe with observations.
        pairwise_diff_weights (dict):  {df_column_name:weight} dictionary.
            Default value = None.
        skip: df columns that will not enter the clustering and should
            therefore be skipped. Default value = ("id", "time_utc")
        default: Default weight to be assigned for a non-skipped df column if
            the column name is present in df but not in pairwise_diff_weights.
            Default value = 1.

    Returns:
        numpy.ndarray: weights to be passed to the routine that calculates the
            distance matrix.

    Raises:
        ValueError: If the dataframe 'lat' column is not followed by the 'lon'
            column.

    """
    if df.columns.get_loc("lon") - df.columns.get_loc("lat") != 1:
        raise ValueError("'lat' column is not followed by 'lon' column")

    weights = []
    col2weight = {c: ("geo_dist" if c == "lon" else c) for c in df.columns}
    for col in df.columns[~df.columns.isin(list(skip) + ["lat"])]:
        try:
            weights.append(pairwise_diff_weights[col2weight[col]])
        except (KeyError, TypeError):
            weights.append(default)
    return np.array(weights, dtype=np.float64)


def get_silhouette_samples(df, distance_matrix):
    """Calculate silhouette scores for every obs in df.

    Args:
        df (pandas.Dataframe): Dataframe with observations.
        distance_matrix (HollowSymmetricMatrix): Obs distance matrix.

    Returns:
        pandas.DataFrame: Copy of df with added silhouette samples info.

    """
    # We will only consider true clusters for the calculation of
    # the silhouette coeff, i.e., points with label<0 will be excluded from
    # the calculation. This means that we need to use a slice of the distance
    # matrix in the calculation corresponding to the valid points.
    i_valid_obs = df.reset_index(drop=True).index[df["cluster_label"] >= 0]
    if len(i_valid_obs) == 0:
        logger.warning("No valid obs to calculate silhouette coeffs with")
        return -np.ones(len(df.index))

    reduced_labels = df["cluster_label"].iloc[i_valid_obs]
    if len(reduced_labels.unique()) == 1:
        logger.warning("Only one cluster to calculate silhouette coeffs with")
        return np.ones(len(df.index))

    # Using an intermediate np array is about 10x faster than
    # using df.at[iloc, 'silhouette_score'] = coeff
    all_silhouette_scores = np.empty(len(df.index))
    all_silhouette_scores[:] = np.nan

    reduced_silhouette_scores = metrics.silhouette_samples(
        X=distance_matrix.subspace(i_valid_obs),
        labels=reduced_labels,
        metric="precomputed",
    )
    for iloc, coeff in zip(i_valid_obs, reduced_silhouette_scores):
        all_silhouette_scores[iloc] = coeff

    return all_silhouette_scores


def run_clustering_on_df(
    df,
    method="hdbscan",
    distance_matrix=None,
    distance_matrix_optimize_mode="memory",
    skip=("id", "time_utc"),
    weights_dict=None,
    eps=15,  # eps applies only to dbscan
    min_cluster_size=3,  # min_cluster_size applies only to hdbscan
    min_samples=3,
    n_jobs=-1,
    outlier_rm_method=None,
    max_num_refine_iter=50,
    max_n_stdev_around_mean=2.0,
    trunc_perc=0.25,
    calc_silhouette_samples=True,
):
    """Low-level clustering routine.

    Args:
        df (pandas.Dataframe): Dataframe with observations.
        method (str): {"hdbscan", "dbscan", "rsl", "optics"}
            Clustering method.
        distance_matrix (HollowSymmetricMatrix): Obs distance matrix.
            Default value = None.
        distance_matrix_optimize_mode (str): The distance matrix optimization
            mode. Default value = "memory".
        skip (tuple): Columns to skip in df.
            Default value = ("id", "time_utc").
        weights_dict (dict): obs_name --> obs_weight map. Default value = None.
        eps (float):  DBSCAN's eps parameter. Default value = 15.0.
        min_cluster_size (int):  HDBSCAN's min_cluster_size. Default value = 3.
        min_samples (int): (H)DBSCAN's min_samples. Default value = 3.
        n_jobs (int): Max number of local-host parallel jobs.
            Default value = -1.
        outlier_rm_method (str):  Outlier removal method. Default value = None.
        max_num_refine_iter (int):  Max number of iterations for the
            "iterative" ourlier removal method. Default value = 50.
        max_n_stdev_around_mean (float):  Max number of stdev from cluster obs
            mean for an observation to be considered OK in the "iteractive"
            outlier removal method. Default value = 2.0.
        trunc_perc (float):  Percentage used in array truncation when
            calculating stdevs and means in the "iterative" outlier removal
            method. Default value = 0.25.
        calc_silhouette_samples (bool):  Calculate or not silhouette_samples?
            Default value = True.

    Returns:
        pandas.DataFrame: Copy of df with clustering added info.

    Raises:
        NotImplementedError: If the `method` choice is not valid.

    """
    method = method.lower()
    # Compute clustering using DBSCAN or HDBSCAN
    if method not in ["dbscan", "hdbscan", "rsl", "optics"]:
        raise NotImplementedError('Method "{}" not available.'.format(method))
    if len(df.index) == 0:
        logger.warning("Dataframe has no rows")
        return df

    # Set weights to be used in the metrics for the various
    # generalised distances. The distances used in the metrics
    # will be used_dist(i) = weight(i)*real_dist(i)
    weights = weights_dict_to_np_array(df, weights_dict)

    # We will not do any df = StandardScaler().fit_transform(df),
    # as we'll use a metric based on earth distances

    if distance_matrix is None:
        # My tests indicate that passing a pre-computed distance matrix to
        # dbscan can be up to 2.5x faster than passing a metrics function (if
        # they both are written in pure python) to fit df. If they are both
        # written in fortran and interfaced via f2py3, or then written in
        # python but jit-compiled with numba, then the relative speed up
        # can reach up to 120x.
        distance_matrix = calc_distance_matrix(
            # Drop columns that won't be used in the clustering
            df.drop(list(skip), axis=1),
            weights,
            optimize_mode=distance_matrix_optimize_mode,
            num_threads=n_jobs,
        )

    # Running clustering with the computed distance matrix
    logger.debug("    > Running clustering method '%s'...", method)
    tstart = time.time()
    if method == "dbscan":
        db = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric="precomputed",
            n_jobs=n_jobs,
        ).fit(distance_matrix)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        df["is_core_point"] = core_samples_mask
    elif method == "hdbscan":
        # For more info on the parameters, see
        # <https://hdbscan.readthedocs.io/en/latest/parameter_selection.html>
        db = HDBSCAN(
            min_samples=min_samples,
            min_cluster_size=min_cluster_size,
            metric="precomputed",
            core_dist_n_jobs=n_jobs,
            allow_single_cluster=True,
            # Default cluster_selection_method: 'eom'. Sometimes it leads to
            # clusters that are too big. Using 'leaf' seems better.
            cluster_selection_method="leaf",
        ).fit(distance_matrix)
    elif method == "optics":
        db = OPTICS(
            min_samples=min_samples,
            min_cluster_size=min_cluster_size,
            n_jobs=n_jobs,
            metric="precomputed",
        ).fit(distance_matrix)
    elif method == "rsl":
        db = RobustSingleLinkage(
            # cut: The reachability distance value to cut the cluster
            #      heirarchy at to derive a flat cluster labelling.
            cut=eps,  # default=0.4
            # Reachability distances will be computed with regard to the
            # k nearest neighbors.
            k=min_samples,  # default=5
            # Ignore any clusters in the flat clustering with size less
            # than gamma, and declare points in such clusters as noise points.
            gamma=min_cluster_size,  # default=5
            metric="precomputed",
        ).fit(distance_matrix)
    logger.debug(
        "      * Done with %s. Elapsed: %.2fs", method, time.time() - tstart,
    )
    # Update df with cluster label info. It is important that this is done
    # right before calling filter_outliers, as the filter_outliers function
    # expects 'cluster_label' to be the last column in the dataframe
    df["cluster_label"] = db.labels_

    # Refine clustering if requested
    # It is important to have 'cluster_label' as the last column
    # when running the iterative refine routine
    if outlier_rm_method:
        df = filter_outliers(
            df,
            db=db,
            outlier_rm_method=outlier_rm_method,
            # Args that apply only to LOF
            distance_matrix=distance_matrix,
            # Args that only apply for the iterative method
            skip=skip,
            max_num_refine_iter=max_num_refine_iter,
            max_n_stdev_around_mean=max_n_stdev_around_mean,
            trunc_perc=trunc_perc,
            weights=weights,
            method=method,
            weights_dict=weights_dict,
            eps=eps,
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            n_jobs=n_jobs,
            reclustering_function=self_consistent_reclustering,
        )

    # Calculate silhouette scores and update df with this.
    # We'll be reordering the dataframe later, and calculating the score
    # before doing that avoids the need to also reorder the dist matrix.
    if calc_silhouette_samples:
        df["silhouette_score"] = get_silhouette_samples(df, distance_matrix)

    return df


# self_consistent_reclustering is used in the "reclustering" outlier removal
# method. Disable logging in the function to reduce output clutter.
def suspendlogging(func):
    """Suspend logging in the function it decorates.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.

    """
    # Adapted from: <https://stackoverflow.com/questions/7341064/
    #               disable-logging-per-method-function>

    @wraps(func)
    def _inner(*args, **kwargs):
        previousloglevel = logger.getEffectiveLevel()
        try:
            logger.setLevel(logging.WARN)
            return func(*args, **kwargs)
        finally:
            logger.setLevel(previousloglevel)

    return _inner


@suspendlogging
def self_consistent_reclustering(df, distance_matrix, **kwargs):
    """Recluster obs in df until further clustering on df returns df itself.

    Args:
        df (pandas.Dataframe): Pandas dataframe with observations and initial
            clustering info.
        distance_matrix (HollowSymmetricMatrix): Matrix of distances between
            the obs in df.
        **kwargs: Keyword args passed to run_clustering_on_df.

    Returns:
        pandas.Dataframe: Copy of df where obs have been clustered multiple
            times until run_clustering_on_df(df, ...) = df.

    """
    n_iter = 0
    n_removed = 0
    n_noise = np.count_nonzero(df["cluster_label"] < 0)
    while n_noise != 0:
        noise_mask = df["cluster_label"] < 0
        df_noise = df[noise_mask]
        i_valid_obs = np.nonzero((~noise_mask).values)[0]

        df = df.drop(df[noise_mask].index)
        df = df.drop(["cluster_label"], axis=1)
        df_rec = run_clustering_on_df(
            df,
            outlier_rm_method=None,
            distance_matrix=distance_matrix.subspace(i_valid_obs),
            calc_silhouette_samples="silhouette_score" in df.columns,
            **kwargs,
        )
        n_noise = np.count_nonzero(df_rec["cluster_label"] < 0)
        df = pd.concat([df_noise, df_rec]).sort_index()
        n_iter += 1
        n_removed += n_noise
        logger.debug("        * Iter #%d: %d new noise pts", n_iter, n_noise)
    logger.debug("    > Done with reclustering. %d removed obs.", n_removed)
    return df


def _cluster_netatmo_obs_one_domain(df, config, **kwargs):
    """Cluster netatmo obs inside a given domain.

    Helper for the main routine cluster_netatmo_obs

    Args:
        df (pandas.Dataframe): Pandas dataframe with observations.
        config (ParsedConfig): Parsed configs.
        **kwargs: Keyword args passed to run_clustering_on_df.

    Returns:
        pandas.DataFrame: Copy of df with clustering added info.

    """
    time_start_clustering = time.time()
    logger.debug("Performing clustering...")
    outlier_rm_method = config.get_clustering_opt("outlier_removal.method")
    df = run_clustering_on_df(
        df=df,
        method=config.general.clustering_method,
        distance_matrix_optimize_mode=config.general.custom_metrics_optimize_mode,
        weights_dict=config.get_clustering_opt("obs_weights"),
        eps=config.get_clustering_opt("eps"),
        min_cluster_size=config.get_clustering_opt("min_cluster_size"),
        min_samples=config.get_clustering_opt("min_samples"),
        outlier_rm_method=outlier_rm_method,
        max_num_refine_iter=config.get_clustering_opt(
            "outlier_removal.{}.max_n_iter".format(outlier_rm_method)
        ),
        max_n_stdev_around_mean=config.get_clustering_opt(
            "outlier_removal.{}.max_n_stdev".format(outlier_rm_method)
        ),
        **kwargs,
    )
    time_end_clustering = time.time()
    logger.debug(
        "Done with clustering. Elapsed: %.2fs",
        time_end_clustering - time_start_clustering,
    )

    return df


def cluster_netatmo_obs(df, config, **kwargs):
    """Cluster NetAtmo observations.

    Args:
        df (pandas.Dataframe): Pandas dataframe with observations.
        config (ParsedConfig): Parsed configs.
        **kwargs: Keyword args passed to _cluster_netatmo_obs_one_domain.

    Returns:
        pandas.DataFrame: Copy of df with clustering added info.

    """
    # Load domain configs from config
    domain = Domain.construct_from_dict(config.domain)

    # Trim obs to keep only those inside domain. Do this here instead of
    # upon reading so we do this only once.
    n_rmvd = len(df.index)
    df = domain.trim_obs(df)
    n_rmvd -= len(df.index)
    if n_rmvd > 0:
        logger.debug("Removed %d obs outside %s domain", n_rmvd, domain.name)

    df_rejected = None
    if domain.n_subdomains > 1:
        # Perform preliminary clustering on small domains in order to
        # eliminate stations at low cpu/mem cost (O(n^2))
        logger.debug(
            "DTG=%s: Preliminary clustering over %d subdomains...",
            df.metadata_dict["dtg"],
            domain.n_subdomains,
        )
        domain_split_dfs = []
        # Silhouette samples are not needed at this point
        pre_clustering_kwargs = kwargs.copy()
        pre_clustering_kwargs["calc_silhouette_samples"] = False
        for isubd, subdomain in enumerate(domain.split()):
            df_sub = subdomain.trim_obs(df)

            min_cluster_size = config.get_clustering_opt("min_cluster_size")
            if min_cluster_size is UndefinedConfigValue:
                min_cluster_size = config.get_clustering_opt("min_samples")
            if len(df_sub.index) < min_cluster_size:
                logger.debug(
                    "DTG=%s: Too few obs (=%d) in subdomain %d/%d. Rejecting.",
                    df.metadata_dict["dtg"],
                    len(df_sub.index),
                    isubd + 1,
                    domain.n_subdomains,
                )
                df_sub["cluster_label"] = -1
                domain_split_dfs.append(df_sub)
                continue
            logging.debug(
                "DTG=%s: Pre-clustering %d obs in subdomain %d/%d",
                df.metadata_dict["dtg"],
                len(df_sub.index),
                isubd + 1,
                domain.n_subdomains,
            )
            df_sub = _cluster_netatmo_obs_one_domain(
                df=df_sub, config=config, **pre_clustering_kwargs
            )

            domain_split_dfs.append(df_sub)

        # Gather results from preliminary clustering in a single dataframe
        df_rejoined_split = pd.concat(domain_split_dfs, ignore_index=True)

        # Mark with flag -3 obs that were removed by outlier removal methods at
        # the pre-clustering stage (which are flagged with "-2")
        df_rejoined_split["cluster_label"].mask(
            df_rejoined_split["cluster_label"] == -2, -3, inplace=True
        )

        # Check for stations missed in the splits, (unlikely, but just in case)
        df_split_missed = df[~df["id"].isin(df_rejoined_split["id"])]
        if len(df_split_missed.index) > 0:
            logger.warning(
                "%d obs missed during subdomain split. Rejecting.",
                len(df_split_missed.index),
            )
            # Mark missed obs with cluster label -4
            df_split_missed["cluster_label"] = -4
            df_rejoined_split = pd.concat(
                [df_rejoined_split, df_split_missed], ignore_index=True
            )

        # Reset df: Only accepted obs will be passed on to the whole-domain
        # clustering. Rejections will be added again to df after that.
        df_rejected = df_rejoined_split[
            df_rejoined_split["cluster_label"] < 0
        ].copy()
        cols_to_drop = [c for c in df_rejected.columns if c not in df.columns]
        df = df_rejoined_split
        df = df[~df["id"].isin(df_rejected["id"])].drop(cols_to_drop, axis=1)
        df = df.reset_index(drop=True)

    # Run whole-domain clustering, regardless of splitting in subdomains or not
    if domain.n_subdomains > 1:
        logger.debug(
            "DTG=%s: Main clustering over whole domain...",
            df.metadata_dict["dtg"],
        )
    df = _cluster_netatmo_obs_one_domain(df=df, config=config, **kwargs)

    if df_rejected is not None:
        # Put back eventual obs rejected at the pre-clustering step
        if "original_cluster_label" in df.columns:
            df_rejected["original_cluster_label"] = df_rejected[
                "cluster_label"
            ].copy()
        df = pd.concat([df, df_rejected], ignore_index=True)

    # Now we're done.
    return df


def report_clustering_results(df):
    """Print some relevant info about the clustering.

    Args:
        df (pandas.DataFrame): Dataframe with clustering info.

    """
    if len(df.index) == 0:
        logger.info("Dataframe has no rows. No results to report.")
        return

    n_obs = len(df.index)
    noise_data_df = df[df["cluster_label"] < 0]
    n_noise_clusters = len(noise_data_df["cluster_label"].unique())
    noise_count = len(noise_data_df)
    n_clusters = len(df["cluster_label"].unique()) - n_noise_clusters
    n_accepted = n_obs - noise_count

    logger.info("Number of obs passed to the clustering routine: %d", n_obs)
    logger.info("Estimated number of clusters: %d", n_clusters)
    logger.info("Estimated number of accepted obs: %d", n_accepted)
    logger.info(
        "Estimated number of noise obs: %d (%.1f%% rejection rate)",
        noise_count,
        100.0 * noise_count / n_obs,
    )
    try:
        silhouette_score = df["silhouette_score"].mean(skipna=True)
        logger.info("Mean silhouette score: %.3f", silhouette_score)
    except KeyError:
        pass
