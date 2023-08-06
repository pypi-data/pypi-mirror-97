import numpy as np
import logging

from ..utils import axes_handed, log_and_raise
from ..constants import int_, float_, complex_, fp_eps, ETA_0, C_0
from ..mode import Mode, ModePlane, dot_product
from .Source import VolumeSource, ModeSource, PlaneWave, PlaneSource

class SourceData(object):
    """Class used internally to store data related to a Source added in a 
    specific Simulation.
    """

    def __init__(self, source):

        # Reference to the source that the data corresponds to
        self.source = source

        # Mesh normalization, set by Simulation
        self.mesh_norm = 1

        # Mesh in time and time dependence, set by Simulation
        self.tmesh = None
        self.time_dep = np.zeros((0, 2), dtype=float_)

        # A complex-valued source can be used to launch complex-valued 
        # eigenmodes. It includes a second space and time dependence 
        # corresponding to the imaginary part of the source.
        self.complex = False

        # Phase offset of the magnetic current M and the electric current J.
        self.phaseJ = 0
        self.phaseM = 0

        # Extra variables specific to ModeSource
        if isinstance(source, ModeSource):
            # Variables to store the mode plane, mode, and mode index
            self.mode_plane = ModePlane(source.span, source.norm_ind)
            self.mode = None
            if (isinstance(source, PlaneWave) or 
                            isinstance(source, PlaneSource)):
                # No choice in modes
                self.mode_ind = 0
            else:
                # Must be set using Simulation.set_mode(source, mode_ind)
                self.mode_ind = None

            # Phases accountint for the temporal and spatial offset between J 
            # and M, set by Simulation.
            self.phaseMJ_s = 0
            self.phaseMJ_t = 0

    def _mesh_norm(self, mesh_step):
        """Normalize source by ``mesh_step`` in a given direction, if the span 
        of the source in that direction is zero. This is to avoid changes in 
        radiated power when the spatial discretization is changed.
        """

        self.mesh_norm = 1
        for dim in range(3):
            if np.abs(self.source.span[dim, 1] -
                        self.source.span[dim, 0]) < fp_eps:
                self.mesh_norm /= mesh_step[dim]

    def _set_tdep(self, tmesh, phaseM=0.):
        """Compute the time-dependence of the source currents.
        
        Parameters
        ----------
        tmesh : array_like
            Array of shape (Nt, ) defining the mesh in time, in seconds.
        phaseM : float, optional
            Phase offset of the magnetic current M from the electric current J.
        """

        self.phaseM = phaseM
        tdJ = self.source.source_time._get_time(tmesh, self.phaseJ)
        tdM = self.source.source_time._get_time(tmesh, self.phaseM)

        self.tmesh = tmesh
        self.time_dep = np.stack((tdJ, tdM), axis=1).astype(float_)

        # Time dependence offset by pi/2 for complex-valued sources
        tdJ = self.source.source_time._get_time(tmesh, np.pi/2 + self.phaseJ)
        tdM = self.source.source_time._get_time(tmesh, np.pi/2 + self.phaseM)
        self.time_dep_im = np.stack((tdJ, tdM), axis=1).astype(float_)

    def _get_spectrum(self, freqs):
        return self.source.source_time._get_spectrum(freqs, self.tmesh)

    def _currents(self, src_inds):
        """Source currents (Jx, Jy, Jz, Mx, My, Mz) at grid locations 
        specified by the global grid indexes ``src_inds``.
        """

        if isinstance(self.source, VolumeSource):
            src_amps = np.zeros((src_inds.shape[0], 6), dtype=float_)
            src_amps[:, self.source.components==1] = \
                self.source.amplitude * self.mesh_norm

        elif isinstance(self.source, ModeSource):
            """ Currents for the eigenmode source are defined through the 
            fields of the mode through the equivalence principle. Only 
            tangential currents are nonzero. ``src_inds`` are the indexes in 
            the global grid, so to get the indexing in the 2D plane, we use 
            ``mode_plane.span_inds``, which gives the beginning and end 
            indexes of the plane in the global grid.
            """

            src_amps = np.zeros((src_inds.shape[0], 6), dtype=complex_)
            mplane = self.mode_plane

            # Indexing in the 2D plane. 
            inds1 = src_inds[:, mplane.cross_inds[0]] - \
                        mplane.span_inds[mplane.cross_inds[0], 0]
            inds2 = src_inds[:, mplane.cross_inds[1]] - \
                        mplane.span_inds[mplane.cross_inds[1], 0]

            # Electric current sources from magnetic field of the eigenmode.
            src_amps[:, mplane.cross_inds[0]] = \
                                    self.mode.H[1, inds1, inds2].ravel()
            src_amps[:, mplane.cross_inds[1]] = \
                                    -self.mode.H[0, inds1, inds2].ravel()

            # Magnetic current sources from electric field of the eigenmode.
            src_amps[:, 3 + mplane.cross_inds[0]] = \
                                    -self.mode.E[1, inds1, inds2].ravel()
            src_amps[:, 3 + mplane.cross_inds[1]] = \
                                    self.mode.E[0, inds1, inds2].ravel()
            
            # +/-1 depending on handedness of mode_plane axes
            ax_fact = axes_handed([mplane.cross_inds[0], mplane.cross_inds[1],
                                    mplane.norm_ind])
            # dir_ind is +/-1 for positive/negative direction
            src_amps[:, 3:] *= ax_fact*self.source.dir_ind
            # Overall source amplitude
            src_amps *= self.source.amplitude * self.mesh_norm
            # Extra correction because J and M are not co-localized
            src_amps /= np.sqrt(np.cos(self.phaseMJ_s))

        return src_amps

    def _compute_modes_plane_wave(self, Nmodes):
        """ Compute modes without matrix diagonalization.
        """

        source = self.source
        mplane = self.mode_plane

        eps2D = mplane.eps
        if np.amax(eps2D) - np.amin(eps2D) > 1e-5:
            log_and_raise(
                "'PlaneWave' is intended to be placed "
                "entirealy in a homogeneous material.",
                RuntimeError
            )

        if Nmodes > 1:
            log_and_raise(
                "Only a single mode can be computed for a "
                "'PlaneWave' the plane wave with a specified polarization.",
                RuntimeError
            )

        frequency = source.source_time.frequency

        """ Mode fields are defined w.r.t. ModePlane axes, which are 
        [cross_ind1, cross_ind2, norm_ind]. """
        N1, N2 = eps2D.shape
        neff = np.sqrt(np.amax(eps2D))
        E = np.zeros((3, N1, N2))
        H = np.zeros((3, N1, N2))
        if source.epol_ind < source.hpol_ind:
            # E is polarized along first cross-index
            E[0, :, :] = 1
            H[1, :, :] = neff/ETA_0
        else:
            # E is polarized along second cross-index
            E[1, :, :] = 1
            H[0, :, :] = -neff/ETA_0

        mplane.freqs = [frequency]
        mode = Mode(E, H, neff, keff=0)
        flux = dot_product((E, H), (E, H), mplane.mesh_step)
        mode.E /= np.sqrt(flux)
        mode.H /= np.sqrt(flux)
        mode.kvector = np.array([0, 0, source.dir_ind * mode.neff])
        mode.kvector *= 2 * np.pi * source.source_time.frequency / C_0
        mplane.modes = [[mode]]

    def _compute_modes_plane_source(self, Nmodes):
        """ Compute (oblique) wave mode without matrix diagonalization.
        """

        source = self.source
        mplane = self.mode_plane

        eps2D = mplane.eps
        if np.amax(eps2D) - np.amin(eps2D) > 1e-5:
            log_and_raise(
                "'PlaneSource' is intended to be placed "
                "entirealy in a homogeneous material.",
                RuntimeError
            )

        if Nmodes > 1:
            log_and_raise(
                "Only a single mode can be computed for a "
                "'PlaneSource' the plane wave with a specified polarization.",
                RuntimeError
            )

        frequency = source.source_time.frequency

        """ Mode fields are defined w.r.t. ModePlane axes, which are 
        [cross_ind1, cross_ind2, norm_ind]. """
        N1, N2 = eps2D.shape
        neff = np.sqrt(np.amax(eps2D))
        E = np.zeros((3, N1, N2), dtype=complex_)
        H = np.zeros((3, N1, N2), dtype=complex_)

        # kvector in units of effective index, based on diffraction order
        d1 = N1 * mplane.mesh_step[0]
        d2 = N2 * mplane.mesh_step[1]
        k1 = source.diff_order[0] * 2*np.pi / d1 
        k2 = source.diff_order[1] * 2*np.pi / d2 
        k0 = 2 * np.pi * neff * frequency / C_0
        if k0 ** 2 <= k1**2 + k2**2:
            raise ValueError("Diffraction order [%d, %d] not available"%(
                            source.diff_order[0], source.diff_order[1]) +\
                            "for PlaneSource size and frequency.")
        kn = np.sqrt(k0**2 - k1**2 - k2**2)
        # Unit vector along the propagation axis
        dir_vec = np.array([k1, k2, kn])/k0
        # k-vector in 1/micron
        kvector = source.dir_ind * k0 * dir_vec

        # Unit vector along axis normal to injection plane
        norm_vec = np.array([0, 0, 1])

        if np.linalg.norm(source.polarization) < fp_eps:
            # Unit vector for S polarization
            # Add a tiny bit of offset to break S-P degeneracy at theta = 0
            dvec = np.copy(dir_vec)
            if np.linalg.norm(np.cross(norm_vec, dvec)) < fp_eps:
                dvec[0] += fp_eps
            S_vec = np.cross(norm_vec, dvec)
            S_vec /= np.sqrt(S_vec.dot(S_vec))

            # Unit vector for P polarization
            P_vec = np.cross(S_vec, dir_vec)
            P_vec /= np.sqrt(P_vec.dot(P_vec))

            # E-field polarization vector
            E_vec = np.cos(source.pol_angle)*P_vec +\
                        np.sin(source.pol_angle)*S_vec
            # H-field polarization vector
            H_vec = - np.sin(source.pol_angle)*P_vec +\
                        np.cos(source.pol_angle)*S_vec
        else:
            E_vec = source.polarization[[mplane.cross_inds[0],
                                         mplane.cross_inds[1],
                                         mplane.norm_ind]]
            E_vec -= np.dot(E_vec, dir_vec) * dir_vec
            E_vec /= np.sqrt(E_vec.dot(E_vec))
            H_vec = np.cross(dir_vec, E_vec)
            H_vec /= np.sqrt(H_vec.dot(H_vec))

        # Add impedence
        H_vec *= neff/ETA_0

        """ Finally need to account for the Yee grid locations of each component
        through mplane.mesh. E[0] and H[1] are co-locallized in the 
        cross-section plane, and same for E[1] and H[0]. The offset in the 
        normal direction is taken into account later. """
        xg, yg = np.meshgrid(mplane.mesh_e1[0],
                             mplane.mesh_e1[1])
        E[0, :, :] = E_vec[0]*np.exp(1j*(xg*kvector[0] + yg*kvector[1])).T
        H[1, :, :] = H_vec[1]*np.exp(1j*(xg*kvector[0] + yg*kvector[1])).T
        xg, yg = np.meshgrid(mplane.mesh_e2[0],
                             mplane.mesh_e2[1])
        E[1, :, :] = E_vec[1]*np.exp(1j*(xg*kvector[0] + yg*kvector[1])).T
        H[0, :, :] = H_vec[0]*np.exp(1j*(xg*kvector[0] + yg*kvector[1])).T

        if np.linalg.norm(np.cross(norm_vec, dir_vec)) > 2*fp_eps:
            self.complex = True

        mplane.freqs = [frequency]
        mode = Mode(E, H, neff, keff=0)
        flux = dot_product((E, H), (E, H), mplane.mesh_step)
        mode.E /= np.sqrt(flux)
        mode.H /= np.sqrt(flux)
        mode.kvector = kvector
        mplane.modes = [[mode]]

    def _compute_modes_mode_source(self, Nmodes):
        """ Compute general eigenmodes using matrix diagonalization.
        """
        frequency = self.source.source_time.frequency
        self.mode_plane.compute_modes(Nmodes, frequency)