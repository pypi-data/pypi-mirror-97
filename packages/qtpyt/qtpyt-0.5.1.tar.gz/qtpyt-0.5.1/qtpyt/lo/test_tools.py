import numpy as np
from qtpyt.lo.tools import extract_orthogonal_subspaces

def test_U1():
    h = np.arange(16).reshape(4,4)
    s = np.eye(4)
    bfs_m = [1]

    hs_mm, hs_ii, hs_im, U = extract_orthogonal_subspaces(h, s, bfs_m)
    np.testing.assert_allclose(hs_mm[0], h[1,1])
    np.testing.assert_allclose(hs_ii[0], h[np.ix_([0,2,3],[0,2,3])])
    np.testing.assert_allclose(hs_im[0], h[np.ix_([0,2,3],[1])])

def test_U2():
    h = np.random.random((4,4))
    s = np.random.random((4,4))
    s += s.T
    s /= 2
    bfs_m = [1]

    hs_mm, hs_ii, hs_im, U = extract_orthogonal_subspaces(h, s, bfs_m)
    np.testing.assert_allclose(hs_mm[0], h[1,1])
    np.testing.assert_allclose(hs_im[1], np.zeros((4-1,1)), atol=1e-16)