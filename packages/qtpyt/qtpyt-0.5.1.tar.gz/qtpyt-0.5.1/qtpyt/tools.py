import numpy as np

def remove_pbc(basis, A_kMM, direction='x', eps=-1e-3):
    """Mask matrix elements above diagonal along `direction`.

    """

    # Transport direction
    p_dir = 'xyz'.index(direction)

    L = basis.atoms.cell[p_dir, p_dir]

    cutoff = L/2 - eps
    # Coordinates of central unit cell i (along transport)
    centers_p_i = basis.centers[:, p_dir]
    # Coordinates of neighbooring unit cell j
    # centers_p_j = centers_p_i + L
    # Distance between j atoms and i atoms
    dist_p_ji = np.abs(centers_p_i[:, None] - centers_p_i[None, :])
    # Mask j atoms farther than L
    mask_ji = (dist_p_ji < cutoff).astype(A_kMM.dtype)

    A_kMM *= mask_ji[None, :]