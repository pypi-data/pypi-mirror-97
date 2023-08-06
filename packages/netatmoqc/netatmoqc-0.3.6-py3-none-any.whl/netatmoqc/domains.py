#!/usr/bin/env python3
"""Implement model domain functionality."""
import copy
import logging

import attr
import numpy as np
import pyproj

from .metrics import haversine_distance
from .plots import DEF_FIGSHOW_CONFIG, get_domain_fig

logger = logging.getLogger(__name__)

# We'll approximate the Earth as a sphere
_EARTH_RADIUS = 6.3710088e6  # Mean earth radius in meters
_EQUATOR_PERIM = 2 * np.pi * _EARTH_RADIUS


@attr.s
class GridAxisConfig:
    """Configs for a grid axis."""

    # pylint: disable=locally-disabled, too-few-public-methods
    start = attr.ib()
    end = attr.ib()
    npts = attr.ib(validator=attr.validators.instance_of(int))
    npts_ezone = attr.ib(validator=attr.validators.instance_of(int), default=0)

    def __attrs_post_init__(self):
        if self.npts < 1:
            raise ValueError("npts must be larger than zero")
        if self.npts_ezone < 0:
            raise ValueError("npts_ezone must be positive")
        if self.start > self.end:
            self.start, self.end = self.end, self.start


class Grid2D:
    """A general grid in two dimensions, named x and y by convention."""

    def __init__(self, xaxis, yaxis, tstep=0.0):
        """Initialise params. Axis limits are open-ended intervals."""
        self._xaxis = self._validated_axis_info(xaxis)
        self._yaxis = self._validated_axis_info(yaxis)
        if tstep < 0:
            raise ValueError("tstep must be >= 0")
        self.tstep = tstep

        self.cart2grid = np.vectorize(self._cart2grid_non_vec)

    @staticmethod
    def _validated_axis_info(axis):
        if not isinstance(axis, GridAxisConfig):
            raise TypeError(
                "expected type 'GridAxisConfig', got '%s' instead"
                % (type(axis).__name__)
            )
        return axis

    @property
    def nx(self):
        """Return the number of grid points along the x-direction."""
        return self._xaxis.npts

    @nx.setter
    def nx(self, value):
        if value < 1:
            raise ValueError("nx must be larger than zero")
        self._xaxis.npts = value

    @property
    def nx_ezone(self):
        """Return number of extension zone grid pts along the x-direction."""
        return self._xaxis.npts_ezone

    @nx_ezone.setter
    def nx_ezone(self, value):
        if value < 0:
            raise ValueError("nx_ezone must be positive")
        self._xaxis.npts_ezone = value

    @property
    def ny(self):
        """Return the number of grid points along the y-direction."""
        return self._yaxis.npts

    @ny.setter
    def ny(self, value):
        if value < 1:
            raise ValueError("ny must be larger than zero")
        self._yaxis.npts = value

    @property
    def ny_ezone(self):
        """Return number of extension zone grid pts along the y-direction."""
        return self._yaxis.npts_ezone

    @ny_ezone.setter
    def ny_ezone(self, value):
        if value < 0:
            raise ValueError("ny_ezone must be positive")
        self._yaxis.npts_ezone = value

    @property
    def xmin(self):
        """Return the smallest value of x in the grid."""
        return self._xaxis.start

    @property
    def xmax(self):
        """Return the largest value of x in the grid."""
        return self._xaxis.end

    @property
    def xlims(self):
        """Return (xmin, xmax)."""
        return self.xmin, self.xmax

    @property
    def ymin(self):
        """Return the smallest value of y in the grid."""
        return self._yaxis.start

    @property
    def ymax(self):
        """Return the largest value of y in the grid."""
        return self._yaxis.end

    @property
    def ylims(self):
        """Return (ymin, ymax)."""
        return self.ymin, self.ymax

    @property
    def ezone_xmax(self):
        """Return the max value of x within the projected extension zone."""
        return self.xmax + self.nx_ezone * self.x_spacing

    @property
    def ezone_ymax(self):
        """Return the max value of y within the projected extension zone."""
        return self.ymax + self.ny_ezone * self.y_spacing

    @property
    def x_spacing(self):
        """Return the spacing, in meters, between nearest grid x-coords."""
        return (self.xmax - self.xmin) / self.nx

    @property
    def y_spacing(self):
        """Return the spacing, in meters, between nearest grid y-coords."""
        return (self.ymax - self.ymin) / self.ny

    @property
    def ncells(self):
        """Return the total number of grid cells."""
        return self.nx * self.ny

    def _cart2grid_non_vec(self, x, y):
        """Return grid (i, j) cell containing projected (x, y) coords."""
        i = int((x - self.xmin) / self.x_spacing)
        j = int((y - self.ymin) / self.y_spacing)
        if i < 0 or i > self.ncells - 1:
            i = None
        if j < 0 or j > self.ncells - 1:
            j = None
        return i, j

    def ij2xy_map(self):
        """Return grid2x, grid2y such that x=grid2x[i, j], y=grid2y[i, j]."""
        # We can then work with x=grid2x[i, j], y=grid2y[i, j]
        xvals = np.linspace(self.xmin, self.xmax, self.nx, endpoint=False)
        yvals = np.linspace(self.ymin, self.ymax, self.ny, endpoint=False)
        grid2x, grid2y = np.meshgrid(xvals, yvals)
        return grid2x, grid2y

    @property
    def corners(self):
        """Return tuple of projected (x, y) coords of the grid corners."""
        return (
            (self.xmin, self.ymin),
            (self.xmax, self.ymin),
            (self.xmax, self.ymax),
            (self.xmin, self.ymax),
        )

    @property
    def ezone_corners(self):
        """Return tuple of projected (x, y) coords of the ezone corners."""
        return (
            (self.xmax, self.ymin),
            (self.ezone_xmax, self.ymin),
            (self.ezone_xmax, self.ezone_ymax),
            (self.xmin, self.ezone_ymax),
            (self.xmin, self.ymax),
            (self.xmax, self.ymax),
        )


class DomainProjection:
    """Cartographic projection to be used in a domain."""

    def __init__(self, name="merc", lon0=0.0, lat0=0.0):
        """Initialise with passed attrs and add a transformer attr."""
        self.name = name
        self.lon0 = lon0
        self.lat0 = lat0
        self.transformer = pyproj.Proj(self.projparams)

    @property
    def full_name(self):
        """Return the full name of the used projection."""
        proj2projname = dict(
            merc="Mercator",
            stere="Polar Stereographic",
            lcc="Lambert Conformal Conic",
        )
        return proj2projname.get(self.name, self.name)

    @property
    def projparams(self):
        """Return the domain's projparams. See <https://proj.org>."""
        return dict(
            # Lambert conformal conic
            proj=self.name,
            R=_EARTH_RADIUS,
            lat_0=self.lat0,  # Lat of domain center. Is this maybe latc?
            lon_0=self.lon0,  # Lon of domain center. Is this maybe lonc?
            lat_1=self.lat0,  # 1st standard parallel
            lat_2=self.lat0,  # 2nd standard parallel
            # a, b: semimajor and semiminor axes (ellipsoidal planet)
            a=_EARTH_RADIUS,
            b=_EARTH_RADIUS,
        )

    def lonlat2xy(self, lon, lat):
        """Convert (lon, lat), in degrees, into projected (x, y) in meters."""
        # lat, lon in degrees
        # returns x, y in meters
        return self.transformer(longitude=lon, latitude=lat)

    def xy2lonlat(self, x, y):
        """Convert projected (x, y), in meters, into (lon, lat) in degrees."""
        lon, lat = self.transformer(x, y, inverse=True)
        return lon, lat


class DomainGrid(Grid2D):
    """A 2D grid with (lon, lat) <--> (x, y) projection awareness."""

    def __init__(self, *args, proj, **kwargs):
        """Initialise attrs from parent Grid2D class and add proj attr."""
        super().__init__(*args, **kwargs)
        self._proj = proj

    @property
    def proj(self):
        """Return the grid's associated DomainProjection object."""
        return self._proj

    @property
    def nlon(self):
        """Return the number of grid points along the longitude axis."""
        return self.nx

    @nlon.setter
    def nlon(self, value):
        self.nx = value

    @property
    def nlat(self):
        """Return the number of grid points along the latitude axis."""
        return self.ny

    @nlat.setter
    def nlat(self, value):
        self.ny = value

    def lonlat2grid(self, lon, lat):
        """Convert (lon, lat) into grid cell coord (i, j)."""
        x, y = self.proj.lonlat2xy(lon, lat)
        return self.cart2grid(x, y)

    def ij2lonlat_map(self):
        """Return g2lon, g2lat such that lon=g2lon[i, j], lat=g2lat[i, j]."""
        return self.proj.xy2lonlat(*self.ij2xy_map())

    @property
    def corners_lonlat(self):
        """Return tuple of (lon, lat) coords of the grid corners."""
        return tuple(self.proj.xy2lonlat(*xy) for xy in self.corners)

    @property
    def ezone_corners_lonlat(self):
        """Return tuple of (lon, lat) coords of the extension zone corners."""
        return tuple(self.proj.xy2lonlat(*xy) for xy in self.ezone_corners)

    def thin_obs(self, df, method="nearest"):
        """Return df with only one entry per grid point."""
        if method not in ["nearest", "first"]:
            raise NotImplementedError(
                "'method' must be one of: 'nearest', 'first'"
            )

        if len(df.index) == 0:
            return df

        # Add grid (i, j) info
        icol, jcol = self.lonlat2grid(
            df["lon"].to_numpy(), df["lat"].to_numpy()
        )
        df["i"] = icol
        df["j"] = jcol

        if method == "nearest":
            # Get (lon, lat) for grid points
            g2lon, g2lat = self.ij2lonlat_map()

            # Sort data by distance to nearest grid point
            def _dist(lon, lat, i, j):
                p0 = np.array([lon, lat])
                p1 = np.array([g2lon[i, j], g2lat[i, j]])
                return haversine_distance(p0, p1)

            df = df.loc[
                df.apply(lambda x: _dist(x.lon, x.lat, x.i, x.j), axis=1)
                .sort_values(ascending=True)
                .index
            ]

        # Remove all but one (the first) entry at each grid (i, j)
        df = df.groupby(["i", "j"], as_index=False, sort=False).first()

        # Remove no longer needed (i, j) info
        df = df.drop(["i", "j"], axis=1)

        return df


class Domain:
    """Model domain geometry and grid.

    See <https://hirlam.org/trac/wiki/HarmonieSystemDocumentation/ModelDomain>.

    """

    def __init__(
        self,
        name="",
        center_lonlat=(0.0, 0.0),
        proj_lon0_lat0=(0.0, 0.0),
        lmrt=False,
        ngrid_lonlat=(1, 1),
        grid_spacing=_EQUATOR_PERIM,
        ezone_ngrid=0,
        subdomain_split=(1, 1),
        coarse_grid_factor=0,
        tstep=0.0,
    ):
        """Initialise name, geometry, projection & grid/thinning grid attrs."""
        self.name = name

        # subdomain splits
        self._nsplit_lonlat = subdomain_split

        #########################
        # Initialise projection #
        #########################
        self.lmrt = lmrt

        def init_proj(ngrid_lonlat, proj_lon0_lat0, grid_spacing):
            """Help routine to initialise domain projection."""
            if self.lmrt and abs(proj_lon0_lat0[1]) > 0:
                logger.warning(
                    "lat0 should be 0 if lmrt=True. Resetting lat0 to 0."
                )
                proj_lon0_lat0 = (proj_lon0_lat0[0], 0.0)

            y_range = ngrid_lonlat[1] * grid_spacing
            return DomainProjection(
                name=self._auto_choose_projname(
                    lat0=proj_lon0_lat0[1], y_range=y_range
                ),
                lon0=proj_lon0_lat0[0],
                lat0=proj_lon0_lat0[1],
            )

        proj = init_proj(ngrid_lonlat, proj_lon0_lat0, grid_spacing)

        ###################
        # Initialise grid #
        ###################
        def init_grid(ngrid_lonlat, grid_spacing, ezone_ngrid):
            """Help routine to initialise domain grid."""
            # (a) Get projected coords of grid center
            center_xy = proj.lonlat2xy(
                lon=center_lonlat[0], lat=center_lonlat[1]
            )
            # (b) Grid x-axis
            x_range = ngrid_lonlat[0] * grid_spacing
            xmin = center_xy[0] - 0.5 * x_range
            xmax = center_xy[0] + 0.5 * x_range
            grid_xaxis = GridAxisConfig(
                start=xmin,
                end=xmax,
                npts=ngrid_lonlat[0],
                npts_ezone=ezone_ngrid,
            )
            # (c) Grid y-axis
            y_range = ngrid_lonlat[1] * grid_spacing
            ymin = center_xy[1] - 0.5 * y_range
            ymax = center_xy[1] + 0.5 * y_range
            grid_yaxis = GridAxisConfig(
                start=ymin,
                end=ymax,
                npts=ngrid_lonlat[1],
                npts_ezone=ezone_ngrid,
            )
            # (d) Set _grid attr
            return DomainGrid(
                xaxis=grid_xaxis, yaxis=grid_yaxis, proj=proj, tstep=tstep,
            )

        self._grid = init_grid(ngrid_lonlat, grid_spacing, ezone_ngrid)

        # Thinning grid
        if coarse_grid_factor < 1:
            self._thinning_grid = None
        else:
            # If you don't deepcopy here then you end up altering self.grid
            self._thinning_grid = copy.deepcopy(self.grid)
            self._thinning_grid.nx //= coarse_grid_factor
            self._thinning_grid.ny //= coarse_grid_factor
            self._thinning_grid.nx_ezone //= coarse_grid_factor
            self._thinning_grid.ny_ezone //= coarse_grid_factor

        ##############################################
        # Create vectorized versions of some methods #
        ##############################################
        self.contains_lonlat = np.vectorize(self._contains_lonlat_non_vec)

    @classmethod
    def construct_from_dict(cls, config):
        """Construct domain from info in the config dict.

        Args:
            config (netatmoqc.config.ConfigDict): Configs dictionary.

        Returns:
            netatmoqc.domains.Domain: New class instance constructed from
                info in the config dict.

        """
        return cls(
            name=config.name,
            ngrid_lonlat=(config.nlon, config.nlat),
            center_lonlat=(config.lonc, config.latc),
            proj_lon0_lat0=(config.lon0, config.lat0),
            grid_spacing=config.gsize,
            ezone_ngrid=config.ezone,
            lmrt=config.lmrt,
            subdomain_split=(config.split.lon, config.split.lat),
            coarse_grid_factor=config.thinning_grid_coarse_factor,
            tstep=config.tstep,
        )

    def _auto_choose_projname(self, lat0, y_range):
        """Define domain projection."""
        # Do this in a way close to what is explained at
        # <https://hirlam.org/trac/wiki/HarmonieSystemDocumentation/ModelDomain>

        latrange = 180 * y_range / _EQUATOR_PERIM
        if self.lmrt or latrange > 35 or np.isclose(latrange, 0):
            # <https://proj.org/operations/projections/merc.html>
            # <https://desktop.arcgis.com/en/arcmap/10.3/guide-books/
            #  map-projections/mercator.htm>
            rtn = "merc"
        elif np.isclose(lat0, 90.0):
            # <https://proj.org/operations/projections/stere.html>
            # <https://desktop.arcgis.com/en/arcmap/10.3/guide-books/
            #  map-projections/polar-stereographic.htm>
            rtn = "stere"
        else:
            # <https://proj.org/operations/projections/lcc.html>
            # <https://desktop.arcgis.com/en/arcmap/10.3/guide-books/
            #  map-projections/lambert-conformal-conic.htm>
            rtn = "lcc"

        return rtn

    @property
    def grid(self):
        """Return the grid used in the domain discretisation."""
        return self._grid

    @property
    def thinning_grid(self):
        """Return the grid used for thinning of observations in the domain."""
        return self._thinning_grid

    @property
    def proj(self):
        """Return the domain's associated DomainProjection object."""
        # Make sure the domain and the domain's grid use the same projection
        return self.grid.proj

    @property
    def center_lonlat(self):
        """Return the (lon, lat) coords of the domain center."""
        center_x = 0.5 * (self.grid.xmin + self.grid.xmax)
        center_y = 0.5 * (self.grid.ymin + self.grid.ymax)
        return self.proj.xy2lonlat(center_x, center_y)

    @property
    def n_subdomains(self):
        """Return the #subdomains given by self.split with default args."""
        return np.prod(self._nsplit_lonlat)

    def split(self, nsplit_lon=None, nsplit_lat=None):
        """Split a domain "nsplit_lon(lat)" times along the lon(lat) axis.

        Args:
            nsplit_lon (int): Number of divisions along the longitude axis.
                (Default value = None).
            nsplit_lat (int): Number of divisions along the latitude axis.
                (Default value = None).

        Returns:
            list: List of subdomains (Domain objects) obtained as a result of
                the split.

        Raises:
            TypeError: If nsplit_lon, nsplit_lon are not integers.
            ValueError: If nsplit_lon and nsplit_lat do not divide
                nlon and nlat, respectively.

        """
        if nsplit_lon is None:
            nsplit_lon = self._nsplit_lonlat[0]
        if nsplit_lat is None:
            nsplit_lat = self._nsplit_lonlat[1]

        if not isinstance(nsplit_lon, int):
            raise TypeError("'nsplit_lon' must be an integer")
        if not isinstance(nsplit_lat, int):
            raise TypeError("'nsplit_lat' must be an integer")
        if nsplit_lon <= 0:
            raise ValueError("'nsplit_lon' must be larger than zero")
        if nsplit_lat <= 0:
            raise ValueError("'nsplit_lat' must be larger than zero")
        if self.grid.nlon % nsplit_lon != 0:
            raise ValueError("'nsplit_lon' must divide nlon")
        if self.grid.nlat % nsplit_lat != 0:
            raise ValueError("'nsplit_lat' must divide nlat")

        new_nlon = self.grid.nlon // nsplit_lon
        new_nlat = self.grid.nlat // nsplit_lat
        nsplit = nsplit_lon * nsplit_lat

        splits = []
        for ilat in range(nsplit_lat):
            new_yc = (
                self.grid.ymin + (ilat + 0.5) * new_nlat * self.grid.y_spacing
            )
            for ilon in range(nsplit_lon):
                new_xc = (
                    self.grid.xmin
                    + (ilon + 0.5) * new_nlon * self.grid.x_spacing
                )
                new_lonc, new_latc = self.proj.xy2lonlat(new_xc, new_yc)
                split = self.__class__(
                    name="{} Split {}/{}".format(
                        self.name, ilat * nsplit_lat + ilon + 1, nsplit
                    ),
                    ngrid_lonlat=(new_nlon, new_nlat),
                    center_lonlat=(new_lonc, new_latc),
                    proj_lon0_lat0=(self.proj.lon0, self.proj.lat0),
                    # We're using same spacing along x and y
                    grid_spacing=self.grid.x_spacing,
                    # We don't want the splits to have extension zones
                    ezone_ngrid=0,
                    lmrt=self.lmrt,
                    tstep=self.grid.tstep,
                )
                splits.append(split)
        return splits

    def trim_obs(self, df):
        """Remove from dataframe "df" those obs that lie outside the domain.

        Args:
            df (pandas.Dataframe): Dataframe to be trimmed.

        Returns:
            pandas.Dataframe: Trimmed dataframe.

        """
        if len(df.index) == 0:
            return df
        trimmed_df = df[self.contains_lonlat(df.lon, df.lat)].copy()
        trimmed_df = trimmed_df.reset_index(drop=True)
        return trimmed_df

    @property
    def minlat(self):
        """Return the min latitude of the domain's corners."""
        return min(lonlat[1] for lonlat in self.grid.corners_lonlat)

    @property
    def minlon(self):
        """Return the min longitude of the domain's corners."""
        return min(lonlat[0] for lonlat in self.grid.corners_lonlat)

    @property
    def maxlat(self):
        """Return the max latitude of the domain's corners."""
        return max(lonlat[1] for lonlat in self.grid.corners_lonlat)

    @property
    def maxlon(self):
        """Return the max longitude of the domain's corners."""
        return max(lonlat[0] for lonlat in self.grid.corners_lonlat)

    @property
    def ezone_maxlat(self):
        """Return the max latitude of the domain's ezone corners."""
        return max(lonlat[1] for lonlat in self.grid.ezone_corners_lonlat)

    @property
    def ezone_maxlon(self):
        """Return the max longitude of the domain's ezone corners."""
        return max(lonlat[0] for lonlat in self.grid.ezone_corners_lonlat)

    @property
    def ezone_minlat(self):
        """Return the min latitude of the domain's ezone corners."""
        return min(lonlat[1] for lonlat in self.grid.ezone_corners_lonlat)

    @property
    def ezone_minlon(self):
        """Return the min longitude of the domain's ezone corners."""
        return min(lonlat[0] for lonlat in self.grid.ezone_corners_lonlat)

    def _contains_lonlat_non_vec(self, lon, lat):
        """Return True if (lon, lat) is within domain, and False otherwise."""
        x, y = self.proj.lonlat2xy(lon, lat)
        return (self.grid.xmin <= x < self.grid.xmax) and (
            self.grid.ymin <= y < self.grid.ymax
        )

    def get_fig(self, **kwargs):
        """Get domain figure.

        Args:
            **kwargs: Passed to get_domain_fig.

        Returns:
            go.Figure: Domain figure.

        """
        return get_domain_fig(self, **kwargs)

    def show(self, config=None, **kwargs):
        """Show domain figure.

        Args:
            config (dict): Plotly's fig.show config, not our parsed config
                file.
            **kwargs: Passed to self.get_fig.

        """
        default_config = DEF_FIGSHOW_CONFIG.copy()
        if config is not None:
            default_config.update(config)
        config = default_config

        fig = self.get_fig(**kwargs)
        fig.show(config=config)
