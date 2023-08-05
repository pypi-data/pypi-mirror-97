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

from ..kernel_functions.kernel_function import KernelFunction
from .covariance_function import CovarianceFunction


class KernelBased(CovarianceFunction):
    """

    """
    def __init__(self, kernel_function):

        self.kernel_function = kernel_function
        hyperparameters = [kernel_function]

        super(CovarianceFunction, self).__init__("Cov", hyperparameters)

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
        covariance = self.kernel_function.function(
            mat_a=mat_a,
            mat_b=mat_b,
            only_diagonal=only_diagonal
        )

        return covariance

    def dk_dx(self, mat_a, mat_b=None):
        """
        Measures gradient of the distance between solutions of A and B in X.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :return: 3D array with the gradient in every dimension of X.
        :rtype:
        """
        dk_dx = self.kernel_function.dk_dx(
            mat_a=mat_a,
            mat_b=mat_b
        )

        return dk_dx

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
        dk_dtheta = self.kernel_function.dk_dtheta(
            mat_a=mat_a,
            mat_b=mat_b,
            trans=trans
        )

        return dk_dtheta

    def get_kernel_function(self):
        """

        :return:
        :rtype:
        """
        return self.kernel_function

    def set_kernel_function(self, kernel_function):
        """

        :param kernel_function:
        :type kernel_function:
        :return:
        :rtype:
        """
        assert isinstance(kernel_function, KernelFunction), \
            "Is not instance of CovarianceFunction"

        self.kernel_function = kernel_function
        self.set_hyperparam("Ker", kernel_function)
