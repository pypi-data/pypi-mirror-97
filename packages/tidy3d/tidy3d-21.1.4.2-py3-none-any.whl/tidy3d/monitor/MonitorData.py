import numpy as np

from .Monitor import TimeMonitor, FreqMonitor, ModeMonitor
from ..constants import int_, float_, complex_, fp_eps, C_0
from ..mode import ModePlane

class MonitorData(object):
    """Class used internally to store data related to a Monitor added in a 
    specific Simulation.
    """

    def __init__(self, monitor):

        # Reference to the monitor that the data corresponds to
        self.monitor = monitor

        # To be set by Simulation
        self.name = None

        # Everything below is set after a run of store_data() or load_fields()
        self.data = False # To be set to True after data is loaded

        # Raw E and H data as returned by the solver
        self._E = np.empty((3, 0, 0, 0, 0), dtype=float_)
        self._H = np.empty((3, 0, 0, 0, 0), dtype=float_)
        # Poynting flux if computed after a solve
        self.S = np.empty((3, 0, 0, 0, 0), dtype=float_)

        # Mesh defining the positions at which the fields are returned
        self.xmesh = np.empty((0, ), dtype=float_)
        self.ymesh = np.empty((0, ), dtype=float_)
        self.zmesh = np.empty((0, ), dtype=float_)
        self.mesh_step = np.empty((3, ), dtype=float_)

        # Mesh in time, for a TimeMonitor
        self.tmesh = np.empty((0, ), dtype=float_)
        self.tind_beg = 0
        self.tind_end = 0
        self.Nt = 0

        # Frequencies, for a FreqMonitor
        self.freqs = np.empty((0, ), dtype=float_)
        if isinstance(monitor, FreqMonitor):
            self.freqs = np.array(monitor.freqs, dtype=float_)

        # Indexes defining the span of the Monitor in the simulation grid in 
        # which it is embedded.
        self.mnt_inds = np.empty((0, 3), dtype=int_)
        self.inds_beg = np.zeros((3, ), dtype=int_)
        self.inds_end = np.zeros((3, ), dtype=int_)

        # Source normalization, which may be set later for FreqMonitors
        self.set_source_norm(None) 

    # def __repr__(self):
    #     if self.data==False:
    #         rep += "Has data: False"
    #     else:
    #         rep += "Has data: xmesh, ymesh, zmesh, freqs, " + ", ".join(
    #                                         [f.upper() for f in self.field])
    #         if hasattr(self, 'S'):
    #             rep += ", S"

    #     rep += "}\n"
    #     return rep

    @property
    def E(self):
        """ (V/m) Electric field, if it was requested by the monitor and 
        after the data has been loaded.
        """
        return self._E * self.source_norm[None, None, None, None, :]

    @property
    def H(self):
        """ (A/m) Magnetic field, if it was requested by the monitor and 
        after the data has been loaded.
        """
        return self._H * self.source_norm[None, None, None, None, :]

    def _set_tmesh(self, tmesh):
        """ Set the time mesh of the monitor. At the end of a simulation run, 
        the field values are syncronized to be on the ``tmesh`` as defined 
        here. This involves recording one extra step in the solver, and 
        averaging the H-fields, which live on a (n + 1/2)*dt time mesh.
        """
 
        # Step to compare to in order to handle t_start = t_stop
        if np.array(tmesh).size < 1:
            dt = 1e-20
        else:
            dt = tmesh[1] - tmesh[0]

        # If t_stop is None, record until the end
        t_stop = self.monitor.t_stop
        if self.monitor.t_stop is None:
            t_stop = tmesh[-1]
            self.tind_end = tmesh.size
        else:
            tend = np.nonzero(tmesh <= self.monitor.t_stop)[0]
            if tend.size > 0:
                self.tind_end = tend[-1] + 1
            else:
                self.tind_end = 0

        # If equal (within dt), record one time step
        if np.abs(self.monitor.t_start - t_stop) < dt:
            self.tind_beg = np.max([self.tind_end - 1, 0])
        else:
            tbeg = np.nonzero(tmesh[0:self.tind_end] >= 
                                self.monitor.t_start)[0]
            if tbeg.size > 0:
                self.tind_beg = tbeg[0]
            else:
                self.tind_beg = self.tind_end

        self.tmesh = tmesh[self.tind_beg:self.tind_end]
        self.Nt = self.tind_end - self.tind_beg

    def _set_mode_plane(self):
        self.norm_ind = self.monitor.norm_ind
        self.cross_inds = [0, 1, 2]
        self.cross_inds.pop(self.norm_ind)
        self.mode_plane = ModePlane(self.monitor.span, self.norm_ind)

    def _store_data(self, mnt_data, mnt_inds, field):
        """ Store the raw monitor values returned by the solver.
        
        Parameters
        ----------
        mnt_data : np.ndarray
            An array of shape ``(Np, 3, Nsample)``, where ``Np`` is the total 
            number of monitor points, and ``Nsample`` is either the number of 
            time steps in a ``TimeMonitor``, or the number of requested 
            frequencies in a ``FreqMonitor``.
        mnt_inds : np.ndarray
            An array of shape ``(Np, 3)`` giving the x, y, and z index for 
            each point in the simulation grid.

        Note
        ----
        ``MonitorData.E`` and ``MonitorData.H`` are stored in the format 
        ``(3, indx, indy, indz, samp_ind)``, where ``samp_ind`` is either a 
        time or a frequency index.
        """

        self.mnt_inds = mnt_inds
        self.inds_beg = np.amin(mnt_inds, axis = 0)
        self.inds_end = np.amax(mnt_inds, axis = 0) + 1
        mnt_dims = self.inds_end - self.inds_beg
        if field.lower()=='e':
            self._E = np.zeros((3, mnt_dims[0], mnt_dims[1], mnt_dims[2], 
                        mnt_data.shape[2]), dtype=mnt_data.dtype)
            for ipol in range(3):
                self._E[ipol, mnt_inds[:, 0]-self.inds_beg[0],
                    mnt_inds[:, 1]-self.inds_beg[1],
                    mnt_inds[:, 2]-self.inds_beg[2], :] = mnt_data[:, ipol, :]
        elif field.lower()=='h':
            self._H = np.zeros((3, mnt_dims[0], mnt_dims[1], mnt_dims[2], 
                        mnt_data.shape[2]), dtype=mnt_data.dtype)
            for ipol in range(3):
                self._H[ipol, mnt_inds[:, 0]-self.inds_beg[0],
                    mnt_inds[:, 1]-self.inds_beg[1],
                    mnt_inds[:, 2]-self.inds_beg[2], :] = mnt_data[:, ipol, :]
        self.data = True

    def _load_fields(self, inds_beg, inds_end, E, H, symmetries, Nxyz):
        """ Load the fields returned by the solver. This also applies any 
        symmetries that were present in the simulation.
        """

        # By default just store index and field values, unless changed below
        self.inds_beg = inds_beg
        self.inds_end = inds_end
        self._E = E
        self._H = H

        # Auxiliary variable for slicing along a given axis
        slices = (slice(None), slice(None), slice(None),
                        slice(None), slice(None))

        for dim, sym in enumerate(symmetries):

            # Auxiliary variable for symmetry eigenvalue along current axis
            svals = np.ones((3, 1, 1, 1, 1))
            svals[dim] = -1

            if sym==-1 and inds_beg[dim]==0:
                self.inds_beg[dim] = Nxyz[dim]//2 - inds_end[dim]
                self.inds_end[dim] = Nxyz[dim]//2 + inds_end[dim]
                sl = list(slices)
                sl[dim+1] = slice(-1, None, -1)
                if E.size > 0:
                    self._E = np.concatenate((-svals*self._E[tuple(sl)],
                                self._E), axis=dim+1)
                if H.size > 0:
                    self._H = np.concatenate((svals*self._H[tuple(sl)],
                                self._H), axis=dim+1)

            if sym==1 and inds_beg[dim]==0:
                ibeg = 1
                iend = min(inds_end[dim], Nxyz[dim]//2+1)
                self.inds_beg[dim] = Nxyz[dim]//2 - (iend - ibeg)
                self.inds_end[dim] = Nxyz[dim]//2 + (iend - ibeg)
                sl1 = list(slices)
                sl1[dim+1] = slice(iend-1, ibeg-1, -1)
                sl2 = list(slices)
                sl2[dim+1] = slice(ibeg, iend)  
                if E.size > 0:
                    self._E = np.concatenate((svals*self._E[tuple(sl1)],
                                self._E[tuple(sl2)]), axis=dim+1)
                if H.size > 0:
                    self._H = np.concatenate((-svals*self._H[tuple(sl1)],
                                self._H[tuple(sl2)]), axis=dim+1)
        self.data = True

    def set_source_norm(self, src_data):
        """Normalize the stored fields.
        
        Parameters
        ----------
        src_data : src_data or None
            A :class:`.SourceData` object from whose spectrum the fields are 
            normalized.
        """

        if isinstance(self.monitor, TimeMonitor):
            self.source_norm = np.ones((1, ), dtype=float_)
        elif src_data is None:
            self.source_norm = np.ones((len(self.freqs), ), dtype=float_)
        else:
            spectrum = src_data._get_spectrum(self.freqs)
            self.source_norm = np.array(1/np.abs(spectrum))