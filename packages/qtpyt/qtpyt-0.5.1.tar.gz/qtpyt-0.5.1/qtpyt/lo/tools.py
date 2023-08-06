import numpy as np
from math import sqrt
from scipy import linalg as la


dagger = lambda mat: np.conj(mat.T)


def rotate_matrix(h, u):
    return np.dot(u.T.conj(), np.dot(h, u))


def get_subspace(matrix, index):
    """Get the subspace spanned by the basis function listed in index"""
    assert matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]
    return matrix.take(index, 0).take(index, 1)


def normalize(matrix, S=None):
    """Normalize column vectors.

    ::

      <matrix[:,i]| S |matrix[:,i]> = 1

    """
    for col in matrix.T:
        if S is None:
            col /= np.linalg.norm(col)
        else:
            col /= np.sqrt(np.dot(col.conj(), np.dot(S, col)))


def get_orthonormal_subspace(h_ii, s_ii, index_j=None):
    """Get orthonormal eigen-values and -vectors of subspace j."""
    if index_j is not None:
        h_sub_jj  = get_subspace(h_ii, index_j)
        s_sub_jj  = get_subspace(s_ii, index_j)
    else:
        h_sub_jj = h_ii
        s_sub_jj = s_ii
    e_j, v_jj = np.linalg.eig(np.linalg.solve(s_sub_jj, h_sub_jj))
    normalize(v_jj, s_sub_jj)  # normalize: <v_j|s|v_j> = 1
    permute_list = np.argsort(e_j.real)
    e_j = np.take(e_j, permute_list)
    v_jj = np.take(v_jj, permute_list, axis=1)
    return v_jj, e_j


def subdiagonalize(h_ii, s_ii, index_j):
    """Subdiagonalize a block in the Hamiltonian."""
    nb = h_ii.shape[0]
    nb_sub = len(index_j)
    v_jj, e_j = get_orthonormal_subspace(h_ii, s_ii, index_j)
    # Setup transformation matrix
    c_ii = np.identity(nb, h_ii.dtype)
    for i in range(nb_sub):
        for j in range(nb_sub):
            c_ii[index_j[i], index_j[j]] = v_jj[i, j]

    h1_ii = rotate_matrix(h_ii, c_ii)
    s1_ii = rotate_matrix(s_ii, c_ii)

    return h1_ii, s1_ii, c_ii, e_j


def subdiagonalize_atoms(basis, h_ii, s_ii, a=None):
    """Get rotation matrix for subdiagonalization of given(all) atoms."""
    from scipy.linalg import block_diag
    if a is None:
        a = range(len(basis.atoms))
    if isinstance(a, int):
        a = [a]
    U_mm = []
    e_aj = []
    na_tot = len(basis.atoms)
    for a0 in range(na_tot):
        bfs = basis.get_indices(a0)
        if a0 in a:
            v_jj, e_j = get_orthonormal_subspace(h_ii,s_ii,bfs)
            U_mm.append(v_jj)
            e_aj.append(e_j)
        else:
            U_mm.append(np.eye(len(bfs)))
    U_mm = block_diag(*U_mm)
    return U_mm, e_aj


def cutcoupling(h, s, index_n):
    for i in index_n:
        s[:, i] = 0.0
        s[i, :] = 0.0
        s[i, i] = 1.0
        Ei = h[i, i]
        h[:, i] = 0.0
        h[i, :] = 0.0
        h[i, i] = Ei


def lowdin_rotation(h, s, index_j=None):
    if index_j:
        s_jj = get_subspace(s, index_j)
    else:
        s_jj = s
    eig, U_jj = np.linalg.eigh(s_jj)
    eig = np.abs(eig)
    U_jj = np.dot(U_jj / np.sqrt(eig), dagger(U_jj))
    return U_jj


def get_U1(bfs_m, bfs_i, c_MM=None):
    """Get rotation matrix to extract sub-block defined 
    by matrix indices `bfs_m` to the bottom rigth of the 
    matrix. If a rotation c_MM is given apply permutation to c_MM.

    """
    nbf = len(bfs_m) + len(bfs_i)
    if c_MM is None:
        c_MM = np.eye(nbf)
    U1 = np.take(c_MM, np.concatenate([bfs_i, bfs_m]), axis=1)
    """If apply is True permute inplace bfs_m bfs_i"""
    bfs_m[:] = range(nbf-len(bfs_m), nbf)
    bfs_i[:] = range(nbf-len(bfs_m))
    return U1, bfs_m, bfs_i


def get_U2(s1_MM, bfs_m, bfs_i):
    """Get rotation matrix that orthogonalizes sub-blocks spanned
    by indices `bfs_m` and `bfs_i`, respectively.
    
    """
    nbf = len(bfs_m) + len(bfs_i)
    s_mm = get_subspace(s1_MM, bfs_m)
    s_mi = s1_MM.take(bfs_m,axis=0).take(bfs_i,axis=1)
    U_mi = - np.linalg.inv(s_mm).dot(s_mi)
    U2 = np.eye(s1_MM.shape[0])
    U2[np.ix_(bfs_m,bfs_i)] = U_mi
    return U2


def get_U2T(s1_MM, bfs_m, bfs_i):
    """Get rotation matrix that orthogonalizes sub-blocks spanned
    by indices `bfs_m` and `bfs_i`, respectively.
    
    """
    nbf = len(bfs_m) + len(bfs_i)
    s_ii = get_subspace(s1_MM, bfs_i)
    s_im = s1_MM.take(bfs_i,axis=0).take(bfs_m,axis=1)
    U_im = - np.linalg.inv(s_ii).dot(s_im)
    U2T = np.eye(s1_MM.shape[0])
    U2T[np.ix_(bfs_i,bfs_m)] = U_im
    return U2T


def extract_orthogonal_subspaces(h_MM, s_MM, bfs_m, c_MM=None, T=False):
    nbf = h_MM.shape[0]
    bfs_i = np.setdiff1d(range(nbf), bfs_m)
    U1, bfs_m, bfs_i = get_U1(bfs_m, bfs_i, c_MM)
    h1_MM = rotate_matrix(h_MM, U1)
    s1_MM = rotate_matrix(s_MM, U1)
    U2 = get_U2(s1_MM, bfs_m, bfs_i) if not T else get_U2T(s1_MM, bfs_m, bfs_i)
    h2_MM = rotate_matrix(h1_MM, U2)
    s2_MM = rotate_matrix(s1_MM, U2)
    hs_mm, hs_ii, hs_im = split_subspaces(h2_MM, s2_MM, bfs_m, bfs_i)
    U = U1.dot(U2)
    return hs_mm, hs_ii, hs_im, U

                 
def split_subspaces(h_MM, s_MM, bfs_m, bfs_i):
    nbf = h_MM.shape[0]
    h_ii = get_subspace(h_MM, bfs_i)
    s_ii = get_subspace(s_MM, bfs_i)
    h_mm = get_subspace(h_MM, bfs_m)
    s_mm = get_subspace(s_MM, bfs_m)
    h_im = h_MM.take(bfs_i,axis=0).take(bfs_m,axis=1)
    s_im = s_MM.take(bfs_i,axis=0).take(bfs_m,axis=1)
    return (h_mm, s_mm), (h_ii, s_ii), (h_im, s_im)


def flatten(iterables):
    return (elem for iterable in iterables for elem in iterable)


def get_orthogonal_subspaces(basis, h_MM, s_MM, a=None, cutoff=np.inf):
    """Split matrix in hybridization and active spaces.
       Active space contains orbital(s) of atom(s) a with
       abs(energy) < cutoff"""
    nbf = len(h_MM)
    c_MM, e_aj = subdiagonalize_atoms(basis, h_MM, s_MM, a)
    bfs_imp = basis.get_indices(a)
    bfs_m = [bfs_imp[i] for i, eigval in enumerate(flatten(e_aj)) if abs(eigval)<cutoff]
    return extract_orthogonal_subspaces(h_MM, s_MM, bfs_m, c_MM)


def order_transform(basis, groups=None, nuc=None):
    """Order orbital indices using group of atoms and atomic elements.
    
    For each subset of atoms, group the atoms of the same kind and order
    the orbital indices in scending order. When both `groups` and `nuc` 
    are None, treat the whole set of atoms as a single group.

    Args:
        basis : (Basis object)
        groups : (list of lists) 
            List of the atoms in each group.
        nuc : (int)
            Number of sequential unit cells in atoms.
            Each unit cell is considered a group.
    """
    atoms = basis.atoms
    symbols = atoms.symbols

    elements = set(symbols)
    natoms = len(atoms)
    
    if groups is not None:
        try:
            groups[0][0]
        except IndexError:
            raise ValueError('`groups` must be a list of lists of atoms in each group.')
        nuc = len(groups)
        range_uc = lambda uc: groups[uc]
    else:
        if nuc is not None:
            if not natoms%nuc==0.:
                raise ValueError('Number of unit cells are not a dividend of atoms.')
            nuc_atoms = natoms//nuc;
        else:
            nuc = 1
            nuc_atoms = natoms
        range_uc = lambda uc: range(uc*nuc_atoms, (uc+1)*nuc_atoms)
    
    indices = []
    for uc in range(nuc):
        indices.append(list(
            list(filter(
                lambda a: symbols[a]==elem, range_uc(uc)
                )) for elem in elements))
    
    perm_indices = []
    for uc in indices:
        for elem in uc:
            perm_indices.extend(
                basis.get_indices(elem).reshape(len(elem),-1).T.flatten())
    
    U = np.eye(basis.nao).take(perm_indices, axis=1)
    return U, indices


def get_ll_mm_rr(H, S, nbf_l, nbf_m, nbf_r):
    rng_l = list(range(nbf_l))
    rng_m = list(range(nbf_l,nbf_l+nbf_m))
    rng_r = list(range(nbf_l+nbf_m,nbf_l+nbf_m+nbf_r))
    s_lm = S.take(rng_l,0).take(rng_m,1)
    h_lm = H.take(rng_l,0).take(rng_m,1)
    s_rm = S.take(rng_r,0).take(rng_m,1)
    h_rm = H.take(rng_r,0).take(rng_m,1)
    h_mm = get_subspace(H, rng_m)
    s_mm = get_subspace(S, rng_m)
    return (h_lm, s_lm), (h_mm, s_mm), (h_rm, s_rm)


def get_lead_orthogonal(greenfunction):
    s_ll = greenfunction.selfenergies[0].s_ii
    s_rr = greenfunction.selfenergies[1].s_ii
    h_ll = greenfunction.selfenergies[0].h_ii
    h_rr = greenfunction.selfenergies[1].h_ii
    s_lm = greenfunction.selfenergies[0].s_im
    s_rm = greenfunction.selfenergies[1].s_im
    h_lm = greenfunction.selfenergies[0].h_im
    h_rm = greenfunction.selfenergies[1].h_im
    h_mm = greenfunction.H
    s_mm = greenfunction.S
    nbf_l = len(h_ll)
    nbf_r = len(h_rr)
    nbf_m = len(h_mm)
    s_ml = dagger(s_lm)
    s_mr = dagger(s_rm)
    h_ml = dagger(h_lm)
    h_mr = dagger(h_rm)
    U_lm = - la.inv(s_ll).dot(s_lm)
    U_rm = - la.inv(s_rr).dot(s_rm)
    U = np.array(block([[np.eye(nbf_l),U_lm,0],[0,np.eye(nbf_m),0],[0,U_rm,np.eye(nbf_r)]]))
    S = np.array(block([[s_ll,s_lm,0],[s_ml,s_mm,s_mr],[0,s_rm,s_rr]]))
    H = np.array(block([[h_ll,h_lm,0],[h_ml,h_mm,h_mr],[0,h_rm,h_rr]]))
    S = rotate_matrix(S,U)
    H = rotate_matrix(H,U)
    return get_ll_mm_rr(H, S, nbf_l, nbf_m, nbf_r)