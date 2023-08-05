# -*- coding: utf-8 -*-
#
#    Copyright 2020 Ibai Roman
#
#    This file is part of GPlib.
#
#    GPlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GPlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GPlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import scipy.linalg


class MultivariateGaussian(object):
    """
    Multivariate Gaussian distribution
    """
    def __init__(self, mean, covariance,
                 cached_cov_matrix=None, cached_l_matrix=None):
        self.mean = mean
        self.covariance = covariance
        self.l_matrix = MultivariateGaussian._get_l_matrix(
            covariance,
            cached_cov_matrix,
            cached_l_matrix
        )

    def sample(self, n_samples=10):
        """

        :param n_samples:
        :type n_samples:
        :return:
        :rtype:
        """
        rnd = np.random.randn(self.l_matrix.shape[0], n_samples)

        return self.mean.reshape(-1, 1) + np.dot(self.l_matrix, rnd)

    def conditional_mean(self, data_y, ka_matrix, test_mean):
        """

        :param data_y:
        :type data_y:
        :param ka_matrix:
        :type ka_matrix:
        :param test_mean:
        :type test_mean:
        :return:
        :rtype:
        """
        alpha = scipy.linalg.cho_solve(
            (self.l_matrix, True),
            data_y - self.mean
        )

        new_mean = np.dot(ka_matrix.T, alpha) + test_mean

        return new_mean

    def conditional_cov(self, kxa_matrix, kxb_matrix, kab_matrix):
        """

        :param kxa_matrix:
        :type kxa_matrix:
        :param kxb_matrix:
        :type kxb_matrix:
        :param kab_matrix:
        :type kab_matrix:
        :return:
        :rtype:
        """

        beta_a = scipy.linalg.solve_triangular(
            self.l_matrix,
            kxa_matrix,
            lower=True,
            check_finite=False
        )

        if kxb_matrix is not None:
            beta_b = scipy.linalg.solve_triangular(
                self.l_matrix,
                kxb_matrix,
                lower=True,
                check_finite=False
            )
        else:
            beta_b = beta_a

        if kab_matrix.shape[0] == kab_matrix.shape[1]:
            new_covariance = kab_matrix - np.dot(beta_a.T, beta_b)
        else:
            new_covariance = kab_matrix - \
                np.sum(np.power(beta_a, 2), axis=0).reshape(-1, 1)
            new_covariance = new_covariance.clip(min=1e-20)

        return new_covariance

    def get_log_likelihood(self, data_y, dmu_dtheta=None, dk_dtheta=None):
        """

        :param data_y:
        :type data_y:
        :param dmu_dtheta:
        :type dmu_dtheta:
        :param dk_dtheta:
        :type dk_dtheta:
        :return:
        :rtype:
        """
        alpha = scipy.linalg.cho_solve(
            (self.l_matrix, True),
            data_y - self.mean
        )
        
        log_likelihood = self._log_likelihood(data_y, alpha)

        result = (log_likelihood, )

        if dmu_dtheta is not None and dk_dtheta is not None:
            dlog_likelihood_dtheta = self._dlog_likelihood_dtheta(
                alpha,
                dmu_dtheta,
                dk_dtheta
            )
            result += (dlog_likelihood_dtheta, )

        if len(result) == 1:
            result = result[0]

        return result

    def get_log_predictive_density(self, data_y):
        """
        Measure the log predictive density

        :param data_y:
        :type data_y:
        :return:
        :rtype:
        """
        var = np.diagonal(self.covariance)[:, None]
        return MultivariateGaussian._log_density(data_y, var, self.mean)

    def get_log_loocv_density(self, data_y):
        """
        Measure the log predictive density

        :param data_y:
        :type data_y:
        :return:
        :rtype:
        """
        inv_cov = scipy.linalg.cho_solve(
            (self.l_matrix, True),
            np.eye(self.l_matrix.shape[0])
        )

        diag_inv_cov = np.diagonal(inv_cov)[:, None]

        mean = data_y - np.divide(np.dot(inv_cov, data_y), diag_inv_cov)

        var = np.divide(1.0, diag_inv_cov)

        return MultivariateGaussian._log_density(data_y, var, mean)

    def _log_likelihood(self, data_y, alpha):
        """
        Measure the log Likelihood

        :param data_y:
        :type data_y:
        :param alpha:
        :type alpha:
        :return:
        :rtype:
        """
        llikelihood = -np.sum(np.log(np.diag(self.l_matrix))) - \
            0.5 * np.dot((data_y - self.mean).T, alpha)[0, 0] - \
            0.5 * self.l_matrix.shape[0] * np.log(2.0 * np.pi)

        return llikelihood

    def _dlog_likelihood_dtheta(self, alpha, dmu_dtheta, dk_dtheta):
        """
        Measure the gradient log Likelihood

        :param alpha:
        :type alpha:
        :param dmu_dtheta:
        :type dmu_dtheta:
        :param dk_dtheta:
        :type dk_dtheta:
        :return:
        :rtype:
        """
        k_inv = scipy.linalg.cho_solve(
            (self.l_matrix, True),
            np.eye(self.l_matrix.shape[0]))
        jacobian = np.outer(alpha, alpha) - k_inv

        grad_llikelihood = []
        # Log amplitude gradient.
        for dmu_dtheta_i in dmu_dtheta:
            grad_llikelihood.append(
                0.5 * np.trace(np.dot(jacobian, dmu_dtheta_i))
            )
        # Log amplitude gradient.
        for dk_dtheta_i in dk_dtheta:
            grad_llikelihood.append(
                0.5 * np.trace(np.dot(jacobian, dk_dtheta_i))
            )

        return grad_llikelihood

    @staticmethod
    def _log_density(fy, var, mean):
        """
        Measure the log density

        :param fy:
        :type fy:
        :param var:
        :type var:
        :param mean:
        :type mean:
        :return:
        :rtype:
        """
        log_predictive_density = \
            -0.5 * np.log(var) - \
            np.power((fy - mean), 2) / (2.0 * var) - \
            0.5 * np.log(2 * np.pi)

        return log_predictive_density

    @staticmethod
    def _get_l_matrix(covariance, cached_cov_matrix, cached_l_matrix=None):
        """

        :param covariance:
        :type covariance:
        :param cached_cov_matrix:
        :type cached_cov_matrix:
        :param cached_l_matrix:
        :type cached_l_matrix:
        :return:
        :rtype:
        """
        if cached_l_matrix is None:
            return MultivariateGaussian._chol(covariance)

        if covariance is None:
            return cached_l_matrix

        if cached_l_matrix.shape[0] < covariance.shape[0]:
            return MultivariateGaussian._update_chol(
                covariance,
                cached_l_matrix,
                offset=0
            )

        return MultivariateGaussian._downdate_chol(
            cached_cov_matrix,
            cached_l_matrix,
            offset=0,
            size=(cached_l_matrix.shape[0] - covariance.shape[0])
        )

    @staticmethod
    def _chol(k_matrix):
        """
        Compute cholesky decomposition

        :param k_matrix:
        :type k_matrix:
        :return:
        :rtype:
        """
        MultivariateGaussian._check_k_matrix(k_matrix)

        # Solve cholesky decomposition
        l_matrix = MultivariateGaussian._jittered_chol(k_matrix)

        MultivariateGaussian._check_l_matrix(l_matrix, k_matrix)

        return l_matrix

    @staticmethod
    def _update_chol(k_matrix, l_matrix, offset=0):
        """

        :param k_matrix:
        :type k_matrix:
        :param l_matrix:
        :type l_matrix:
        :param offset:
        :type offset:
        :return:
        :rtype:
        """
        MultivariateGaussian._check_k_matrix(k_matrix)

        b_i = k_matrix.shape[0] - offset
        new_i = l_matrix.shape[0] - offset
        new_l_matrix = np.zeros(k_matrix.shape)
        new_l_matrix[:new_i, :new_i] = l_matrix[:new_i, :new_i]
        new_l_matrix[new_i:b_i:, :new_i] = scipy.linalg.solve_triangular(
            l_matrix[:new_i, :new_i],
            k_matrix[:new_i, new_i:b_i],
            lower=True,
            check_finite=False
        ).T

        new_l_matrix[b_i:, :new_i] = l_matrix[new_i:, :new_i]
        new_l_matrix[new_i:b_i, new_i:b_i] = \
            MultivariateGaussian._jittered_chol(
                k_matrix[new_i:b_i, new_i:b_i] -
                np.dot(
                    new_l_matrix[new_i:b_i:, :new_i],
                    new_l_matrix[new_i:b_i:, :new_i].T
                )
            )
        new_l_matrix[b_i:, new_i:b_i] = scipy.linalg.solve_triangular(
            new_l_matrix[new_i:b_i, new_i:b_i],
            k_matrix[b_i:, new_i:b_i].T -
            np.dot(
                new_l_matrix[new_i:b_i:, :new_i],
                new_l_matrix[b_i:, :new_i].T
            ),
            lower=True,
            check_finite=False
        ).T
        new_l_matrix[b_i:, b_i:] = MultivariateGaussian._jittered_chol(
            np.dot(l_matrix[new_i:, new_i:], l_matrix[new_i:, new_i:].T) -
            np.dot(
                new_l_matrix[b_i:, new_i:b_i],
                new_l_matrix[b_i:, new_i:b_i].T
            )
        )

        MultivariateGaussian._check_l_matrix(new_l_matrix, k_matrix)

        return new_l_matrix

    @staticmethod
    def _downdate_chol(k_matrix, l_matrix, offset=0, size=0):
        """

        :param k_matrix:
        :type k_matrix:
        :param l_matrix:
        :type l_matrix:
        :param offset:
        :type offset:
        :param size:
        :type size:
        :return:
        :rtype:
        """
        MultivariateGaussian._check_k_matrix(k_matrix)

        b_i = k_matrix.shape[0] - offset
        new_i = b_i - size
        new_size = k_matrix.shape[0] - size
        new_l_matrix = np.zeros((new_size, new_size))
        new_l_matrix[:new_i, :new_i] = l_matrix[:new_i, :new_i]
        new_l_matrix[new_i:, new_i:] = MultivariateGaussian._jittered_chol(
            np.dot(l_matrix[b_i:, b_i:], l_matrix[b_i:, b_i:].T) +
            np.dot(l_matrix[b_i:, new_i:b_i], l_matrix[b_i:, new_i:b_i].T)
        )
        new_l_matrix[new_i:, :new_i] = l_matrix[b_i:, :new_i]

        new_k_matrix = np.vstack((
            np.hstack((k_matrix[:new_i, :new_i], k_matrix[:new_i, b_i:])),
            np.hstack((k_matrix[b_i:, :new_i], k_matrix[b_i:, b_i:]))
        ))

        MultivariateGaussian._check_l_matrix(new_l_matrix, new_k_matrix)

        return new_l_matrix

    @staticmethod
    def _check_k_matrix(k_matrix):
        """

        :param k_matrix:
        :type k_matrix:
        :return:
        :rtype:
        """

        # Empty
        if k_matrix.size == 0:
            return np.empty((0, 0))

        # Non finite values in covariance matrix
        if not np.all(np.isfinite(k_matrix)):
            raise np.linalg.LinAlgError("Non finite values in cov matrix")

        # Covariance matrix is not symmetric
        if np.max(np.abs(k_matrix - k_matrix.T)) > 1e-20:
            raise np.linalg.LinAlgError("Covariance matrix is not symmetric")

    @staticmethod
    def _jittered_chol(k_matrix):
        """

        :param k_matrix:
        :type k_matrix:
        :return:
        :rtype:
        """

        l_matrix = None
        jitter = 1e-30
        max_jitter = 1e-6
        k_corrected = k_matrix
        while l_matrix is None and jitter < max_jitter:
            l_matrix, error = scipy.linalg.lapack.dpotrf(
                np.ascontiguousarray(k_corrected),
                lower=1
            )
            if error != 0:
                l_matrix = None
                k_corrected = k_matrix + jitter * np.eye(k_matrix.shape[0])
                jitter *= 10

        if l_matrix is None:
            raise np.linalg.LinAlgError("Can't compute cholesky decomposition")

        return l_matrix

    @staticmethod
    def _check_l_matrix(l_matrix, k_matrix):
        """

        :param l_matrix:
        :type l_matrix:
        :param k_matrix:
        :type k_matrix:
        :return:
        :rtype:
        """

        # Non finite values in L matrix
        if not np.all(np.isfinite(l_matrix)):
            raise np.linalg.LinAlgError("Non finite values in L matrix")

        # Main diagonal of L not positive
        if np.min(np.diagonal(l_matrix)) <= 0.0:
            raise np.linalg.LinAlgError("Main diagonal of L not positive")

        # Errors in L matrix multiplication
        if np.max(np.abs(k_matrix - np.dot(l_matrix, l_matrix.T))) > 1e-4:
            raise np.linalg.LinAlgError("Errors in L matrix multiplication")
