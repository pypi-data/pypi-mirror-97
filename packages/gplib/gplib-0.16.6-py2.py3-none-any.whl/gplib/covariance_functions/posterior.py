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

from .covariance_function import CovarianceFunction


class Posterior(CovarianceFunction):
    """

    """
    def __init__(self, prior_gp, prior_data):
        
        self.prior_gp = prior_gp
        self.prior_data = prior_data

        super(Posterior, self).__init__(
            "Cov", self.prior_gp.covariance_function.get_hyperparams(),
        )

    def marginalize_covariance(self, mat_a, mat_b=None, only_diagonal=False):
        """
        Measures the distance matrix between solutions of A and B, and
        applies the kernel function element-wise to the distance matrix.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :param only_diagonal:
        :type only_diagonal:
        :return: Result matrix with kernel function applied element-wise.
        :rtype:
        """

        kxa_matrix = self.prior_gp.covariance_function.marginalize_covariance(
            self.prior_data['X'],
            mat_a
        )

        if mat_b is None:
            if only_diagonal:
                kab_matrix = \
                    self.prior_gp.covariance_function.marginalize_covariance(
                        mat_a, only_diagonal=True
                    )
            else:
                kab_matrix = \
                    self.prior_gp.covariance_function.marginalize_covariance(
                        mat_a
                    )
            kxb_matrix = None
        else:
            kab_matrix = \
                self.prior_gp.covariance_function.marginalize_covariance(
                    mat_a, mat_b
                )
            kxb_matrix = \
                self.prior_gp.covariance_function.marginalize_covariance(
                    self.prior_data['X'],
                    mat_b
                )

        prior_multivariate_gaussian = self.prior_gp.marginalize_gp(
            self.prior_data['X'], add_noise=True
        )
        covariance = prior_multivariate_gaussian.conditional_cov(
            kxa_matrix,
            kxb_matrix,
            kab_matrix
        )

        return covariance

    def dk_dx(self, mat_a, mat_b=None):
        """
        Measures gradient of the distance between solutions of A and B in X.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :param mat_b: List of solutions in lines and dimensions in columns.
        :return: 3D array with the gradient in every dimension of X.
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def dk_dtheta(self, mat_a, mat_b=None, trans=False):
        """
        Measures gradient of the distance between solutions of A and B in the
        hyper-parameter space.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :param trans: Return results in the transformed space.
        :type trans:
        :return: 3D array with the gradient in every
         dimension the length-scale hyper-parameter space.
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")
