import numpy as np

from .misc import listify
from .log import log_and_raise

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
            log_and_raise(
                "Incorrect object span (max value smaller than " "min value).",
                ValueError
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


def axes_handed(axes):
    """Return +1 if the axes indexes in the list ``axes`` form a right-handed
    coordinate system, and -1 if they form a left-handed one.
    """

    if listify(axes) in [[0, 1, 2], [1, 2, 0], [2, 0, 1]]:
        return 1
    elif listify(axes) in [[0, 2, 1], [1, 0, 2], [2, 1, 0]]:
        return -1
    else:
        log_and_raise("Unrecognized list of axes indexes.", ValueError)
