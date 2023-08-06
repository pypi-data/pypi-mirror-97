import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

from ..constants import EPSILON_0, ETA_0, C_0, MU_0
from .derivatives import compute_derivative_matrices
from .Mode import Mode

def compute_modes(eps_cross, freq, mesh_step, pml_layers, num_modes=1):
    """Solve for the modes of a waveguide cross section.
    
    Parameters
    ----------
    eps_cross : array_like or tuple of array_like
        Either a single 2D array defining the relative permittivity in the 
        cross-section, or three 2D arrays defining the permittivity at the Ex, 
        Ey, and Ez locations of the Yee cell, respectively.
    freq : float
        (Hertz) Frequency at which the eigenmodes are computed.
    mesh_step : list or tuple of float
        (micron) Step size in x, y and z. The mesh step in z is currently 
        unused, but it could be needed if numerical dispersion is to be taken 
        into account.
    pml_layers : list or tuple of int
        Number of pml layers in x and y.
    num_modes : int, optional
        Number of modes to be computed.
    
    Returns
    -------
    list of dict
        A list of all the computed modes. Each entry is a dictionary with the 
        real and imaginary part of the effective index of the waveguide and 
        all the E and H field components.
    """
    omega = 2*np.pi*freq
    k0 = omega / C_0

    dt = 7.281106e-17
    # k0 = np.sin(dt*omega/2)/dt*2/C_0

    if isinstance(eps_cross, np.ndarray):
        eps_xx, eps_yy, eps_zz = [eps_cross]*3
    else:
        eps_xx, eps_yy, eps_zz = eps_cross

    Nx, Ny = eps_xx.shape
    N = eps_xx.size

    matrices = compute_derivative_matrices(omega, (Nx, Ny), tuple(pml_layers), 
                                            tuple(mesh_step[:2]))

    # Normalize by k0 to match the EM possible notation
    Dxf, Dxb, Dyf, Dyb = [mat/k0 for mat in matrices]

    inv_eps_zz = sp.spdiags(1/eps_zz.flatten(), [0], N, N)
    P11 = -Dxf.dot(inv_eps_zz).dot(Dyb)
    P12 = Dxf.dot(inv_eps_zz).dot(Dxb) + sp.eye(N)
    P21 = -Dyf.dot(inv_eps_zz).dot(Dyb) - sp.eye(N)
    P22 = Dyf.dot(inv_eps_zz).dot(Dxb)
    Q11 = -Dxb.dot(Dyf)
    Q12 = Dxb.dot(Dxf) + sp.spdiags(eps_yy.flatten(), [0], N, N)
    Q21 = -Dyb.dot(Dyf) - sp.spdiags(eps_xx.flatten(), [0], N, N)
    Q22 = Dyb.dot(Dxf)

    Pmat = sp.bmat([[P11, P12], [P21, P22]])
    Qmat = sp.bmat([[Q11, Q12], [Q21, Q22]])
    A = Pmat.dot(Qmat)

    n_max = np.sqrt(np.max(eps_cross))
    vals, vecs = solver_eigs(A, num_modes, guess_value=-n_max**2)
    vre, vim = -np.real(vals), -np.imag(vals)

    # Sort by descending real part
    sort_inds = np.argsort(vre)[::-1]
    vre = vre[sort_inds]
    vim = vim[sort_inds]
    vecs = vecs[:, sort_inds]

    # Real and imaginary part of the effective index
    neff_tmp = np.sqrt(vre/2 + np.sqrt(vre**2 + vim**2)/2)
    keff = vim/2/(neff_tmp + 1e-10)

    # Correct formula taking numerical dispersion into account
    # neff = 2/mesh_step[2]*np.arcsin((neff_tmp + 1j*keff)*mesh_step[2]/2)
    neff = neff_tmp

    # Field components from eigenvectors
    Ex = vecs[:N, :]
    Ey = vecs[N:, :]

    # Get the other field components; normalize according to CEM
    Hs = -Qmat.dot(vecs)/(neff + 1j*keff)[np.newaxis, :]/ETA_0
    Hx = Hs[:N, :]
    Hy = Hs[N:, :]

    Hz = Dxf.dot(Ey) - Dyf.dot(Ex)
    Ez = inv_eps_zz.dot((Dxb.dot(Hy) - Dyb.dot(Hx)))

    # Store all the information about the modes.
    modes = []
    for im in range(num_modes):
        E = np.array([Ex[:, im].reshape(Nx, Ny),
                        Ey[:, im].reshape(Nx, Ny),
                        Ez[:, im].reshape(Nx, Ny)])
        H = np.array([Hx[:, im].reshape(Nx, Ny),
                        Hy[:, im].reshape(Nx, Ny),
                        Hz[:, im].reshape(Nx, Ny)])
        modes.append(Mode(E, H, neff[im], keff[im]))

    if vals.size == 0:
        raise RuntimeError("Could not find any eigenmodes for this waveguide")

    return modes

def solver_eigs(A, num_modes, guess_value=1.0):
    """ Find ``num_modes`` eigenmodes of ``A`` cloest to ``guess_value``.

    Parameters
    ----------
    A : scipy.sparse matrix
        Square matrix for diagonalization.
    num_modes : int
        Number of eigenmodes to compute.
    guess_value : float, optional
    """

    values, vectors = spl.eigs(A, k=num_modes, sigma=guess_value)
    return values, vectors