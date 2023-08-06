import numpy as np

from ..utils import inside_box, inside_box_inds, cs2span, listify, list2str
from ..utils import log_and_raise
from ..utils.check import check_3D_lists
from ..constants import int_, float_, fp_eps, xyz_list, xyz_dict, C_0

class Monitor(object):
    """Base class for defining field monitors.
    """
    def __init__(self, center, size, field, name=None):
        """Base constructor. Available subclasses:

        - :class:`.TimeMonitor`
        - :class:`.FreqMonitor`
        - :class:`.ModeMonitor`
        """
        check_3D_lists(center=listify(center), size=listify(size))
        self.center = np.array(center)
        self.size = np.array(size)
        self.span = cs2span(self.center, self.size)
        self.field = []
        for f in listify(field):
            if f.lower() in ['e', 'h']:
                self.field.append(f.lower())
            else:
                log_and_raise(
                    f"Unrecognized field {f}. Valid values are 'E' and 'H'.",
                    ValueError
                )

        self.name = None if name is None else str(name)

    def _inside(self, mesh):
        """ Get a mask equal to one if a point is inside the monitor region, 
        and zero if outside.
        
        Parameters
        ----------
        mesh : 3-tuple
            Defines the x, y, and z mesh. 
        """
        return inside_box(self.span, mesh, include_zero_size=True)

    def _inside_inds(self, mesh):
        """ Get indexes of the points at which the fields are to be recored.
        
        Parameters
        ----------
        mesh : 3-tuple
            Defines the x, y, and z mesh. 
        
        Returns
        -------
        Pinds : np.ndarray
            An array of shape (Np, 3), where Np is the total number of mesh 
            points in the monitor region.
        """
        inds = inside_box_inds(self.span, mesh, include_zero_size=True)
        indsm = np.meshgrid(np.arange(inds[0][0], inds[0][1]), 
                            np.arange(inds[1][0], inds[1][1]),
                            np.arange(inds[2][0], inds[2][1]),
                            indexing='ij')
        if indsm[0].size==0: 
            return np.zeros((0, 3), dtype=int_)

        return np.stack([inds.ravel() for inds in indsm], axis=1).astype(int_)

class TimeMonitor(Monitor):
    """Monitor recording the time-domain fields within a 3D region.
    """

    def __init__(self, center, size, t_start=0, t_stop=None, 
                    field=['E', 'H'], name=None):
        """ Construct.
        
        Parameters
        ----------
        center : array_like
            (micron) x, y, and z position of the center of the Monitor.
        size : array_like
            (micron) Size in x, y, and z.
        t_start : float, optional
            (second) Starting time of field recording.
        t_stop : float, optional
            (second) Stopping time of field recording. If ``None``, record 
            until the end of the simulation.
        field : list, optional
            List of fields to be recorded. Valid entries are 
            ``'E'`` and ``'H'``.
        name : str, optional
            Custom name of the monitor.

        Note
        ----
        Time monitors can result in very large amounts of data if defined over 
        a large spatial region. Recommended usage is either recording the full 
        time evolution of a single point in space, or using ``t_start`` and 
        ``t_stop`` to record just a few time steps of a larger region. 
        """
        super().__init__(center, size, field)
        self.t_start = t_start
        self.t_stop = t_stop

    def __repr__(self):
        rep = "Tidy3D TimeMonitor: {\n"
        rep += "name     = %s\n"%self.name
        rep += "center   = %s\n" % list2str(self.center, "%1.4f")
        rep += "size     = %s\n" % list2str(self.size, "%1.4f")
        rep += "t_start  = %1.2e,\n"%self.t_start
        if self.t_stop is None:
            rep += "t_stop   = None\n"
        else:
            rep += "t_stop   = %1.2e,\n"%self.t_stop

        rep += "Store E:  %s\n"%('e' in self.field)
        rep += "Store H:  %s\n"%('h' in self.field)
        rep += "}\n"

        return rep

class FreqMonitor(Monitor):
    """Monitor recording a discrete Fourier transform of the fields within a 
    3D region, for a given list of frequencies.
    """
    
    def __init__(self, center, size, freqs, field=['E', 'H'], name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            (micron) x, y, and z position of the center of the Monitor.
        size : array_like
            (micron) Size in x, y, and z.
        freqs : float or array_like
            Frequencies at which the fields are sampled.
        field : list, optional
            List of fields to be recorded. Valid entries are 
            ``'E'`` and ``'H'``.
        name : str, optional
            Custom name of the monitor.
        """

        super().__init__(center, size, field, name)
        self.freqs = listify(freqs)
        self.lambdas = C_0 / np.array(freqs)

    def __repr__(self):
        rep = "Tidy3D FreqMonitor: {\n"
        rep += "name     = %s\n"%self.name
        rep += "center   = %s\n" % list2str(self.center, "%1.4f")
        rep += "size     = %s\n" % list2str(self.size, "%1.4f")
        rep += "freqs    = %s\n" % list2str(self.freqs, "%1.2e")

        rep += "Store E:  %s\n"%('e' in self.field)
        rep += "Store H:  %s\n"%('h' in self.field)
        rep += "}\n"

        return rep

class ModeMonitor(FreqMonitor):
    """ :class:`.FreqMonitor` subclass defining a 2D plane in which the recorded 
    frequency-domain fields can be decomposed into propagating eigenmodes.
    """
    
    def __init__(self, center, size, freqs, name=None):
        """ Construct.

        Parameters
        ----------
        center : array_like
            (micron) 3D vector defining the center of the 2D plane.
        size : array_like
            (micron) 3D vector defining the size of the 2D plane. Exactly one 
            of the values must be ``0``, defining the normal direction.
        freqs : float or list of float
            Frequencies at which the fields are sampled.
        name : str, optional
            Custom name of the monitor.
        """

        # Get normal direction from size
        self.norm_ind = np.nonzero(size < fp_eps)[0]
        if self.norm_ind.size !=1:
            log_and_raise(
                "Exactly one element of ModeMonitor 'size' must be zero.",
                ValueError
            )
            
        self.norm_ind = int(self.norm_ind)
        self.normal = xyz_list[self.norm_ind]

        super().__init__(center, size, freqs, field=['E', 'H'], name=name)

    def __repr__(self):
        rep = "Tidy3D ModeMonitor: {\n"
        rep += "name     = %s\n"%self.name
        rep += "normal   = %s\n"%self.normal
        rep += "center   = %s\n" % list2str(self.center, "%1.4f")
        rep += "size     = %s\n" % list2str(self.size, "%1.4f")
        rep += "freqs    = %s\n" % list2str(self.freqs, "%1.2e")
        rep += "}\n"

        return rep