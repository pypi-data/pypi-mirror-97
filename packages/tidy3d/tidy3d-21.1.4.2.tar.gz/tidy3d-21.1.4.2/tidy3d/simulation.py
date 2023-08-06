import numpy as np
import json
import h5py
import logging

from .utils import listify, list2str, object_name, cs2span
from .utils.log import log_and_raise, DivergenceError
from .utils.check import check_3D_lists
from .constants import int_, float_, fp_eps, C_0, pec_eps, pmc_eps

from .grid import Grid
from .structure import Structure, Box
from .material import Medium
from . import PEC, PMC

from .source import Source, ModeSource, SourceData
from .monitor import Monitor, TimeMonitor, FreqMonitor, ModeMonitor
from .monitor import MonitorData

from .json_ops import write_parameters, write_structures, write_sources
from .json_ops import write_monitors

class Simulation(object):
    """
    Main class for building a simulation model.
    """
    from .utils.check import _check_size, _check_monitor_size
    from .source._simulation import _compute_modes_source, set_mode, spectrum
    from .monitor._simulation import _compute_modes_monitor, data, poynting
    from .monitor._simulation import flux, decompose
    from .json_ops import _read_simulation
    from .viz import _fmonitors_png, _structure_png
    from .viz import viz_eps_2D, viz_field_2D, viz_modes
    from .viz import viz_source, viz_source_spectrum, viz_source_time

    def __init__(self,
                size,
                center=[0., 0., 0.],
                resolution=None,
                mesh_step=None,
                structures=None,
                sources=None,
                monitors=None,
                symmetries=[0, 0, 0],
                pml_layers=[0, 0, 0],
                run_time=0.,
                courant=0.9
                ):
        """Construct.

        Parameters
        ----------
        center : array_like, optional
            (micron) 3D vector defining the center of the simulation domain.
        size : array_like, optional
            (micron) 3D vector defining the size of the simulation domain.
        resolution : float or array_like, optional
            (1/micron) Number of grid points per micron, or a 3D vector 
            defining the number of grid points per mircon in x, y, and z.
        mesh_step : float or array_like, optional
            (micron) Step size in all directions, or a 3D vector defining the 
            step size in x, y, and z seprately. If provided, ``mesh_step`` 
            overrides the ``resolution`` parameter, otherwise 
            ``mesh_step = 1/resolution``.
        structures : Structure or List[Structure], optional
            Empty list (default) means vacuum. 
        sources : Source or List[Source], optional
            Source(s) to be added to the simulation.
        monitors : Monitor or List[Monitor], optional
            Monitor(s) to be added to the simulation.
        symmetries : array_like, optional
            Array of three integers defining reflection symmetry across a 
            plane bisecting the simulation domain normal to the x-, y-, and 
            z-axis, respectively. Each element can be ``0`` (no symmetry), 
            ``1`` (even, i.e. 'PMC' symmetry) or ``-1`` (odd, i.e. 'PEC' 
            symmetry). Note that the vectorial nature of the fields must be 
            taken into account to correctly determine the symmetry value.
        pml_layers : array_like, optional
            Array of three integers defining the number of PML layers on both 
            sides of the simulation domain along x, y, and z. When set to 
            ``0`` (default), periodic boundary conditions are applied.
        run_time : float, optional
            (second) Total electromagnetic evolution time.
        courant : float, optional
            Courant stability factor, must be smaller than 1, or more 
            generally smaller than the smallest refractive index in the 
            simulation.
        """

        check_3D_lists(center=listify(center), size=listify(size),
                            symmetries=listify(symmetries),
                            pml_layers=listify(pml_layers))

        logging.info("Initializing simulation...")

        # Set PML size. Npml defines the number of layers on all 6 sides.
        self.pml_layers = listify(pml_layers)
        self.Npml = np.vstack((pml_layers, pml_layers)).astype(int_).T

        # Set spatial mesh step
        if mesh_step is None:
            if resolution is None:
                log_and_raise(
                    "Either 'mesh_step' or 'resolution' must be set.",
                    ValueError
                )
            mesh_step = 1/np.array(resolution)
        else:
            if resolution is not None:
                logging.info(
                    "Note: parameter 'mesh_step' overrides 'resolution'."
                    )

        # Set simulation size inside the PML and including the PML
        self.center = np.array(center, dtype=float_)
        self.size_in = np.array(size, dtype=float_)
        self.size = self.size_in + 2*np.array(pml_layers)*mesh_step
        self.span = cs2span(self.center, self.size)

        # Initialize grid
        self.grid = Grid(self.span, mesh_step, symmetries, courant)

        logging.info(
            f"Mesh step (micron): {list2str(self.grid.mesh_step, '%1.2e')}.\n"
            "Simulation domain in number of grid points: "
            f"{list2str(self.grid.Nxyz, '%d')}."
            )

        # Computational domain including symmetries, if any
        self.span_sym = np.copy(self.span)
        self.Nxyz_sym = np.copy(self.grid.Nxyz)
        for d, sym in enumerate(symmetries):
            if sym==-1:
                self.span_sym[d, 0] += self.size[d]/2
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2
            elif sym==1:
                self.span_sym[d, 0] += self.size[d]/2 - self.grid.mesh_step[d]
                self.span_sym[d, 1] += self.grid.mesh_step[d]
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2 + 2
        # Print new size, if there are any symmetries
        if np.any(np.array(symmetries)!=0):
            logging.info(
                "Computation domain (after symmetries): "
                f"{list2str(self.Nxyz_sym, '%d')}."
            )
        # Total number of points in computational domain (after symmetries)
        self.Np = np.prod(self.Nxyz_sym)
        logging.info(
            f"Total number of grid points: {self.Np:.2e}."
        )

        # Set up run time
        self.set_time(run_time, courant)
        logging.info(f"Total number of time steps: {self.Nt}.")
        if self.Nt <= 0:
            logging.warning(
                f"run_time = {self.run_time:.2e} smaller than a single "
                f"simulation time step dt = {self.grid.dt:.2e}.",
            )

        # Check the simulation size
        self._check_size()

        # Materials and indexing populated when adding ``Structure`` objects.
        self._mat_inds = [] # material index of each structure
        self._materials = [] # list of materials included in the simulation
        self._structures = []

        # List containing SourceData for all sources, and a dictionary 
        # used to get SourceData from id(source), e.g. src_data = 
        # self._source_ids[id(source)]
        self._source_data = []
        self._source_ids = {}

        # List containing MonitorData for all monitors, and a dictionary 
        # used to get MonitorData from id(monitor)
        self._monitor_data = []
        self._monitor_ids = {}

        # Structures and material indexing for symmetry boxes
        self._structures_sym = [] # PEC/PMC boxes added for symmetry
        self._mat_inds_sym = []

        # Add structures, sources, monitors, symmetries
        if structures:
            self.add(structures)
        if sources:
            self.add(sources)
        if monitors:
            self.add(monitors)
        self._add_symmetries(symmetries)

        # JSON file from which the simulation is loaded
        self.fjson = None

    def __repr__(self):
        rep = "Tidy3D Simulation:\n"
        rep += "center      = %s\n" % list2str(self.center, "%1.4f")
        rep += "size        = %s\n" % list2str(self.size_in, "%1.4f")
        rep += "size w. pml = %s\n" % list2str(self.size, "%1.4f")
        rep += "mesh_step   = %s\n" % list2str(self.grid.mesh_step, "%1.4f")
        rep += "run_time    = %1.2e\n"%self.run_time
        rep += "symmetries  = %s\n" % list2str(self.symmetries, "%d")
        rep += "pml_layers  = %s\n\n" % list2str(self.pml_layers, "%d")

        rep += "Number of grid points in x, y, z: %s\n" % list2str(
                    self.grid.Nxyz, "%d")
        rep += "    after symmeries             : %s\n"%list2str(
                    self.Nxyz_sym, "%d")
        rep += "Total number of grid points: %d\n" % np.prod(self.grid.Nxyz)
        rep += "    after symmetries:        %d\n" % self.Np

        rep += "Number of time steps       : %d\n" % self.Nt
        rep += "Number of structures       : %d\n"%len(self._structures)
        rep += "Number of sources          : %d\n"%len(self.sources)
        rep += "Number of monitors         : %d\n"%len(self.monitors)

        return rep

    @property
    def materials(self):
        """ List containing all materials included in the simulation."""
        return self._materials

    @property
    def mat_inds(self):
        """ List containing the material index in :attr:`.materials` of every 
        structure in :attr:`.structures`. """
        return self._mat_inds + self._mat_inds_sym

    @property
    def structures(self):
        """ List containing all :class:`Structure` objects. """
        return self._structures + self._structures_sym

    @structures.setter
    def structures(self, new_struct):
        raise RuntimeError("Structures can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    @property
    def sources(self):
        """ List containing all :class:`Source` objects. """
        return [src_data.source for src_data in self._source_data]

    @sources.setter
    def sources(self, new_sources):
        raise RuntimeError("Sources can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    @property
    def monitors(self):
        """ List containing all :class:`.Monitor` objects. """
        return [mnt_data.monitor for mnt_data in self._monitor_data]

    @monitors.setter
    def monitors(self, new_monitors):
        raise RuntimeError("Monitors can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    def _add_structure(self, structure):
        """ Adds a Structure object to the list of structures and to the 
        permittivity array. """
        self._structures.append(structure)

        try:
            mind = self.materials.index(structure.material)
            self._mat_inds.append(mind)
        except ValueError:
            if len(self.materials) < 200:
                self._materials.append(structure.material)
                self._mat_inds.append(len(self.materials)-1)
            else:
                log_and_raise(
                    "Maximum 200 distinct materials allowed.",
                    RuntimeError
                )

    def _add_source(self, source):
        """ Adds a Source object to the list of sources.
        """

        if id(source) in self._monitor_ids.keys():
            logging.warning("Source already in Simulation, skipping.")
            return

        src_data = SourceData(source)
        src_data.name = object_name(self._source_data, source, 'source')
        src_data._mesh_norm(self.grid.mesh_step)
        src_data._set_tdep(self.grid.tmesh)
        self._source_data.append(src_data)
        self._source_ids[id(source)] = src_data

        if isinstance(source, ModeSource):
            src_data.mode_plane._set_eps(self)

    def _add_monitor(self, monitor):
        """ Adds a time or frequency domain Monitor object to the 
        corresponding list of monitors.
        """

        if id(monitor) in self._monitor_ids.keys():
            logging.warning("Monitor already in Simulation, skipping.")
            return

        mnt_data = MonitorData(monitor)
        mnt_data.name = object_name(self._monitor_data, monitor, 'monitor')
        self._monitor_data.append(mnt_data)
        self._monitor_ids[id(monitor)] = mnt_data

        memGB = self._check_monitor_size(monitor)
        logging.info(
            f"Estimated data size of monitor {mnt_data.name}: {memGB:.4f}."
            )

        # Initialize the ModePlane of a ModeMonitor
        if isinstance(monitor, ModeMonitor):
            mnt_data._set_mode_plane()
            mnt_data.mode_plane._set_eps(self)

    def _add_symmetries(self, symmetries):
        """ Add all symmetries as PEC or PMC boxes.
        """
        self.symmetries = listify(symmetries)
        for dim, sym in enumerate(symmetries):
            if sym not in [0, -1, 1]:
                log_and_raise(
                    "Reflection symmetry values can be 0 (no symmetry), "
                    "1, or -1.",
                    ValueError
                )
            elif sym==1 or sym==-1:
                sym_cent = np.copy(self.center)
                sym_size = np.copy(self.size)
                sym_cent[dim] -= self.size[dim]/2
                sym_size[dim] = sym_size[dim] + fp_eps
                sym_mat = PEC if sym==-1 else PMC
                sym_pre = 'pec' if sym==-1 else 'pmc'
                self._structures_sym.append(Box(center=sym_cent,
                                                size=sym_size,
                                                material=sym_mat,
                                                name=sym_pre + '_sym%d'%dim))
                try:
                    mind = self.materials.index(sym_mat)
                    self._mat_inds_sym.append(mind)
                except ValueError:
                    self._materials.append(sym_mat)
                    self._mat_inds_sym.append(len(self.materials)-1)

    def _pml_config(self):
        """Set the CPML parameters. Default configuration is hard-coded. This 
        could eventually be exposed to the user, or, better, named PML 
        profiles can be created.
        """
        cfs_config = {'sorder': 3, 'smin': 0., 'smax': None, 
                    'korder': 3, 'kmin': 1., 'kmax': 3., 
                    'aorder': 1, 'amin': 0., 'amax': 0}
        return cfs_config

    def _get_eps(self, mesh, edges='in', pec_val=pec_eps, pmc_val=pmc_eps):
        """ Compute the permittivity over a given mesh. For large simulations, 
        this could be computationally heavy, so preferably use only over small 
        meshes (e.g. 2D cuts). 
        
        Parameters
        ----------
        mesh : tuple
            Three 1D arrays defining the mesh in x, y, z.
        edges : {'in', 'out', 'average'}
            When an edge of a structure sits exactly on a mesh point, it is 
            counted as in, out, or an average value of in and out is taken.
        pec_val : float
            Value to use for PEC material.
        pmc_val : float
            Value to use for PMC material.
        
        Returns
        -------
        eps : np.ndarray
            Array of size (mesh[0].size, mesh[1].size, mesh[2].size) defining 
            the relative permittivity at each point.
        """

        Nx, Ny, Nz = [mesh[i].size for i in range(3)]

        eps = np.ones((Nx, Ny, Nz), dtype=float_)

        # Apply all structures
        for struct in self.structures:

            eps_val = struct._get_eps_val(pec_val, pmc_val)
            struct._set_val(mesh, eps, eps_val, edges=edges)

        # return eps array after filling in all structures
        return eps

    def add(self, objects):
        """Add a list of objects, which can contain structures, sources, and 
        monitors.
        """

        for obj in listify(objects):
            if isinstance(obj, Structure):
                self._add_structure(obj)
            elif isinstance(obj, Source):
                self._add_source(obj)
            elif isinstance(obj, Monitor):
                self._add_monitor(obj)

    def set_time(self, run_time=None, courant=None):
        """Change the value of the run time of the simulation and the time 
        step determined by the courant stability factor.
        
        Parameters
        ----------
        run_time : None or float
            (second) If a float, the new ``run_time`` of the simulation. 
        courant : None or float, optional
            If a float, the new courant factor to be used.
        """

        if run_time:
            self.run_time = run_time

        if courant:
            self.courant = courant
            self.grid.set_time_step(courant)

        if run_time or courant:
            self.grid.set_tmesh(self.run_time)
            self.Nt = np.array(self.grid.tmesh.size)

            # Update all sources that are already in the simulation
            try:
                for src_data in self._source_data:
                    src_data._set_tdep(self.grid.tmesh)
            except AttributeError:
                pass

    def source_norm(self, source):
        """Normalize all frequency monitors by the spectrum of a 
        :class:`.Source` object.
        
        Parameters
        ----------
        source : Source or None
            If ``None``, the normalization is reset to the raw field output.
        """

        if source is None:
            for mnt_data in self._monitor_data:
                mnt_data.set_source_norm(None)
            return

        src_data = self._source_ids[id(source)]

        for mnt_data in self._monitor_data:
            mnt_data.set_source_norm(src_data)

    def compute_modes(self, mode_object, Nmodes):
        """Compute the eigenmodes of the 2D cross-section of a 
        :class:`.ModeSource` or :class:`.ModeMonitor` object, assuming 
        translational invariance in the third dimension. The eigenmodes are 
        computed in decreasing order of propagation constant, at the central 
        frequency of the :class:`.ModeSource` or for every frequency in the 
        list of frequencies of the :class:`.ModeMonitor`. In-plane, periodic 
        boundary conditions are assumed, such that the mode shold decay at the 
        boundaries, or be matched with periodic boundary conditions in the 
        simulation. Use :meth:`.viz_modes` to visuzlize the computed 
        eigenmodes.
        
        Parameters
        ----------
        mode_object : ModeSource or ModeMonitor
            The object defining the 2D plane in which to compute the modes.
        Nmodes : int
            Number of eigenmodes to compute.
        """

        if isinstance(mode_object, Monitor):
            self._compute_modes_monitor(mode_object, Nmodes)
        elif isinstance(mode_object, Source):
            self._compute_modes_source(mode_object, Nmodes)

    def export(self):
        """Return a dictionary with all simulation parameters and objects.
        """
        js = {}
        js["parameters"] = write_parameters(self)
        js["sources"] = write_sources(self)
        js["monitors"] = write_monitors(self)
        js["materials"], js["structures"] = write_structures(self)

        return js

    def export_json(self, fjson):
        """Export the simulation specification to a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """

        self.fjson = fjson
        with open(fjson, 'w') as json_file:
            json.dump(self.export(), json_file, indent=4)

    @classmethod
    def import_json(cls, fjson):
        """Import a simulation specification from a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """
        
        with open(fjson, 'r') as json_file:
            js = json.load(json_file)

        sim = cls._read_simulation(js)
        sim.fjson = fjson

        return sim

    def load_results(self, dfile):
        """Load all monitor data recorded from a Tidy3D run.
        The data from each monitor can then be queried using 
        :meth:`.data`.
        
        Parameters
        ----------
        dfile : str
            Path to the file containing the simulation results.
        """

        mfile = h5py.File(dfile, "r")

        if "diverged" in mfile.keys():
            if mfile["diverged"][0] == 1:
                log_and_raise(mfile["diverged_msg"][0], DivergenceError)

        for (im, mnt_data) in enumerate(self._monitor_data):
            mname = mnt_data.name
            mnt_data._load_fields(mfile[mname]["indspan"][0, :],
                            mfile[mname]["indspan"][1, :],
                            np.array(mfile[mname]["E"]),
                            np.array(mfile[mname]["H"]), 
                            self.symmetries, self.grid.Nxyz)
            mnt_data.xmesh = np.array(mfile[mname]["xmesh"])
            mnt_data.ymesh = np.array(mfile[mname]["ymesh"])
            mnt_data.zmesh = np.array(mfile[mname]["zmesh"])
            mnt_data.mesh_step = self.grid.mesh_step

        mfile.close()
        fmonitors = [mnt for mnt in self.monitors
                            if isinstance(mnt, FreqMonitor)]
        if len(fmonitors) > 0:
            if len(self.sources) > 0: 
                self.source_norm(self.sources[0])
                logging.info(
                    "Applying source normalization to all frequency "
                    "monitors using source index 0.\nTo revert, "
                    "use Simulation.source_norm(None)."
                    )
                if len(self.sources) > 1:
                    logging.info(
                        "To select a different source for the normalization: "
                        "Simulation.source_norm(source)."
                        )