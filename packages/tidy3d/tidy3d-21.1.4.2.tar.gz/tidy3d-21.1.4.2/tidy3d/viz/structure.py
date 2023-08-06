import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from ..constants import xyz_dict, xyz_list, fp_eps, pec_eps, pmc_eps
from ..utils import log_and_raise


def _eps_cmap(eps_r, alpha=1, cmap=None, clim=None):

    if cmap == None:
        cmap = "Greys"
    cm = mpl.cm.get_cmap(cmap, 256)

    # New map based on cmap with 256 colors and alpha as specified
    newmap = cm(np.linspace(0, 1, 256))
    newmap[:, 3] = alpha

    if clim is None:
        epsmax = np.amax(eps_r)
        # Get the minimum value that's larger than the PEC value
        cmin = np.amin(eps_r[eps_r > pec_eps], initial=epsmax)
        cl = [cmin, epsmax + fp_eps]
    else:
        cl = list(clim)

    # Make sure we're larger than the PEC value
    # PMC and PEC colors are appended below
    cl[0] = max(cl[0], pec_eps)

    # Make eps = 1 completely transparent if it is at the lower bound
    if np.abs(cl[0] - 1) < fp_eps:
        newmap[0, 3] = 0

    bounds = np.hstack((-4e6, -2e6, np.linspace(cl[0], cl[1], 256)))
    eps_cmap = np.vstack(([0, 0, 1, 1], [1, 0, 0, 1], newmap))
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=258)

    return mpl.colors.ListedColormap(eps_cmap), norm, bounds


def _get_inside(objects, mesh):
    """Get a mask defining points inside a list of objects.

    Parameters
    ----------
    objects : list of Structure, Source, or Monitor objects
    mesh : tuple of 3 1D arrays, or None

    Returns
    -------
    mask : np.ndarray
        Array of size (mesh[0].size, mesh[1].size, mesh[2].size) where each
        element is one if inside any of the objects, and zero otherwise.
    """

    Nx, Ny, Nz = [mesh[i].size for i in range(3)]

    mask = np.zeros((Nx, Ny, Nz))
    for obj in objects:
        mtmp = obj._inside(mesh)
        mask[mtmp > 0] = 1
        # print(obj, np.sum(mask))

    return mask


def _plot_eps(
    eps_r,
    cmap=None,
    clim=None,
    ax=None,
    extent=None,
    cbar=False,
    cax=None,
    alpha=1,
):

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    cmplot, norm, bounds = _eps_cmap(eps_r, alpha, cmap, clim)

    im = ax.imshow(
        eps_r,
        interpolation="none",
        norm=norm,
        cmap=cmplot,
        origin="lower",
        extent=extent,
    )

    if cbar:
        if cax is not None:
            plt.colorbar(im, ax=ax, cax=cax, boundaries=bounds[3:])
        else:
            plt.colorbar(im, ax=ax, boundaries=bounds[3:])

    return im


def viz_eps_2D(
    self,
    normal="x",
    position=0.0,
    ax=None,
    cbar=False,
    clim=None,
    source_alpha=0.3,
    monitor_alpha=0.3,
    pml_alpha=0.2,
):
    """Plot the relative permittivity distribution of a 2D cross-section of
    the simulation.

    Parameters
    ----------
    normal : {'x', 'y', 'z'}
        Axis normal to the cross-section plane.
    position : float, optional
        Position offset along the normal axis.
    ax : Matplotlib axis object, optional
        If ``None``, a new figure is created.
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    source_alpha : float, optional
        If larger than zero, overlay all sources in the simulation,
        with opacity defined by ``source_alpha``.
    monitor_alpha : float, optional
        If larger than zero, overlay all monitors in the simulation,
        with opacity defined by ``monitor_alpha``.
    pml_alpha : float, optional
        If larger than zero, overlay the PML boundaries of the simulation,
        with opacity defined by ``pml_alpha``.

    Returns
    -------
    Matplotlib image object

    Note
    ----
    The plotting is discretized at the center positions of the Yee grid and
    is for illustrative purposes only. In the FDTD computation, the exact
    Yee grid is used and the permittivity values depend on the field
    polarization.
    """

    grid = self.grid

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    # Get normal and cross-section axes indexes
    norm = xyz_dict[normal]
    cross = [0, 1, 2]
    cross.pop(norm)

    # Get centered mesh for permittivity discretization
    mesh = [[], [], []]
    ind = np.nonzero(position < grid.mesh[norm])[0]
    if ind.size == 0:
        log_and_raise(
            "Plane position outside of simulation domain.", RuntimeError
        )
    else:
        ind = ind[0]
    mesh[norm] = np.array([grid.mesh[norm][ind]])
    mesh[cross[0]] = grid.mesh[cross[0]]
    mesh[cross[1]] = grid.mesh[cross[1]]

    eps_r = np.squeeze(self._get_eps(mesh))

    # Get mesh for source and monitor discretization
    if ind > 0:
        mesh_sp = [[], [], []]
        mesh_sp[norm] = grid.mesh[norm][ind - 1 : ind + 1]
        mesh_sp[cross[0]] = mesh[cross[0]]
        mesh_sp[cross[1]] = mesh[cross[1]]

    # Set axes xlim and ylim if not provided
    sim_xlim = (grid.mesh[cross[0]][0], grid.mesh[cross[0]][-1])
    sim_ylim = (grid.mesh[cross[1]][0], grid.mesh[cross[1]][-1])

    # Define axes extent, labels and title
    extent = list(sim_xlim) + list(sim_ylim)
    x_lab = xyz_list[cross[0]]
    y_lab = xyz_list[cross[1]]
    ax_tit = x_lab + y_lab
    ax_tit += "-plane at " + xyz_list[norm] + "=%1.2eum" % position

    # Transparent color
    transp = (0, 0, 0, 0)
    # Colors for monitors, sources, pml, and border
    mnt_color = (236 / 255, 203 / 255, 32 / 255)
    src_color = (78 / 255, 145 / 255, 78 / 255)
    pml_color = (229 / 255, 127 / 255, 25 / 255)
    pbc_color = (75 / 255, 0, 130 / 255)

    # # Set axis background color
    # ax.set_facecolor(pml_color)

    # Plot and set axes properties
    im = _plot_eps(eps_r.T, clim=clim, ax=ax, extent=extent, cbar=cbar)
    ax.set_xlabel(x_lab + " (um)")
    ax.set_ylabel(y_lab + " (um)")
    ax.set_title(ax_tit)

    # Plot simulation domain borders depending on boundaries
    npml = self.Npml[[cross[0], cross[1]], :]
    # In order of bottom, right, top, left
    border_pmls = [npml[1, 0], npml[0, 1], npml[1, 1], npml[0, 0]]
    x_border = [extent[0], extent[1], extent[1], extent[0], extent[0]]
    y_border = [extent[2], extent[2], extent[3], extent[3], extent[2]]
    for ib, bpml in enumerate(border_pmls):
        if bpml > 0:
            border_color = pml_color
        else:
            border_color = pbc_color
        ax.plot(
            [x_border[ib], x_border[ib + 1]],
            [y_border[ib], y_border[ib + 1]],
            color=border_color,
        )

    def squeeze_mask(mask, axis):
        inds = [slice(None), slice(None), slice(None)]
        inds[axis] = 1
        return np.squeeze(mask[tuple(inds)])

    if monitor_alpha > 0:
        mnt_alpha = min(monitor_alpha, 1)
        mnt_c = list(mnt_color)
        mnt_c.append(mnt_alpha)
        mnt_mask = squeeze_mask(_get_inside(self.monitors, mesh=mesh_sp), norm)
        mnt_cmap = mpl.colors.ListedColormap(np.array([transp, mnt_c]))
        ax.imshow(
            mnt_mask.T,
            clim=(0, 1),
            cmap=mnt_cmap,
            origin="lower",
            extent=extent,
        )

    if source_alpha > 0:
        src_alpha = min(source_alpha, 1)
        src_c = list(src_color)
        src_c.append(src_alpha)
        src_mask = squeeze_mask(_get_inside(self.sources, mesh=mesh_sp), norm)
        src_cmap = mpl.colors.ListedColormap(np.array([transp, src_c]))
        ax.imshow(
            src_mask.T,
            clim=(0, 1),
            cmap=src_cmap,
            origin="lower",
            extent=extent,
        )

    if pml_alpha > 0:
        pml_alpha = min(pml_alpha, 1)
        pml_c = list(pml_color)
        pml_c.append(pml_alpha)
        pml_mask = np.squeeze(
            np.zeros((mesh[0].size, mesh[1].size, mesh[2].size))
        )
        N1, N2 = pml_mask.shape
        pml_mask[: npml[0, 0], :] = 1
        pml_mask[N1 - npml[0, 1] :, :] = 1
        pml_mask[:, : npml[1, 0]] = 1
        pml_mask[:, N2 - npml[1, 1] :] = 1
        pml_cmap = mpl.colors.ListedColormap(np.array([transp, pml_c]))
        ax.imshow(
            pml_mask.T,
            clim=(0, 1),
            cmap=pml_cmap,
            origin="lower",
            extent=extent,
        )

    return im


def _structure_png(self, folder_path, aspect_ratio=None):
    """
    Export png images of 2D cross-sections of the simulation at the domain
    center in x, y, and z.

    Parameters
    ----------
    folder_path : string
        Path in which the images will be exported.
    aspect_ratio : float or None
        Fix the width/height image ratio. If ``None``, the smallest aspect
        ratio of the three plots is used in all.
    """

    figs = [
        plt.figure(0, constrained_layout=True),
        plt.figure(1, constrained_layout=True),
        plt.figure(2, constrained_layout=True),
    ]
    ims = []
    clims = np.empty((3, 2))

    if not aspect_ratio:
        # Take the smallest aspect ratio
        sim_ars = [
            self.size[1] / self.size[2],
            self.size[0] / self.size[2],
            self.size[0] / self.size[1],
        ]
        aspect_ratio = np.min(sim_ars)

    for norm_ind, normal in enumerate(["x", "y", "z"]):
        cinds = [0, 1, 2]
        cinds.pop(norm_ind)
        ax = figs[norm_ind].add_subplot(111)
        im = self.viz_eps_2D(
                normal=normal, position=self.center[norm_ind], ax=ax
            )
        ims.append(im)
        eps_r = np.array(im.get_array())
        epsmax = np.amax(eps_r)
        clims[norm_ind, 0] = np.amin(eps_r[eps_r > pec_eps], initial=epsmax)
        clims[norm_ind, 1] = epsmax
        sim_width = self.size[cinds[0]]
        sim_height = self.size[cinds[1]]
        sim_aspect = sim_width / sim_height
        if sim_aspect > aspect_ratio:
            new_height = sim_width / aspect_ratio
            ax.set_ylim(-new_height / 2, new_height / 2)
        elif sim_aspect < aspect_ratio:
            new_width = sim_height * aspect_ratio
            ax.set_xlim(-new_width / 2, new_width / 2)

    # Set the same clims in all plots
    clim_glob = [np.amin(clims[:, 0]), np.amax(clims[:, 1])]
    # Get a new color norm based on the global clims. eps_r is irrelevant.
    _, norm, _ = _eps_cmap(eps_r, clim=clim_glob)

    # Set new clims and save figures
    for norm_ind, normal in enumerate(["x", "y", "z"]):
        fname = "simulation_%scent.png" % normal
        plt.figure(norm_ind)
        ims[norm_ind].set_norm(norm)
        plt.savefig(folder_path + fname, dpi=150)
        plt.close(figs[norm_ind])
