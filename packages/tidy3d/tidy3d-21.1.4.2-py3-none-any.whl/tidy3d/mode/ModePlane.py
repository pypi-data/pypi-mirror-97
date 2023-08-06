import numpy as np
from ..constants import float_
from ..utils import inside_box_inds, listify, log_and_raise
from .solver import compute_modes
from .dot_product import dot_product

class ModePlane(object):
    """2D plane for computation of modes used in ModeSource and ModeMonitor. The 
    coordinate system with respect to which meshes and fields are defined here 
    is always such that the z-axis is normal to the plane.
    """
    def __init__(self, span, norm_ind):
        """Construct.
        
        Parameters
        ----------
        span : np.ndarray of shape (3, 2)
            (micron) Defines (xmin, xmax), (ymin, ymax), (zmin, zmax) of the 
            mode plane.
        norm_ind : int
            Specifies the normal direction. We must then also have 
            ``span[mode_ind, 0] = span[mode_ind, 1]``.
        """
        self.span = span
        self.norm_ind = norm_ind
        self.cross_inds = [0, 1, 2]
        self.cross_inds.pop(self.norm_ind)

        """Variables below to be set after based on the Simulation object to 
        which the ModePlane is added. """

        # Permittivity and mesh at the center of the Yee cell.
        self.mesh = None
        self.eps = None
        # Permittivity and mesh for field components along the two 
        # cross-section directions and the normal direction
        self.mesh_e1 = None
        self.eps_e1 = None
        self.mesh_e2 = None
        self.eps_e2 = None
        self.mesh_en = None
        self.eps_en = None

        """List of modes, set by a call to ``compute_modes()``. The first list 
        dimension is equal to the number of sampling frequencies, while the 
        second dimension is the number of computed modes. Each mode is given by 
        a dictionary with the fields and propagation constants."""
        self.modes = [[]]
        self.freqs = []

    def _set_eps(self, sim):
        """ Set the mesh of the ModePlane based on a global simulation mesh, 
        and the indexing of that mesh w.r.t. the simulation grid.
        """
        indsx, indsy, indsz = inside_box_inds(self.span, sim.grid.mesh,
                                            include_zero_size=True)
        if np.any([inds[0]==inds[1] for inds in (indsx, indsy, indsz)]):
            log_and_raise(
                "Mode plane position is outside simulation domain.",
                ValueError
            )

        """Array of shape (3, 2) of int defining the starting and stopping 
        index in the global simulation grid of the ModePlane span."""
        self.span_inds = np.array([[inds[0], inds[1]] 
                                    for inds in (indsx, indsy, indsz)])

        # Space and time resolution from global grid.
        self.mesh_step = (sim.grid.mesh_step[self.cross_inds[0]], 
                     sim.grid.mesh_step[self.cross_inds[1]],
                     sim.grid.mesh_step[self.norm_ind])
        self.time_step = sim.grid.dt

        meshes = []
        epses = []
        sim_ms = [sim.grid.mesh, sim.grid.mesh_ex,
                    sim.grid.mesh_ey, sim.grid.mesh_ez]
        for im, mesh in enumerate(sim_ms):
            # Average the edges for the Yee grid coordinates, otherwise 
            # include them in eps (used for plotting)
            edges = 'average' if im > 0 else 'in'
            plane_mesh = (mesh[0][indsx[0]:indsx[1]],
                          mesh[1][indsy[0]:indsy[1]],
                          mesh[2][indsz[0]:indsz[1]])
            meshes.append([plane_mesh[self.cross_inds[0]], 
                          plane_mesh[self.cross_inds[1]],
                          plane_mesh[self.norm_ind]])
            eps = sim._get_eps(plane_mesh, edges=edges)
            if np.prod(eps.shape)== 0 or np.count_nonzero(eps.shape==1) > 1:
                log_and_raise(
                    "Mode plane cross-section size too small.",
                    ValueError
                )
            epses.append(np.squeeze(eps))

        self.mesh = meshes[0]
        self.mesh_e1 = meshes[1 + self.cross_inds[0]]
        self.mesh_e2 = meshes[1 + self.cross_inds[1]]
        self.mesh_en = meshes[1 + self.norm_ind]
        self.eps = epses[0]
        self.eps_e1 = epses[1 + self.cross_inds[0]]
        self.eps_e2 = epses[1 + self.cross_inds[1]]
        self.eps_en = epses[1 + self.norm_ind]

    def compute_modes(self, Nmodes, freqs, pml_layers=[0, 0]):
        """ Compute the ``Nmodes`` eigenmodes in decreasing order of 
        propagation constant at every frequency in the list ``freqs``.
        """

        if self.eps is None:
            raise ValueError("ModePlane object has not been added to a "
                            "simulation yet.")

        # Add a little bit of anisotropy to break potential degeneracy
        epses = [self.eps_e1, self.eps_e2 + 1e-6, self.eps_en]
        self.freqs = listify(freqs)
        self.modes = []
        for frequency in self.freqs:
            # Get modes
            modes = compute_modes(epses, frequency,
                                    mesh_step=self.mesh_step,
                                    pml_layers=pml_layers,
                                    num_modes=Nmodes)
            
            for mode in modes:
                # Normalize to unit power flux
                fields_cent = mode.fields_to_center()
                flux = dot_product(fields_cent, fields_cent, self.mesh_step)
                mode.E /= np.sqrt(flux)
                mode.H /= np.sqrt(flux)
                # Make largest E-component real
                mode.fix_efield_phase()

            self.modes.append(modes)