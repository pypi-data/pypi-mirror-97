import numpy as np
import logging

from ..constants import int_, float_, complex_, fp_eps, ETA_0, C_0
from ..mode import dot_product, Mode
from ..utils.log import log_and_raise, SourceError

from .Source import VolumeSource, ModeSource, PlaneWave, PlaneSource

def _compute_modes_source(self, source, Nmodes):
    src_data = self._src_data(source)
    if isinstance(source, PlaneSource):
        src_data._compute_modes_plane_source(Nmodes)
    elif isinstance(source, PlaneWave):
        src_data._compute_modes_plane_wave(Nmodes)
    elif isinstance(source, ModeSource):
        src_data._compute_modes_mode_source(Nmodes)

def _src_data(self, source):
    """Get the source data object from a source, if it is in the simulation.
    """
    try:
        src_data = self._source_ids[id(source)]
        return src_data
    except KeyError:
        log_and_raise("Source is not in Simulation!", SourceError)

def spectrum(self, source, freqs):
    """Returns the spectrum of a :class:`.Source`.
    
    Parameters
    ----------
    source : Source
        A source in the simulation.
    freqs : array_like
        (Hz) Array of frequencies to evaluate the spectrum over.
    """
    src_data = self._src_data(source)
    return src_data._get_spectrum(freqs)

def set_mode(self, source, mode_ind, compute_mode=True):
    """Set the index of the mode to be used by the mode source. The modes can 
    be pre-computed with :meth:`.compute_modes`. Use :meth:`.viz_modes` to 
    visualize the modes and select the desired mode index.
    
    Parameters
    ----------
    source : ModeSource
        A mode source in the simulation.
    mode_ind : int
        Index of the mode to use.
    compute_mode : bool, optional
        If ``True`` (default), the eigenmode computation up to ``mode_ind`` 
        is called. Otherwise, the mode is not explicitly computed.
    """

    src_data = self._src_data(source)
    mplane = src_data.mode_plane

    if isinstance(source, PlaneWave) or isinstance(source, PlaneSource):
        if mode_ind > 0:
            log_and_raise(
                "Plane wave mode index can only be set to 0, "
                "denoting the plane wave with a specified polarization.",
                RuntimeError
            )
        src_data.mode_ind = 0

        if not compute_mode:
            return
        if src_data.mode is None:
            self.compute_modes(source, 1)
        src_data.mode = mplane.modes[0][mode_ind]


    elif isinstance(source, ModeSource):

        src_data.mode_ind = mode_ind
        
        # Compute modes if selected mode index not currently stored
        if mode_ind >= len(mplane.modes[0]):
            msg = "Selected mode index larger than number of stored modes. "
            if not compute_mode:
                msg += ("Recommended verifying the mode using "
                        "viz_modes(source, mode_ind).")
                logging.info(msg)
                return
            msg += "Recomputing eigenmodes modes up to mode index."
            logging.info(msg)
            self.compute_modes(source, mode_ind + 1)

        # Copy selected mode dictionary
        mode = mplane.modes[0][mode_ind].to_dict()

        # Check that mode is localized
        Eedge = np.sum(np.abs(mode['E'][:, 0, :])**2 +
                        np.abs(mode['E'][:, -1, :])**2) + \
                np.sum(np.abs(mode['E'][:, :, 0])**2 +
                        np.abs(mode['E'][:, :, -1])**2)
        Enorm = np.sum(np.abs(mode['E'])**2)

        if Eedge/Enorm > 1e-3:
            logging.warning(
                "Mode field does not decay at boundaries, "
                "which may produce unexpected results."
                )

        for key in ['E', 'H']:
            max_im = np.amax(np.abs(np.imag(mode[key])))
            if max_im > 1e-5:
                logging.warning(
                    f"Ignoring imaginary part of field {key} "
                    f"with maximum magnitude {max_im:.4f}"
                    )
            mode[key] = np.real(mode[key])

        src_data.mode = Mode(mode['E'], mode['H'], mode['neff'], mode['keff'])
        neff_z = source.dir_ind*src_data.mode.neff
        src_data.mode.kvector = np.array([0, 0, neff_z])
        src_data.mode.kvector *= 2*np.pi * source.source_time.frequency / C_0

    # Account for phase offset between M and J sources because of 
    # spatial and temporal mismatch.
    # Temporal offset phase
    src_data.phaseMJ_t = np.pi * source.source_time.frequency * \
                        src_data.mode_plane.time_step
    # Spatial offset phase
    src_data.phaseMJ_s = - src_data.mode.kvector[2]/2 * \
                        src_data.mode_plane.mesh_step[2]
    phaseM = src_data.phaseMJ_t + src_data.phaseMJ_s
    src_data._set_tdep(self.grid.tmesh, phaseM)