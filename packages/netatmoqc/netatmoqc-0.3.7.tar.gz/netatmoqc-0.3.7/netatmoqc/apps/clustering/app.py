#!/usr/bin/env python3
"""Implement the interactive clustering app."""
import logging
import os
import tempfile
import time
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import redis
from dash.dependencies import Input, Output, State
from flask_caching import Cache
from server import server

from netatmoqc.clustering import cluster_netatmo_obs, sort_df_by_cluster_size
from netatmoqc.config_parser import (
    ParsedConfig,
    UndefinedConfigValue,
    read_config,
)
from netatmoqc.domains import Domain
from netatmoqc.dtgs import Dtg
from netatmoqc.load_data import (
    read_netatmo_data_for_dtg,
    remove_irregular_stations,
)
from netatmoqc.logs import CustomFormatter
from netatmoqc.metrics import haversine_distance
from netatmoqc.plots import make_clustering_fig

logger = logging.getLogger(__name__)
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(CustomFormatter())
logging.basicConfig(level=logging.INFO, handlers=[logger_handler])


config = read_config(os.getenv("NETATMOQC_CONFIG_PATH", "config.toml"))
domain = Domain.construct_from_dict(config.domain)

app = dash.Dash(
    name="clustering",
    server=server,
    url_base_pathname="/clustering/",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

# Fix duplicate log items
# TODO: Find a better way to do this without affecting Flask's own logging
if app.logger.hasHandlers():
    app.logger.handlers.clear()

app.title = "iObs NetAtmo Clustering"

# Using cache in order to share data between callbacks
# See <https://dash.plotly.com/sharing-data-between-callbacks> for details
try:
    # Test if we have a working redis server running.
    redis_server = redis.Redis("localhost", socket_connect_timeout=1)
    redis_server.ping()
    logger.info("Using redis caching")
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    CACHE_CONFIG = {"CACHE_TYPE": "redis", "CACHE_REDIS_URL": redis_url}
except redis.exceptions.ConnectionError:
    cache_dir = tempfile.TemporaryDirectory(prefix="netatmo_clustering_tmp")
    logger.info("Caching via redis unavailable. Caching to %s", cache_dir.name)
    # See <https://stackoverflow.com/questions/12868222/
    #      performance-of-redis-vs-disk-in-caching-application>
    CACHE_CONFIG = {
        "CACHE_TYPE": "filesystem",
        "CACHE_DIR": cache_dir.name,
    }
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)
# Clear cache on startup to avoid susprises after, e.g., updates
cache.clear()


def description_card():
    """Return a Div containing dashboard title & descriptions."""
    return html.Div(
        id="description-card",
        children=[
            html.H5("NetAtmoQC"),
            html.H3("Interactive Data Clustering"),
            html.Div(
                id="intro",
                children="Quality-Control of NetAtmo Station Data via Clustering",
            ),
        ],
        style={"text-align": "center"},
    )


def generate_obs_weights_panel():
    """Generate the observation weights panel."""

    def obs_weight_cell(var_name, default=1.0, minval=0.0, maxval=np.inf):
        """Return a div for an obs weight cell."""
        # Get defaults from config file if defined. Use the ones
        # defined in the calls to this function otherwise.
        try:
            default_from_config = config.get_clustering_opt("obs_weights", {})[
                var_name
            ]
            if default_from_config is UndefinedConfigValue:
                raise AttributeError(
                    'obs_weights not defined for "{}"'.format(var_name)
                )
            default = default_from_config
            logger.debug(
                'Using config file default "%s" for "%s" weight',
                default,
                var_name,
            )
        except (AttributeError, KeyError):
            logger.debug(
                'Using hard-coded default "%s" for "%s" weight',
                default,
                var_name,
            )

        cell = html.Div(
            id="{}_weight_div".format(var_name),
            children=[
                html.P(var_name, id="{}_weight_label".format(var_name)),
                dcc.Input(
                    id="{}_weight".format(var_name),
                    type="number",
                    inputMode="numeric",
                    min=minval,
                    max=maxval,
                    value=default,
                    style=dict(width="90%"),
                ),
            ],
            style=dict(display="table-cell"),
        )
        return cell

    panel = html.Div(
        id="obs_weights_div",
        children=[
            html.Details(
                title="Weights for the calculated differences",
                children=[
                    html.Summary("Weights for the calculated differences"),
                    html.Div(
                        children=[
                            obs_weight_cell("geo_dist", default=1.0),
                            obs_weight_cell("alt"),
                            obs_weight_cell("temperature", default=5.0),
                            obs_weight_cell("mslp"),
                        ],
                        style=dict(display="table-row"),
                    ),
                    html.Br(),
                    html.Div(
                        children=[
                            obs_weight_cell("pressure", default=0.0),
                            obs_weight_cell("humidity"),
                            obs_weight_cell("sum_rain_1"),
                        ],
                        style=dict(display="table-row"),
                    ),
                ],
                style=dict(display="table"),
            ),
        ],
    )
    return panel


allowed_cluster_methods = ["hdbscan", "dbscan", "rsl", "optics"]
allowed_outlier_rm_method = ["Iterative", "GLOSH", "LOF", "Reclustering"]


def generate_control_card():
    """Return a Div containing controls for graphs."""
    return html.Div(
        id="control-card",
        children=[
            html.P("Clustering method"),
            dcc.Dropdown(
                id="method-select",
                options=[
                    {"label": i, "value": i} for i in allowed_cluster_methods
                ],
                value=allowed_cluster_methods[0],
            ),
            html.Br(),
            # Put min_samples and eps input in their own Divs to be able to
            # put them side-by-side.
            # Adapted from <https://community.plotly.com/t/setting-the-layout-
            #               of-a-button-and-input-box/6519/3>
            html.Div(
                [
                    html.P("min_samples"),
                    dcc.Input(
                        id="min_samples",
                        type="number",
                        inputMode="numeric",
                        min=1,
                        value=5,
                        step=1,
                        required=True,
                        style=dict(display="table-cell",),
                    ),
                ],
                style=dict(display="table-cell"),
            ),
            # The min_cluster_size input should not show when using dbscan.
            # The way to create conditional inputs in dash is to put them in
            # separate Divs and change the Divs' "display" attr to "none" in
            # a callback.
            # Adapted from: <https://stackoverflow.com/questions/50213761/
            #                changing-visibility-of-a-dash-component-by-
            #                updating-other-component>
            html.Div(
                id="min_cluster_size_div",
                children=[
                    html.P("min_cluster_size", id="min_cluster_size_label"),
                    dcc.Input(
                        id="min_cluster_size",
                        type="number",
                        inputMode="numeric",
                        min=2,
                        value=5,
                        step=1,
                        style=dict(display="table-cell",),
                    ),
                ],
                style=dict(display="table-cell"),
            ),
            # The eps input should not show when using hdbscan. Doing similarly
            # to min_cluster_size above.
            html.Div(
                id="eps_div",
                children=[
                    html.P("eps", id="eps_label"),
                    dcc.Input(
                        id="eps",
                        type="number",
                        inputMode="numeric",
                        min=0.0,
                        value=10.0,
                        style=dict(display="table-cell",),
                    ),
                ],
                style=dict(display="table-cell"),
            ),
            html.Br(),
            #
            html.Div(
                id="optionals_div",
                children=[
                    html.Div(
                        id="outlier_rm_method_div",
                        children=[
                            html.Br(),
                            html.P(
                                "Post-Clustering Outlier Removal (Optional)"
                            ),
                            dcc.Dropdown(
                                id="outlier_rm_method",
                                options=[{"label": "None", "value": None}]
                                + [
                                    {"label": i, "value": i.lower()}
                                    for i in allowed_outlier_rm_method
                                ],
                                value="glosh",
                            ),
                        ],
                        style={"display": "block", "text-align": "center"},
                    ),
                    html.Div(
                        # The 'style' property of this div will be
                        # set via callback
                        id="max_num_refining_iter_div",
                        children=[
                            html.Div(
                                children=[
                                    html.Br(),
                                    html.P("Max #refining iterations"),
                                    dcc.Input(
                                        id="max_num_refine_iter",
                                        type="number",
                                        inputMode="numeric",
                                        min=1,
                                        value=100,
                                        step=1,
                                    ),
                                ],
                                style={
                                    "display": "table-cell",
                                    "text-align": "center",
                                },
                            ),
                            html.Div(
                                children=[
                                    html.Br(),
                                    html.P("Max #stdev around mean"),
                                    dcc.Input(
                                        id="max_n_std_around_mean",
                                        type="number",
                                        inputMode="numeric",
                                        min=1,
                                        value=2,
                                    ),
                                ],
                                style={
                                    "display": "table-cell",
                                    "text-align": "center",
                                },
                            ),
                        ],
                        style=dict(display="table-row"),
                    ),
                ],
            ),
            html.Br(),
            #
            generate_obs_weights_panel(),
            html.Br(),
            #
            html.Div(
                id="dtg_div",
                children=[
                    html.Div(
                        id="date-div",
                        children=[
                            html.P("Date"),
                            dcc.DatePickerSingle(
                                id="date-picker-select",
                                min_date_allowed=datetime(2018, 4, 1),
                                max_date_allowed=datetime.today(),
                                initial_visible_month=datetime(2018, 4, 1),
                                date="2018-04-01",
                                display_format="YYYY-MM-DD",
                            ),
                        ],
                        style=dict(display="table-cell"),
                    ),
                    html.Div(
                        id="cycle-div",
                        children=[
                            html.P("Cycle"),
                            dcc.Input(
                                id="cycle-select",
                                type="number",
                                inputMode="numeric",
                                min=0,
                                max=21,
                                value=0,
                                step=3,
                            ),
                        ],
                        style=dict(display="table-cell"),
                    ),
                ],
                style=dict(display="table-row"),
            ),
            #
            html.Br(),
            html.Div(
                id="plot-btn-outer",
                children=[
                    html.Button(
                        id="plot-btn",
                        children="Run Clustering and Plot",
                        n_clicks=0,
                    ),
                ],
            ),
        ],
    )


# returns top indicator div
def indicator(text, id_value):
    """Return the html.Div for one app indicator."""
    # Adapted from Dash gallery's app "dash-salesforce-crm"
    return html.Div(
        id="{}_div".format(id_value),
        children=[
            html.Div(
                children=[
                    html.P(id=id_value, className="indicator_value",),
                    html.P(text, className="indicator_text",),
                ],
            ),
        ],
        className="indicator pretty_container",
        style=dict(textAlign="center"),
    )


def generate_indicators():
    """Generate the indicators used in the app."""
    indicators = html.Div(
        id="indicators_div",
        children=[
            indicator("Mean Silhouette Score", "silhouette_coeff_indicator"),
            indicator("# Clusters", "nclusters_indicator"),
            indicator("# Accepted Obs", "naccepted_indicator"),
            indicator("# Clustering Noise", "nrejected_indicator"),
            indicator("# Clustering Outliers", "nremoved_indicator"),
            indicator("# Total Rejected", "nremoved_total_indicator"),
        ],
        style=dict(display="flex"),
    )
    return indicators


def generate_right_column_elements():
    """Generate the elements of the right-hand side column."""
    children = [
        html.Div(
            id="clustering_plot_div",
            children=[dcc.Graph(id="clustering_plot",)],
        ),
        html.Div(
            id="clustered_data_table_card",
            children=[
                html.B("Data after processing by clustering algorithm"),
                html.Hr(),
                dash_table.DataTable(
                    id="clustered_data_table",
                    data=[],
                    columns=[],
                    export_columns="all",
                    sort_action="native",
                    filter_action="native",
                    # Styling
                    style_cell=dict(padding="10px",),
                    style_header=dict(
                        backgroundColor="rgb(2,21,70)",
                        color="white",
                        textAlign="center",
                    ),
                    # Control table scrolling
                    # Don't use fixed_rows right now. It causes formatting
                    # issues at the moment (tested with dash v1.11 and v1.12)
                    style_table=dict(
                        maxHeight="300px",
                        overflowY="scroll",
                        overflowX="auto",
                    ),
                ),
            ],
        ),
    ]
    return children


app.layout = html.Div(
    id="app-container",
    children=[
        # Left column
        html.Div(
            id="left-column",
            className="three columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"],
                    id="output-clientside",
                    style={"display": "none"},
                )
            ],
        ),
        # Right column
        html.Div(
            # Setting "style=dict(position='relative')" here so that the
            # position-related style options in the dcc.Loading work relative
            # to this container div.
            id="right-column",
            className="nine columns",
            style=dict(position="relative"),
            children=[
                generate_indicators(),
                html.B("Visualisation of Clusters"),
                html.Div(id="calculated_dist", children=[],),
                html.Hr(),
                dcc.Loading(
                    # Embed the the right-hand side column inside a dcc.Loading
                    # so that a spinner is shown while updating.
                    id="clustering_plot-spinner",
                    # type is one of:
                    #     'graph', 'cube', 'circle', 'dot', or 'default'
                    type="graph",
                    fullscreen=False,
                    children=generate_right_column_elements(),
                    # Put spinner in the middle of the container Div
                    style={
                        "position": "absolute",
                        "top": "50%",
                        "left": "50%",
                        "transform": "translate(-50%, -50%)",
                    },
                ),
            ],
        ),
    ],
)


# perform expensive computations in this "global store"
# these computations are cached in a globally available
# redis memory store which is available across processes
# and for all time.
@cache.memoize()
def read_data_df(str_date, cycle):
    """Read data for DTG composed by str_date and cycle."""
    dtg = Dtg(datetime.strptime(str_date, "%Y-%m-%d").replace(hour=cycle))
    df = read_netatmo_data_for_dtg(dtg, rootdir=config.general.data_rootdir)
    df, _ = remove_irregular_stations(df)
    return df


# Show/hide eps input when appropriate.
@app.callback(
    [
        Output(component_id="eps_div", component_property="style"),
        Output(
            component_id="min_cluster_size_div", component_property="style"
        ),
    ],
    [Input(component_id="method-select", component_property="value")],
)
def show_hide_depending_on_method(method):
    """Show/hide menus depending on clustering method."""
    if method == "dbscan":
        eps_div_style = {"display": "table-cell"}
        min_cluster_size_div_style = {"display": "none"}
    else:
        eps_div_style = {"display": "none"}
        min_cluster_size_div_style = {"display": "table-cell"}
    return (eps_div_style, min_cluster_size_div_style)


#
@app.callback(
    [
        Output(
            component_id="max_num_refining_iter_div",
            component_property="style",
        ),
    ],
    [Input(component_id="outlier_rm_method", component_property="value")],
)
def show_hide_max_num_refining_iter(outlier_rm_method):
    """Show/hide max_num_refining_iter menu according to outlier_rm_method."""
    if outlier_rm_method == "iterative":
        return [{"display": "table-row"}]
    return [{"display": "none"}]


# Producing plot
@app.callback(
    [
        Output("clustering_plot", "figure"),
        Output("clustered_data_table", "columns"),
        Output("clustered_data_table", "data"),
        Output("silhouette_coeff_indicator", "children"),
        Output("nclusters_indicator", "children"),
        Output("naccepted_indicator", "children"),
        Output("nrejected_indicator", "children"),
        Output("nremoved_indicator", "children"),
        Output("nremoved_total_indicator", "children"),
    ],
    [Input("plot-btn", "n_clicks")],
    [
        State("method-select", "value"),
        State("min_samples", "value"),
        State("min_cluster_size", "value"),
        State("eps", "value"),
        State("date-picker-select", "date"),
        State("cycle-select", "value"),
        State("outlier_rm_method", "value"),
        State("max_num_refine_iter", "value"),
        State("max_n_std_around_mean", "value"),
        State("geo_dist_weight", "value"),
        State("alt_weight", "value"),
        State("temperature_weight", "value"),
        State("mslp_weight", "value"),
        State("pressure_weight", "value"),
        State("humidity_weight", "value"),
        State("sum_rain_1_weight", "value"),
    ],
)
def run_clustering_and_make_plot(
    n_clicks,
    method,
    min_samples,
    min_cluster_size,
    eps,
    date,
    cycle,
    outlier_rm_method,
    max_num_refining_iter,
    refine_max_std,
    geo_dist_weight,
    alt_weight,
    temperature_weight,
    mslp_weight,
    pressure_weight,
    humidity_weight,
    sum_rain_1_weight,
):
    """Control the app. Main app routine."""
    # pylint: disable=locally-disabled, too-many-locals, too-many-arguments
    empty_fig = make_clustering_fig(pd.DataFrame(), domain=domain)
    empty_rtn = (empty_fig, [], [], "-", "-", "-", "-", "-", "-")
    if n_clicks == 0:
        return empty_rtn

    logger.info("Reading data...")
    start_read_data = time.time()
    df = read_data_df(date, cycle)
    end_read_data = time.time()
    logger.info(
        "Done reading data. Elapsed: %.1fs", end_read_data - start_read_data
    )

    n_obs = len(df.index)
    if n_obs == 0:
        logger.error("ERROR:  No data found for selected DTG.")
        return empty_rtn

    # Create a config obj with params
    clustering_config = ParsedConfig(
        {
            "general": dict(
                clustering_method=method,
                custom_metrics_optimize_mode=config.general.custom_metrics_optimize_mode,
                dtgs=dict(
                    list=config.general.dtgs,
                    cycle_length=config.general.dtgs.cycle_length.freqstr,
                ),
            ),
            "clustering_method.%s"
            % (method): dict(
                eps=eps,
                min_cluster_size=min_cluster_size,
                min_samples=min_samples,
                outlier_removal={
                    "method": outlier_rm_method,
                    outlier_rm_method: dict(
                        max_n_iter=max_num_refining_iter,
                        max_n_stdev=abs(refine_max_std),
                    ),
                },
                obs_weights=dict(
                    geo_dist=geo_dist_weight,
                    alt=alt_weight,
                    temperature=temperature_weight,
                    mslp=mslp_weight,
                    pressure=pressure_weight,
                    humidity=humidity_weight,
                    sum_rain_1=sum_rain_1_weight,
                ),
            ),
            "domain": config.domain,
        }
    )

    time_start_clustering = time.time()
    logger.info("Running %s...", method)
    df = cluster_netatmo_obs(
        df=df, config=clustering_config, calc_silhouette_samples=True,
    )
    df = sort_df_by_cluster_size(df)
    time_end_clustering = time.time()
    logger.info(
        "%s performed in %.1fs",
        method,
        time_end_clustering - time_start_clustering,
    )

    noise_data_df = df[df["cluster_label"] < 0]
    n_noise_clusters = len(noise_data_df["cluster_label"].unique())
    noise_count = len(noise_data_df)
    n_rm_refining = (df["cluster_label"] < -1).sum()
    n_rm_clustering = noise_count - n_rm_refining
    n_clusters = len(df["cluster_label"].unique()) - n_noise_clusters
    n_accepted = n_obs - noise_count
    silhouette_score = df["silhouette_score"].mean(skipna=True)

    logger.debug("Estimated number of clusters: %d", n_clusters)
    logger.debug("Estimated number of noise points: %d", noise_count)
    logger.debug("Estimated number of clustered obs: %d", n_accepted)
    logger.debug("Mean silhouette score: %.3f", silhouette_score)

    fig = make_clustering_fig(df, domain=domain)

    # Preparing update to table
    # Formatting column values for better presentation
    for cname in df.columns:
        if cname in ["lat", "lon"]:
            df[cname] = df[cname].map("{:.4f}".format)
        elif cname in [
            "alt",
            "pressure",
            "mslp",
            "temperature",
            "humidity",
            "sum_rain_1",
        ]:
            df[cname] = df[cname].map("{:.1f}".format)
        elif cname in ["silhouette_score", "GLOSH", "LOF"]:
            df[cname] = df[cname].map("{:.2f}".format)
    df["time_utc"] = df["time_utc"].dt.strftime("%Y-%m-%d %H:%M:%S")
    # We'll set column IDs to the same values as their col names, but
    # this is not a requirement
    columns = [{"name": n, "id": n, "selectable": True} for n in df.columns]
    data = df.to_dict("records")

    return (
        fig,
        columns,
        data,
        dcc.Markdown("**{:.2f}**".format(silhouette_score)),
        dcc.Markdown("**{}**".format(n_clusters)),
        dcc.Markdown(
            "**{} ({:.2f}%)**".format(n_accepted, 100.0 * n_accepted / n_obs)
        ),
        dcc.Markdown(
            "**{} ({:.2f}%)**".format(
                n_rm_clustering, 100.0 * n_rm_clustering / n_obs
            )
        ),
        dcc.Markdown(
            "**{} ({:.2f}%)**".format(
                n_rm_refining, 100.0 * n_rm_refining / n_obs
            )
        ),
        dcc.Markdown(
            "**{} ({:.2f}%)**".format(noise_count, 100.0 * noise_count / n_obs)
        ),
    )


# Report distance between points upon selection fo two points
@app.callback(
    [Output(component_id="calculated_dist", component_property="children")],
    [
        # Set clickmode='event+select' in the figure layout, and then
        # use 'selectedData' here instead of 'clickData'
        Input(
            component_id="clustering_plot", component_property="selectedData"
        ),
    ],
)
def geodist_upon_pt_pair_selection(selected_data):
    """Return geodist between selected points in the app."""
    if (selected_data is None) or (len(selected_data["points"]) != 2):
        return [html.P("")]

    pt0 = [selected_data["points"][0][attr] for attr in ["lat", "lon"]]
    pt1 = [selected_data["points"][1][attr] for attr in ["lat", "lon"]]
    rtn = html.Span(
        "Haversine distance between selected points: {:.3f} km".format(
            haversine_distance(np.array(pt0), np.array(pt1))
        )
    )
    return [rtn]


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
