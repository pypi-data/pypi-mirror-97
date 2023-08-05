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

from .validation import Validation


class Unfold(Validation):
    """

    """
    def __init__(self, fold_len):
        self.fold_len = fold_len

    def get_folds(self, data_set):
        """

        :param data_set:
        :type data_set:
        :return:
        :rtype:
        """
        return self.split_data(
            data_set,
            n_reps=1,
            stratified=False,
            shuffle=False,
            folds_n=1,
            fold_len=self.fold_len
        )
