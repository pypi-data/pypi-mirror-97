#!/usr/bin/env python3
"""Implement Dtg object, Dtgs container, and related routines."""
import logging
from datetime import datetime, timedelta
from functools import partial

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from pytz import timezone

logger = logging.getLogger(__name__)


@np.vectorize
def epoch2datetime(epoch):
    """Convert unix epoch into datetime object."""
    return datetime.fromtimestamp(epoch, timezone("utc"))


@np.vectorize
def datetime2epoch(dt):
    """Convert datetime object into unix epoch."""
    reference = datetime(1970, 1, 1, tzinfo=timezone("utc"))
    epoch = int((dt - reference).total_seconds())
    return epoch


class Dtg(datetime):
    """Implement Dtg object: NWP data assimilation time window."""

    def __init__(self, *args, **kwargs):
        """Set cycle_length attribute.

        Args:
            *args: Positional args passed to datetime.
            *kwargs: Keyword args passed to datetime.

        Attributes:
            cycle_length (str): The length of the assimilation window.

        """
        # Set a default of 3H for the length of a cycle.
        # Without the context provided by a cycle length, a
        # DTG has no meaning.
        self.set_cycle_length(kwargs.get("cycle_length", "3H"))

    def __new__(cls, *args, **kwargs):
        """Create new instance keeping only Dtg-compatible datetime attrs."""
        # cycle_length checks will only be performed in __init__
        kwargs.pop("cycle_length", None)

        # timezone will be set to UTC if not passed
        try:
            tzinfo = args[7]
            args = args[:7]
        except IndexError:
            tzinfo = kwargs.pop("tzinfo", timezone("utc"))
        if isinstance(tzinfo, str):
            tzinfo = timezone(tzinfo)
        if "tzinfo" not in kwargs:
            kwargs["tzinfo"] = tzinfo

        # Make it possible to create instance using either string or an
        # instance of datetime as the 1st positional argument. Keep support
        # for the datetime instantiation behaviour (with integers for year,
        # month, day, etc).
        if len(args) > 0 and not isinstance(args[0], int):
            if not any(isinstance(args[0], c) for c in [str, datetime]):
                raise TypeError(
                    "Cannot convert input '{}' ".format(args[0])
                    + "of type '{}' ".format(type(args[0]).__name__)
                    + "to {}".format(cls.__name__)
                )

            if len(args) > 1:
                raise ValueError(
                    "Only one positional argument is allowed "
                    + "if the first argument is not an integer"
                )

            try:
                # Add support to the YYYYMMDDHH standard DTG format
                # Assumed to be in UTC unless tzinfo is specified
                dt = datetime.strptime(args[0], "%Y%m%d%H")
                dt = dt.replace(tzinfo=kwargs["tzinfo"])
            except (ValueError, TypeError):
                # pd.Timestamp is flexible with string and datetime-like args
                # It is more convenient using pd.Timestamp than trying to
                # guess the type and format of args[0] manually
                ts_kwargs = kwargs.copy()
                try:
                    if args[0].tzinfo is not None:
                        ts_kwargs.pop("tzinfo")
                except AttributeError:
                    pass
                dt = pd.Timestamp(*args, **ts_kwargs).to_pydatetime()
                dt = dt.astimezone(kwargs["tzinfo"])

            # Clear args and pass only kwargs to datetime's __new__
            args = ()
            for att in [
                "year",
                "month",
                "day",
                "hour",
                "minute",
                "second",
                "microsecond",
                "tzinfo",
            ]:
                kwargs[att] = getattr(dt, att)

        new_instance = super().__new__(cls, *args, **kwargs)
        # Make sure DTGs don't have subdivisions smaller than one hour
        # This can easily happen if the instance is created based on string
        # or datetime-like arguments, or when it is created as a result of an
        # addition/subtraction operation
        eqv_valid_instance = super().__new__(
            cls,
            new_instance.year,
            new_instance.month,
            new_instance.day,
            new_instance.hour,
            tzinfo=new_instance.tzinfo,
        )
        if new_instance.as_datetime() != eqv_valid_instance.as_datetime():
            msg = "Dtg {} not allowed: ".format(new_instance.as_datetime())
            msg += "Minimum allowed Dtg subdivision is an hour"
            raise ValueError(msg)

        return new_instance

    def __reduce_ex__(self, protocol):
        # We define this method so that pickle knows how to recover a pickled
        # object of this class. If we don't do this, then pickle tries to pass
        # a bytes object to the classe's __new__ method upon inpickling. This
        # also indirectly affects copy and deepcopy. See a similar issue at
        # <https://stackoverflow.com/questions/59571625/
        #  unable-to-pickle-datetime-subclass>
        # Using functools.partial to be able to pass kwargs
        callable_for_new = partial(type(self), cycle_length=self.cycle_length)
        args = (self.isoformat(),)
        return callable_for_new, args

    # Handy type conversions
    def as_pandas_timestamp(self):
        """Return a copy as a panda's Timestamp object."""
        return pd.Timestamp(self)

    def as_datetime(self):
        """Return a copy as a datetime.datetime object."""
        return self.as_pandas_timestamp().to_pydatetime()

    # Useful little methods/properties
    @property
    def cycle_length(self):
        """Return the length of the data assimilation cycle."""
        return self._cycle_length

    @property
    def cycle_start(self):
        """Return the earliest observation time encompassed by the DTG."""
        return self.as_pandas_timestamp() - 0.5 * self.cycle_length.delta

    @property
    def cycle_end(self):
        """Return the first observation time not encompassed by the DTG."""
        return self.as_pandas_timestamp() + 0.5 * self.cycle_length.delta

    @property
    def assimilation_window(self):
        """Return the DTG's assimilation window: [cycle_start, cycle_end)."""
        return pd.Interval(self.cycle_start, self.cycle_end, closed="left")

    def get_next(self):
        """Return the next DTG."""
        return self + self.cycle_length

    def get_previous(self):
        """Return the previous DTG."""
        return self - self.cycle_length

    # cycle_length-related methods
    def compatible_with_cycle_length(self, cycle_length="self"):
        """Check if DTG is compatible with cycle length.

        Args:
            cycle_length (str): A cycle length. Default value = "self".

        Returns:
            bool: True if DTG is compatible with cycle length else False.

        """
        if cycle_length is None:
            return True

        if cycle_length == "self":
            cycle_length = self.cycle_length
        else:
            cycle_length = to_offset(cycle_length)
        # It is convenient to check this using pandas Timestamp objects
        # At the time of writing this, inheriting from pd.Timestamp lead
        # to strange behaviours.
        dtg = pd.Timestamp(self)
        return (dtg - dtg.normalize()) % cycle_length == timedelta(0)

    def set_cycle_length(self, cycle_length):
        """Set the assimilation cycle length associated with the DTG.

        Args:
            cycle_length (str): The new cycle length.

        Raises:
            ValueError: If cycle_length smaller that min allowed, or if Dtg
                not compatible with cycle_length.

        """
        # Set a default of 3H for the length of a cycle.
        # Without the context provided by a cycle length, a
        # DTG has no meaning.
        cycle_length = to_offset(cycle_length)
        # Validate cycle_length
        min_cycle_length = to_offset("1H")
        ref_date = datetime(2000, 1, 1)
        new_date = ref_date + cycle_length
        min_allowed_new_date = ref_date + min_cycle_length
        if new_date < min_allowed_new_date:
            raise ValueError(
                "Min allowed cycle_length is "
                + str(min_cycle_length)
                + ". Passed cycle_length={}".format(cycle_length)
            )
        if not self.compatible_with_cycle_length(cycle_length):
            raise ValueError(
                "Dtg {} not compatible with cycle_length {}".format(
                    self, cycle_length
                )
            )
        self._cycle_length = cycle_length

    # Override some methods to ensure results are consistent with Dtg type
    def replace(self, *args, **kwargs):
        """Overrride datetime's "replace" method.

        Args:
            *args: Args passed to datetime's original method.
            **kwargs: Keyword args passed to datetime's original method.

        Returns:
            Dtg:  Dtg with the appropriate fields replaced.

        """
        new = super().replace(*args, **kwargs)
        return Dtg(new, cycle_length=self.cycle_length)

    # Behaviour under action of + and - operands
    def __add__(self, delta):
        new_datetime = self.as_datetime() + delta
        return self.__class__(new_datetime, cycle_length=self.cycle_length)

    def __radd__(self, delta):
        return self.__add__(delta)

    def __sub__(self, other):
        new = self.as_datetime() - other
        try:
            # Casting to Dtg will work provided that "other" is a
            # timedelta-like obj and it does not violate cycle_length
            return self.__class__(new, cycle_length=self.cycle_length)
        except TypeError:
            # This will happen if "other" is any datetime-like object
            return new

    # Make sure we consider cycle_length when comparing for equality
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        eq_timestamp = super().__eq__(other)
        same_cycle_length = self.cycle_length == other.cycle_length
        return eq_timestamp and same_cycle_length

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.strftime("%Y-%m-%dT%H %Z")

    def __repr__(self):
        return "{}('{}', cycle_length='{}')".format(
            self.__class__.__name__,
            self.isoformat(),
            self.cycle_length.freqstr,
        )


class DtgContainer:
    """Implement a container for instances of the Dtg class."""

    def __init__(self, data=None, start=None, end=None, cycle_length=None):
        """Validate input and set corresponding attribiutes.

        Args:
            data (Dtg or list of Dtg): Dtg or list of Dtgs.
            start (Dtg): First Dtg.
            end (Dtg): Last Dtg.
            cycle_length (str): Length of the assimilation window.

        Raises:
            ValueError: If dtg parameters are missing or inconsistent.

        """
        # Validate input:
        # (i) data and (start, end) are mutually exclusive (avoid ambiguities)
        if data is None:
            if (start is None) or (end is None):
                raise ValueError(
                    "Need 'start' and 'end' and if 'data' is not passed"
                )
            # msg_which_input and input_vals will be used later on in the
            # cycle_length validation
            msg_which_input = "'start' and 'end'"
            input_vals = [start, end]
        else:
            if (start is not None) or (end is not None):
                raise ValueError(
                    "Pass either just 'data' or both 'start' and 'end'"
                )
            msg_which_input = "the elements of 'data'"
            input_vals = data
        # (ii) Decide whether to get cycle_length from
        #      data/start/end or from class arg
        try:
            # Calling method ".freqstr" because, since pandas v1.1.0, "freq"
            # objects stopped being hashable and the following line would cause
            # TypeError "unhashable type: 'pandas._libs.tslibs.offsets.Hour'"
            data_c_length = list({d.cycle_length.freqstr for d in input_vals})
        except AttributeError:
            data_c_length = []

        if cycle_length is None:
            if len(data_c_length) == 1:
                cycle_length = data_c_length[0]
            else:
                raise ValueError(
                    "No (or inconsistent) 'cycle_length' info found in "
                    + "{}, and no 'cycle_length' ".format(msg_which_input)
                    + "passed to '{}'".format(self.__class__.__name__)
                )
        elif len(data_c_length) > 0:
            logger.warning(
                (
                    "The value(s) of the 'cycle_length' attribute(s) of "
                    "%s will be replaced by the 'cycle_length' value "
                    "passed to the '%s' constructor (=%s)"
                ),
                msg_which_input,
                self.__class__.__name__,
                cycle_length,
            )

        # Populate attributes
        self._cycle_length = to_offset(cycle_length)
        if data is None:
            self._start = Dtg(start, cycle_length=self.cycle_length)
            self._end = Dtg(end, cycle_length=self.cycle_length)
            self._data = None
        else:
            self._start = None
            self._end = None
            # Convert data to Dtg for consistency, and make it immutable
            self._data = tuple(
                Dtg(d, cycle_length=self.cycle_length) for d in data
            )

    @property
    def cycle_length(self):
        """Return the assimilation cycle length associated with the DTG."""
        return self._cycle_length

    def __len__(self):
        if self._data is None:
            max_index = abs((self._end - self._start).total_seconds())
            max_index /= self.cycle_length.nanos * 1e-9
            return int(max_index) + 1
        return len(self._data)

    def __getitem__(self, item):
        # We don't need to define __iter__ when we make an obj indexable
        if self._data is not None:
            return self._data[item]

        sign = np.sign((self._end - self._start).total_seconds())

        def calc_nth_item(n):
            if (n > len(self) - 1) or (n < -len(self)):
                raise IndexError(
                    "{} index out of range".format(self.__class__.__name__)
                )
            return self._start + sign * (n % len(self)) * self.cycle_length

        if isinstance(item, slice):
            return [calc_nth_item(i) for i in range(len(self))[item]]
        return calc_nth_item(item)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (
            other.cycle_length == self.cycle_length
            and other._data == self._data
            and other._start == self._start
            and other._end == self._end
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        rtn = "{} object:\n".format(self.__class__.__name__)
        if self._data is None:
            rtn += "    start={}, end={}\n".format(self._start, self._end)
        else:
            rtn += "    data=[{}]\n".format(", ".join(map(str, self._data)))
        rtn += "    cycle_length={}".format(self.cycle_length)
        return rtn

    __str__ = __repr__
