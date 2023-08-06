import numpy as np
import logging

from ..constants import int_, float_, complex_, fp_eps, xyz_dict, xyz_list
from ..utils.em import poynting_flux
from ..utils import log_and_raise
from ..mode import dot_product

from .Monitor import ModeMonitor

def _compute_modes_monitor(self, mode_object, Nmodes):
    """Compute the eigenmodes of the 2D cross-section of a ModeMonitor object.
    """   

    mnt_data = self._monitor_ids[id(mode_object)]
    mnt_data.mode_plane.compute_modes(Nmodes, mnt_data.freqs)

def data(self, monitor):
    """Return a dictionary with all the stored data in a :class:`.Monitor`.
    
    Parameters
    ----------
    monitor : Monitor
        The queried monitor.
    
    Returns
    -------
    dict
        Dictonary with all the set data fields in the monitor. For example, in 
        a frequency monitor, after a simulation run, ``dict['E']`` and 
        ``dict['H']`` are 5D arrays of shape ``(3, Nx, Ny, Nz, Nf)`` The first 
        index is the vector component of the field, while the next four 
        dimensions index the x, y, z, position index and the frequency index 
        at which the data was stored.
    """
    mnt_data = self._monitor_ids[id(monitor)]

    data_dict = {
                'E': mnt_data.E,
                'H': mnt_data.H,
                'S': mnt_data.S,
                'xmesh': mnt_data.xmesh,
                'ymesh': mnt_data.ymesh,
                'zmesh': mnt_data.zmesh,
                'tmesh': mnt_data.tmesh,
                'freqs': mnt_data.freqs,
                }

    return_dict = {}

    for key, val in data_dict.items():
        if val.size > 0:
            return_dict[key] = val

    return return_dict

def poynting(self, monitor):
    """Compute the Poynting vector at every point recorded by a 
    :class:`.Monitor`. Returns the instantaneous power flux per unit area at 
    every time for a :class:`.TimeMonitor`, and the time-averaged power flux 
    per unit area at every frequency for a :class:`.FreqMonitor`.
     
    Returns
    -------
    np.ndarray
        (Watt/micron\ :sup:`2`) The Poynting vector, i.e. the directed power 
        flux per unit area, at every sampling point of the monitor. Same shape 
        as the ``E`` and ``H`` fields stored in the monitor.
    """

    mnt_data = self._monitor_ids[id(monitor)]

    if mnt_data.E.size==0:
        log_and_raise(
            "No electric field stored in the monitor.",
            ValueError
        )
    if mnt_data.H.size==0:
        log_and_raise(
            "No magnetic field stored in the monitor.",
            ValueError
        )

    mnt_data.S = poynting_flux(mnt_data.E, mnt_data.H)
    return mnt_data.S

def flux(self, monitor, normal=None):
    """Compute the area-integrated Poynting flux in a given direction. 
    This is the total power flowing through a plane orthogonal to the 
    ``normal`` direction. If the monitor is larger than one in that 
    direction, the flux at every pixel is returned. Returns the instantaneous 
    power flux at every time for a :class:`.TimeMonitor`, and the 
    time-averaged power flux at every frequency for a :class:`.FreqMonitor`.
    
    Parameters
    ----------
    normal : {'x', 'y', 'z'}, or None
        If ``None``, normal is set to the first dimension along which the 
        Monitor spans a single pixel.
    
    Returns
    -------
    np.ndarray
        (Watt) The Poynting flux, an array of shape ``(Nsample, Np)``, where 
        ``Np`` are the number of points in the monitor volume along the 
        normal direction, while ``Nsample`` is the number of time steps 
        or frequencies in the monitor.
    """

    mnt_data = self._monitor_ids[id(monitor)]

    if normal is None:
        dmin = np.argmin(mnt_data.inds_end - mnt_data.inds_beg)
        normal = xyz_list[dmin]
    try:
        norm_ind = xyz_dict[normal]
    except:
        log_and_raise("'normal' must be one of 'x', 'y', or 'z'.", ValueError)

    cross_inds = [0, 1, 2]
    cross_inds.pop(norm_ind)

    if mnt_data.S.size==0:
        self.poynting(monitor)

    # Compute numerical integral.
    fl = np.prod(mnt_data.mesh_step[cross_inds]) * \
                np.sum(mnt_data.S[norm_ind, :, :, :, :],
                    axis=(cross_inds[0], cross_inds[1]))

    # Transpose so that time/frequency index comes first
    return fl.T

def decompose(self, mode_monitor, Nmodes=None):
    """Compute the decomposition of the fields recorded in a 
    :class:`.ModeMonitor` into the eigenmodes in the monitor plane.  
    
    Parameters
    ----------
    Nmodes : int or None, optional
        Compute the decmposition into the first ``Nmodes`` of the monitor. 
        If ``None``, the modes stored from the last call of 
        :meth:`.compute_modes` will be used.
    
    Returns
    -------
    np.ndarray
        A tuple of two arrays giving the overlap coefficients of the mode 
        fields with the forward- and backward-propagating eigenmodes, 
        respectively. Each array has shape ``(Nfreqs, Nmodes)``, where 
        ``Nfreqs`` is the number of frequencies in the monitor.
    """

    if not isinstance(mode_monitor, ModeMonitor):
        log_and_raise("'ModeMonitor' instance expected.", TypeError)

    mnt_data = self._monitor_ids[id(mode_monitor)]

    if Nmodes is not None:
        if Nmodes > len(mnt_data.mode_plane.modes[0]):
            self.compute_modes(mode_monitor, Nmodes)

    if len(mnt_data.mode_plane.modes[0])==0:
        log_and_raise(
            "No modes found in monitor, provide 'Nmodes' argument or use "
            "'Simulation.compute_modes() first.",
            RuntimeError
        )

    if mnt_data.data is False:
        log_and_raise(
            "Solver results not loaded into monitor yet.",
            RuntimeError
        )

    Nfreqs = len(mnt_data.freqs)
    Nmodes = len(mnt_data.mode_plane.modes[0])
    positive_coeff = np.zeros((Nfreqs, Nmodes), dtype=complex_)
    negative_coeff = np.zeros((Nfreqs, Nmodes), dtype=complex_)

    for ifreq in range(Nfreqs):
        # Need to get the monitor field of shape (3, Ncross1, Ncross2)
        E = mnt_data.E[mnt_data.cross_inds, :, :, :, ifreq]
        H = mnt_data.H[mnt_data.cross_inds, :, :, :, ifreq]
        fields_monitor = (np.squeeze(E, axis=1 + mnt_data.norm_ind),
                        np.squeeze(H, axis=1 + mnt_data.norm_ind))

        for imode, mode in enumerate(mnt_data.mode_plane.modes[ifreq]):
            # Fields of the mode snapped to Yee grid centers
            (Em, Hm) = mode.fields_to_center()
            # Overlap with positive-direction mode
            positive_coeff[ifreq, imode] = dot_product(
                                    (Em, Hm), fields_monitor,
                                    mnt_data.mode_plane.mesh_step)
            # Overlap with negative-direction mode.
            # Note: the sign of the fields is correct only for the tangential 
            # components, but those are the only ones entering the dot product.
            negative_coeff[ifreq, imode] = dot_product(
                                    (np.conj(Em), -np.conj(Hm)), 
                                    fields_monitor,
                                    mnt_data.mode_plane.mesh_step)

    return positive_coeff, negative_coeff