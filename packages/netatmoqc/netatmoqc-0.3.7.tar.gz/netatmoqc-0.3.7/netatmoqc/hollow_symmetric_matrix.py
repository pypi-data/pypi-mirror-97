#!/usr/bin/env python3
"""Implement HollowSymmetricMatrix class and related routines."""
import copy
import logging
import time

import humanize
import numpy as np
from numba import njit, prange

logger = logging.getLogger(__name__)


class HsmDiagNotStoredInCompactForm(Exception):
    """Exception to inform that HSM matrix is not in compact form."""

    def __init__(
        self,
        *args,
        msg="Diagonal elements of HSM matrix are not stored in compact form",
        **kwargs
    ):
        """Initialise with a default exception message."""
        super().__init__(msg, *args, **kwargs)


@njit(cache=True)
def _matrix_index_to_data_index(order, i, j):
    """Hollow symmetric matrix 'matrix -> compact array' index conversion.

    Given a hollow symmetric matrix M of order "order" and a linear array,
    say "M_data", that stores only the independent elements of M, return the
    index i_data such that

                M(i, j) = M_data(i_data)

    This function is used in the HollowSymmetricMatrix class.

    Args:
        order (int): Order of the hollow symmetric matrix.
        i (int): Matrix row index.
        j (int): Matrix column index.

    Returns:
        int:
            * In the interval [0, n*(n - 1)/2) if i != j
            * -(order + 1) if i == j (flagging thus that i==j elements are not
                stored).
                The choice of returning "-(order + 1)" for i==j instead of
                raising an exception is because numba only implemented support
                to handling exceptions in python < 3.7, but we need this to be
                used with python >= 3.6.10.

    Raises:
        ValueError: If order < 1.
        IndexError: If the condition "-order <= i,j < order" does not hold.

    """
    if order < 1:
        raise ValueError("Argument 'order' must be larger than zero")
    if i < -order or i >= order:
        # Numba doesn't allow a nicely formatted msg with indice values here
        raise IndexError("Index i should be larger than -(order + 1)")
    if j < -order or j >= order:
        raise IndexError("Index j should be larger than -(order + 1)")

    # Wrap around valid negative indices
    if i < 0:
        i += order
    if j < 0:
        j += order

    if i == j:
        # Flag that there's no index corresponding to i==j
        return -(order + 1)

    if i > j:
        # Enforce M(i, j) = M(j, i)
        i, j = j, i

    # n_indep_els_before_row: Total number of independent elements
    # located in the rows prior to row=i for the matrix M
    n_indep_els_before_row = i * order - (i * (i + 1)) // 2

    return n_indep_els_before_row + (j - i - 1)


@njit(cache=True)
def _data_index_to_matrix_index(n, i_data, check_bounds=True):
    """Hollow symmetric matrix 'compact array -> matrix' index conversion.

    Given a hollow symmetric matrix M of order "n" and a linear array, say
    "M_data", that stores only the independent elements of M, return the matrix
    indices (i, j) such that

                M(i, j) = M_data(i_data)

    This is the inverse of what is done in _matrix_index_to_data_index.

    This routine assumes
                        0 <= i_data < n(n-1)/2

    This function is used in the HollowSymmetricMatrix class, where
    consistency between the arguments is enforced.

    Row-major order.

    Args:
        n (int): Order of the hollow symmetric matrix (HSM).
        i_data (int): Index of data entry in the compact array that stores the
            independent elements of the HSM.
        check_bounds (bool): Whether or not to assert that n and i_data
            correspond to matrix indices (i, j) within bounds.
            (Default value = True).

    Returns:
        {
            int: Matrix row index,
            int: Matrix column index
        }

    Raises:
        ValueError: If check_bounds evaluates to True and n, i_data are outside
            their allowed ranges.

    """
    if check_bounds:
        if n < 1:
            raise ValueError("Arg 'n' must be larger than zero")
        if i_data < 0 or i_data >= n * (n - 1) / 2:
            raise ValueError("Arg 'i_data' not in the range [0, n*(n-1)/2)")

    i = (
        int(0.5 * ((2 * n + 1) - np.sqrt((2 * n + 1) ** 2 - 8 * (n + i_data))))
        - 1
    )
    j = (1 + i_data + i) - (i * (2 * n - i - 1)) // 2
    return i, j


@njit(cache=True, parallel=True)
def _to_dense(data, n, dtype):
    """Dense matrix form of a hollow symmetric matrix from its compact form.

    Takes an array 'data', assumed to hold the independent elements of a hollow
    symmetric M of order 'n', and returns a full (dense) representation of M.

    Assumes that len(data) = n*(n - 1)/2.
    No checks, however, are made on len(data). If you want to provide this
    functionality in an external API, please expose a wrapper to this function
    where this is asserted.

    This function is used in the HollowSymmetricMatrix class, where
    consistency between the arguments is enforced.

    Args:
        data (numpy.array): Array that stores the independent elements of the
            hollow symmetric matrix (hsm), i.e., the HSM's compact form.
        n (int): The order of the HSM.
        dtype (numpy.dtype): dtype of the data.

    Returns:
        np.nparray: Dense representation of the HSM (full 2D matrix form).

    """
    dense = np.zeros(shape=(n, n), dtype=dtype)
    for idata in prange(len(data)):
        i, j = _data_index_to_matrix_index(n, idata, check_bounds=False)
        data_value = data[idata]
        dense[i, j] = data_value
        dense[j, i] = data_value
    return dense


@njit(cache=True, parallel=True)
def _to_compact(dense, dtype):
    """Compact matrix form of a hollow symmetric matrix from its dense form.

    Args:
        dense (np.nparray): Dense representation of the HSM (full matrix form).
        dtype (numpy.dtype): dtype of the data.

    Returns:
        numpy.array: Array with the independent elements of the HSM

    Raises:
        ValueError: If dense is not a 2D, square matrix.

    """
    if dense.ndim != 2:
        raise ValueError("dense.ndim != 2")
    if dense.shape[0] != dense.shape[1]:
        raise ValueError("'dense' is not a square matrix")

    n = dense.shape[0]
    n_indep = (n ** 2 - n) // 2
    compact = np.zeros(n_indep, dtype=dtype)
    for idata in prange(len(compact)):
        i, j = _data_index_to_matrix_index(n, idata, check_bounds=False)
        compact[idata] = dense[i, j]
    return compact


@njit(cache=True)
def _get_hsm_subspace_from_compact(compact, indices):
    """Subspace of an HSM compact, as "irow in indices & icol=irow".

    Args:
        compact (numpy.array): Array with the independent elements of the HSM
        indices (list): Indices of the subdimentions of the HSM to include in
            the subspace.

    Returns:
        numpy.array: Compact form of the selected subspace.

    Raises:
        ValueError: If the number of elements in the subspace is not
            consistent with the passed indices.

    """
    n_indep = len(compact)
    n = int(np.rint(0.5 * (1.0 + np.sqrt(1.0 + 8.0 * n_indep))))
    new_n = len(indices)
    new_n_indep = (new_n ** 2 - new_n) // 2
    new_compact = np.zeros(new_n_indep, dtype=compact.dtype)

    idata_new = 0
    for i in indices:
        for j in indices:
            if i >= j:
                continue
            idata = _matrix_index_to_data_index(n, i, j)
            new_compact[idata_new] = compact[idata]
            idata_new += 1
    if idata_new != len(new_compact):
        raise ValueError("Number of calcd elements do not match the expected")
    return new_compact


@njit(cache=True)
def _get_submatrix_from_hsm_compact(hsm_compact, order, bcasted_keys):
    """Extract submatrix from a HollowSymmetricMatrix in dense form.

    Memory-efficient way to extract a submatrix from HollowSymmetricMatrix
    objects using fancy indexing. It does not require the conversion of the
    HollowSymmetricMatrix object into its dense form, and requires extra mem
    allocation for the submatrix elemnts only.

    Used in the __getitem__ method of HollowSymmetricMatrix

    Args:
        hsm_compact (numpy.array): Array with the compact form of the HSM.
        order (int): Order of the HSM.
        bcasted_keys (list): Broadcasted keys passed to the __getitem__
            method that calls this function. See also the function
            _getitem_keys_to_bcast_arrays.

    Returns:
        np.ndarray: Submatrix selected according to the indices contructed
            from bcasted_keys.

    """
    submatrix_shape = bcasted_keys[0].shape
    n_data = bcasted_keys[0].size
    submatrix_as_linear = np.empty(n_data, dtype=hsm_compact.dtype)
    i_data = 0
    for i_list, j_list in zip(bcasted_keys[0], bcasted_keys[1]):
        for i, j in zip(i_list, j_list):
            i_data_in_compact = _matrix_index_to_data_index(order, i, j)
            if i_data_in_compact < -order:
                # If _matrix_index_to_data_index flags "value not stored"
                submatrix_as_linear[i_data] = 0.0
            else:
                submatrix_as_linear[i_data] = hsm_compact[i_data_in_compact]
            i_data += 1
    return submatrix_as_linear.reshape(submatrix_shape)


def _getitem_keys_to_bcast_arrays(keys):
    """Convert keys passed to __getitem__ into broadcasted arrays."""
    if any(isinstance(key, slice) for key in keys):
        raise ValueError("Cannot accept slices as input")
    # Numba likes it better if we return an ndarray here
    return np.array(np.broadcast_arrays(*keys))


@njit(cache=True)
def _slice2range(the_slice, array_length):
    """Convert a slice into a list of indices according to the array length."""
    return range(*the_slice.indices(array_length))


@njit(cache=True)
def _get_hsm_double_slice(hsm_compact, order, row_slice, col_slice):
    """Extract [row_slice, col_slice] from HSM compact form."""
    row_numbers = _slice2range(row_slice, order)
    col_numbers = _slice2range(col_slice, order)
    submatrix_shape = (len(row_numbers), len(col_numbers))
    ndata = len(row_numbers) * len(col_numbers)
    submatrix = np.empty(ndata, dtype=hsm_compact.dtype)
    i_data = 0
    for i in row_numbers:
        for j in col_numbers:
            i_data_in_compact = _matrix_index_to_data_index(order, i, j)
            if i_data_in_compact < -order:
                # _matrix_index_to_data_index flag for "value is not stored"
                submatrix[i_data] = 0.0
            else:
                submatrix[i_data] = hsm_compact[i_data_in_compact]
            i_data += 1
    return submatrix.reshape(submatrix_shape)


def _get_hsm_row_slice(hsm_compact, order, the_slice):
    """Extract row slice from a HollowSymmetricMatrix in compact form."""
    return _get_hsm_double_slice(hsm_compact, order, the_slice, slice(None))


def _get_hsm_col_slice(hsm_compact, order, the_slice):
    """Extract column slice from a HollowSymmetricMatrix in compact form."""
    return _get_hsm_double_slice(hsm_compact, order, slice(None), the_slice)


class _MemSize:
    """Prepare a "pretty-print" form of the HollowSymmetricMatrix memsize."""

    def __init__(self, size_in_bytes):
        if size_in_bytes < 0:
            raise ValueError("Arg 'size_in_bytes' cannot be negative")
        self.bytes = size_in_bytes

    def __repr__(self):
        return "{}(size_in_bytes={})".format(type(self).__name__, self.bytes)

    def __str__(self):
        return humanize.naturalsize(self.bytes)


# Dict mapping numpy funcs into our eventual custom implementations for them.
# To be edited via the decorator defined below.
_NUMPY_FUNCTIONS_HANDLED_BY_HSM = {}


# Define a decorator to allow us to define custom implementations of some numpy
# array functions. See <https://numpy.org/doc/stable/user/basics.dispatch.html>
def _implements_np_function_for_hsm(np_function):
    """Register __array_function__ implementation for HollowSymmetricMatrix."""

    def decorator(func):
        """Get decorator to add implementations of numpy array functions."""
        _NUMPY_FUNCTIONS_HANDLED_BY_HSM[np_function] = func
        return func

    return decorator


class HollowSymmetricMatrix(np.lib.mixins.NDArrayOperatorsMixin):
    """Hollow symmetric matrix with flexible memory storage options.

    A hollow symmetric matrix is a square matrix M of order n that satisfies:
        * M[i, j] = M[j, i] for all i, j in range(n)
        * M[i, i] = 0 for all i in range(n)

    There are therefore only (n**2 - n)/2 independent elements in such a
    matrix. A new instance of this class will store only the independent
    elements of a hollow symmetric matrix, while allowing access to such
    elements via regular matrix indexing.

    The order n of the underlying hollow symmetric matrix is inferred from
    the passed data array. A ValueError will be raised if the length of the
    data array is incompatible with the number of independent elements of a
    hollow symmetric matrix.

    There "optimize_mode" arg accepts three choices:
        * "speed"
            - The matrix will be stored in its dense (full) form
            - Copies will be returned as numpy 2D float64 arrays
        * "memory":
            - The matrix will be stored in compact form
            - Copies will return HollowSymmetricMatrix instances
        * "speed_mem_compromise":
            - The matrix will be stored in its dense (full) form
            - Copies will return HollowSymmetricMatrix instances
    When used with HDBSCAN, the following relation holds for memory usage:
                "memory" < "speed_mem_compromise" < "speed",
    and the inverse relation holds for execution times.

    """

    def __init__(self, data, dtype=None, optimize_mode="memory"):
        """Initialise data, optimize_mode and 'T' attrs."""
        self._set_data(data, dtype)

        # Decide how the matrix elements will be stored
        self._optimize_mode = optimize_mode.lower()
        opt_mode_choices = ["speed", "speed_mem_compromise", "memory"]
        if self._optimize_mode not in opt_mode_choices:
            msg = "'{}' not allowed for the 'optimize_mode' arg. "
            msg += "Please choose from: {}"
            msg = msg.format(optimize_mode, ", ".join(opt_mode_choices))
            raise ValueError(msg)
        if self._optimize_mode == "memory":
            self.convert_to_compact_storage()
        else:
            # self then becomes just a container for the 2D numpy array.
            # The difference between "speed" and "speed_mem_compromise"
            # modes lies in how self.copy behaves.
            self.convert_to_dense_storage()

        logger.debug("Init new %s object:\n%s", type(self).__name__, self)

    @classmethod
    def validated_data(cls, data):
        """Get HSM-compatible version of data. ValueError if not possible."""
        if np.ndim(data) == 1:
            n_indep = len(data)
            order = 0.5 * (1.0 + np.sqrt(1.0 + 8.0 * n_indep))
            nearest_int_order = int(np.rint(order))
            if abs(order - nearest_int_order) > 1e-8:
                nearest_n_indep = int(
                    0.5 * nearest_int_order * (nearest_int_order - 1)
                )
                msg = "len(data)={0} incompatible with {1}: {2} elements "
                msg += "needed for a {3}x{3} matrix (closest option)"
                msg = msg.format(
                    n_indep, cls.__name__, nearest_n_indep, nearest_int_order
                )
                raise ValueError(msg)
        elif np.ndim(data) == 2:
            if not np.equal(*np.shape(data)):
                raise ValueError("'data' is not a square matrix")
            if not np.allclose(data, np.transpose(data)):
                logger.warning(
                    "%s: Data not symmetric. Copying upper-diag into lower!",
                    cls.__name__,
                )
                # The diag should be zero, so we won't subtract it here.
                # If it isn't zero, then this will be taken care of next.
                triu = np.triu(data)
                data = triu + triu.T
            if any(data[_, _] != 0 for _ in range(np.shape(data)[0])):
                logger.warning(
                    "%s: Resetting diagonal elements to %s",
                    cls.__name__,
                    type(data[0, 0])(0),
                )
                # Note that np.fill_diagonal takes care of typecasting
                np.fill_diagonal(data, 0)
        else:
            raise ValueError(
                "%s: ndim(data) should be 1 or 2. Got %s."
                % (cls.__name__, np.ndim(data))
            )
        return data

    def _set_data(self, new, check_data_consistency=True, dtype=None):
        """Set/reset self._data."""
        if check_data_consistency:
            new = self.__class__.validated_data(new)
        if dtype is None:
            self._data = np.array(new)
        else:
            self._data = np.array(new, dtype=dtype)
        # The underlying data array should not be directly modified externally
        self._data.flags.writeable = False

    @property
    def optimize_mode(self):
        """Return the mode for which the matrix is optimised."""
        return self._optimize_mode

    @property
    def data_mem_usage(self):
        """Return mem usage of the data array contained within self."""
        return _MemSize(self._data.nbytes)

    @property
    def dtype(self):
        """Return the matrix data type."""
        return self._data.dtype

    @property
    def order(self):
        """Return the matrix order, as in "order N" for an NxN matrix."""
        if self.stored_as_compact:
            n_indep = len(self._data)
            rtn = int(np.rint(0.5 * (1.0 + np.sqrt(1.0 + 8.0 * n_indep))))
        else:
            rtn = self._data.shape[0]

        return rtn

    @property
    def n_indep_els(self):
        """Return the #independent (non-redundant off-diagonal) elements."""
        return (self.order ** 2 - self.order) // 2

    @property
    def shape(self):
        """Return the matrix shape."""
        return (self.order, self.order)

    @property
    def ndim(self):
        """Return the number of dimensions of the matrix."""
        return 2

    @_implements_np_function_for_hsm(np.transpose)
    def transpose(self):
        """Transpose of a HollowSymmetricMatrix object: A copy of the object.

        This also implements np.transpose for HollowSymmetricMatrix objects

        Returns:
            netatmoqc.hollow_symmetric_matrix.HollowSymmetricMatrix: Just a
                copy of self, as HollowSymmetricMatrix objects are, well,
                symmetric.

        """
        return self.copy()

    # Create a "T" property as an alias for self.transpose()
    T = property(transpose)

    @property
    def stored_as_compact(self):
        """Return True if matrix is stored in compact mode, False otherwise."""
        return self._data.ndim == 1

    @property
    def stored_as_dense(self):
        """Return True if matrix is stored in dense mode, False otherwise."""
        return not self.stored_as_compact

    def compact_form(self):
        """Return the compact-form representation of the matrix."""
        if self.stored_as_compact:
            rtn = self._data
        else:
            logger.debug("%s: Computing compact form", type(self).__name__)
            start = time.time()
            rtn = _to_compact(self._data, self.dtype)
            # Set the return value to read-only for consistency,
            # as this is how it would be if self.stored_as_compact
            # since self._data is read-only
            rtn.flags.writeable = False
            logger.debug(
                "Done computing compact form. Elapsed: %.2fs",
                time.time() - start,
            )

        return rtn

    def dense_form(self):
        """Return the dense-form representation of the matrix."""
        if self.stored_as_dense:
            rtn = self._data
        else:
            logger.debug(
                "%s: Computing %s dense form", type(self).__name__, self.shape
            )
            start = time.time()
            rtn = _to_dense(self._data, self.order, self.dtype)
            # Set the return value to read-only for consistency,
            # as this is how it would be if self.stored_as_dense
            # since self._data is read-only
            rtn.flags.writeable = False
            logger.debug(
                "Done computing dense form. Elapsed: %.2fs",
                time.time() - start,
            )

        return rtn

    def subspace(self, indices):
        """Subspace of self constructed as "irow in indices & icol=irow"."""
        logger.debug("%s: Subspace requested", type(self).__name__)

        # In case we get, e.g., panda Series objects
        indices = np.array(indices)

        # Fancy indexing as below is quicker than [indices, :][:, indices]
        if self.stored_as_compact:
            new_data = _get_hsm_subspace_from_compact(
                self.compact_form(), indices
            )
        else:
            new_data = self[indices[:, np.newaxis], indices]

        return self.__class__(
            new_data, dtype=self.dtype, optimize_mode=self.optimize_mode,
        )

    def convert_to_dense_storage(self):
        """Change matrix storage mode to "dense"."""
        if self.stored_as_dense:
            return
        logger.debug("%s: Switch to dense storage", type(self).__name__)
        self._set_data(self.dense_form(), check_data_consistency=False)

    def convert_to_compact_storage(self):
        """Change matrix storage mode to "compact"."""
        if self.stored_as_compact:
            return
        logger.debug("%s: Switch to compact storage", type(self).__name__)
        self._set_data(self.compact_form(), check_data_consistency=False)

    def index_dense_to_compact(self, i, j):
        """Return integer I such that self.data[I] == self[i, j]."""
        if i == j:
            raise HsmDiagNotStoredInCompactForm
        return _matrix_index_to_data_index(self.order, i, j)

    def index_compact_to_dense(self, data_i):
        """Return (i, j) such that self.data[data_i] == self[i, j]."""
        return _data_index_to_matrix_index(self.order, data_i)

    def __array__(self, dtype=None, copy=False, order=None):
        # See <https://numpy.org/devdocs/user/basics.dispatch.html>
        # TODO: Remove the ".astype(np.float64)" when possible.
        # HDBSCAN requires that the result of np.array(self) to have
        # dtype=numpy.float64. There's an open feature request at
        # <https://github.com/scikit-learn-contrib/hdbscan/issues/108>
        # (checked on 2020-09-02) for support to other types. Let's wait.
        logger.debug("%s: Calling '__array__'  method", type(self).__name__)
        return self.dense_form().astype(np.float64)

    def __getitem__(self, ij_tuple):
        if self.stored_as_dense:
            # Use numpy's own __getitem__
            rtn = self.dense_form()[ij_tuple]
        elif all(isinstance(index, int) for index in ij_tuple):
            # Just an element, neither slices nor fancy indexing
            try:
                i_data = self.index_dense_to_compact(*ij_tuple)
                rtn = self.compact_form()[i_data]
            except HsmDiagNotStoredInCompactForm:
                rtn = 0.0
        elif all(isinstance(_, slice) for _ in ij_tuple):
            logger.debug("%s: Get row and column slices", type(self).__name__)
            rtn = _get_hsm_double_slice(
                self.compact_form(), self.order, *ij_tuple
            )
        elif isinstance(ij_tuple[0], slice):
            logger.debug("%s: Get row slice", type(self).__name__)
            rtn = _get_hsm_row_slice(
                self.compact_form(), self.order, ij_tuple[0]
            )[:, ij_tuple[1]]
        elif isinstance(ij_tuple[1], slice):
            logger.debug("%s: Get column slice", type(self).__name__)
            rtn = _get_hsm_col_slice(
                self.compact_form(), self.order, ij_tuple[1]
            )[ij_tuple[0], :]
        else:
            logger.debug(
                "%s: Get fancy-indexed submatrix", type(self).__name__
            )
            bcasted_keys = _getitem_keys_to_bcast_arrays(ij_tuple)
            rtn = _get_submatrix_from_hsm_compact(
                self.compact_form(), self.order, bcasted_keys
            )

        return rtn

    def copy(self):
        """Return a copy of the matrix, formatted depending on optimize_mode.

        Returns:
            {
                numpy.ndarray: If optimize_mode == "speed". Dense form.
                netatmoqc.hollow_symmetric_matrix.HollowSymmetricMatrix: If
                    optimize_mode != "speed".
            }

        """
        logger.debug("%s: Calling 'copy'  method", type(self).__name__)
        if self.optimize_mode == "speed":
            # HDBSCAN calls this method multiple times, and then calls
            # np.asarray on the returned copy. If self is optimized for
            # speed, then let's return a numpy array already. This is going
            # to cost in memory, as the returned array is not simply a copy
            # of the already available dense form, but rather the dense
            # form casted into np.float64 (HDBSCAN requires this; see the
            # __array__ method).
            rtn = np.asarray(self)
        else:
            # In this case, __array_ufunc__ will be called if numpy ufuncs
            # are called with self as arg. Besides this:
            # * If optimize_mode == "speed_mem_compromise", then the dense
            # form is available (having thus an increased memory use w.r.t.
            # optimize_mode == "memory"), but it won't be cast into np.float64
            # unless np.asarray is called on self (thus reducing memory usage
            # w.r.t. optimize_mode == "speed").
            # * If optimize_mode == "memory", then the dense form is not kept
            # on memory and will be calculated only when necessary and kept
            # on memory only as long it is needed for. This saves memory but
            # increases computation.
            rtn = copy.copy(self)
        return rtn

    def __setitem__(self, ij_tuple, value):
        try:
            boolean_indexing = ij_tuple.dtype == np.bool
        except AttributeError:
            boolean_indexing = np.array(ij_tuple).dtype == np.bool

        if boolean_indexing:
            if isinstance(ij_tuple, type(self)):
                self._data.flags.writeable = True
                if self.stored_as_dense:
                    self._data[ij_tuple.dense_form()] = value
                else:
                    self._data[ij_tuple.compact_form()] = value
                self._data.flags.writeable = False
            else:
                initially_as_compact = self.stored_as_compact
                self.convert_to_dense_storage()
                self._data.flags.writeable = True
                self._data[ij_tuple] = value
                # Using self._set_data to check for invalid values
                self._set_data(self._data)
                if initially_as_compact:
                    self.convert_to_compact_storage()
        elif all(isinstance(_, (int, np.integer)) for _ in ij_tuple):
            # Just an element, neither slices nor fancy indexing
            self._data.flags.writeable = True
            try:
                i_data = self.index_dense_to_compact(*ij_tuple)
                if self.stored_as_dense:
                    # Make sure the matrix remains symmetric
                    self._data[ij_tuple] = value
                    self._data[ij_tuple[::-1]] = value
                else:
                    self._data[i_data] = value
            except HsmDiagNotStoredInCompactForm:
                # Make sure the matrix remains hollow
                logger.warning(
                    "Cannot set %s diagnonal elements. Doing nothing.",
                    type(self).__name__,
                )
            self._data.flags.writeable = False
        else:
            msg = "Setting {} items is only supported via bool or int indices"
            raise NotImplementedError(msg.format(type(self).__name__))

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        ufunc_method = getattr(ufunc, method)
        if all(isinstance(_, self.__class__) for _ in inputs):
            logger.debug(
                "%s: __array_ufunc__ handling same-class '%s.%s'",
                type(self).__name__,
                ufunc.__name__,
                method,
            )

            # Test if the ufunc still returns a hollow symmetric matrix
            try:
                test_hsm = np.array([0, 1, 1, 0]).reshape(2, 2)
                test_inputs = tuple(test_hsm.astype(_.dtype) for _ in inputs)
                test_result = ufunc_method(*test_inputs, **kwargs)
                result_is_hsm = (
                    # Check 1: Result is a matrix
                    test_result.ndim == 2
                    # Check 2: Result matrix is square
                    and np.equal(*test_result.shape)
                    # Check 3: Result matrix is symmetric
                    and np.allclose(test_result, test_result.T)
                    # Check 2: Result matrix diagonal is zero
                    and np.allclose(
                        ufunc_method(*test_inputs, **kwargs).diagonal(),
                        test_hsm.diagonal().astype(test_result.dtype),
                    )
                )
            except (ValueError, AttributeError):
                result_is_hsm = False

            if result_is_hsm and any(_.stored_as_compact for _ in inputs):
                new_inputs = tuple(_.compact_form() for _ in inputs)
            else:
                new_inputs = tuple(_.dense_form() for _ in inputs)
            result = ufunc_method(*new_inputs, **kwargs)

            if result_is_hsm:
                # Return another instance of type(self)
                if result.ndim != 1:
                    result = _to_compact(result, dtype=result.dtype)
                return self.__class__(
                    result,
                    dtype=result.dtype,
                    optimize_mode=self.optimize_mode,
                )
            else:
                # Return whatever the ufunc call returns
                logger.debug(
                    "ufunc '%s.%s(%s)' returning '%s', not '%s'",
                    ufunc.__name__,
                    method,
                    ", ".join(type(_).__name__ for _ in inputs),
                    type(result).__name__,
                    type(self).__name__,
                )
                return result
        else:
            # Act on the dense form, which is just a regular 2D numpy array
            logger.debug(
                "%s: __array_ufunc__ handling mixed-class '%s.%s'",
                type(self).__name__,
                ufunc.__name__,
                method,
            )
            new_inputs = [
                np.asarray(inp) if isinstance(inp, self.__class__) else inp
                for inp in inputs[:2]
            ]
            return ufunc_method(*new_inputs, **kwargs)

    def __array_function__(self, func, types, args, kwargs):
        """Allow class to define how numpy functions operate on its objects."""
        # Adapted from Numpy's own suggestions found on:
        # <https://numpy.org/neps/nep-0018-array-function-protocol.html>
        # <https://numpy.org/doc/stable/user/basics.dispatch.html>

        # Allow subclasses that don't override __array_function__
        # to handle HollowSymmetricMatrix objects
        if not all(issubclass(t, (self.__class__, np.ndarray)) for t in types):
            return NotImplemented

        try:
            # Use our custom implementation, if available
            array_func = _NUMPY_FUNCTIONS_HANDLED_BY_HSM[func]
            logger.debug(
                "%s (%s): Using custom implementation '%s' for numpy's '%s'",
                type(self).__name__,
                "__array_function__",
                array_func.__name__,
                func.__name__,
            )
        except KeyError:
            # Use NumPy's private implementation without __array_function__
            # dispatching if we don't have a custom implementation
            array_func = func._implementation
            logger.debug(
                "%s (%s): Using numpy's own implementation of '%s'",
                type(self).__name__,
                "__array_function__",
                func.__name__,
            )
        return array_func(*args, **kwargs)

    def __repr__(self):
        txt = "%s(\n"
        txt += "    shape=%s\n"
        txt += "    dtype=%s\n"
        txt += "    optimize_mode=%s\n"
        if self.stored_as_dense:
            txt += "    storage='dense' (%s elements stored in memory)\n"
            txt += "    memsize='%s'\n"
            txt += "    data:\n%s\n"
            data = self.dense_form()
        else:
            txt += "    storage='compact' (%s elements stored in memory)\n"
            txt += "    memsize=%s\n"
            txt += "    data=%s\n"
            data = self.compact_form()
        txt += ")"
        return txt % (
            type(self).__name__,
            self.shape,
            self.dtype,
            self.optimize_mode,
            data.size,
            self.data_mem_usage,
            data,
        )

    def __str__(self):
        order = self.order
        return self.dense_form().__str__() if order < 5 else self.__repr__()
