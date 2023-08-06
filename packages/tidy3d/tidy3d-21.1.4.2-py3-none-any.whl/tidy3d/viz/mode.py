import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from ..utils import listify, log_and_raise 
from ..monitor import ModeMonitor
from ..source import ModeSource
from .field import _plot_field_2D

def _mode_plane(sim, mode_plane, freq_ind=0, mode_inds=0,
                val='abs', cbar=False, eps_alpha=0.3, clim=None):

    minds = listify(mode_inds)
    grid_list = [(1, 2, 0, 'y', 'z'),
                (0, 2, 1, 'x', 'z'),
                (0, 1, 2, 'x', 'y')]

    (d1, d2, dn, x_lab, y_lab) = grid_list[mode_plane.norm_ind]
    N1, N2 = mode_plane.eps.shape

    if eps_alpha<=0:
        eps_r = None
    else:
        eps_r = mode_plane.eps

    mesh_c1 = mode_plane.mesh[0]
    mesh_c2 = mode_plane.mesh[1]
    extent = [mesh_c1[0], mesh_c1[-1], mesh_c2[0], mesh_c2[-1]]
    aspect = (extent[3]-extent[2])/(extent[1]-extent[0])

    fig, axs = plt.subplots(len(minds), 2, figsize=(8, 4*aspect*len(minds)),
                            constrained_layout=True)
    if len(minds)==1:
        axs = axs.reshape((1, 2))

    for iax, imode in enumerate(minds):
        (E, _) = mode_plane.modes[freq_ind][imode].fields_to_center()
        Ec1 = E[0, :, :]
        Ec2 = E[1, :, :]

        _clim = clim
        if clim is None:
            cmax = np.amax(np.abs(np.vstack((Ec1, Ec2))))
            if val=='abs':
                _clim = (0, cmax)
            else:
                _clim = (-cmax, cmax)

        subtitle = "f=%1.2eTHz, "%(mode_plane.freqs[freq_ind]*1e-12)
        subtitle += "n=%1.2f"%mode_plane.modes[freq_ind][imode].neff
        ax_title = "Mode %d, E%s"%(imode, x_lab) + "\n" + subtitle
        _plot_field_2D(Ec1, eps_r, extent, x_lab, y_lab, ax_title,
                        val=val, ax=axs[iax, 0], cbar=False, clim=_clim,
                        eps_alpha=eps_alpha)
        ax_title = "Mode %d, E%s"%(imode, y_lab) + "\n" + subtitle
        _plot_field_2D(Ec2, eps_r, extent, x_lab, y_lab, ax_title,
                        val=val, ax=axs[iax, 1], cbar=cbar, clim=_clim,
                        eps_alpha=eps_alpha)

    return fig

def viz_modes(self, mode_obj, mode_inds=0, freq_ind=0,
                val='abs', cbar=False, clim=None, eps_alpha=0.3):
    """Plot the field distribution of the 2D eigenmodes of 
    a :class:`.ModeSource` or a :class:`.ModeMonitor` object.
    
    Parameters
    ----------
    mode_obj : ModeSource or ModeMonitor
        An object on which :meth:`.Simulation.compute_modes` can be used.
    mode_inds : array_like, optional
        Mode indexes of the stored modes to be plotted.
    freq_ind : int, optional
        Frequency index of the stored modes to be plotted.
    val : {'re', 'im', 'abs'}, optional
        Plot the real part (default), or the imaginary or absolute value of 
        the field components.
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    eps_alpha : float, optional
        If larger than zero, overlay the underlying permittivity distribution, 
        with opacity defined by eps_alpha.

    Returns
    -------
    Matplotlib figure object

    Note
    ----
    If the modes have not been computed yet, or ``mode_inds`` exceeds the 
    largest mode index that is stored in ``mode_obj``, 
    :meth:`.Simulation.compute_modes` will be called.
    """

    if isinstance(mode_obj, ModeSource):
        mode_pl = self._source_ids[id(mode_obj)].mode_plane
    elif isinstance(mode_obj, ModeMonitor):
        mode_pl = self._monitor_ids[id(mode_obj)].mode_plane
    else:
        log_and_raise(
            "Input 0 should be an instance of ModeSource or ModePlane.",
            ValueError
        )

    nfreqs = len(mode_pl.modes)

    # Check if frequency index out of bounds
    if nfreqs < freq_ind:
        log_and_raise(
            f"Frequency index {freq_ind} our of bounds for "
            f"stored modes number of frequencies {nfreqs}.",
            ValueError
        )

    # Check if modes have not been computed yet, or if fewer than requested
    if len(mode_pl.modes[freq_ind]) <= np.amax(mode_inds):
        self.compute_modes(mode_obj, np.amax(mode_inds) + 1)

    fig = _mode_plane(self, mode_pl, freq_ind, mode_inds,
                val=val, cbar=cbar, clim=clim, eps_alpha=eps_alpha)

    return fig