import numpy as np
from scipy.spatial.distance import cdist

from .kpts import (
                   monkhorst_pack, apply_inversion_symm, 
                   build_partial_kpts, partial_bloch_sum)

def remove_pbc(basis, A_kMM, direction='x', eps=-1e-3):
    """Mask matrix elements above diagonal connecting neighbors cells
    in parallel direction.

    """

    # Transport direction
    p_dir = 'xyz'.index(direction)

    L = basis.atoms.cell[p_dir, p_dir]

    cutoff = L - eps
    # Coordinates of central unit cell i (along transport)
    centers_p_i = basis.centers[:, p_dir]
    # Coordinates of neighbooring unit cell j
    centers_p_j = centers_p_i + L
    # Distance between j atoms and i atoms
    dist_p_ji = np.abs(centers_p_j[:, None] - centers_p_i[None, :])
    # Mask j atoms farther than L
    mask_ji = (dist_p_ji > cutoff).astype(A_kMM.dtype)

    A_kMM *= mask_ji[None, :]


def oder_indices(basis, N, order='xyz', positions=None):
    repeated = basis.repeat(N)
    if positions is not None:
        idx = cdist(repeated.centers, positions).argmin(1) 
        return repeated.get_index(idx)
    else:
        idx = repeated.argsort(order)
        return repeated.get_indices(idx)


def prepare_leads_matrices(basis, H_kMM, S_kMM, size, offset=(0.,0.,0.), direction='x'):
    """Prepare input matrices for PrincipalLayer.
    
    Args:
        basis : basis function descriptor.
        H_kMM : Hamiltonian matrices in k-space.
        S_kMM : Overlap matrices in k-space.
        size, offset : Monkhorst-Pack used to sample Brillouin Zone.
    """

    kpts = monkhorst_pack(size, offset)
    if kpts.shape[0] > H_kMM.shape[0]:
        # Switch to irreducible k-points
        kpts = apply_inversion_symm(kpts)[0]

    kpts_p, kpts_t = build_partial_kpts(size, offset, direction)

    p_dir = 'xyz'.index(direction)

    R = [0,0,0]
    H_kii = partial_bloch_sum(H_kMM, kpts, R, kpts_p, kpts_t)
    S_kii = partial_bloch_sum(S_kMM, kpts, R, kpts_p, kpts_t)

    R[p_dir] = 1
    H_kij = partial_bloch_sum(H_kMM, kpts, R, kpts_p, kpts_t)
    S_kij = partial_bloch_sum(S_kMM, kpts, R, kpts_p, kpts_t)

    # remove_pbc(basis, H_kij, direction)
    # remove_pbc(basis, S_kij, direction)

    return kpts_t, H_kii, S_kii, H_kij, S_kij


def prepare_central_matrices(basis, H_kMM, S_kMM, size, offset=(0.,0.,0.), direction='x'):
    """Prepare input matrices for PrincipalLayer.
    
    Args:
        basis : basis function descriptor.
        H_kMM : Hamiltonian matrices in k-space.
        S_kMM : Overlap matrices in k-space.
        size, offset : Monkhorst-Pack used to sample Brillouin Zone.
    """
    from qtpyt.tools import remove_pbc

    kpts = monkhorst_pack(size, offset)
    if kpts.shape[0] > H_kMM.shape[0]:
        # Switch to irreducible k-points
        kpts = apply_inversion_symm(kpts)[0]

    remove_pbc(basis, H_kMM, direction)
    remove_pbc(basis, S_kMM, direction)

    return kpts, H_kMM, S_kMM