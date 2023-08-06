import time
import numpy as np
from collections import OrderedDict, Iterable


def _od_sort(v):
    """Return an OrderedDict of v.  If v is a dict, the returned
    OrderedDict will be sorted by the values of v.

    """
    if isinstance(v, dict):
        return OrderedDict(sorted(list(v.items()), key=lambda el: el[1]))
    else:
        return OrderedDict(v)


class CDSMatrix(object):
    """Interface to LIGO CDS front end EPICS matrix parts.

    CDSMatrix is initialized with a channel access prefix for the
    matrix channels (e.g. 'LSC-PD_DOF_MTRX'), and {name: index} dicts
    or [(name, index)] tuple lists for the matrix rows and columns:

    >>> LSCvac = CDSMatrix(prefix='LSC-PD_DOF_MTRX',
    ...                    rows={'DARM': 1,
    ...                          'MICH': 2,
    ...                          'PRCL': 3,
    ...                          'SRCL': 4,
    ...                          'CARM': 5,
    ...                          },
    ...                    cols={'OMC': 1,
    ...                          'POP9Q': 3,
    ...                          'POP45Q': 5,
    ...                          'REFL9Q': 7,
    ...                          'REFL45Q': 9,
    ...                         })
    >>> 

    If the "ramping" option is set True, the matrix will be treated as
    a "ramping" matrix, and the put methods will put values to the
    element SETTING channels.

    NOTE: for ramping matrices, values will not be set until the
    load() method has been called.

    The defined rows and columns will automatically be sorted by index
    at initialization, unless they are specified as lists of tuples,
    in which case the specified ordering is preserved.  This is
    relevant for methods that return lists of elements (get(), put(),
    etc.).

    Channel name strings for matrix elements can be retrieved by
    calling the instance with (row, column) name pairs:

    >>> LSCvac('MICH', 'POP45Q')
    'LSC-PD_DOF_MTRX_2_5'

    The get(), put(), is_ramping(), and zero() methods can be used to
    interact with the matrix via an EPICS ezca built-in object.  See
    their individual help for more info.  The TRAMP property can be
    used to set the matrix ramp, and load() can be used to load all
    values that have been set for a "ramping" matrix.  Individual
    matrix elements call also be accessed vai the getitem/setitem
    syntax:

    >>> LSCvac['MICH', 'POP45']
    0.0
    >>> LSCvac['MICH', 'POP45Q'] = 1
    H1:LSC-PD_DOF_MTRX_2_5 => 1

    Many methods, including __call__(), get(), put(), is_ramping(),
    and zero(), can access multiple elements of the matrix at once.
    If neither row/col are specified, all matrix elements will be
    used.  If either row/col is specified, just the elements from the
    specified row/col are used.  If both row and col are specified,
    just the specified element is used.

    The get_matrix() method returns the full matrix as a numpy.matrix
    object.  Similarly, the put_matrix() method will take a
    numpy.matrix object and write it into the full matrix.

    Examples:

    >>> LSCvac.get('PRCL', 'POP9Q')
    0.0
    >>> LSCvac.put('PRCL', 'POP9Q', 3)
    H1:LSC-PD_DOF_MTRX_3_3 => 3
    >>> LSCvac.get('PRCL')
    [0.0, 0.0, 0.0, 0.0, 0.0]
    >>> LSCvac.put('PRCL', 0)
    H1:LSC-PD_DOF_MTRX_3_1 => 0
    H1:LSC-PD_DOF_MTRX_3_3 => 0
    H1:LSC-PD_DOF_MTRX_3_5 => 0
    H1:LSC-PD_DOF_MTRX_3_7 => 0
    H1:LSC-PD_DOF_MTRX_3_9 => 0
    >>> LSCvac.put('PRCL', [1,2,3,4,5])
    H1:LSC-PD_DOF_MTRX_3_1 => 1
    H1:LSC-PD_DOF_MTRX_3_3 => 2
    H1:LSC-PD_DOF_MTRX_3_5 => 3
    H1:LSC-PD_DOF_MTRX_3_7 => 4
    H1:LSC-PD_DOF_MTRX_3_9 => 5
    >>> LSCvac.TRAMP = 3
    >>> LSCvac.load()

    """
    def __init__(self, prefix, rows, cols, ramping=False):
        """Initialize CDSMatrix.

        'prefix' is channel access prefix for the entire matrix.
        'rows' is a dict or list of (name, index) tuples.
        'cols' is a dict or list of (name, index) tuples.
        'ramping' is a bool to indicate the matrix is ramping type [False].

        """
        self.__prefix = prefix
        if ramping:
            self.__ramping = True
        else:
            self.__ramping = False
        self.__rows = _od_sort(rows)
        self.__cols = _od_sort(cols)

    def __repr__(self):
        s = """
CDSMatrix('%s', ramping=%s,
          rows=%s,
          cols=%s)""" % (self.__prefix,
                         self.__ramping,
                         self.__rows,
                         self.__cols)
        return s.strip()

    @property
    def rows(self):
        """Row definition"""
        return self.__rows

    @property
    def cols(self):
        """Column definition"""
        return self.__cols

    @property
    def shape(self):
        """Shape of matrix as a (rows, cols) tuple"""
        return (len(self.rows), len(self.cols))

    ##########

    def __rc_iter(self, row=None, col=None):
        """Iterator over (r,c) index pairs for the specified row,column names."""
        if row:
            rs = [self.__rows[row]]
        else:
            rs = list(self.__rows.values())
        if col:
            cs = [self.__cols[col]]
        else:
            cs = list(self.__cols.values())
        for r in rs:
            for c in cs:
                yield r,c

    def __el(self, r, c, prefix=None):
        pre = self.__prefix
        if prefix:
            pre += '_' + prefix
        return '%s_%s_%s' % (pre, r, c)

    def __call__(self, row=None, col=None, prefix=None):
        """Return (row, col) channel names.

        If neither row/col are specified, a list of all channels is
        returned.  If either row/col is specified, a list of channels
        for the specified row/col are returned.  If both row and col
        are specified, just the channel of the specified element is
        returned.

        A prefix may be provided to return e.g. 'SETTING' or 'RAMPING'
        channels.

        """
        chans = [self.__el(r,c,prefix) for r,c in self.__rc_iter(row, col)]
        if len(chans) == 1:
            return chans[0]
        else:
            return chans

    ##########
    # ezca methods:

    def __get(self, chan):
        return ezca[chan]

    def __put(self, chan, value):
        ezca[chan] = value

    def get_ind(self, r, c, prefix=None):
        """Get value from element by index."""
        return self.__get(self.__el(r, c, prefix))

    def put_ind(self, r, c, val):
        """Put value to element by index."""
        prefix = None
        if self.__ramping:
            prefix = 'SETTING'
        self.__put(self.__el(r, c, prefix), val)

    @property
    def TRAMP(self):
        """Current value of TRAMP."""
        return self.__get(self.__prefix+'_TRAMP')

    @TRAMP.setter
    def TRAMP(self, val):
        """Set TRAMP."""
        self.__put(self.__prefix+'_TRAMP', val)

    def load(self, wait=False):
        """Load all matrix elements for ramping matrix.

        If wait=True, load() will not return until all elements have
        completed ramping.

        """
        self.__put(self.__prefix+'_LOAD_MATRIX', 1)
        if wait:
            time.sleep(1)
            while any(self.is_ramping()):
                continue
            return True

    ##########

    def get(self, row=None, col=None):
        """Get value from element by name.

        If neither row/col are specified, a list of values for every
        element in the matrix is returned.  If either row/col is
        specified, a list of values for all elements in the specified
        row/col is returned.  If both row and col are specified, the
        value for just that element is returned.

        """
        d = [self.get_ind(r,c) for r,c in self.__rc_iter(row, col)]
        if len(d) == 1:
            return d[0]
        else:
            return d

    def get_matrix(self):
        """Return numpy.matrix for entire matrix.

        """
        return np.matrix([self.get(row=row) for row in self.rows])

    def put(self, row=None, col=None, value=None):
        """Put value to elements by name.

        If neither row/col are specified, value is put to all elements
        in the matrix.  If either row/col is specified, value is put
        to all elements in the specified row/col.  If both row and col
        are specified, the value is put to just that element.

        """
        if value is None:
            raise TypeError("Must specify value to put.")
        inds = list(self.__rc_iter(row, col))
        nel = len(inds)
        if isinstance(value, Iterable):
            if len(value) != nel:
                raise IndexError("value must be same length as number of elements to be set.")
        else:
            value = nel*[value]
        for rcv in zip(inds, value):
            (r, c), v = rcv
            self.put_ind(r, c, v)

    def put_matrix(self, matrix):
        """Write numpy.matrix to entire matrix.

        ValueError will be returned if matrix shapes do not agree.

        """
        if matrix.shape != self.shape:
            raise ValueError("matrix shapes do not agree.")
        r = 0
        for row in matrix.tolist():
            r += 1
            c = 0
            for v in row:
                c += 1
                self.put_ind(r, c, v)

    def __getitem__(self, rc):
        """Get element value."""
        return self.get(*rc)

    def __setitem__(self, rc, value):
        """Set element value."""
        row, col = rc
        self.put(row, col, value)

    def is_ramping(self, row=None, col=None):
        """True if elements are ramping.

        If neither row/col are specified, a list of is_ramping bools
        is returned for every element in the matrix.  If either
        row/col is specified, a list of is_ramping bools is returned
        for every elements in the specified row/col.  If both row and
        col are specified, the is_ramping bool for just that element
        is returned.

        """
        t= [self.get_ind(r, c, prefix='RAMPING') != 0
            for r, c in self.__rc_iter(row, col)]
        if len(t) == 1:
            return t[0]
        else:
            return t

    def zero(self, row=None, col=None):
        """Zero elements in the matrix.

        Equivalent to put(..., value=0)

        """
        self.put(row=row, col=col, value=0)
