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

from .mean_function import MeanFunction

from ..parameters.parameter import Parameter
from ..parameters.none_parameter_transformation import \
    NoneParameterTransformation


class Fixed(MeanFunction):
    """

    """
    def __init__(self, mean=0.):
        hyperparams = [
            Parameter(
                "mean",
                transformation=NoneParameterTransformation,
                default_value=[[mean]]
            )
        ]

        super(Fixed, self).__init__(hyperparams)

    def marginalize_mean(self, x):
        """

        :param x:
        :return:
        """

        return np.ones((x.shape[0], 1)) * self.get_param_value('mean')

    def dmu_dx(self, x):
        """

        :param x:
        :type x:
        :return:
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def dmu_dtheta(self, x, trans=False):
        """

        :param x:
        :type x:
        :param trans:
        :type trans:
        :return:
        :rtype:
        """

        return tuple()
