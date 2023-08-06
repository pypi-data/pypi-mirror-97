from qtpyt import xp
from qtpyt.block_tridiag.recursive import (dyson_method, spectral_method, coupling_method_N1)
from qtpyt.block_tridiag.btmatrix import (empty_buffer, BTMatrix)

from qtpyt.base._kernels import (_mul,_mulc,get_lambda,dagger)

class Solver:
    """The parent class of a generic solver.

    The principal task of Solver is to setup the inverse Green's
    function matrix which is then inverted by the child solver.
    It also offloas the Hamiltonian and Overlap matrices to GPU.

    """
    def __init__(self, greenfunction, method):
        N = len(greenfunction.hs_list_ii)
        self.greenfunction = greenfunction
        self.method = method
        
        # Possibly offload to GPU.
        gf = self.greenfunction
        gf.hs_list_ii[0] = xp.asarray(gf.hs_list_ii[0])
        for q in range(1,N):
            gf.hs_list_ii[q] = xp.asarray(gf.hs_list_ii[q])
            gf.hs_list_ij[q-1] = xp.asarray(gf.hs_list_ij[q-1])

        self.Ginv = empty_buffer(N)
        self.gammas = [None for _ in range(len(greenfunction.selfenergies))]

    def inv(self, Ginv, *args, **kwargs):
        return self.method(Ginv.m_qii, Ginv.m_qij, Ginv.m_qji, *args, **kwargs)

    def get_Ginv(self, energy):
        gf = self.greenfunction
        z = energy + gf.eta * 1.j
        for q, (h_ii, s_ii) in enumerate(gf.hs_list_ii):
            self.Ginv.m_qii[q] = _mul(z,h_ii,s_ii)
        # Upper and lower diagonals.
        for q, (h_ij, s_ij) in enumerate(gf.hs_list_ij):
            self.Ginv.m_qij[q] = _mul(z,h_ij,s_ij)
            self.Ginv.m_qji[q] = _mulc(z,h_ij.T,s_ij.T)
        # Add selfenergies
        for i, (block, selfenergy) in enumerate(gf.selfenergies):
            # Possibly offload to GPU.
            sigma = xp.asarray(selfenergy.retarded(energy))
            self.Ginv.m_qii[block] -= sigma
            self.gammas[i] = get_lambda(sigma)

        return self.Ginv

    def get_transmission(self, energy):
        raise NotImplementedError('{self.__class__.__name__} does not implement transmission.')

    def get_retarded(self, energy):
        raise NotImplementedError('{self.__class__.__name__} does not implement retarded.')

    def get_spectrals(self, energy):
        raise NotImplementedError('{self.__class__.__name__} does not implement spectrals.')


class Spectral(Solver):
    def __init__(self, greenfunction):
        super().__init__(greenfunction, spectral_method)
        self.A1 = None
        self.A2 = None

    def get_spectrals(self, energy):
        gf = self.greenfunction
        if energy != gf.energy:
            gf.energy = energy
            Ginv = self.get_Ginv(energy)
            self.A1 = None
            self.A2 = None
            A1, A2 = self.inv(Ginv, self.gammas[0], self.gammas[1])
            self.A1 = BTMatrix(*A1)
            self.A2 = BTMatrix(*A2)
        return self.A1, self.A2

    def get_transmission(self, energy):
        A2 = self.get_spectrals(energy)[1]
        gamma_L = self.gammas[0]
        T_e =  gamma_L.dot(A2[0,0]).real.trace()
        return T_e

    def get_retarded(self, energy):
        A1, A2 = self.get_spectrals(energy)
        return A1+A2


class Coupling(Solver):
    def __init__(self, greenfunction):
        super().__init__(greenfunction, coupling_method_N1)
    
    def get_transmission(self, energy):
        gf = self.greenfunction
        gf.energy = energy
        Ginv = self.get_Ginv(energy)
        g_N1 = self.inv(Ginv)
        gamma_L = self.gammas[0]
        gamma_R = self.gammas[1]
        T_e = xp.einsum('ij,jk,kl,lm->im',gamma_R,g_N1,
                        gamma_L,dagger(g_N1),optimize=True).real.trace()
        return T_e


class Dyson(Solver):
    def __init__(self, greenfuncition, trans=True):
        super().__init__(greenfuncition, dyson_method)
        self.G = None
        self.g_1N = None
        self.trans = trans

    def get_retarded(self, energy):
        gf = self.greenfunction
        if energy != gf.energy:
            gf.energy = energy
            Ginv = self.get_Ginv(energy)
            self.G = None
            if self.trans:
                g_1N, G = self.inv(Ginv, trans=True)
                self.g_1N = g_1N
                self.G = BTMatrix(*G)
            else:
                G = self.inv(Ginv, trans=False)
                self.G = BTMatrix(*G)
        return self.G
    
    def get_transmission(self, energy):
        _ = self.get_retarded(energy)
        gamma_L = self.gammas[0]
        gamma_R = self.gammas[1]
        T_e = xp.einsum('ij,jk,kl,lm->im',gamma_L,self.g_1N,
            gamma_R,dagger(self.g_1N),optimize=True).real.trace()
        return T_e