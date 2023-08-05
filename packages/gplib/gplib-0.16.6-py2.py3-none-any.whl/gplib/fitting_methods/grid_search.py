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

import time

import numpy as np

from .fitting_method import FittingMethod
from ..parameters.parameter import Parameter


class GridSearch(FittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, group=None,
                 nested_fit_method=None):

        self.obj_fun = obj_fun
        self.group = Parameter.GRID_GROUP
        if group is not None:
            self.group = group
        self.max_fun_call = max_fun_call
        super(GridSearch, self).__init__(nested_fit_method)

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
        if budget is None or self.max_fun_call < budget:
            max_fun_call = self.max_fun_call
        else:
            max_fun_call = budget

        start = time.time()

        best_state = {
            'name': self.__class__.__name__,
            'fun_calls': 0,
            'improvements': 0,
            'restarts': 0,
            'time': 0,
            'value': np.inf
        }
        best_state.update(self.save_state(model))
        initial_state = self.save_state(model)

        param_grid = model.get_grid(
            limit=max_fun_call,
            only_group=self.group,
            trans=False
        )

        if len(param_grid) < 1:
            param_grid = [[]]

        i = 0
        while best_state['fun_calls'] < max_fun_call and i < len(param_grid):
            current_params = param_grid[i]
            i += 1

            # run optimization
            value = np.inf
            self.load_state(model, initial_state)
            model.set_param_values(
                current_params,
                only_group=self.group,
                trans=False
            )
            nested_log = None
            try:
                if self.nested_fit_method is not None:
                    nested_log = self.nested_fit_method.fit(
                        model,
                        folds,
                        budget=(max_fun_call - best_state['fun_calls'] - 1),
                        verbose=verbose
                    )
                    best_state['fun_calls'] += nested_log['fun_calls']
                value = self.obj_fun(
                    model=model,
                    folds=folds,
                    grad_needed=False
                )
            except (AssertionError, np.linalg.linalg.LinAlgError) as ex:
                if verbose:
                    print(ex)

            best_state['fun_calls'] += 1
            best_state['restarts'] += 1
            if value < best_state['value']:
                best_state['improvements'] += 1
                best_state['value'] = value
                best_state['state'] = model.get_param_values(
                    only_group=self.group,
                    trans=False
                )
                best_state['nested'] = nested_log

        end = time.time()

        assert best_state['improvements'], "No params were found"

        self.load_state(model, best_state)

        best_state['time'] = end - start

        return best_state

    def save_state(self, model):
        """

        :param model:
        :type model:
        :return:
        :rtype:
        """
        state = self.nested_save_state(model)
        state['state'] = model.get_param_values(
            only_group=self.group,
            trans=False
        )

        return state

    def load_state(self, model, state):
        """

        :param model:
        :type model:
        :param state:
        :type state:
        :return:
        :rtype:
        """
        model.set_param_values(
            state['state'],
            only_group=self.group,
            trans=False
        )
        self.nested_load_state(model, state)
