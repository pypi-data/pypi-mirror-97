import numpy as np

from generalized_elastic_net import GeneralizedElasticNet


def test_fit():
    N = 3
    K = 4
    Xmat = np.random.randn(N, K)
    Yvec = np.random.randn(N)
    lam_1 = 0.0034
    lam_2 = 0
    sigma = np.diag([1] * K)
    wvec = np.ones(K)
    lowbo = -1e5 * np.ones(K)
    upbo = np.inf * np.ones(K)
    s = GeneralizedElasticNet(lam_1=lam_1, lam_2=lam_2, lowbo=lowbo, upbo=upbo, wvec=wvec, sigma=sigma)
    s.fit(Xmat=Xmat, Yvec=Yvec)
    print(s.predict(X=Xmat), Yvec, s.coef_)
