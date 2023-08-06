from qtpyt import xp
from qtpyt.base._kernels import (_mul,_mulc,get_lambda,dottrace,dagger)


class GreenFunction():
    """Equilibrium retarded Green function."""

    def __init__(self, H, S=None, selfenergies=[], eta=1e-5):
        self.H = xp.asarray(H)
        self.S = xp.asarray(S)
        self.selfenergies = selfenergies

        self.eta = eta
        self.energy = None

        self.Ginv = xp.empty(H.shape, complex)
        self.gammas = [None for _ in range(len(selfenergies))]

    @property
    def eta(self):
        return self._eta

    @eta.setter
    def eta(self, eta):
        """The Schroeadinger equation for a coupled system
        should have the same eta. Hence, the default is to
        recursively modify the eta in all selfenergies."""
        self._eta = eta
        for i, (indices, selfenergy) in enumerate(self.selfenergies):
            selfenergy.eta = eta

    def get_Ginv(self, energy):
        if energy != self.energy:
            self.energy = energy
            z = energy + self.eta * 1.j
            self.Ginv[:] = _mul(z,self.H,self.S)
            # Add selfenergies
            for i, (indices, selfenergy) in enumerate(self.selfenergies):
                sigma = xp.asarray(selfenergy.retarded(energy))
                self.Ginv[indices] -= sigma
                self.gammas[i] = get_lambda(sigma)
 
        return self.Ginv

    def retarded(self, energy):
        G = self.get_Ginv(energy)
        return xp.linalg.inv(G)

    def apply_retarded(self, energy, X):
        """Apply retarded Green function to X.

        Returns the matrix product G^r(e) . X
        """
        Ginv = self.get_Ginv(energy)
        return xp.linalg.solve(Ginv, X)

    def get_dos(self, energy):
        """Total density of states -1/pi Im(Tr(GS))"""
        GS = self.apply_retarded(energy, self.S)
        return -GS.imag.trace() / xp.pi

    def get_pdos(self, energy):
        """Total density of states -1/pi Im(Tr(GS))"""
        GS = self.apply_retarded(energy, self.S)
        return -GS.imag.diagonal() / xp.pi

    def get_transmission(self, energy):

        Ginv = self.get_Ginv(energy)
        gamma_L = self.gammas[0]
        gamma_R = self.gammas[1]
        # TODO :: improve with single factorization compatible with GPU
        a_mm = xp.linalg.solve(Ginv, gamma_L)
        b_mm = xp.linalg.solve(dagger(Ginv), gamma_R)
        T_e = dottrace(a_mm, b_mm).real

        return T_e
