import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from ..constants import xyz_dict, xyz_list
from ..utils import listify, log_and_raise
from ..monitor import TimeMonitor

from .structure import _plot_eps

def _monitor_slice(sim, mnt_data, sind=None, normal=None, normal_ind=0,
                    field='E', val='re', comp='z', eps_alpha=0):

    # Import in order to distinguish in the axis title
    from ..monitor import TimeMonitor, FreqMonitor

    if normal is None:
        dmin = np.argmin(mnt_data.inds_end - mnt_data.inds_beg)
        normal = ['x', 'y', 'z'][dmin]

    inds = {'x': 0, 'y': 1, 'z': 2}
    comp_ind = inds[comp]
    if field.lower()=='e':
        ftmp = mnt_data.E[:, :, :, :, sind]
        ftit = 'E'
    elif field.lower()=='h':
        ftmp = mnt_data.H[:, :, :, :, sind]
        ftit = 'H'
    elif field.lower()=='s':
        ftmp = mnt_data.S[:, :, :, :, sind]
        ftit = 'S'

    if isinstance(mnt_data.monitor, TimeMonitor):
        tit_string = 't='+"%1.2e"%(mnt_data.tmesh[sind]*1e12)+'fs'
    elif isinstance(mnt_data.monitor, FreqMonitor):
        tit_string = 'f='+"%1.2e"%(mnt_data.freqs[sind]*1e-12)+'THz'

    if val=='int':
        fvals = ftmp[0, :, :, :]**2 + ftmp[1, :, :, :]**2 + ftmp[2, :, :, :]**2
        ax_tit = "||%s||^2"%ftit
    else:
        fvals = ftmp[comp_ind, :, :, :]
        ax_tit = val + "(" + ftit +  comp + ")"

    mbeg = mnt_data.inds_beg
    mend = mnt_data.inds_end

    if normal=='x':
        fvals = fvals[normal_ind, :, :]
        norm_pos = sim.grid.mesh[0][mbeg[0]+normal_ind]
        mesh = (np.array([norm_pos]), sim.grid.mesh[1][mbeg[1]:mend[1]],
                    sim.grid.mesh[2][mbeg[2]:mend[2]])
    elif normal=='y':
        fvals = fvals[:, normal_ind, :]
        norm_pos = sim.grid.mesh[1][mbeg[1]+normal_ind]
        mesh = (sim.grid.mesh[0][mbeg[0]:mend[0]], np.array([norm_pos]),
                    sim.grid.mesh[2][mbeg[2]:mend[2]])
    elif normal=='z':
        fvals = fvals[:, :, normal_ind]
        norm_pos = sim.grid.mesh[2][mbeg[2]+normal_ind]
        mesh = (sim.grid.mesh[0][mbeg[0]:mend[0]],
                    sim.grid.mesh[1][mbeg[1]:mend[1]], np.array([norm_pos]))

    if eps_alpha<=0:
        eps_r = None
    else:
        eps_r = np.squeeze(sim._get_eps(mesh))
        
    grid_dict = {
            'x': (1, 2, 0, 'y', 'z'),
            'y': (0, 2, 1, 'x', 'z'),
            'z': (0, 1, 2, 'x', 'y'),
            }

    (d1, d2, dn, x_lab, y_lab) = grid_dict[normal]
    grid1 = sim.grid.mesh[d1][mbeg[d1]:mend[d1]]
    grid2 = sim.grid.mesh[d2][mbeg[d2]:mend[d2]]
    extent = [grid1[0], grid1[-1], grid2[0], grid2[-1]]

    ax_tit += ', ' + tit_string
    ax_title = 'Monitor ' + mnt_data.name + ', ' + normal + '=' + \
                '%1.2eum\n'%norm_pos + ax_tit

    return (fvals, eps_r, extent, x_lab, y_lab, ax_title)

def _plot_field_2D(fvals, eps_r, extent, x_lab, y_lab, ax_title,
                    val, ax, cbar, clim, eps_alpha):

    cmap = "RdBu"
    cmap_eps = "Greys"
    if val=='re':
        fvals = np.real(fvals)
    elif val=='im':
        fvals = np.imag(fvals)
    else:
        cmap = "magma"
        cmap_eps = "Greys_r"
        fvals = np.abs(fvals)

    fmax = np.amax(np.abs(fvals))
    if clim is None:
        if cmap=="RdBu":
            clim = (-fmax, fmax)
        else:
            clim = (0, fmax)

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    im = ax.imshow(fvals.T, extent=extent, cmap=cmap, clim=clim, origin='lower')
    if eps_r is not None:
        ealph = min(eps_alpha, 1)
        if (np.amax(eps_r) - np.amin(eps_r) > 1e-10):
            _plot_eps(eps_r.T, cmap=cmap_eps, clim=None, ax=ax, extent=extent,
                        cbar=False, alpha=eps_alpha)

    if cbar==True:
        plt.colorbar(im, ax=ax, shrink=0.8)

    ax.set_xlabel(x_lab + " (um)")
    ax.set_ylabel(y_lab + " (um)")
    ax.set_title(ax_title)

    return im

def _check_monitor(mnt_data, field):
    if field.lower()=='e':
        if mnt_data.E.size==0:
            log_and_raise(
                "Monitor has no stored E-field values.",
                RuntimeError
            )
    elif field.lower()=='h':
        if mnt_data.H.size==0:
            log_and_raise(
                "Monitor has no stored H-field values.",
                RuntimeError
            )
    elif field.lower()=='s':
        if mnt_data.S.size==0:
            log_and_raise(
                "Monitor has no stored S-field values. Run the simulation and "
                "use Simulation.poynting(Monitor) to compute S.",
                RuntimeError
            )     
    else:
        log_and_raise("'field' can be 'E' or 'H'.", ValueError)

def viz_field_2D(self, monitor, sample_ind=0, normal=None, normal_ind=0,
                    field='E', val='re', comp='z', ax=None, cbar=False,
                    clim=None, eps_alpha=0.3):
    """Plot a 2D cross-section of a field stored in a :class:`.Monitor`.
    
    Parameters
    ----------
    monitor : Monitor
        The monitor to be queried.
    sample_ind : int, optional
        Index of the frequency in a :class:`.FreqMonitor` or the time step in 
        a :class:`.TimeMonitor`.
    normal : None, optional
        Axis normal to the 2D plane of plotting. If ``None``, the shortest 
        dimension is taken as the normal.
    normal_ind : int, optional
        Spatial index along the normal dimension, for 3D monitors.
    field : {'E', 'H', 'S'}, optional
        Which field to plot.
    val : {'re', 'im', 'abs', 'int'}, optional
        Plot the real part (default), or the imaginary part, or the 
        absolute value of a field component, or the total field intensity. 
    comp : {'x', 'y', 'z'}, optional
        Component of the field to plot. If ``val`` is ``'int'``, this 
        parameter has no effect.
    ax : Matplotlib axis object, optional
        If None, a new figure is created. 
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    eps_alpha : float, optional
        If larger than zero, overlay the underlying permittivity 
        distribution, with opacity defined by ``eps_alpha``.
    
    Returns
    -------
    Matplotlib image object
    """

    mnt_data = self._monitor_ids[id(monitor)]
    _check_monitor(mnt_data, field)

    (fvals, eps_r, extent, x_lab, y_lab, ax_title) = _monitor_slice(
                                    self, mnt_data, sample_ind, normal,
                                    normal_ind, field, val, comp, eps_alpha)

    im = _plot_field_2D(fvals, eps_r, extent, x_lab, y_lab, ax_title,
                        val, ax, cbar, clim, eps_alpha)

    return im

def _fmonitors_png(self, folder_path, val='int', comp='z'):
    """
    Export png images of 2D cross-sections for all frequency monitors in a 
    given simulation. For 3D monitors, all 2D slices along the shortest 
    dimension are exported. 
    
    Parameters
    ----------
    folder_path : string
        Path in which the images will be exported.
    val : str, optional
        ``val`` supplied to :meth:`.viz_field_2D`.
    comp : str, optional
        ``comp`` suplied to :meth:`.viz_field_2D`.
    """

    fig = plt.figure(constrained_layout=True)

    for (ip, monitor) in enumerate(self.monitors):

        # Only export frequency monitors
        if isinstance(monitor, TimeMonitor):
            continue 

        mnt_data = self._monitor_ids[id(monitor)]
        mdims = mnt_data.inds_end - mnt_data.inds_beg
        min_dir = np.argmin(mdims)
        normal = xyz_list[min_dir]

        for normal_ind in range(mdims[min_dir]):
            for (find, _) in enumerate(mnt_data.freqs):
                try:
                    ax = fig.add_subplot(111)
                    self.viz_field_2D(monitor, sample_ind=find, normal=normal,
                                normal_ind=normal_ind, val=val, comp=comp,
                                ax=ax, cbar=True)
                    fname = mnt_data.name
                    fname += "_find%d_nind%d.png"%(find, normal_ind)
                    plt.savefig(folder_path+fname)
                    plt.clf()
                except:
                    print("Could not export image for monitor index %d"%ip +
                          ", normal index %d, frequency index %d."%(
                            normal_ind, find))

    plt.close(fig)