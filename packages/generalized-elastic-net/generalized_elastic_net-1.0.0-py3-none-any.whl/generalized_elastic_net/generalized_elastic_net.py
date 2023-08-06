import copy
from math import sqrt

import numpy as np
from sklearn.utils.validation import check_is_fitted


class GeneralizedElasticNet(object):
    """
    Linear regression with combined generalized L1 and L2 regularizer and rectangle-range constraint.

    :param lam_1: Constant that multiplies the L1 penalty term. For numerical reasons, using lam_1 = 0 if the Lasso
                  object is not advised.
    :type lam_1: float

    :param lam_2: Constant that multiplies the L2 penalty term. For numerical reasons, using lam_2 = 0 if the ridge
                  object is not advised.
    :type lam_2: float

    :param lowbo: Lower bounds for the coefficients. Each elements should be in (-inf,upbo).
    :type lowbo: array-like of shape (n_features,)

    :param upbo: Upper bounds for the coefficients. Each elements should be in (lowbo, inf].
    :type upbo: array-like of shape (n_features,)

    :param wvec: Penalty weights for individual features.
    :type wvec: array-like of shape (n_features,)

    :param sigma: Penalty weights for interactions between any two features.
    :type sigma: ndarray of (n_features, n_features)

    :param err_tol: The tolerance for the optimization: if the updates are smaller than ``err_tol``, the interation
                    continues until it is smaller than ``tol``.
    :type err_tol: float, default=1e-8

    :param text: If equals to 'On', print error of the last iteration, otherwise no print
    :type text: str, default='Off'

    :param text_fr: Text-printing frequency, only works when text is 'On'
    :type text_fr: int, default=200
    """

    def __init__(self, lam_1, lam_2, lowbo, upbo, wvec, sigma, err_tol=1e-8, text='Off', text_fr=200):
        self.lam_1 = lam_1
        self.lam_2 = lam_2
        self.lowbo = lowbo
        self.upbo = upbo
        self.wvec = wvec
        self.sigma = sigma
        self.err_tol = err_tol
        self.text = text
        self.text_fr = text_fr

    @staticmethod
    def _muqprrwl1(Amat, lvec, bvec, dvec, v0, err_tol, text, text_fr):
        """
        The algorithm solves quadratic programming with rectangle range and weighted L1 regularizer, i.e.
        minimize (1/2) v' Amat v + bvec' v + dvec' |v - v0| over v subject to v in [0, lvec]

        :param Amat: A strictly positive definite matrix
        :type Amat: ndarray of (n_samples, n_samples)

        :param lvec: The upper bound vector
        :type lvec: array-like of shape (n_samples,)

        :param bvec: A vector
        :type bvec: array-like of shape (n_samples,)

        :param dvec: The regularization term
        :type dvec: array-like of shape (n_samples,)

        :param v0: The shifting vector
        :type v0: array-like of shape (n_samples,)

        :param err_tol: The tolerance for the optimization: if the updates are smaller than ``err_tol``, the interation
                        continues until it is smaller than ``tol``.
        :type err_tol: float

        :param text: If equals to 'On', print difference to the result of the last iteration, otherwise no print
        :type text: str

        :param text_fr: Text-printing frequency, only works when text is 'On'
        :type text_fr: int

        :return: Solution of optimization
        :rtype: array-like of shape (n_samples,)
        """

        A_plus = copy.deepcopy(Amat)
        A_plus[A_plus < 0] = 0

        A_minus = copy.deepcopy(Amat)
        A_minus[A_minus > 0] = 0
        A_minus = abs(A_minus)

        v = np.array([1.0 for x in range(len(bvec))])

        old_v = np.array([0 for x in range(len(bvec))])
        v0 = v0.astype(float)
        v0[np.where(v0 == 0)] = 0.00000001

        updateFactor = np.array([1.0 for x in range(len(bvec))])
        count = 0
        while (((old_v - v) ** 2).sum() > err_tol):
            v[np.where(v == 0)] = 0.00000001
            updateFactor0 = v0 / v
            updateFactor0[np.where(updateFactor0 == 0)] = 0.00000001
            dFa = np.array(A_plus.dot(v))
            dFb = copy.deepcopy(bvec)
            dFc = np.array(A_minus.dot(v))
            for i in range(len(bvec)):
                if dFa[i] == 0:
                    dFa[i] = 0.00000001
                if dFa[i] * updateFactor0[i] + (dFb[i] - dvec[i]) - dFc[i] / updateFactor0[i] > 0:
                    updateFactor[i] = float(
                        (-(dFb[i] - dvec[i]) + sqrt((dFb[i] - dvec[i]) ** 2 + 4 * dFa[i] * dFc[i])) / (2 * dFa[i]))
                elif dFa[i] * updateFactor0[i] + (dFb[i] + dvec[i]) - dFc[i] / updateFactor0[i] < 0:
                    updateFactor[i] = float(
                        (-(dFb[i] + dvec[i]) + sqrt((dFb[i] + dvec[i]) ** 2 + 4 * dFa[i] * dFc[i])) / (2 * dFa[i]))
                else:
                    updateFactor[i] = updateFactor0[i]
            if np.count_nonzero(~np.isnan(updateFactor)) == len(bvec):
                old_v = copy.deepcopy(v)
                v = np.minimum(lvec, updateFactor * v)
            else:
                break
            if (count % text_fr == 0) & (text == 'On'):
                print(((old_v - v) ** 2).sum())
            count += 1

        return v

    def fit(self, Xmat, Yvec):
        """
        Fit model.

        :param Xmat: Data.
        :type Xmat: ndarray of (n_samples, n_features)
        :param Yvec: Target.
        :type Yvec: array-like of shape (n_samples,)
        """

        p = Xmat.shape[1]
        Amat = Xmat.transpose().dot(Xmat) + self.lam_2 * self.sigma
        bvec = 2 * Amat.dot(self.lowbo) - 2 * Xmat.transpose().dot(Yvec)
        Amat = 2 * Amat
        dvec = self.lam_1 * self.wvec
        v0 = np.maximum(0, -self.lowbo)
        lvec = self.upbo - self.lowbo
        v = GeneralizedElasticNet._muqprrwl1(Amat=Amat, lvec=lvec, bvec=bvec, dvec=dvec, v0=v0, err_tol=self.err_tol,
                                             text=self.text,
                                             text_fr=self.text_fr)

        self.coef_ = v + self.lowbo
        return self

    def predict(self, X):
        """
        Decision function of the linear model.

        :param X: data
        :type X: ndarray of shape (n_samples, n_features)
        :return: The predicted decision function.
        :rtype: ndarray of shape (n_samples,)
        """
        check_is_fitted(self, "coef_")
        return np.dot(X, self.coef_)
