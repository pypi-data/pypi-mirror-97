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


class FittingMethod(object):
    """

    """

    def __init__(self, nested_fit_method=None):

        self.nested_fit_method = nested_fit_method

    def fit(self, model, folds, budget=None, verbose=False):
        """

        :param model:
        :type model:
        :param folds:
        :type folds:
        :param budget:
        :type budget:
        :param verbose:
        :type verbose:
        :return:
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def save_state(self, model):
        """

        :param model:
        :type model:
        :return:
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def load_state(self, model, state):
        """

        :param model:
        :type model:
        :param state:
        :type state:
        :return:
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def nested_save_state(self, model):
        """

        :param model:
        :type model:
        :return:
        :rtype:
        """
        state = {}
        if self.nested_fit_method is not None:
            state['nested'] = self.nested_fit_method.save_state(model)

        return state

    def nested_load_state(self, model, state):
        """

        :param model:
        :type model:
        :param state:
        :type state:
        :return:
        :rtype:
        """

        if self.nested_fit_method is not None:
            self.nested_fit_method.load_state(model, state['nested'])
