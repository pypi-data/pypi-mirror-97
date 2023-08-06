import numpy as np

from ._recursive import get_G
from .unfold import bloch_unfold


class PrincipalLayer:
    """Principal Layer (PL) Green's function.
    
    Allows to compute a surface Green's Function for a supercell (SC)
    composed of a repeating principal layer (PL). The inputs are
    converged Hamiltonians and Overlaps for the PL evaluated at 
    tranverse k-points.
    
    """

    def __init__(self, kpts, hs_kii, hs_kij, Nr=None, eta=1e-5):
        """
        Args:
            kpts : np.ndarray (shape = (# of k-points, 3))
                tranverse k-points.
            hs_kii : (tuple, list)
                pointers to onsite Hamiltonians and Overlaps (at kpts).
            hs_kij : (tuple, list)
                pointers to coupling Hamiltonians and Overlaps (at kpts).
            Nr : tuple (size = (3,))
                # of transverse PLs.
                    
        """

        self.kpts = kpts
        self.h_kii, self.s_kii = hs_kii
        self.h_kij, self.s_kij = hs_kij
        self.Nr = Nr or self.Nk
        assert self.kpts.shape[1] == 3, "Invalid k-points. Must have (x,y,z) components."
        assert len(self.Nr) == 3, "Invalid # of transverse PLs. Must be (Nx, Ny, Nz)."

        self.h_ii = self.bloch_unfold(self.h_kii) # onsite supercell.
        self.s_ii = self.bloch_unfold(self.s_kii) # coupling to neighbor supercell.

        self.energy = None
        self.bias = 0.
        self.eta = eta

        self.G_kii = np.empty((kpts.shape[0],) + 2*(self.h_kii.shape[1],), complex)
        self.G = np.empty(2*(self.nbf_i,), complex) 

    @property
    def nbf_i(self):
        """# of supercell basis functions."""
        return self.h_ii.shape[0]

    @property
    def H(self): # Alias
        return self.h_ii

    @property
    def S(self): # Alias
        return self.s_ii

    @property
    def Nk(self):
        """# of transverse k-points"""
        return np.array([len(set(self.kpts[:,i])) for i in range(3)])

    def get_G(self, energy):
        """Get retarded Green function at specified energy."""
        if energy != self.energy:
            self.energy = energy
            get_G(self.G_kii, self.h_kii, self.s_kii, self.h_kij, 
                    self.s_kij, self.energy, self.eta, self.bias)
            self.bloch_unfold(self.G_kii, self.G)
        return self.G

    def bloch_unfold(self, A, out=None):
        """Unfold to supercell matrix.
        
        Args:
            A : Matrices at transverse k-points.
            out : (optional) supercell matrix 
        """
        return bloch_unfold(A, self.kpts, self.Nr, out)

    def dos(self, energy):
        """Total density of states -1/pi Im(Tr(GS))"""
        G = self.get_G(energy)
        return - np.dot(G, self.S).imag.trace() / np.pi

    def pdos(self, energy):
        """Projected density of states -1/pi Im(SGS/S)"""
        G = self.get_G(energy)
        SGS = np.linag.multi_dot([self.S, G, self.S])
        return - (SGS.diagonal() / self.S.diagonal()).imag / np.pi


class PrincipalSelfEnergy(PrincipalLayer):
    """Principal Layer (PL) Self-energy.
    
    Allows to compute a surface self-energy for a supercell (SC)
    composed of a repeating principal layer (PL). The inputs are
    converged Hamiltonians and Overlaps for the PL evaluated at 
    tranverse k-points.
    

    TODO :: order return!
    """

    ids = ['left','right']

    def __init__(self, kpts, hs_kii, hs_kij, Nr=None, eta=1e-5, id='left'):

        assert id in PrincipalSelfEnergy.ids, f"Invalid id for Principal self-energy. Choose between {PrincipalSelfEnergy.ids}"
        self.id = id
        if id == 'right':
            h_kij = hs_kij[0].swapaxes(1,2).conj()
            s_kij = hs_kij[1].swapaxes(1,2).conj()
            hs_kij = (h_kij, s_kij)

        super().__init__(kpts, hs_kii, hs_kij, Nr, eta)

        self.h_im = self.bloch_unfold(self.h_kij)
        self.s_im = self.bloch_unfold(self.s_kij)

        self.sigma_mm = np.empty(2*(self.nbf_i,), complex)

    def retarded(self, energy):
        """Return self-energy (sigma) evaluated at specified energy."""
        if energy != self.energy:
            z = energy - self.bias + self.eta * 1.j
            tau_im = z * self.s_im - self.h_im
            G = self.get_G(energy)
            tau_mi = z * self.s_im.T.conj() - self.h_im.T.conj()
            tau_mi.dot(G).dot(tau_im, out=self.sigma_mm)

        return self.sigma_mm

    def get_lambda(self, energy):
        """Return the lambda (aka Gamma) defined by i(S-S^d).

        Here S is the retarded selfenergy, and d denotes the hermitian
        conjugate.
        """
        sigma_mm = self.retarded(energy)
        return 1.j * (sigma_mm - sigma_mm.T.conj())