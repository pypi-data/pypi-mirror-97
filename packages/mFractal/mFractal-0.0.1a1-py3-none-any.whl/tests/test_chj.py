import numpy as np
import mFractal as mf

def test_chj_alpha():

    qi = -15
    qf = 15
    Io = 2
    Np = 8

    qValues = np.arange(qi, qf + 1)
    scales = np.arange(Io, Np + 1)

    with open('data/series.txt', 'r') as f:
        x = f.readlines()

    x = np.genfromtxt(x, delimiter='\t')
    Timeseries = x[:, 1]

    with open('data/out.txt', 'r') as f:
        y = f.readlines()
    out = np.genfromtxt(y, delimiter=',')

    alpha, falpha, Dq, Rsqr_alpha, Rsqr_falpha, Rsqr_Dq, muScale, Md, Ma, Mf = mf.chj(
        Timeseries, qValues, scales)

    diff_alpha = alpha - out[:,0]

    assert np.round(np.sum(diff_alpha), 1) == 0


def test_chj_falpha():

    qi = -15
    qf = 15
    Io = 2
    Np = 8

    qValues = np.arange(qi, qf + 1)
    scales = np.arange(Io, Np + 1)

    with open('data/series.txt', 'r') as f:
        x = f.readlines()

    x = np.genfromtxt(x, delimiter='\t')
    Timeseries = x[:, 1]

    with open('data/out.txt', 'r') as f:
        y = f.readlines()
    out = np.genfromtxt(y, delimiter=',')

    alpha, falpha, Dq, Rsqr_alpha, Rsqr_falpha, Rsqr_Dq, muScale, Md, Ma, Mf = mf.chj(
        Timeseries, qValues, scales)

    diff_alpha = falpha - out[:, 1]

    assert np.round(np.sum(diff_alpha), 1) == 0
