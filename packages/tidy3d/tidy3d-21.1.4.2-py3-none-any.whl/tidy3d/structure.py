import numpy as np
from matplotlib.path import Path

# gdspy is only needed for the GdsSlab structure
try:
    import gdspy
except ImportError:
    pass

from .material import Medium, PEC, PMC
from .utils import inside_box, cs2span, log_and_raise
from .constants import fp_eps, int_, float_, xyz_dict

class Structure(object):
    """
    Base class for regions defined by geometric shapes in a simulation domain.
    """

    def __init__(self, material, name=None):
        """Base class for structures. Available subclasses:

        - :class:`.Box`
        - :class:`.Sphere`
        - :class:`.Cylinder`
        - :class:`.PolySlab`
        - :class:`.GdsSlab`
        """
        self.material = material
        self.name = str(name) if name else None

        # if bounds are not set (default), self.bounds is None,
        # otherwise it's a (3,2) array specifying bounding box min and max
        # values along each dimension
        self.bounds = None

    def _inside(self, mesh, include_edges=True):
        """Elementwise indicator function for the structure.
        
        Parameters
        ----------
        mesh : tuple
            3-tuple defining the xgrid, ygrid and zgrid.
        include_edges : bool
            Whether a point sitting exactly on a mesh point (within numerical 
            precision) should be returned as inside (True) or outside (False) 
            the structure.
        
        Note
        ----
        ``include_edges`` will in the future be replaced by actual dielectric 
        smoothening.
        
        Returns
        -------
        mask : np.ndarray
            A 3D array of shape (mesh[0].size, mesh[1].size, mesh[2].size) 
            that is 1 inside the structure and 0 outside, and a continuous 
            value between 0 and 1 at interfaces if smoothen==True.
        """

        raise NotImplementedError(
            "inside() needs to be implemented by Structure subclasses"
        )

    def _get_eps_val(self, pec_val, pmc_val):
        """ get epsilon value for structure """

        if isinstance(self.material, Medium):
            return self.material.eps
        elif isinstance(self.material, PEC):
            return pec_val
        elif isinstance(self.material, PMC):
            return pmc_val

    def _set_val_direct(self, mesh, val_arr, val, edges='average'):
        """ Set value ``val`` to all elements of array ``val_arr`` defined 
        over sptial ``mesh``, which are inside the current Structure."""

        if edges=='in' or edges=='average':
            mask = self._inside(mesh, include_edges=True)
        if edges=='average':
            mask += self._inside(mesh, include_edges=False)
            mask = mask.astype(float_)/2
        if edges=='out':
            mask = self._inside(mesh, include_edges=False)
        mask_bool = mask > 0
        mask_in = mask[mask_bool]
        val_arr[mask_bool] = (1 - mask_in)*val_arr[mask_bool] + val*mask_in

    def _set_val(self, mesh, val_arr, val, edges='average'):
        """ Set value ``val`` to all elements of array ``val_arr`` defined 
        over sptial ``mesh``, which are inside the current Structure. This 
        uses ``_set_val_direct`` only after applying the bounding box, if 
        known."""

        # no bounds defined, do the most naive thing
        if self.bounds is None:
            self._set_val_direct(mesh, val_arr, val, edges=edges)
            return

        bound_inds = self._get_bounding_indices(mesh)

        # mesh is completely outside bounds, skip this structure
        if bound_inds is None:
            return

        sub_mesh, sub_arr = self._get_sub_problem(mesh, val_arr, bound_inds)
        self._set_val_direct(sub_mesh, sub_arr, val, edges=edges)

    def _get_bounding_indices(self, mesh):
        """ uses self.bounds to compute min and max bounding indices in mesh
        
        Parameters
        ----------
        mesh : tuple
            3-tuple defining the xgrid, ygrid and zgrid.
        
        Returns
        -------
        bound_inds : np.ndarray
            A 3D array of shape (3, 2) 
            bound_inds[d, :] gives the indices into `mesh` that are closest to 
            min and max values in dimension `d`. 
            for safety, min is rounded down to the nearest index and 
            max is rounded up to the nearest index
        """

        # if bounds are not defined for this structure, just return None
        if self.bounds is None:
            return None

        # unpack bounds and mesh
        xmin, xmax = self.bounds[0]
        ymin, ymax = self.bounds[1]
        zmin, zmax = self.bounds[2]
        xs, ys, zs = mesh

        # compute indices within the bounding region in each dimension
        ixs_min = np.where(xs > xmin)[0]
        ixs_max = np.where(xs < xmax)[0]
        iys_min = np.where(ys > ymin)[0]
        iys_max = np.where(ys < ymax)[0]
        izs_min = np.where(zs > zmin)[0]
        izs_max = np.where(zs < zmax)[0]

        # check if any conditions gave no matches (bounds outside mesh, skip)
        indices = (ixs_min, ixs_max, iys_min, iys_max, izs_min, izs_max)
        if any([len(i) == 0 for i in indices]):
            return None

        # get the min and max inside bounding indices in each dimension
        ix_min, ix_max = np.min(ixs_min), np.max(ixs_max) + 1
        iy_min, iy_max = np.min(iys_min), np.max(iys_max) + 1
        iz_min, iz_max = np.min(izs_min), np.max(izs_max) + 1

        # construct bounding indices array for constructing sub mesh & sub arr
        return np.array([[ix_min, ix_max], [iy_min, iy_max], [iz_min, iz_max]])

    @staticmethod
    def _get_sub_problem(mesh, arr, bound_inds):
        """ returns a view to sub mesh and sub epsilon array using `bound_inds`
        """

        # unpack bound_inds
        bounds_ix, bounds_iy, bounds_iz = bound_inds
        ix_min, ix_max = bounds_ix
        iy_min, iy_max = bounds_iy
        iz_min, iz_max = bounds_iz

        # get sub mesh
        xs, ys, zs = mesh
        sub_xs = xs[ix_min:ix_max]
        sub_ys = ys[iy_min:iy_max]
        sub_zs = zs[iz_min:iz_max]
        sub_mesh = sub_xs, sub_ys, sub_zs

        # get view into sub epsilon array
        sub_eps = arr[ix_min:ix_max, iy_min:iy_max, iz_min:iz_max]

        return sub_mesh, sub_eps


class Box(Structure):
    """ Box structure, i.e. a 3D rectangular axis-aligned prism.
    """

    def __init__(self, center, size, material, name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            (micron): x, y, and z position of the center of the Box.
        size : array_like
            (micron): size in x, y, and z.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)

        # set bounds
        mins = self.center - self.size / 2 / (1. - fp_eps)
        maxs = self.center + self.size / 2 / (1. - fp_eps)
        self.bounds = np.stack((mins, maxs), axis=1)  # (3, 2)

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Box region."""

        # note: there's a bug here if self.size is
        tmp_span = np.copy(self.span)
        if include_edges == True:
            tmp_span[:, 0] -= fp_eps*(tmp_span[:, 1] - tmp_span[:, 0])
            tmp_span[:, 1] += fp_eps*(tmp_span[:, 1] - tmp_span[:, 0])
        else:
            tmp_span[:, 0] += fp_eps*(tmp_span[:, 1] - tmp_span[:, 0])
            tmp_span[:, 1] -= fp_eps*(tmp_span[:, 1] - tmp_span[:, 0])

        return inside_box(tmp_span, mesh, include_zero_size=False)


class BoxAngled(Structure):
    """ Box structure, i.e. a 3D rectangular block at an angle in x-y plane
    """

    def __init__(self, center, size, angle, material, bounded=True, name=None):
        """ Box positioned at angle in x-y plane
        Parameters
        ----------
        center : array_like
            (micron): x, y, and z position of the center of the Box.
        size : array_like
            (micron): size in x, y, and z.
        angle: float
            (radians) angle to rotate box from x axis
        material : Material
            Material of the structure.
        bounded : bool
            If you want to use the bounded feature 
            (just for testing with and without)
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.center = np.array(center)
        self.size = np.array(size)
        self.angle = angle
        if bounded:
            xy_radius = np.max(self.size[:-1])
            z_size = self.size[-1]
            max_xy_size = 2 * xy_radius * np.sqrt(2)
            size = np.array([max_xy_size, max_xy_size, z_size])
            mins = self.center - size / 2 / (1. - fp_eps)
            maxs = self.center + size / 2 / (1. - fp_eps)
            self.bounds = np.stack((mins, maxs), axis=1)  # (3, 2)

    def _inside(self, mesh, include_edges=False):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Box region."""

        # expand mesh
        xx, yy, zz = np.meshgrid(*mesh, indexing="ij")

        # centered coordinates
        xxc = xx - self.center[0]
        yyc = yy - self.center[1]
        zzc = zz - self.center[2]

        # rotated coords
        xxp = xxc * np.cos(self.angle) - yyc * np.sin(self.angle)
        yyp = xxc * np.sin(self.angle) + yyc * np.cos(self.angle)

        # return 1 if rotated coordinates are inside of box
        inside_x = np.abs(xxp) < self.size[0] / 2
        inside_y = np.abs(yyp) < self.size[1] / 2
        inside_z = np.abs(zzc) < self.size[2] / 2

        return 1.0 * (inside_x * inside_y * inside_z)


class Sphere(Structure):
    """ Sphere structure.
    """

    def __init__(self, center, radius, material, name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            (micron): x, y, z position of the center of the sphere.
        radius : float
            (micron) Radius of the sphere.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.center = np.array(center, dtype=float_)
        self.radius = radius
        mins = self.center - 2 * self.radius / (2. - fp_eps)
        maxs = self.center + 2 * self.radius / (2. - fp_eps)
        self.bounds = np.stack((mins, maxs), axis=1)

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Sphere."""

        xc, yc, zc = self.center

        # this line is abstruse
        r = self.radius * (1 + (include_edges - 0.5) * 2 * fp_eps)

        # cleaned this up:
        #
        # return np.where((x - mesh[0][:, np.newaxis, np.newaxis])**2 +
        #             (y - mesh[1][np.newaxis, :, np.newaxis])**2 +
        #             (z - mesh[2][np.newaxis, np.newaxis, :])**2 < r**2, 1, 0)
        # becomes:

        xx, yy, zz = np.meshgrid(*mesh, indexing="ij")
        return 1.0 * ((xx - xc) ** 2 + (yy - yc) ** 2 + (zz - zc) ** 2 < r ** 2)


class Cylinder(Structure):
    """ Cylinder structure.
    """

    def __init__(self, center, axis, radius, height, material, name=None):
        """Construct.

        Parameters
        ----------
        center : array_like
            (micron): x, y, z position of the center of the sphere.
        axis : str
            ``'x'``, ``'y'``, or ``'z'``.
        radius : float
            (micron) Radius of the cylinder.
        height : float
            (micron) Height of the cylinder along its axis.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.center = np.array(center, dtype=float_)
        self.axis = axis
        self.radius = radius
        self.height = height

        # set bounds
        if axis == "x":
            sizes = np.array([height, 2 * radius, 2 * radius])
        elif axis == "y":
            sizes = np.array([2 * radius, height, 2 * radius])
        elif axis == "z":
            sizes = np.array([2 * radius, 2 * radius, height])
        else:
            # do this error checking elsewhere
            log_and_raise(
                f"Given axis {axis}, must be in ['x', 'y', 'z'].",
                ValueError
            )

        mins = self.center - sizes / 2 / (1. - fp_eps)
        maxs = self.center + sizes / 2 / (1. - fp_eps)
        self.bounds = np.stack((mins, maxs), axis=1)  # (3, 2)

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the Cylinder."""

        ax = xyz_dict[self.axis]
        d_cross = [0, 1, 2]
        d_cross.pop(ax)
        d_a = self.center[ax]
        d1, d2 = self.center[d_cross]
        r = self.radius * (1 + (include_edges - 0.5) * 2 * fp_eps)
        h = self.height * (1 + (include_edges - 0.5) * 2 * fp_eps)

        m = [
            mesh[0][:, np.newaxis, np.newaxis],
            mesh[1][np.newaxis, :, np.newaxis],
            mesh[2][np.newaxis, np.newaxis, :],
        ]
        m_a = m[ax]
        m1 = m[d_cross[0]]
        m2 = m[d_cross[1]]

        return np.where(((d1 - m1)**2 + (d2 - m2)**2 < r**2) *  
                            (np.abs(d_a - m_a) < h/2), 1, 0)


class PolySlab(Structure):
    """ A structure defined as polygon in x and y, and extruded in z.
    """

    def __init__(self, vertices, z_cent, z_size, material, name=None):
        """ Construct.

        Parameters
        ----------
        vertices : array_like
            (micron) Shape (N, 2) defining the polygon vertices in the xy-plane.
        z_cent : float
            (micron) Center of the polygonal slab in z.
        z_size : float
            (micron) Thickness of the slab in z.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.vertices = np.array(vertices, dtype=float_)
        self.z_cent = z_cent
        self.z_size = z_size

        x_min, y_min = np.min(vertices, axis=0)
        x_max, y_max = np.max(vertices, axis=0)
        z_min = z_cent - z_size / 2
        z_max = z_cent + z_size / 2

        mins = np.array([x_min, y_min, z_min])
        maxs = np.array([x_max, y_max, z_max])
        self.bounds = np.stack((mins, maxs), axis=1)  # (3, 2)

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the PolySlab."""

        z_size = self.z_size * (1 + (include_edges - 0.5) * 2 * fp_eps)

        path = Path(self.vertices)
        xm, ym = np.meshgrid(mesh[0], mesh[1])
        points = np.vstack((xm.ravel(), ym.ravel())).T
        mask2d = path.contains_points(points).reshape(xm.shape).T
        maskz = (mesh[2] >= self.z_cent - z_size / 2) * (
            mesh[2] <= self.z_cent + z_size / 2
        )

        return np.where(
            mask2d[:, :, np.newaxis] * maskz[np.newaxis, np.newaxis, :] > 0, 1, 0
        )


class GdsSlab(Structure):
    """ A structure defined through a GDS cell imported through ``gdspy``. 
    All polygons and paths included in the cell are assumed to lie in the 
    xy-plane, with the same center and size in z, and made of the same material.
    """

    def __init__(self, gds_cell, z_cent, z_size, material, name=None):
        """Construct.

        Parameters
        ----------
        gds_cell : gdspy.Cell
            A GDS Cell containing all 2D polygons and paths, in microns.
        z_cent : float
            (micron) Center of the slab(s) in z.
        z_size : float
            (micron) Thickness of the slab(s) in z.
        material : Material
            Material of the structure.
        name : str, optional
            Custom name of the structure.
        """
        super().__init__(material, name)
        self.gds_cell = gds_cell
        self.z_cent = z_cent
        self.z_size = z_size

        vertices = gds_cell.get_polygons()
        xy_min = np.min(vertices, axis=0)
        xy_max = np.max(vertices, axis=0)
        z_min = z_cent - z_size / 2 / (1. - fp_eps)
        z_max = z_cent + z_size / 2 / (1. - fp_eps)

        # GDSpy already does bounds (?)
        # mins = np.array([xy_min, xy_min, z_min])
        # maxs = np.array([xy_max, xy_max, z_max])
        # self.bounds = np.stack((mins, maxs), axis=1) # (3, 2)

    def _inside(self, mesh, include_edges=True):
        """Returns a mask defining whether the points in ``mesh`` are inside 
        the PolySlab."""

        z_size = self.z_size * (1 + (include_edges - 0.5) * 2 * fp_eps)

        xm, ym = np.meshgrid(mesh[0], mesh[1])
        points = np.vstack((xm.ravel(), ym.ravel())).T
        mask2d = (
            np.array(gdspy.inside(points, self.gds_cell.get_polygons()))
            .reshape(xm.shape)
            .T
        )
        maskz = (mesh[2] >= self.z_cent - z_size / 2) * (
            mesh[2] <= self.z_cent + z_size / 2
        )

        return np.where(
            mask2d[:, :, np.newaxis] * maskz[np.newaxis, np.newaxis, :] > 0, 1, 0
        )
