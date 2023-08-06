# Generalized Elastic Net Library
- Version:
- Released: 
- Publication: [arXiv]

Generalized elastic net is a penalty method for variable selection and regularization in high-dimensional sparse linear models. It generalizes and outperforms the lasso, ridge, and nonnegative elastic net through (1) capturing the penalty weights for individual features or/and interactions between any two features; (2) controling the range of the coefficients.

The algorithm is available through this public Python library. It applys multiplicative updates on a quadratic programming problem but contains absolute values of variables and a rectangle-range constraint. The algorithm is shown to converge monotonically to the global in the publication.

## To install
The generalized elastic net library requires Python 3 and is pip friendly. To get started, simply do:
```
pip install generalized-elastic-net
```
or check out the code from out GitHub repository.
You can now use the package in Python with:
```
from generalized_elastic_net import GeneralizedElasticNet
```

## Example
Input parameters: 
```
>>> N = 3
>>> K = 4
>>> Xmat = np.random.randn(N, K)
>>> Yvec = np.random.randn(N)
>>> print(Yvec)
[-0.72166018 -0.18367545 -0.77768828]
>>> lam_1 = 0.0034
>>> lam_2 = 0
>>> sigma = np.diag([1] * K)
>>> wvec = np.ones(K)
>>> lowbo = -1e5 * np.ones(K)
>>> upbo = np.inf * np.ones(K)
```
Fit the model:
```
>>> s = GeneralizedElasticNet(lam_1=lam_1, lam_2=lam_2, lowbo=lowbo, upbo=upbo, wvec=wvec, sigma=sigma)
>>> s.fit(Xmat=Xmat, Yvec=Yvec)
```
Output prediction:
```
>>> print(s.predict(X=Xmat))
[-0.72167257 -0.18245943 -0.77582073]
```
Output coefficients:
```
>>> print(s.coef_)
[-21095.74451325 -94129.49591188  25282.3047479  -10810.57632817]
```

