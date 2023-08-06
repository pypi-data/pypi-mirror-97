#!/usr/bin/env python3
"""Code for the scattergeo_timeseries app."""
import logging
import os
from datetime import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from server import server

from netatmoqc.config_parser import read_config
from netatmoqc.domains import Domain
from netatmoqc.load_data import (
    read_netatmo_data_for_dtg,
    remove_irregular_stations,
)
from netatmoqc.logs import CustomFormatter
from netatmoqc.plots import generate_single_frame, init_fig_dict

logger = logging.getLogger(__name__)
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(CustomFormatter())
logging.basicConfig(level=logging.INFO, handlers=[logger_handler])

config = read_config(os.getenv("NETATMOQC_CONFIG_PATH", "config.toml"))
domain = Domain.construct_from_dict(config.domain)

app = dash.Dash(
    name="scattergeo_timeseries",
    server=server,
    url_base_pathname="/scattergeo_timeseries/",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)


def description_card():
    """Return a Div containing dashboard title & descriptions."""
    return html.Div(
        id="description-card",
        children=[
            html.H5("NetAtmo Data Explorer"),
            html.H3("NetAtmo Data Explorer Dashboard"),
            html.Div(id="intro", children="An aid to explore NetAtmo data",),
        ],
        style={"text-align": "center"},
    )


variable_list = [
    "temperature",
    "pressure",
    "mslp",
    "alt",
    "humidity",
    "sum_rain_1",
]


def generate_control_card():
    """Return: A Div containing controls for graphs."""
    return html.Div(
        id="control-card",
        children=[
            html.P("Select variable"),
            dcc.Dropdown(
                id="variable-select",
                options=[{"label": i, "value": i} for i in variable_list],
                value=variable_list[0],
            ),
            html.Br(),
            html.P("Select time range"),
            dcc.DatePickerRange(
                id="date-picker-select",
                minimum_nights=0,
                start_date=dt(2018, 4, 1),
                end_date=dt(2018, 4, 1),
                min_date_allowed=dt(2018, 4, 1),
                max_date_allowed=dt.today(),
                initial_visible_month=dt(2018, 4, 1),
            ),
            html.Br(),
            html.Br(),
            html.Div(
                id="plot-btn-outer",
                children=html.Button(
                    id="plot-btn", children="Make Plot", n_clicks=0
                ),
            ),
        ],
    )


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
            id="right-column",
            className="nine columns",
            children=[
                html.Div(
                    id="scattergeo_plot_div",
                    children=[
                        html.B("My Plot"),
                        html.Hr(),
                        dcc.Graph(id="netatmo_data_plot"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("netatmo_data_plot", "figure"),
    [Input("plot-btn", "n_clicks")],
    [
        State("date-picker-select", "start_date"),
        State("date-picker-select", "end_date"),
        State("variable-select", "value"),
    ],
)
def prepare_animation(n_clicks, start_date, end_date, dataset_var):
    """Prepare the animation to be shown."""
    if n_clicks == 0:
        return domain.get_fig(max_ngrid=0)

    fig_dict, sliders_dict = init_fig_dict(
        domain, dataset_var, frame_duration=300
    )

    # Determine map boundaries and max/min plotted values
    minval_dataset_var = float("inf")
    maxval_dataset_var = -float("inf")

    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
        try:
            start_date = dt.strptime(start_date, fmt).replace(hour=0)
            break
        except ValueError:
            pass
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
        try:
            end_date = dt.strptime(end_date, fmt).replace(hour=21)
            break
        except ValueError:
            pass

    for idtg, dtg in enumerate(pd.date_range(start_date, end_date, freq="3H")):
        logger.info("Reading data for %s", dtg)
        df = read_netatmo_data_for_dtg(
            dtg, rootdir=config.general.data_rootdir
        )
        df, _ = remove_irregular_stations(df)
        logger.debug("    * Done. Now adding frame.")

        # Control of map boundaries
        minval_dataset_var = min(minval_dataset_var, min(df[dataset_var]))
        maxval_dataset_var = max(maxval_dataset_var, max(df[dataset_var]))

        frame_dict = fig_dict.copy()
        # plotly.graph_objs.Frame objects have no "frames" property
        frame_dict.pop("frames", None)
        frame_dict["name"] = str(dtg)
        frame, slider_step = generate_single_frame(
            df, dataset_var, frame_duration=30, frame=frame_dict
        )

        if idtg == 0:
            fig_dict["data"] = [frame["data"]] + fig_dict["data"]
        fig_dict["frames"].append(frame)
        sliders_dict["steps"].append(slider_step)

    # Adjust colourbar
    cbar_minnval = 0
    cbar_maxval = maxval_dataset_var
    if minval_dataset_var * maxval_dataset_var < 0:
        cbar_maxval = max(np.abs((minval_dataset_var, maxval_dataset_var)))
        cbar_minnval = -cbar_maxval
    for iframe, frame in enumerate(fig_dict["frames"]):
        frame["data"]["marker"]["cmin"] = cbar_minnval
        frame["data"]["marker"]["cmax"] = cbar_maxval
        fig_dict["frames"][iframe] = frame

    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)

    return fig


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
