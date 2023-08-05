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

from .mean_function import MeanFunction


class Posterior(MeanFunction):
    """

    """
    def __init__(self, prior_gp, prior_data):

        self.prior_gp = prior_gp
        self.prior_data = prior_data

        super(Posterior, self).__init__(
            self.prior_gp.mean_function.get_hyperparams()
        )

    def marginalize_mean(self, x):
        """
        Marginalize posterior mean

        :param x:
        :return:
        """
        ka_matrix = self.prior_gp.\
            covariance_function.marginalize_covariance(
                self.prior_data['X'], x)
        test_mean = self.prior_gp.mean_function.marginalize_mean(x)

        prior_multivariate_gaussian = self.prior_gp.marginalize_gp(
            self.prior_data['X'], add_noise=True
        )
        mean = prior_multivariate_gaussian.conditional_mean(
            self.prior_data['Y'],
            ka_matrix,
            test_mean
        )

        return mean

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

        raise NotImplementedError("Not Implemented. This is an interface.")
