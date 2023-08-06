from qtpyt import xp

from qtpyt.base._kernels import (_mul,_mulc)
from qtpyt.base.greenfunction import GreenFunction


class SelfEnergy(GreenFunction):

    ids = ['left','right']
    
    def __init__(self, hs_ii, hs_im, selfenergies=[], eta=1e-5, id='left'):
        super().__init__(hs_ii[0], hs_ii[1], selfenergies, eta)

        assert id in SelfEnergy.ids, f"Invalid id for Principal self-energy. Choose between {PrincipalSelfEnergy.ids}"
        self.id = id
        if id == 'right':
            h_im = hs_im[0].swapaxes(0,1).conj()
            s_im = hs_im[1].swapaxes(0,1).conj()
            hs_im = (h_im, s_im)
        
        self.h_im = xp.asarray(hs_im[0]) 
        self.s_im = xp.asarray(hs_im[1])
        
        self.eta = eta
        self.bias = 0.
        self.energy = None

        self.sigma_mm = xp.empty(2*(self.nbf_m,), complex)

    @property
    def nbf_i(self):
        return self.h_im.shape[0]

    @property
    def nbf_m(self):
        return self.h_im.shape[1]

    def retarded(self, energy):
        """Return self-energy (sigma) evaluated at specified energy."""
        if energy != self.energy:
            # self.energy = energy # Done by Green's function.
            z = energy - self.bias + self.eta * 1.j
            tau_im = _mul(z,self.h_im,self.s_im)
            Ginv = self.get_Ginv(energy)
            a_im = xp.linalg.solve(Ginv, tau_im)
            tau_mi = _mulc(z,self.h_im.T,self.s_im.T)
            xp.dot(tau_mi, a_im, out=self.sigma_mm)

        return self.sigma_mm

    def get_lambda(self, energy):
        """Return the lambda (aka Gamma) defined by i(S-S^d).

        Here S is the retarded selfenergy, and d denotes the hermitian
        conjugate.
        """
        sigma_mm = self.retarded(energy)
        return 1.j * (sigma_mm - sigma_mm.T.conj())
