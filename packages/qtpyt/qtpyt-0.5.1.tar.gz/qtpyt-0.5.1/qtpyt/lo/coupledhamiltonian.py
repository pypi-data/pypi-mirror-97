import numpy as np
from .tools import subdiagonalize, rotate_matrix, dagger, \
                   order_diagonal, cutcoupling, get_subspace


from .tk_gpaw import subdiagonalize_atoms, get_bfs_indices, \
                     extract_orthogonal_subspaces, flatten

class CoupledHamiltonian:

    def __init__(self, H, S, selfenergies):
        self.H = H
        self.S = S
        self.selfenergies = selfenergies

    def align_bf(self, align_bf):
        h_mm = self.H
        s_mm = self.S
        h1_ii = self.selfenergies[0].h_ii
        if align_bf is not None:
            diff = ((h_mm[align_bf, align_bf] - np.real(h1_ii[align_bf, align_bf])) /
                    s_mm[align_bf, align_bf])
            # print('# Aligning scat. H to left lead H. diff=', diff)
            h_mm -= diff * s_mm
        return diff

    def apply_rotation(self, c_mm):
          h_mm = self.H
          s_mm = self.S
          h_mm[:] = rotate_matrix(h_mm, c_mm)
          s_mm[:] = rotate_matrix(s_mm, c_mm)
          # Rotate coupling between lead and central region
          for alpha, sigma in enumerate(self.selfenergies):
              sigma.h_im[:] = np.dot(sigma.h_im, c_mm)
              sigma.s_im[:] = np.dot(sigma.s_im, c_mm)

    def diagonalize(self, apply=False):
        nbf = len(self.H)
        return self.subdiagonalize_bfs(range(nbf), apply)

    def subdiagonalize_bfs(self, bfs, apply=False):
      bfs = np.array(bfs)
      h_mm = self.H
      s_mm = self.S
      ht_mm, st_mm, c_mm, e_m = subdiagonalize(h_mm, s_mm, bfs)
      if apply:
          self.apply_rotation(c_mm)
          return

      c_mm = np.take(c_mm, bfs, axis=0)
      c_mm = np.take(c_mm, bfs, axis=1)
      return ht_mm, st_mm, e_m.real, c_mm

    def cutcoupling_bfs(self, bfs, apply=False):
      bfs = np.array(bfs)
      h_pp = self.H.copy()
      s_pp = self.S.copy()
      cutcoupling(h_pp, s_pp, bfs)
      if apply:
          self.H = h_pp
          self.S = s_pp
          for alpha, sigma in enumerate(self.selfenergies):
              for m in bfs:
                  sigma.h_im[:, m] = 0.0
                  sigma.s_im[:, m] = 0.0
      return h_pp, s_pp

    def take_bfs(self, bfs, apply=False):
        nbf = len(self.H)
        c_mm = np.eye(nbf).take(bfs,1)
        h_pp = rotate_matrix(self.H, c_mm)
        s_pp = rotate_matrix(self.S, c_mm)
        if apply:
            self.H = h_pp
            self.S = s_pp
            for alpha, sigma in enumerate(self.selfenergies):
                sigma.h_im = np.dot(sigma.h_im, c_mm)
                sigma.s_im = np.dot(sigma.s_im, c_mm)
                sigma.sigma_mm = np.empty(self.H.shape, complex)
        return h_pp, s_pp, c_mm

    def lowdin_rotation(self, apply=False):
      h_mm = self.H
      s_mm = self.S
      eig, rot_mm = np.linalg.eigh(s_mm)
      eig = np.abs(eig)
      rot_mm = np.dot(rot_mm / np.sqrt(eig), dagger(rot_mm))
      if apply:
          self.apply_rotation(rot_mm)
          return

      return rot_mm

    def order_diagonal(self, apply=False):
      h_mm = self.H
      s_mm = self.S
      ht_mm, st_mm, c_mm = order_diagonal(h_mm, s_mm)
      if apply:
          self.apply_rotation(c_mm)
          return

      return ht_mm, st_mm, c_mm

    def subdiagonalize_atoms(self, calc, a=None, apply=False):
        h_mm = self.H
        s_mm = self.S
        c_MM, e_aj = subdiagonalize_atoms(calc, h_mm, s_mm, a)
        if apply:
            #Apply subdiagonalization
            self.apply_rotation(c_MM)
            return
        return c_MM, e_aj


    # def take_bfs_activespace(self, calc, a, key=lambda x: abs(x)<np.inf,
    #                          cutoff=np.inf, include=False, orthogonal=True):
    #     '''
    #         key     := Apply condition to eigenvalues of subdiagonalized atoms.
    #         cutoff  := Cutoff for effective embedding to incudle in active space,
    #                    form subdiagonalized [a] orbitals.
    #         include := include cut orbitlas into selfenergy embedding.
    #     '''
    #     h_mm = self.H
    #     s_mm = self.S
    #     nbf = h_mm.shape[-1]
    #
    #     c_MM, e_aj = subdiagonalize_atoms(calc, h_mm, s_mm, a)
    #     bfs_imp = get_bfs_indices(calc, a)
    #     # In [a] but not in active space
    #     bfs_not_m = [bfs_imp[i] for i,
    #                                 eigval in enumerate(flatten(e_aj))
    #                  if not key(eigval)] #Take complementary
    #     # Active space
    #     bfs_m = list(np.setdiff1d(bfs_imp,bfs_not_m))
    #     # o := orbitals other atoms not in [a]
    #     bfs_m_and_o_i = list(np.setdiff1d(range(nbf),bfs_not_m))
    #     nbfs_m_and_o = len(bfs_m_and_o_i)
    #
    #     #Apply subdiagonalization
    #     self.apply_rotation(c_MM)
    #
    #     if cutoff<np.inf:
    #         # h_imp = get_subspace(self.H, bfs_imp)
    #         # s_imp = get_subspace(self.S, bfs_imp)
    #         #Effective active space := activespace and effective embedding
    #         bfs_eff_i = []
    #         bfs_eff_imp = []
    #         for bfm in bfs_m: # for each bfm (bfm := basis of active)
    #             row_m_imp = abs(self.H[bfm,bfs_imp])
    #             #Index of couplings in [a]
    #             coupling  = np.where(row_m_imp>cutoff)[0]
    #             bfs_eff_imp = np.union1d(bfs_eff_imp, coupling)
    #             #Effective active embedding for bfm
    #             bfs_emb_i = np.arange(self.H.shape[0])[bfs_imp][coupling]
    #             #Effective activespace
    #             bfs_eff_i = np.union1d(bfs_eff_i, bfs_emb_i)
    #         #Unify with others
    #         bfs_eff_i = bfs_eff_i.tolist()
    #         bfs_m_and_o_i = np.union1d(bfs_eff_i, bfs_m_and_o_i).tolist()
    #         #Modify activespace with effective active space
    #         h_imp = get_subspace(self.H, bfs_eff_i)
    #         s_imp = get_subspace(self.S, bfs_eff_i)
    #     else:
    #         h_imp = get_subspace(self.H, bfs_m)
    #         s_imp = get_subspace(self.S, bfs_m)
    #
    #
    #     if include:
    #         from .internalselfenergy import InternalSelfEnergy
    #         #Subdiagonalized space of [a]
    #         h_mm = get_subspace(self.H, bfs_imp)
    #         s_mm = get_subspace(self.S, bfs_imp)
    #         #Indecixes in impurities [a]
    #         bfs_not_m_imp = [i for i,
    #                                eigval in enumerate(flatten(e_aj))
    #                          if not key(eigval)] #Take complementary
    #         # Active space
    #         bfs_m_imp = list(np.setdiff1d(np.arange(len(h_mm)),bfs_not_m_imp))
    #         hs_mm, hs_ii, hs_im =  extract_orthogonal_subspaces(h_mm,
    #                                                             s_mm,
    #                                                             bfs_m_imp, #Modify
    #                                                             bfs_not_m_imp, #Modify
    #                                                             orthogonal=orthogonal)
    #         #Embed rest of subdiagonalized orbitas (in [a]).
    #         h_im = np.zeros((len(bfs_not_m),len(self.H)), complex)
    #         s_im = np.zeros((len(bfs_not_m),len(self.H)), complex)
    #         h_im[:,bfs_m] = hs_im[0]
    #         s_im[:,bfs_m] = hs_im[1]
    #         # h_im.take(bfs_m_and_o_i, axis=1)
    #         # s_im.take(bfs_m_and_o_i, axis=1)
    #         selfenergy = InternalSelfEnergy(hs_ii, (h_im, s_im)) #Coupling to leads is None!
    #         self.selfenergies.append(selfenergy)
    #
    #
    #     #Take (effective) activespace
    #     self.take_bfs(bfs_m_and_o_i, apply=True)
    #
    #     return h_imp, s_imp

    def order_species(self, calc, sort_diag=False, apply=False):

        atoms = calc.atoms

        # Order atomic species
        symbols = np.array(atoms.symbols)
        species = set(symbols)
        indices_xa = [None for _ in range(len(species))]
        for e, elem in enumerate(species):
            indices_xa[e] = np.where(symbols==elem)[0]

        # Subdiagonalize atoms
        p_mm = self.subdiagonalize_atoms(calc, apply=False)
        # Order orbitals within species
        u_mm = self.order_subset(calc, indices_xa,
                                 sort_diag=sort_diag, apply=False)
        c_mm = p_mm.dot(u_mm)
        if apply:
            self.apply_rotation(c_mm)
            return

        return c_mm

    def order_subset(self, calc, indices_xa, sort_diag=False, apply=False):
        '''This function is supposed to be used in subdiagonalized Hamiltoninans to
        order the atomic orbital indices within groups [x] of atoms [a] specified by
        indices_xa. [a] can be a list of lists and/or lists and ints.'''
        h_mm = self.H
        s_mm = self.S
        m = h_mm.shape[-1]

        perm_list = []
        for indices_a in indices_xa:
            try:
                indices_a[0][0]
            except TypeError:
                # indices_a is a list of int
                bfs_i = get_bfs_indices(calc, indices_a, 'append')
            else:
                # indices_a is a list of lists of atoms forming a block
                bfs_i = []
                for jj in indices_a:
                    bfs_i.append(get_bfs_indices(calc, jj))
            bfs_i = np.array(bfs_i)
            if sort_diag:
                # Order diagonal in subset
                bfs_i = bfs_i.T
            perm_list.extend(bfs_i.flatten())
        # Rotation matrix
        c_mm = np.eye(m).take(perm_list, axis=1)
        if apply:
            self.apply_rotation(c_mm)
            return

        return c_mm


    def get_activespace(self, calc, a, key=lambda x: abs(x)<np.inf, orthogonal=True, inverse=False):
        '''
            key     := Apply condition to eigenvalues of subdiagonalized atoms.
            inverse := Get embedding instead. Put activespace in selfenergy
        '''
        from .internalselfenergy import InternalSelfEnergy

        h_mm = self.H
        s_mm = self.S
        nbf = h_mm.shape[-1]

        c_MM, e_aj = subdiagonalize_atoms(calc, h_mm, s_mm, a)
        bfs_imp = get_bfs_indices(calc, a)
        # Active space
        bfs_m = [bfs_imp[i] for i,
                                eigval in enumerate(flatten(e_aj))
                 if key(eigval)]
        # Embedding
        bfs_i = list(np.setdiff1d(range(nbf),bfs_m))
        nbf_i = len(bfs_i)

        hs_mm, hs_ii, hs_im =  extract_orthogonal_subspaces(h_mm,
                                                            s_mm,
                                                            bfs_m.copy(), # Do not modify
                                                            bfs_i.copy(), # Do not modify
                                                            c_MM,
                                                            orthogonal)

        # Reduce h_im, s_im
        for selfenergy in self.selfenergies:
            try:
                sigma_mm = np.empty((nbf_i,nbf_i), complex)
                h_im = selfenergy.h_im.take(bfs_i, axis=1)
                s_im = selfenergy.s_im.take(bfs_i, axis=1)
            except IndexError:
                print('selfenergies already ok!')
            else:
                selfenergy.h_im = h_im
                selfenergy.s_im = s_im
                selfenergy.sigma_mm = sigma_mm

        if inverse: #Take embedding instead. Put activespace in embedding
            #Activespace selfenergy
            hs_mi = tuple(hs_im[i].T.conj() for i in range(2))
            selfenergy = InternalSelfEnergy(hs_mm, hs_mi)

            if hasattr(self, 'Ginv'):
                self.Ginv = np.empty(hs_ii[0].shape, complex)

            self.__init__(hs_ii[0], hs_ii[1], self.selfenergies+[selfenergy])

            return e_aj

        #Embedding selfenergy
        selfenergy = InternalSelfEnergy(hs_ii, hs_im,
                                        selfenergies=self.selfenergies)

        if hasattr(self, 'Ginv'):
            self.Ginv = np.empty(hs_mm[0].shape, complex)

        self.__init__(hs_mm[0], hs_mm[1], [selfenergy])

        return e_aj


def set_pzd_carbons(calc, coupledhamiltonian, ext_C=None, int_C=None, Ce=None,
                    Ci=None, apply=True):
    '''This function takes the pz- and d- orbitals of a scattering region.
    coupledhamiltonian can be either a CoupledHamiltonian or GreenFunction.
    If apply is set to False, the indices of the pzd- orbitals are returned
    instead. Note that this function modufies the '''
    from qtpyt.analysis.tk_analysis import get_external_internal
    #
    if (ext_C is None) or (int_C is None):
        ext_C, int_C = get_external_internal(calc.atoms, 'C')

    if (Ce is None) or (Ci is None):
        Ce = [3,6,10,12]
        Ci = [3,6,10,11]

    bfs_ext_i = get_bfs_indices(calc, ext_C, method='append')
    bfs_int_i = get_bfs_indices(calc, int_C, method='append')

    #Take pz- and d- orbitas
    bfs_ext_pzd_i = np.array(bfs_ext_i)[:,Ce]
    bfs_int_pzd_i = np.array(bfs_int_i)[:,Ci]

    #Activespace pz- and d- orbitas
    bfs_m = np.union1d(bfs_int_pzd_i, bfs_ext_pzd_i)
    indices_C = np.union1d(ext_C, int_C)

    #Rotate scattering region
    coupledhamiltonian.subdiagonalize_atoms(calc, indices_C, apply=True)

    if apply:
        #Reduce matrix
        coupledhamiltonian.take_bfs(bfs_m, apply=True)
        return

    return bfs_m

def set_pz_d_embedding(calc, coupledhamiltonian, apply=True):
    ''''''
    from .internalselfenergy import InternalSelfEnergy

    h_mm = coupledhamiltonian.H
    s_mm = coupledhamiltonian.S
    nbf = h_mm.shape[-1]

    bfs_pzd = set_pzd_carbons(calc, coupledhamiltonian, apply=False)
    bfs_pz  = bfs_pzd[::4]
    bfs_d   = np.setdiff1d(bfs_pzd, bfs_pz)

    #Pzd- subspace
    h_pzd = get_subspace(h_mm, bfs_pzd)
    s_pzd = get_subspace(s_mm, bfs_pzd)

    #Pz- and d- indices in pzd- subspace
    bfs_pzd_pz  = np.arange(0,len(bfs_pzd),4)
    bfs_pzd_d   = np.setdiff1d(range(len(bfs_pzd)), bfs_pzd_pz)

    hs_mm, hs_ii, hs_im =  extract_orthogonal_subspaces(h_pzd,
                                                        s_pzd,
                                                        bfs_pzd_pz, #Modify
                                                        bfs_pzd_d, #Modify
                                                        orthogonal=True)

    h_im = np.zeros((len(bfs_d), nbf), dtype=complex)
    s_im = np.zeros((len(bfs_d), nbf), dtype=complex)
    h_im[:,bfs_pz] = hs_im[0]
    s_im[:,bfs_pz] = hs_im[1]
    selfenergy = InternalSelfEnergy(hs_ii, (h_im, s_im))

    if apply:
        coupledhamiltonian.take_bfs(bfs_pz, apply=True)
        coupledhamiltonian.selfenergies.append(selfenergy)
        return

    return bfs_pz, selfenergy


def set_pz_embed_rest(calc, coupledhamiltonian, apply=True):
    '''This function takes the pz- and d- orbitals of a scattering region.
    coupledhamiltonian can be either a CoupledHamiltonian or GreenFunction.
    If apply is set to False, the indices of the pzd- orbitals are returned
    instead. Note that this function modufies the '''
    from .internalselfenergy import InternalSelfEnergy

    h_mm = coupledhamiltonian.H
    s_mm = coupledhamiltonian.S
    nbf = h_mm.shape[-1]

    #
    indices_C = np.where(calc.atoms.symbols=='C')[0]

    #Rotate scattering region
    coupledhamiltonian.subdiagonalize_atoms(calc, indices_C, apply=True)

    #Carbon atom basis function indices
    bfs_C = np.array(get_bfs_indices(calc, indices_C, method='append'))
    #Pz-
    bfs_pz = bfs_C[:,3].flatten()
    #Rest-
    bfs_rest = np.setdiff1d(bfs_C, bfs_pz)

    #Carbon- subspace
    h_cc = get_subspace(h_mm, bfs_C.flatten())
    s_cc = get_subspace(s_mm, bfs_C.flatten())

    #Pz- and rest- indices in Carbon atoms subspace
    bfs_C_pz = np.arange(3, bfs_C.size, bfs_C.shape[1])
    bfs_C_rest  = np.setdiff1d(range(bfs_C.size), bfs_C_pz)

    hs_mm, hs_ii, hs_im =  extract_orthogonal_subspaces(h_cc,
                                                        s_cc,
                                                        bfs_C_pz, #Modify
                                                        bfs_C_rest, #Modify
                                                        orthogonal=True)

    h_im = np.zeros((len(bfs_C_rest), nbf), dtype=complex)
    s_im = np.zeros((len(bfs_C_rest), nbf), dtype=complex)
    h_im[:,bfs_pz] = hs_im[0]
    s_im[:,bfs_pz] = hs_im[1]
    selfenergy = InternalSelfEnergy(hs_ii, (h_im, s_im))

    if apply:
        coupledhamiltonian.take_bfs(bfs_pz, apply=True)
        coupledhamiltonian.selfenergies.append(selfenergy)
        return

    return bfs_pz, selfenergy
