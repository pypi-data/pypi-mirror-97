#!/usr/bin/env python3
"""Parse the config file."""
import copy
import functools
import io
import logging
import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import toml
from dotmap import DotMap

from .dtgs import DtgContainer

logger = logging.getLogger(__name__)

###############################
# General types and functions #
###############################


class UndefinedValueType:
    """UndefinedValueType class.

    This class is defined such that any instance foo satisfies:
        (a) bool(foo) is False
        (b) If return_self_on_attr_error=True, then, for any attribute bar,
            foo.bar is foo. This implies that, for any N>1,
            foo.bar1.bar2.(...).barN is foo

    We will use instances of this class to mark things such as missing
    config file values, unspecified defaults in functions, etc. We don't
    want to use None in these cases, as None may be a valid arg value.

    """

    def __init__(
        self,
        name="<UndefinedValueType object>",
        return_self_on_attr_error=False,
    ):
        """Set instance name and return_self_on_attr_error attr."""
        self._name = name
        self._return_self_on_attr_error = return_self_on_attr_error

    def __setitem__(self, item, val):
        pass

    def __getitem__(self, item):
        return self

    # Define __setstate__ and __getstate__ to handle serialisation (pickling)
    # and avoid recursion errors (UndefinedConfigValue is a recursive object)
    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    def __getattr__(self, item):
        if self._return_self_on_attr_error:
            return self
        raise AttributeError(
            "'{}' object has no attribute '{}'".format(
                self.__class__.__name__, item
            )
        )

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __bool__(self):
        return False

    def __repr__(self):
        return self._name

    __str__ = __repr__


UndefinedConfigValue = UndefinedValueType(
    name="UndefinedConfigValue", return_self_on_attr_error=True
)

NoDefaultProvided = UndefinedValueType(name="NoDefaultProvided")


class UndefinedConfigValueError(Exception):
    """Exception to be raised if UndefinedConfigValue is encountered."""


class ConfigDict(DotMap):
    """Config dictionary.

    Acts like a normal dictionary, except for:
        (a) Accepts getting/setting values using dot notation (inherited from
            the dotmap package). This means that instance.key is equivalent
            to instance[key].
        (b) Accepts getting/setting values using "hierarchy lists", in the
            sense that the retrievals
                        instance[['at1', 'at2', (...), 'atn']],
                        instance[['at1.at2.(...).atn']],
                        instance['at1.at2.(...).atn'],
                        instance.at1.at2.(...).atn
            are equivalent.
        (c) If self._dynamic is True, then, instead of raising KeyError:
            * Retrievals on missing keys return UndefinedConfigValue
            * Sublevels are automatically created if needed upon item setting

    """

    def __init__(self, *args, **kwargs):
        """Make KeyError possible if "_dynamic=True" not explicitly passed."""
        if "_dynamic" not in kwargs:
            kwargs["_dynamic"] = False
        super().__init__(*args, **kwargs)

    def get(self, key, default=UndefinedConfigValue):
        """Implement ".get". Default UndefinedConfigValue instead of None."""
        if not isinstance(key, str):
            # Implement retrievals using "hierarchy lists"
            try:
                key = ".".join(iter(key))
            except (TypeError) as err:
                msg = (
                    "The attribute(s) to be retrieved must be specified "
                    + "either as a string or as an iterable type. "
                    + 'Got "{}" instead (type={})'
                ).format(key, type(key))
                raise TypeError(msg) from err

        def _getattr(obj, key, default=default):
            if isinstance(obj, type(self)):
                try:
                    rtn = super().__getitem__(key)
                    if rtn == type(self)():
                        raise KeyError(key)
                except KeyError:
                    if default is NoDefaultProvided:
                        raise
                    rtn = default
            else:
                try:
                    rtn = getattr(obj, key)
                except AttributeError:
                    rtn = default
            return rtn

        return functools.reduce(_getattr, [self] + key.split("."))

    def __getitem__(self, attr):
        if self._dynamic:
            rtn = self.get(attr, default=UndefinedConfigValue)
        else:
            rtn = self.get(attr, default=NoDefaultProvided)
        return rtn

    def __setitem__(self, attr, val):
        if "." in attr:
            pre, _, post = attr.rpartition(".")
            if self.get(pre) is UndefinedConfigValue:
                if self._dynamic:
                    new_pre = type(self)()
                    new_pre[post] = UndefinedConfigValue
                    new_pre._dynamic = True
                    setattr(self, pre, new_pre)
                else:
                    raise KeyError(attr)
            setattr(self.get(pre) if pre else self, post, val)
        else:
            super().__setitem__(attr, val)

    def set_dynamic_flags(self, boolean):
        """Recursively set "_dynamic" to True/False."""
        boolean = bool(boolean)
        self._dynamic = boolean
        for key, val in self.items():
            if isinstance(val, type(self)):
                val.set_dynamic_flags(boolean)
                self[key] = val
                self[key]._dynamic = boolean
            else:
                pass

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls, _dynamic=self._dynamic)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls, _dynamic=self._dynamic)
        memo[id(self)] = result
        for key, val in self.__dict__.items():
            setattr(result, key, copy.deepcopy(val, memo))
        return result

    def toml_dumps(self):
        """Dump config in TOML format."""
        return toml.dumps(self.toDict(), encoder=toml.TomlPathlibEncoder(dict))

    def __str__(self):
        orig_stdout = sys.stdout
        tmp_stdout = io.StringIO()
        sys.stdout = tmp_stdout
        self.pprint()
        output = tmp_stdout.getvalue()
        sys.stdout = orig_stdout
        return output


######################################################
# Machinery to allow registering config opt metadata #
######################################################


class _MetadataDict(ConfigDict):
    pass


class _ConfigMetadataRegistry(ConfigDict):
    """Class to help register metadata about known config options."""

    def register(
        self,
        key,
        default=NoDefaultProvided,
        minval=NoDefaultProvided,
        maxval=NoDefaultProvided,
        choices=NoDefaultProvided,
        astype=NoDefaultProvided,
        case_sensitive=NoDefaultProvided,
    ):
        """Register a metadata registry entry.

        Args:
            key (str): The key (name) of the param metadata to be registed.
            default (obj):  The default value for the registered metadata.
                (Default value = NoDefaultProvided)
            minval (obj): An optional min value.
                (Default value = NoDefaultProvided).
            maxval (obj): An optional max value.
                (Default value = NoDefaultProvided).
            choices (list): Optional list of allowed choices.
                (Default value = NoDefaultProvided).
            astype (type): Optional type info for the metadata. Used, e.g.,
                for typecasting. (Default value = NoDefaultProvided).
            case_sensitive (bool): Whether future lookups should consider
                character case in the metadata key.
                (Default value = NoDefaultProvided).

        Raises:
            TypeError: If key is not a string.

        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        try:
            # key -> section.key.
            # "section" will be defined using a context manager
            key = "{}.{}".format(section, key)
        except NameError:
            pass

        if astype is NoDefaultProvided and default is not NoDefaultProvided:
            astype = type(default)
        self._dynamic = True
        metadata = _MetadataDict(
            default=default,
            minval=minval,
            maxval=maxval,
            choices=choices,
            astype=astype,
            case_sensitive=case_sensitive,
        )
        metadata._dynamic = False
        self[key] = metadata
        self._dynamic = False

    def copy_template(self, key):
        """Copy contents from self["_template"] to section.key.

        "section" needs to be defined in the upper-level scope,
        using a context manager.

        Args:
            key (str): String such that the destination where the template
                will be copied into is section.key.
        """
        dest_key = "{}.{}".format(section, key)
        if "." in section:
            template_key, _, _dropped = section.rpartition(".")
            template_key = "_template." + template_key + "." + key
        else:
            template_key = "_template." + section + "." + key
        self._dynamic = True
        self[dest_key] = copy.deepcopy(self[template_key])
        self._dynamic = False


config_metadata = _ConfigMetadataRegistry(_dynamic=False)


@contextmanager
def config_section(sec):
    """Yield a config section name for use as context manager."""
    yield sec


###########################################################################
# Registering config options (known opts, defaults, restrictions, etc).   #
# This is where you should change, e.g., in order to add new config opts. #
###########################################################################

# Create a template for filling metadata for the various clustering_methods
with config_section("_template.clustering_method") as section:
    config_metadata.register("eps", default=10.0, minval=0.0)
    config_metadata.register("min_samples", default=5, minval=1)
    config_metadata.register("min_cluster_size", default=5, minval=1)
    # obs_weights not explicitly set will be internally set to 1
    config_metadata.register("obs_weights.geo_dist", default=1.0, minval=0.0)
    config_metadata.register("obs_weights.alt", default=1.0, minval=0.0)
    config_metadata.register(
        "obs_weights.temperature", default=5.0, minval=0.0
    )
    config_metadata.register("obs_weights.pressure", default=0.0, minval=0.0)
    config_metadata.register("obs_weights.mslp", default=1.0, minval=0.0)
    config_metadata.register("obs_weights.humidity", default=1.0, minval=0.0)
    config_metadata.register("obs_weights.sum_rain_1", default=1.0, minval=0.0)
    config_metadata.register(
        "outlier_removal.method",
        default="iterative",
        choices=[None, "lof", "iterative", "reclustering"],
    )
    config_metadata.register(
        "outlier_removal.iterative.max_n_stdev", default=3.0, minval=0.0
    )
    config_metadata.register(
        "outlier_removal.iterative.max_n_iter", default=100, minval=0
    )


# General section
def parsed_path(path):
    """Return path with envvars expanded and as a pathlib.Path obj."""
    return Path(os.path.expandvars(str(path)))


with config_section("general") as section:
    # in/our dirs
    config_metadata.register(
        "data_rootdir", default=".", astype=parsed_path,
    )
    config_metadata.register(
        "outdir",
        default=Path(tempfile.gettempdir()).resolve() / "netatmoqc_output",
        astype=parsed_path,
    )
    # Chosen clustering method
    config_metadata.register(
        "clustering_method",
        default="hdbscan",
        choices=["hdbscan", "dbscan", "optics", "rsl"],
    )
    # DTGs
    config_metadata.register("dtgs.list")
    config_metadata.register("dtgs.start")
    config_metadata.register("dtgs.end")
    config_metadata.register("dtgs.cycle_length", default="3H")
    # Metrics optimisaion scheme
    config_metadata.register(
        "custom_metrics_optimize_mode",
        default="memory",
        choices=["speed", "memory", "speed_mem_compromise"],
    )
    # Data cols to export when saving obsoul output
    config_metadata.register(
        "obsoul_export_params",
        default=["pressure", "temperature", "humidity", "sum_rain_1"],
    )

# "commans section"
with config_section("commands.select") as section:
    config_metadata.register("station_rejection_tol", default=0.15, minval=0.0)

# clustering_method.hdbscan
with config_section("clustering_method.hdbscan") as section:
    config_metadata.copy_template("min_samples")
    config_metadata.copy_template("min_cluster_size")
    config_metadata.copy_template("obs_weights")
    config_metadata.register(
        "outlier_removal.method",
        default="glosh",
        choices=[None, "glosh", "lof", "iterative", "reclustering"],
    )
    config_metadata.copy_template("outlier_removal.iterative")

# clustering_method.dbscan
with config_section("clustering_method.dbscan") as section:
    config_metadata.copy_template("eps")
    config_metadata.copy_template("min_samples")
    config_metadata.copy_template("obs_weights")
    config_metadata.copy_template("outlier_removal")

# clustering_method.optics
with config_section("clustering_method.optics") as section:
    config_metadata.copy_template("min_samples")
    config_metadata.copy_template("min_cluster_size")
    config_metadata.copy_template("obs_weights")
    config_metadata.copy_template("outlier_removal")

# clustering_method.rsl
with config_section("clustering_method.rsl") as section:
    # eps -> cut
    config_metadata.copy_template("eps")
    # min_samples -> k
    config_metadata.copy_template("min_samples")
    # min_cluster_size -> gamma
    config_metadata.copy_template("min_cluster_size")
    config_metadata.copy_template("obs_weights")
    config_metadata.copy_template("outlier_removal")

# domain
with config_section("domain") as section:
    config_metadata.register("name", default="")
    # split the main grid in small grids containing
    # split.lon longitudes and split.lat latitudes
    # for a first clustering. Quicker and saves memory.
    config_metadata.register("split.lon", default=3, minval=1, astype=int)
    config_metadata.register("split.lat", default=4, minval=1, astype=int)
    # These defaults are for the METCOOP25C domain. See
    # <https://hirlam.org/trac/wiki/HarmonieSystemDocumentation/ModelDomain>
    # <https://hirlam.org/trac/browser/Harmonie/scr/Harmonie_domains.pm>
    config_metadata.register("tstep", default=75, minval=0, astype=int)
    config_metadata.register("nlon", default=900, minval=1, astype=int)
    config_metadata.register("nlat", default=960, minval=1, astype=int)
    config_metadata.register(
        "lonc", default=16.763011639, minval=-180, maxval=180
    )
    config_metadata.register(
        "latc", default=63.489212956, minval=-90, maxval=90
    )
    config_metadata.register("lon0", default=15.0, minval=-180, maxval=180)
    config_metadata.register("lat0", default=63.0, minval=-90, maxval=90)
    config_metadata.register("gsize", default=2500.0, minval=0)
    config_metadata.register("ezone", default=11, minval=0, astype=int)
    config_metadata.register("lmrt", default=False, choices=[True, False])
    # At the end of its run, the "select" command uses a coarser version of the
    # domain's grid to thin the returned data (at most one obs per coarse grid
    # point is returned). The config param "thinning_grid_coarse_factor"
    # controls how coarser this coarse grid will be.
    config_metadata.register(
        "thinning_grid_coarse_factor", default=4, minval=0, astype=int
    )


#####################################
# Machinery to parse config options #
#####################################


def _parse_dtg_entires(dtgs_config):
    try:
        cycle_length = dtgs_config["cycle_length"]
    except KeyError:
        cycle_length = "3H"
        logger.warning("Missing cycle_length in config. Setting it to 3H.")

    dtg_range_opt_labels = {"start", "end"}
    if "list" in dtgs_config.keys():
        if not dtg_range_opt_labels.isdisjoint(dtgs_config.keys()):
            logger.warning(
                (
                    'Found DTG options "list" and also at least '
                    'one of [%s]. Parsing only values passed in "list".'
                ),
                ", ".join(dtg_range_opt_labels),
            )
        try:
            dtgs = DtgContainer(dtgs_config["list"], cycle_length=cycle_length)
        except ValueError as err:
            raise ValueError(
                "Bad 'dtg.list' or 'dtg.cycle_length' config."
            ) from err
    else:
        try:
            _ = dtgs_config["start"]
            _ = dtgs_config["end"]
        except (KeyError) as err:
            msg = " Either 'dtgs.list' or both 'dtgs.start' and "
            msg += "'dtgs.end' must specified in config file."
            raise UndefinedConfigValueError(msg) from err
        try:
            dtgs = DtgContainer(
                start=dtgs_config["start"],
                end=dtgs_config["end"],
                cycle_length=cycle_length,
            )
        except (ValueError, TypeError) as err:
            raise ValueError(
                "Bad 'dtg.start/end/cycle_length' config."
            ) from err

    return dtgs


def _raw2parsed(raw, recog_configs=config_metadata, parent_keys=()):
    """Return parsed confif from raw input, validating with metadata.

    Descend recursively into input dict raw and validate raw configs against
    the registered metadata. Configs not that don't have corresponding metadata
    info will be passed unchanged.

    Args:
        raw (dict): Raw configs, as read from config file.
        recog_configs (_ConfigMetadataRegistry): Configs for which we have
            registered metadata. Default value = config_metadata.
        parent_keys (tuple): Tuple of all config dict keys, in order, traversed
            to get to the current raw dict. Default value = (). Used for dicts
            nested within the top-level raw.

    Returns:
        ParsedConfig: Parsed configs from raw.

    Raises:
        ValueError: If any config in raw is not a valid choice, or has an
            invalid value.

    """
    # Do not use mutable data structures for argument defaults (parent_keys)
    parent_keys = list(parent_keys)
    parsed = ConfigDict(_dynamic=True)
    for key, user_val in raw.items():
        # We'll force all keys in the parsed dict to be strings
        key = str(key)
        all_keys = parent_keys + [key]
        full_key = ".".join(all_keys)
        metadata = recog_configs.get(full_key)

        if metadata is UndefinedConfigValue:
            # Leave as is
            logger.warning(
                "Config opt '%s' not recognised. Passed as is.", full_key
            )
            parsed[key] = user_val
            continue

        # Cast to metadata type, if any
        if metadata["astype"] and user_val is not None:
            try:
                user_val = metadata["astype"](user_val)
            except TypeError:
                logger.warning(
                    (
                        "Could not cast config opt '%s=%s' (type '%s') "
                        "into expected type '%s'. Passing without casting."
                    ),
                    full_key,
                    user_val,
                    type(user_val).__name__,
                    metadata["astype"].__name__,
                )

        if isinstance(user_val, dict):
            # Top level of some config section
            # Descend into further eventual dict levels recusively
            parsed[key] = _raw2parsed(user_val, parent_keys=all_keys)
        else:
            # Check if allowed choices (if any) are respected
            if metadata["choices"]:
                if not metadata["case_sensitive"]:
                    # Make it all lowercase
                    metadata["choices"] = [
                        c.lower() if isinstance(c, str) else c
                        for c in metadata["choices"]
                    ]
                    if isinstance(user_val, str):
                        user_val = user_val.lower()
                if user_val not in metadata["choices"]:
                    raise ValueError(
                        (
                            "In config opt '{}': '{}' is not a valid choice. "
                            + "Please choose from: {}"
                        ).format(
                            full_key,
                            user_val,
                            ", ".join(map(str, metadata["choices"])),
                        )
                    )
            # Check value bounds, if specified
            for bound, fun in zip(["minval", "maxval"], [np.less, np.greater]):
                if metadata[bound] is not NoDefaultProvided and fun(
                    user_val, metadata[bound]
                ):
                    raise ValueError(
                        (
                            "In config opt '{}': Value '{}' not allowed. "
                            + "The allowed {} is {}"
                        ).format(full_key, user_val, bound, metadata[bound])
                    )

            # Save parsed value
            parsed[key] = user_val

    parsed._dynamic = False
    return parsed


def _fill_defaults(raw, recog_configs=config_metadata, parent_keys=()):
    """Fill defaults into raw config according to registered metadata.

    Descend recursively into input dict raw and fill in default values
    according to metadata registered in this module.

    Args:
        raw (dict): Raw configs, as read from config file.
        recog_configs (_ConfigMetadataRegistry): Configs for which we have
            registered metadata. Default value = config_metadata.
        parent_keys (tuple): Tuple of all config dict keys, in order, traversed
            to get to the current raw dict. Default value = (). Used for dicts
            nested within the top-level raw.

    Returns:
        dict: Copy of raw with defaults filled in.

    Raises:
        TypeError: If any metadata dict found while parsing raw is not an
            instance of either _MetadataDict or ConfigDict classes.

    """
    # Do not use mutable data structures for argument defaults (parent_keys)
    parent_keys = list(parent_keys)
    parsed = ConfigDict(raw, _dynamic=False)
    for key, metadata in recog_configs.items():
        if key == "_template":
            # We don't want to include the template in the final config
            continue
        all_keys = parent_keys + [key]
        full_key = ".".join(all_keys)
        if isinstance(metadata, _MetadataDict):
            # We should not descend recursively into this
            try:
                user_value = parsed[key]
            except KeyError:
                if metadata.default is NoDefaultProvided:
                    logger.debug(
                        "Missing config opt '%s' with no default", full_key
                    )
                else:
                    logger.debug(
                        "Filling defaults for config opt '%s'", full_key
                    )
                    parsed[key] = metadata.default
                    if metadata.astype:
                        parsed[key] = metadata.astype(parsed[key])
        elif isinstance(metadata, ConfigDict):
            if len(metadata) != 0:
                try:
                    user_value = parsed[key]
                except KeyError:
                    user_value = ConfigDict()
                parsed[key] = _fill_defaults(user_value, metadata, all_keys)
        else:
            raise TypeError(
                "Expected only _MetadataDict or ConfigDict, got %s"
                % (type(metadata))
            )
    return parsed


##########################################################################
# Main objects that the rest of the package will primarily interact with #
##########################################################################


class ParsedConfig:
    """Parsed version of config file or raw dict.

    Each section in config will be accessible as self.section.

    """

    def __init__(
        self,
        arg0=Path().resolve() / "config.toml",
        global_default=NoDefaultProvided,
    ):
        """Initialise "file", "global_default", "raw", and "parsed" attrs."""
        # raw data input
        if isinstance(arg0, dict):
            self._file = None
            self._raw = ConfigDict(arg0, _dynamic=False)
        else:
            self._file = Path(arg0).resolve()
            # Keep the config's raw data, mostly for debugging purposes
            self._raw = ConfigDict(toml.load(self._file), _dynamic=False)

        self.global_default = global_default

        self._parsed = _fill_defaults(_raw2parsed(self._raw))

        # DTGs are treated a bit specially
        self._parsed.general.dtgs = _parse_dtg_entires(
            self._parsed.general.dtgs
        )

        self._parsed.set_dynamic_flags(False)

    # Define __setstate__ and __getstate__ to handle serialisation (pickling)
    # and avoid recursion errors
    def __setstate__(self, state):
        self.__dict__ = state

    def __getstate__(self):
        return self.__dict__

    # Handling the getter method
    # __getattr__ is only called if the attribute does NOT exist
    def __getattr__(self, item):
        return self.get(item, default=NoDefaultProvided)

    def get_clustering_opt(self, item, default=UndefinedConfigValue):
        """Get item from self.clustering_method for configd cluster method."""
        keys_for_get = ["clustering_method", self.general.clustering_method]
        keys_for_get.append(item)
        return self.get(keys_for_get, default)

    def get(self, item, default=UndefinedConfigValue):
        """Implement get method with default UndefinedConfigValue."""
        rtn = self._parsed.get(item, default=UndefinedConfigValue)
        if rtn is UndefinedConfigValue:
            if default is NoDefaultProvided:
                if self.global_default is NoDefaultProvided:
                    raise UndefinedConfigValueError(
                        'Config has no value for "{}", '.format(item)
                        + "and no default has been passed."
                    )

                logger.debug(
                    'No "%s" in config. Using global_default (= %s)',
                    item,
                    self.global_default,
                )
                rtn = self.global_default
            else:
                logger.debug(
                    'No "%s" in config. Using passed default (= %s)',
                    item,
                    default,
                )
                rtn = default

        return rtn

    def toml_dumps(self):
        """Dump config in TOML format."""
        parsed_copy = copy.deepcopy(self._parsed)
        parsed_copy.general.dtgs = self._raw.general.dtgs
        return parsed_copy.toml_dumps()

    def __str__(self):
        parsed_copy = copy.deepcopy(self._parsed)
        parsed_copy.general.dtgs = self._raw.general.dtgs
        return str(parsed_copy)


def read_config(config_path):
    """Read config file at location "config_path".

    Args:
        config_path (pathlib.Path): The path to the config file.

    Returns:
        ParsedConfig: Parsed configs read from config_path.

    """
    logging.info("Reading config file %s", Path(config_path).resolve())
    config = ParsedConfig(config_path, global_default=UndefinedConfigValue)
    return config
