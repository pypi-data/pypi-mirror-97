import numpy as np

def dot_product(fields1, fields2, mesh_step):
    """Dot product between the mode and an arbitrary field distribution, 
    in units of power. Or, if the ``Mode`` object is normalized such that 
    (self, self) = 1, then |(self, fields)|^2 is the fraction of 
    the total power carried by the fields that is specifically carried by 
    ``Mode``.
    
    Parameters
    ----------
    fields1 : tuple
        A tuple of (E, H) fields. Each field is array_like of shape 
        ``(3, Nx, Ny)``, with ``z`` assumed to be the propagation direction.
    fields2 : tuple 
        A second tuple of (E, H) fields, with the same shape as ``fields1``.
    mesh_step : tuple
        dx, dy, dz: mesh step in each direction.
    
    Returns
    -------
    float
        The overlap integral between the ``fields1`` and ``fields2``.
    """

    E1 = fields1[0][:2, :, :]
    H1 = fields1[1][:2, :, :]
    E2 = fields2[0][:2, :, :]
    H2 = fields2[1][:2, :, :]

    cross = np.cross(np.conj(E1), H2, axis=0) + \
            np.cross(E2, np.conj(H1), axis=0)
            
    return 1/4*np.sum(cross)*np.prod(mesh_step[:2])