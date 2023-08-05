# -*- coding: utf-8 -*-
#
#    Copyright 2019 Ibai Roman
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

from .parameters.with_parameters import WithParameters
from .covariance_functions.covariance_function import CovarianceFunction
from .kernel_functions.kernel_function import KernelFunction
from .kernel_functions.white_noise import WhiteNoise
from .covariance_functions.posterior import Posterior as PosteriorCov
from .covariance_functions.kernel_based import KernelBased
from .mean_functions.mean_function import MeanFunction
from .mean_functions.posterior import Posterior as PosteriorMean
from .multivariate_gaussian import MultivariateGaussian


class GaussianProcess(WithParameters):
    """
    GPlib module for Gaussian Process
    """
    def __init__(self, mean_function, covariance_function,
                 noise=True, cache_size=1):

        self.mean_function = mean_function
        assert isinstance(self.mean_function, MeanFunction), \
            "Is not instance of MeanFunction"
        if isinstance(covariance_function, KernelFunction):
            self.covariance_function = KernelBased(covariance_function)
        else:
            self.covariance_function = covariance_function
        assert isinstance(self.covariance_function, CovarianceFunction), \
            "Is not instance of CovarianceFunction"

        self.cache = {
            'size': cache_size,
            'gp_hashes': [],
            'data': [],
            'mgds': []
        }
        hyperparameters = [self.mean_function, self.covariance_function]
        if noise:
            self.noise_covariance_function = KernelBased(WhiteNoise())
            hyperparameters.append(self.noise_covariance_function)
        else:
            self.noise_covariance_function = None

        super(GaussianProcess, self).__init__("GP", hyperparameters)

    def get_posterior(self, data):
        """

        :param data:
        :type data:
        :return:
        :rtype:
        """
        return GaussianProcess(
            PosteriorMean(self, data),
            PosteriorCov(self, data),
            noise=False,
            cache_size=self.cache['size']
        )

    def sample(self, test_points, n_samples=10):
        """
        Sample the prior of the GP

        :param test_points:
        :type test_points:
        :param n_samples:
        :type n_samples:
        :return:
        :rtype:
        """
        multivariate_gaussian = self.marginalize_gp(
            test_points,
            add_noise=False
        )
        return multivariate_gaussian.sample(n_samples)

    def get_log_likelihood(self, data, grad_needed=False):
        """

        :param data:
        :type data:
        :param grad_needed:
        :type grad_needed:
        :return:
        :rtype:
        """

        multivariate_gaussian = self.marginalize_gp(data['X'], add_noise=True)
        dmu_dtheta = None
        dk_dtheta = None
        if grad_needed:
            dmu_dtheta = self.mean_function.dmu_dtheta(
                data['X'], trans=True)
            dk_dtheta = self.covariance_function.dk_dtheta(
                data['X'], trans=True)
            if self.noise_covariance_function is not None:
                dk_dtheta += self.noise_covariance_function.dk_dtheta(
                    data['X'], trans=True)
        return multivariate_gaussian.get_log_likelihood(
            data['Y'],
            dmu_dtheta,
            dk_dtheta
        )

    def get_log_predictive_density(self, data):
        """
        Measure the log predictive density

        :param data:
        :type data:
        :return:
        :rtype:
        """
        multivariate_gaussian = self.marginalize_gp(data['X'], add_noise=True)
        return multivariate_gaussian.get_log_predictive_density(
            data['Y']
        )

    def get_log_loocv_density(self, data):
        """
        Measure the log predictive density

        :param data:
        :type data:
        :return:
        :rtype:
        """
        multivariate_gaussian = self.marginalize_gp(data['X'], add_noise=True)
        return multivariate_gaussian.get_log_loocv_density(
            data['Y']
        )

    def marginalize_gp(self, data_x, add_noise=True):
        """
        Get mean and covariance of following points

        :param data_x:
        :type data_x:
        :param add_noise:
        :type add_noise:
        :return:
        :rtype:
        """

        # Data assertions
        assert not np.isnan(data_x).any(), "NaN values in X"
        assert not np.isinf(data_x).any(), "Inf values in X"

        gp_hash = hash(self)

        best_i = None
        best_size_diff = np.inf
        for cache_i in range(len(self.cache['gp_hashes'])):
            cached_gp_hash = self.cache['gp_hashes'][cache_i]
            if cached_gp_hash == gp_hash:
                cached_data = self.cache['data'][cache_i]

                data_size = min(cached_data.shape[0], data_x.shape[0])
                cached_data_hash = hash(cached_data[:data_size, :].tobytes())
                data_x_hash = hash(data_x[:data_size, :].tobytes())

                size_diff = np.abs(cached_data.shape[0] - data_x.shape[0])

                if cached_data_hash == data_x_hash and \
                        size_diff < best_size_diff:
                    best_i = cache_i
                    best_size_diff = size_diff

        if best_i is not None:
            cached_data = self.cache['data'][best_i]
            cached_l_mgd = self.cache['mgds'][best_i]
            cached_l_matrix = cached_l_mgd.l_matrix
            if cached_data.shape[0] == data_x.shape[0]:
                return cached_l_mgd
            elif cached_data.shape[0] < data_x.shape[0]:
                cached_cov_matrix = None
            else:
                cached_cov_matrix = \
                    self.covariance_function.marginalize_covariance(
                        cached_data
                    )
                if add_noise and self.noise_covariance_function is not None:
                    cached_cov_matrix += self.noise_covariance_function.\
                        marginalize_covariance(cached_data)
        else:
            cached_l_matrix = None
            cached_cov_matrix = None
        covariance = self.covariance_function.marginalize_covariance(data_x)
        if add_noise and self.noise_covariance_function is not None:
            covariance += self.noise_covariance_function.\
                marginalize_covariance(data_x)
        mean = self.mean_function.marginalize_mean(data_x)
        mgd = MultivariateGaussian(
            mean,
            covariance,
            cached_cov_matrix,
            cached_l_matrix
        )

        self.cache['gp_hashes'].append(gp_hash)
        self.cache['data'].append(data_x)
        self.cache['mgds'].append(mgd)

        if len(self.cache['gp_hashes']) > self.cache['size']:
            del self.cache['gp_hashes'][0]
            del self.cache['data'][0]
            del self.cache['mgds'][0]

        return mgd

    def get_kernel_function(self):
        """

        :return:
        :rtype:
        """
        return self.covariance_function.get_kernel_function()

    def set_kernel_function(self, kernel_function):
        """

        :param kernel_function:
        :type kernel_function:
        :return:
        :rtype:
        """
        self.covariance_function.set_kernel_function(kernel_function)
