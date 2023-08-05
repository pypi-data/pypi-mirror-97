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

from .kernel_function import KernelFunction
from ..parameters.parameter import Parameter
from ..parameters.log_parameter_transformation import LogParameterTransformation
from ..parameters.none_parameter_transformation \
    import NoneParameterTransformation


class DotProductFunction(KernelFunction):
    """

    """
    def __init__(self, hyperparams, ls=None, shift=None):

        default_lengthscale = ls
        if default_lengthscale is None:
            default_lengthscale = 1.

        default_shift = shift
        if default_shift is None:
            default_shift = 1.

        hyperparams.append(Parameter(
            'lengthscale',
            transformation=LogParameterTransformation,
            default_value=default_lengthscale
        ))

        hyperparams.append(Parameter(
            'shift',
            transformation=NoneParameterTransformation,
            default_value=default_shift
        ))

        super(DotProductFunction, self).__init__(hyperparams)

    def function(self, mat_a, mat_b=None, only_diagonal=False):
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

        dot_product = self.dot_product(
            mat_a, mat_b=mat_b,
            only_diagonal=only_diagonal
        )

        result = self.dot_product_function(dot_product)

        return result

    def dot_product(self, mat_a, mat_b=None, only_diagonal=False):
        """
        Dot product of A and B.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :param only_diagonal:
        :type only_diagonal:
        :return: dot product between solutions of A and B.
        :rtype:
        """
        mat_a = (mat_a - self.get_param_value('shift')) / \
            self.get_param_value('lengthscale')

        if mat_b is None:
            if only_diagonal:
                return np.sum(np.square(mat_a), axis=1)[:, None]
            return np.dot(mat_a, mat_a.T)

        mat_b = (mat_b - self.get_param_value('shift')) / \
            self.get_param_value('lengthscale')

        return np.dot(mat_a, mat_b.T)

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

    def dot_product_function(self, dot_product):
        """

        :param dot_product:
        :type dot_product:
        :return:
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")
