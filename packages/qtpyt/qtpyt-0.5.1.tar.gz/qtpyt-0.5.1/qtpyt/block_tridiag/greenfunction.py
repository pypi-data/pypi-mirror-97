from qtpyt.block_tridiag.btmatrix import (empty_buffer, BTMatrix)
from qtpyt.block_tridiag import solvers

from math import pi


class GreenFunction:
    """Block Tridiagonal Green's Function.
    
    Allows to compute observables for a scattering region
    embedded in an environment described by selfenergies.
    The Hamiltonian and the Overlap are given as two lists
    containing the diagonal and upper diagonal block-matrices.

    Args:
        hs_list_ii : (list(xp.ndarray(complex, shape=(2,m,m))), len=N)
            List of block matrices on the diagonal. 

                hs_list_ii[i][0] = Hamilton-block[0,0]
                hs_list_ii[i][1] = Overlap-block[0,0]
            
        hs_list_ii : (list(xp.ndarray(complex, shape=(2,m,m))), len=N-1)
            List of block matrices on the upper diagonal. 

                hs_list_ij[i][0] = Hamilton-block[0,1]
                hs_list_ij[i][1] = Overlap-block[0,1]

        selfenergies : (list(block, indices, selfenergy))
            List of selfenergies that couple to this Hamiltonian.

                Hamiltonian[block, block][indices] << selfenergy

        solver : ('str')
            One of the solvers available in Solver given as string. 
            Used to compute selected parts of the Green's function.
            (i.e. invert the matrix.)

    """
    def __init__(self, hs_lists_ii, hs_lists_ij, selfenergies=[], eta=1e-5, solver='spectral'):

        self.hs_list_ii = hs_lists_ii
        self.hs_list_ij = hs_lists_ij

        self.selfenergies = selfenergies
        self.energy = None
        self.eta = eta

        # NOTE this block is called before
        # constructing H and S (see below)
        # to allow offloading the blocks to GPU.
        Solver = solvers.__dict__.get(solver.capitalize(), None)
        assert Solver is not None, "Invalid solver."
        self.solver = Solver(self)

        # Here the Hamiltonian and Overlap may be on GPU.
        def _fill(buffer, i):
            buffer.m_qii[0] = self.hs_list_ii[0][i]
            for q in range(1,buffer.N):
                buffer.m_qii[q] = self.hs_list_ii[q][i]
                buffer.m_qij[q-1] = self.hs_list_ij[q-1][i]
                buffer.m_qji[q-1] = self.hs_list_ij[q-1][i].T

        S = empty_buffer(len(hs_lists_ii))
        H = empty_buffer(len(hs_lists_ii))
        
        _fill(S, 1)
        _fill(H, 0)

        self.S = BTMatrix(S.m_qii, S.m_qij, S.m_qji)
        self.H = BTMatrix(H.m_qii, H.m_qij, H.m_qji)

    @property
    def eta(self):
        return self._eta

    @eta.setter
    def eta(self, eta):
        """The Schroeadinger equation for a coupled system
        should have the same eta. Hence, the default is to
        recursively modify the eta in all selfenergies."""
        self._eta = eta
        for i, (block, selfenergy) in enumerate(self.selfenergies):
            selfenergy.eta = eta

    def get_transmission(self, energy):
        return self.solver.get_transmission(energy)

    def retarded(self, energy, inverse=False):
        return self.solver.retarded(energy)

    def get_dos(self, energy):
        G = self.retarded(energy)
        return - 1/pi * - G.dottrace(self.S).imag

    def get_pdos(self, energy):
        G = self.retarded(energy)
        return - 1/pi * - G.dotdiag(self.S).imag

    # def add_screening(self, V):
    #     if not hasattr(self, 'V'):
    #         self.V = np.zeros(self.nbf)
    #     assert V.size == self.nbf
    #     #Add screening and remove (if exists) current.
    #     h_qii = self.hs_list_ii[0]
    #     if sum(self.V) != 0:
    #         add_diagonal(h_qii, - self.V)
    #     self.V[:] = V
    #     add_diagonal(h_qii, self.V)


    # def remove_screening(self):
    #     h_qii = self.hs_list_ii[0]
    #     add_diagonal(h_qii, -self.V)
    #     self.V[:] = 0.