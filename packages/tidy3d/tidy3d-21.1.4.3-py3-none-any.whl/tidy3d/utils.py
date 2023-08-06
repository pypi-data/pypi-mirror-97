import numpy as np
import subprocess

from .constants import fp_eps, EPSILON_0


def listify(obj):
    # Make a list if not a list
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, tuple):
        return list(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return [obj]


def list2str(li, elem_format):
    # Make a string that looks like the list ``li`` using %-specifying string 
    # ``elem_format`` for each element
    return "[" + " ".join([elem_format % elem for elem in li]) + "]"


def subprocess_cmd(command):
    """Execute a (multi-line) shell command.

    Parameters
    ----------
    command : str
        Semicolon separated lines.
    """
    comm_lines = command.split(";")
    for line in comm_lines:
        comm_list = list(line.split())
        process = subprocess.run(
            comm_list, stdout=None, check=True, stdin=subprocess.DEVNULL
        )


def inside_box_inds(span, mesh, include_zero_size=False):
    """Elementwise indicator function showing which points in a Box ``span``
    are inside a grid defined by ``mesh``.

    Parameters
    ----------
    span : np.ndarray of shape (3, 2)
        Defines (xmin, xmax), (ymin, ymax), (zmin, zmax) of the box.
    mesh : tuple
        3-tuple defining the xgrid, ygrid and zgrid.
    include_zero_size : bool, optional
        If True, a span of zero (max - min = 0) in any direction will be taken
        as one pixel. If False, the mask will be all empty.

    Returns
    -------
    indsx, indsy, indsz: tuple
        Tuples defining the (start, stop) index of the mesh inside the box.
    """

    # Check if min and max values are in order
    for dim in range(3):
        if span[dim, 1] < span[dim, 0]:
            raise ValueError(
                "Incorrect object span (max value smaller than " "min value)."
            )

    # Initialize indexes for no part of the mesh inside the box
    indsx, indsy, indsz = ((0, 0), (0, 0), (0, 0))

    # Do some checks that should return no mesh inside the box
    for dim in range(3):
        # Check if any of the mesh arrays has zero lengt
        if mesh[dim].size == 0:
            return indsx, indsy, indsz
        # Check if box is completely outside mesh
        if (span[dim, 0] > mesh[dim][-1]) or (span[dim, 1] < mesh[dim][0]):
            return indsx, indsy, indsz
        # Check if there's a strictly zero span and it was not requested.
        if (span[dim, 1] - span[dim, 0] == 0) and (not include_zero_size):
            return indsx, indsy, indsz

    indx = np.nonzero((span[0, 0] < mesh[0]) * (mesh[0] < span[0, 1]))[0]
    indy = np.nonzero((span[1, 0] < mesh[1]) * (mesh[1] < span[1, 1]))[0]
    indz = np.nonzero((span[2, 0] < mesh[2]) * (mesh[2] < span[2, 1]))[0]

    # If there's still a zero span and it was not requested, we're done.
    if (indx.size == 0 or indy.size == 0 or indz.size == 0) and (
        not include_zero_size
    ):
        return indsx, indsy, indsz

    # Otherwise, we build the mask. For zero span, we just take the first
    # element of the mesh that is larger than the requested min value.
    if indx.size == 0:
        indx1 = np.nonzero(span[0, 0] <= mesh[0])[0][0]
        indsx = (indx1, indx1 + 1)
    else:
        indsx = (indx[0], indx[-1] + 1)
    if indy.size == 0:
        indy1 = np.nonzero(span[1, 0] <= mesh[1])[0][0]
        indsy = (indy1, indy1 + 1)
    else:
        indsy = (indy[0], indy[-1] + 1)
    if indz.size == 0:
        indz1 = np.nonzero(span[2, 0] <= mesh[2])[0][0]
        indsz = (indz1, indz1 + 1)
    else:
        indsz = (indz[0], indz[-1] + 1)

    return (indsx, indsy, indsz)


def inside_box(span, mesh, include_zero_size=False):
    """Elementwise indicator function showing which points in the ``span`` are
    inside a grid defined by ``mesh``.

    Parameters
    ----------
    span : np.ndarray of shape (3, 2)
        Defines (xmin, xmax), (ymin, ymax), (zmin, zmax) of the box.
    mesh : tuple
        3-tuple defining the xgrid, ygrid and zgrid.
    include_zero_size : bool, optional
        If True, a span of zero (max - min = 0) in any direction will be taken
        as one pixel. If False, the mask will be all empty.

    Returns
    -------
    mask : np.ndarray
        A 3D array of shape (mesh[0].size, mesh[1].size, mesh[2].size)
        that is 1 inside the box and 0 outside.
    """

    # Initialize empty mask
    mask = np.zeros((mesh[0].size, mesh[1].size, mesh[2].size))

    indsx, indsy, indsz = inside_box_inds(span, mesh, include_zero_size)
    mask[indsx[0] : indsx[1], indsy[0] : indsy[1], indsz[0] : indsz[1]] = 1.0

    return mask


def intersect_box(span1, span2):
    """Return a span of a box that is the intersection between two spans."""
    span = np.zeros((3, 2))
    for d in range(3):
        span[d, 0] = max(span1[d, 0], span2[d, 0])
        span[d, 1] = min(span1[d, 1], span2[d, 1])

    return span


def object_name(obj_list, obj, prefix=""):
    """Return a name for the object that is unique within the names in a
    given list. The optional prefix is to be used if object.name is None.
    """
    if obj.name is not None:
        prefix = obj.name

    name_list = [obj.name for obj in obj_list]
    count = 1
    name = prefix
    if obj.name is None:
        name += "_0"

    while name in name_list:
        name = prefix + "_" + str(count)
        count += 1

    return name


def dft_spectrum(time_series, dt, freqs):
    """Computes the frequency spectrum associated to a time series directly
    using the discrete fourier transform, which may become slow for many
    frequencies and time points.

    Parameters
    ----------
    time_series: array_like
        1D array of time-dependent data.
    dt : float, optional
        Step in time over which the time series is recorded.
    freqs : array_like
        Array of frequencies to sample the spectrum at.

    Returns
    -------
    spectrum : array_like
        Array of same size as ``freqs`` giving the complex-valued spectrum.
    """

    frs = np.array(freqs)
    tdep = np.array(time_series)
    tmesh = np.arange(tdep.size) * dt
    spectrum = np.sum(
        tdep[:, np.newaxis]
        * np.exp(2j * np.pi * frs[np.newaxis, :] * tmesh[:, np.newaxis]),
        0,
    ).ravel()

    return dt / np.sqrt(2 * np.pi) * spectrum


def x_to_center(Ex):
    """Interpolate Ex positions to the center of a Yee lattice"""
    return (
        Ex
        + np.roll(Ex, -1, 1)
        + np.roll(Ex, -1, 2)
        + np.roll(np.roll(Ex, -1, 1), -1, 2)
    ) / 4


def y_to_center(Ey):
    """Interpolate Ey positions to the center of a Yee lattice"""
    return (
        Ey
        + np.roll(Ey, -1, 0)
        + np.roll(Ey, -1, 2)
        + np.roll(np.roll(Ey, -1, 0), -1, 2)
    ) / 4


def z_to_center(Ez):
    """Interpolate Ez positions to the center of a Yee lattice"""
    return (
        Ez
        + np.roll(Ez, -1, 0)
        + np.roll(Ez, -1, 1)
        + np.roll(np.roll(Ez, -1, 0), -1, 1)
    ) / 4


def E_to_center(Ex, Ey, Ez):
    return (x_to_center(Ex), y_to_center(Ey), z_to_center(Ez))


def eps_to_center(eps_xx, eps_yy, eps_zz):
    """Interpolate eps_r to the center of the Yee lattice. Used for plotting."""
    # # Simple averaging of one x, y, z values per cell.
    # return (eps_xx + eps_yy + eps_zz)/3

    # Average all 4 eps_xx, 4 eps_yy, and 4 eps_zz values around the
    # cell center, similar to the monitor field recording.
    return (
        x_to_center(eps_xx) + y_to_center(eps_yy) + z_to_center(eps_zz)
    ) / 3


def cs2span(center, size):
    """Get shape (3, 2) span from center and size, each (3, ) arrays."""
    return np.vstack(
        (
            np.array(center) - np.array(size) / 2,
            np.array(center) + np.array(size) / 2,
        )
    ).T


def span2cs(span):
    """Get center, size: each arrays of shape (3,), from a shape (3, 2) array
    span.
    """
    center = np.array([(span[d, 1] + span[d, 0]) / 2 for d in range(3)])
    size = np.array([(span[d, 1] - span[d, 0]) for d in range(3)])
    return center, size


def check_3D_lists(**kwargs):
    """ Verify that input arguments are lists with three elements """
    for key, val in kwargs.items():
        try:
            if not isinstance(val, list) and not isinstance(val, tuple):
                raise ValueError
            if len(val) != 3:
                raise ValueError
            for v in val:
                if type(v) in [list, tuple, np.ndarray]:
                    raise ValueError
        except:
            raise ValueError(
                "'%s' must be array-like with three elements." % key
            )


def axes_handed(axes):
    """Return +1 if the axes indexes in the list ``axes`` form a right-handed
    coordinate system, and -1 if they form a left-handed one.
    """

    if listify(axes) in [[0, 1, 2], [1, 2, 0], [2, 0, 1]]:
        return 1
    elif listify(axes) in [[0, 2, 1], [1, 0, 2], [2, 1, 0]]:
        return -1
    else:
        raise ValueError("Unrecognized list of axes indexes.")


def poynting_flux(E, H):
    """Compute the time-averaged Poynting vector that gives the energy
    flow per unit area per unit time at every point. ``E`` and ``H`` are
    assumed to be arrays of the same shape, as returned by frequency
    monitors. The first dimension is the field polarization (x, y, z), and
    must have size 3.
    """

    if E.shape != H.shape:
        raise ValueError("E and H must have the same dimension.")
    if E.shape[0] != 3:
        raise ValueError("First dimension of fields must have size 3.")

    return 1 / 2 * np.real(np.cross(E, np.conj(H), axis=0))
