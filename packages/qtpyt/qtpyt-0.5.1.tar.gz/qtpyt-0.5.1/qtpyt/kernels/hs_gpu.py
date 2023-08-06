import cupy as cp
from numba import cuda
from math import ceil

threadsperblock = (16,16)

def get_blockspergrid(a, threadsperblock):
    blockspergrid_x = ceil(a.shape[0] / threadsperblock[0])
    blockspergrid_y = ceil(a.shape[1] / threadsperblock[1])
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    return blockspergrid


@cuda.jit
def _geamT(z, h, s, m):
    x, y = cuda.grid(2)
    if x < h.shape[0] and y < h.shape[1]:
        m[y, x] = z * s[x, y] - h[x, y]


@cuda.jit
def _geamC(z, h, s, m):
    x, y = cuda.grid(2)
    if x < h.shape[0] and y < h.shape[1]:
        m[x, y] = z * s[x, y].conjugate() - h[x, y].conjugate()


@cuda.jit
def _get_lambda(sigma, lambd):
    x, y = cuda.grid(2)
    if x < sigma.shape[0] and y < sigma.shape[1]:
        lambd[y, x] = 1.j * (sigma[x, y] - sigma[y, x].conjugate())


def geamT(z, h, s, m=None):
    assert h.flags.c_contiguous & s.flags.c_contiguous
    if m is not None:
        assert m.flags.f_contiguous
    else:
        m = cp.empty(h.shape, complex, order='F')
    blockspergrid = get_blockspergrid(h, threadsperblock)
    _geamT[blockspergrid, threadsperblock](z, h, s, m)
    return m


def geamC(z, h, s, m=None):
    assert h.flags.c_contiguous & s.flags.c_contiguous
    if m is not None:
        assert m.flags.f_contiguous
    else:
        m = cp.empty(h.shape, complex, order='F')
    blockspergrid = get_blockspergrid(h, threadsperblock)
    _geamC[blockspergrid, threadsperblock](z, h, s, m)
    return m


def get_lambda(sigma, lambd=None):
    assert sigma.flags.c_contiguous
    if lambd is not None:
        assert lambd.flags.f_contiguous
    else:
        lambd = cp.empty(sigma.shape, complex, order='F')
    blockspergrid = get_blockspergrid(sigma, threadsperblock)
    _get_lambda[blockspergrid, threadsperblock](sigma, lambd)
    return lambd


if __name__ == '__main__':
    z = complex(2.)

    h = cp.random.random((10,10)).astype(complex)
    s = cp.random.random((10,10)).astype(complex)
    m = cp.empty((10,10), complex, order='F')

    blockspergrid = get_blockspergrid(h, threadsperblock)

    geamT(z, h, s, m)
    expected = z*s.T-h.T
    assert cp.allclose(expected,m)

    geamC(z, h, s, m)
    expected = z*s.conj()-h.conj()
    assert cp.allclose(expected,m)

    sigma = cp.random.random((10,10)).astype(complex)
    lambd = cp.empty((10,10), complex, order='F')

    get_lambda(sigma, lambd)
    expected = 1.j * (sigma - sigma.T.conj()).T
    assert cp.allclose(expected,lambd)