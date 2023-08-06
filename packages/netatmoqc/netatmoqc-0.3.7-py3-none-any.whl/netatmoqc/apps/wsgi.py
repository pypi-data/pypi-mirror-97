#!/usr/bin/env python3
"""Web Server Gateway Interface."""
# pylint: disable=unused-import
# See <https://community.plotly.com/t/multiple-dashboards/4656/3>
import clustering.app
import scattergeo_timeseries.app
from server import server as application
