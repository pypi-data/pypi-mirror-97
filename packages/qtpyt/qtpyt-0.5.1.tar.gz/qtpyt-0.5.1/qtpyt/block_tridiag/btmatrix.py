from itertools import product, accumulate
from qtpyt import xp
import numpy as np
from qtpyt.base._kernels import (dotdiag, dottrace)

def _boudscheck(i,j,N):
    if abs(i)>N:
        raise IndexError(f"Index {i} is out of bound for axis 0 with size {N}")
    if abs(j)>N:
        raise IndexError(f"Index {j} is out of bound for axis 1 with size {N}")
    if abs(j-i)>1:
        raise IndexError(f"Index {i,j} is out of tridiagonal")


def _wraparound(i,j,N):
    return i%N, j%N


class _BTBuffer:
    def __init__(self, N):
        self.N = N
        self.m_qii = [None for _ in range(N)]
        self.m_qij = [None for _ in range(N-1)]
        self.m_qji = [None for _ in range(N-1)]

    def __getitem__(self, pos):
        i, j = pos
        _boudscheck(i,j,self.N)
        i, j =_wraparound(i,j,self.N)
        if i==j:
            return self.m_qii[i]
        if i>j:
            return self.m_qji[i-1]
        return self.m_qji[i-1]

    def __setitem__(self, pos, val):
        i, j = pos
        _boudscheck(i,j,self.N)
        i, j =_wraparound(i,j,self.N)
        if i==j:
            self.m_qii[i] = val 
        if i>j:
            self.m_qji[i-1] = val
        self.m_qji[i-1] = val

    def __iter__(self):
        yield self.m_qii[0]
        for q in range(1,self.N):
            yield self.m_qij[q-1]
            yield self.m_qji[q-1]
            yield self.m_qii[q]

    def __len__(self):
        return self.N


def empty_buffer(N):
    return _BTBuffer(N)


class BTMatrix(_BTBuffer):
    """Helper class for Block Tridiagonal matrices.
    
    Args:
        m_qii : (list(xp.ndarray), len=N)
            List of block matrices on the diagonal. 

        m_qij : (list(xp.ndarray), len=N-1)
            List of block matrices on the upper diagonal. 

        m_qji : (list(xp.ndarray), len=N-1)
            List of block matrices on the lower diagonal. 
    """
    def __init__(self, m_qii, m_qij, m_qji):
        super().__init__(len(m_qii))
        self.m_qii = m_qii
        self.m_qij = m_qij
        self.m_qji = m_qji
        
        shapes = [m.shape[0] for m in self.m_qii]
        self.m = sum(shapes)
        self.shape = np.fromiter(product(shapes, shapes), 'i8,i8').reshape(self.N,self.N)
        self._nodes = np.fromiter(accumulate([0]+shapes),'i8')

    def todense(self):
        order = 'C' if self.m_qii[0].flags.c_contiguous else 'F'
        M = xp.zeros(2*(self.m,), dtype=self.m_qii[0].dtype, order=order)
        M[self.ix_(0,0)] = self.m_qii[0]
        for q in range(1,self.N):
            M[self.ix_(q-1,q)] = self.m_qij[q-1]
            M[self.ix_(q,q-1)] = self.m_qji[q-1]
            M[self.ix_(q,q)] = self.m_qii[q]
        return M

    def ix_(self,i,j=None):
        if j is None: j=i
        il = self._nodes[i]
        jl = self._nodes[j]
        iu = il + self.shape[i,j][0]
        ju = jl + self.shape[i,j][1]
        return (slice(il,iu),
                slice(jl,ju))

    def __eq__(self,other,rtol=1e-05, atol=1e-08):
        allclose = lambda x, y: xp.testing.assert_allclose(x,y,rtol=rtol, atol=atol)
        for a, b in zip(self, other):
            allclose(a, b)

    def diagonal(self):
        return xp.concatenate([self.m_qii[q].diagonal() for q in range(self.N)])

    def trace(self):
        return xp.sum([self.m_qii[q].trace() for q in range(self.N)])

    def dot(self, other):
        out = empty_buffer(self.N)
        out.m_qii[0] = xp.dot(self.m_qii[0], other.m_qii[0])
        for q in range(self.N-1):
            out.m_qii[q+1] = xp.dot(self.m_qii[q+1], other.m_qii[q+1])
            out.m_qii[q] += xp.dot(self.m_qij[q], other.m_qji[q])
            out.m_qii[q+1] += xp.dot(self.m_qji[q], other.m_qij[q])
        return BTMatrix(out.m_qii, out.m_qij, out.m_qji)

    def dotdiag(self, other):
        out = [xp.zeros(self.m_qii[q].shape[0],self.m_qii[q].dtype) for q in range(self.N)]
        dotdiag(self.m_qii[0], other.m_qii[0], out[0])
        for q in range(self.N-1):
            dotdiag(self.m_qii[q+1], other.m_qii[q+1], out[q+1])
            dotdiag(self.m_qij[q], other.m_qji[q], out[q])
            dotdiag(self.m_qji[q], other.m_qij[q], out[q+1])
        return xp.concatenate(out)

    def dottrace(self, other):
        out = complex(0.)
        out = dottrace(self.m_qii[0], other.m_qii[0], out)
        for q in range(self.N-1):
            out = dottrace(self.m_qii[q+1], other.m_qii[q+1], out)
            out = dottrace(self.m_qij[q], other.m_qji[q], out)
            out = dottrace(self.m_qji[q], other.m_qij[q], out)
        return out

    _specials = ['__add__','__sub__','__iadd__',
                 '__isub__','__mul__','__imul__',
                 '__radd__','__rsub__','__rmul__']

    @classmethod
    def _create(cls):
        """
        TODO :: Add option to add diagonal array or constant.
        """
        ##https://code.activestate.com/recipes/496741-object-proxying/
        
        def make_method(name):
            def method(self, other, **kwargs):
                op = getattr(xp.ndarray, name)
                out = empty_buffer(self.N)
                if isinstance(other, BTMatrix):
                    out.m_qii[0] = op(self.m_qii[0], other.m_qii[0])
                    for q in range(1,self.N):
                        out.m_qii[q] = op(self.m_qii[q], other.m_qii[q])
                        out.m_qij[q-1] = op(self.m_qij[q-1], other.m_qij[q-1])
                        out.m_qji[q-1] = op(self.m_qji[q-1], other.m_qji[q-1])
                else:
                    out.m_qii[0] = op(self.m_qii[0], other)
                    for q in range(1,self.N):
                        out.m_qii[q] = op(self.m_qii[q], other)
                        out.m_qij[q-1] = op(self.m_qij[q-1], other)
                        out.m_qji[q-1] = op(self.m_qji[q-1], other)
                return BTMatrix(out.m_qii, out.m_qij, out.m_qji)
            return method
        
        namespace = {}
        for name in cls._specials:
            namespace[name] = make_method(name)
        return type("%s(%s)" % (cls.__name__, xp.ndarray.__name__), (cls,), namespace)

    def __new__(cls, *args, **kwargs):
        theclass = cls._create()
        ins = object.__new__(theclass)
        theclass.__init__(ins, *args, **kwargs)
        return ins
