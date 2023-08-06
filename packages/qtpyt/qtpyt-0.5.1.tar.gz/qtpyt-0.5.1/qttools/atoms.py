import numpy as np
from functools import reduce

from ase.data import covalent_radii
from ase.neighborlist import NeighborList
import ase.neighborlist


def add_hydrogens(atoms):
    """Add hydrogens to organic structure."""
    cov_radii = [covalent_radii[a.number] for a in atoms]
    nl = NeighborList(cov_radii, bothways = True, self_interaction = False)
    nl.update(atoms)

    need_a_H = []
    for a in atoms:
        nlist=nl.get_neighbors(a.index)[0]
        if len(nlist)<3:
            if a.symbol=='C':
                need_a_H.append(a.index)

    print("Added missing Hydrogen atoms: ", need_a_H)

    dCH=1.1
    for a in need_a_H:
        vec = np.zeros(3)
        indices, offsets = nl.get_neighbors(atoms[a].index)
        for i, offset in zip(indices, offsets):
            vec += -atoms[a].position +(atoms.positions[i] + np.dot(offset, atoms.get_cell()))
        vec = -vec/np.linalg.norm(vec)*dCH
        vec += atoms[a].position
        htoadd = ase.Atom('H',vec)
        atoms.append(htoadd)


def apply_order(atoms, indices):
    """Permute indices of atoms inplace."""
    for name, a in atoms.arrays.items():
        atoms.arrays[name] = a[indices]


def sort(atoms, order='xyz', round=1):
    """Sort atoms by positions.

    Args:
        atoms : (ase.Atoms object)
        order : (str) any permutation of 'xyz'
            i.e. 'xyz' means first along 'x', then along 'y'
            and eventually along 'z'.
        round : (int) 
            round atomic position to `round` digits.
    
    Returns:
        sorted atoms.
    """
    positions = atoms.positions.round(round)
    i = order.index('x')
    j = order.index('y')
    k = order.index('z')
    indices = np.lexsort((positions[:,k],positions[:,j],positions[:,i]))
    return atoms[indices]
    

def expand(atoms, n_uc, n_rep, direction='x', sides=[0, 1], round=1):
    """Expand atoms along one direction with terminating atoms.

    Args:
        atoms : (ase.Atoms object)
        n_uc : (int)
            Number of (unit-cell) atoms at the termini to
            include in the expansion.
        n_rep : (int)
            Number of times to repeat the subset of `n_uc` atoms.
        direction : (char)
            Direction along which to perform the expansion.
        sides : (int, list, tuple)
            Whether to expand to the left, right of both ends.
            left  only  - 0
            right only  - 1
            left and right - [0,1]
        round : (int) see sort
    """
    if not atoms.cell.orthorhombic:
        raise NotImplementedError('Cell must be orthorhombic')

    if isinstance(sides, int):
        sides = [sides]

    dirs = [0,1,2]
    d = dirs.pop('xyz'.index(direction))
    order = str(reduce(str.__add__, ['xyz'[i] for i in [d]+dirs])) 
    atoms = sort(atoms, order, round)
    
    cell = atoms.cell[d,d] 
    uc_cell = (atoms[0].position[d] + cell) - atoms[-n_uc].position[d]
    
    for n in range(n_rep):

        uc_ldl = atoms[-n_uc:]
        uc_ldr = atoms[:n_uc]

        uc_ldr.positions[:,d] += cell
        uc_ldl.positions[:,d] -= cell

        if 0 in sides:
            atoms = uc_ldl + atoms
            atoms.cell[d,d] += uc_cell
        if 1 in sides:
            atoms = atoms + uc_ldr
            atoms.cell[d,d] += uc_cell

        atoms.center()
        atoms = sort(atoms, direction)
    return atoms
