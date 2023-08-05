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

from gplib.metrics.metric import Metric


class MetaMetric(Metric):
    """

    """
    def __init__(self, metrics):
        self.metrics = metrics

    def fold_measure(self, model, folds, grad_needed=False):
        results = [[
                metric.measure(
                    model,
                    train_set=train_set,
                    test_set=test_set,
                    grad_needed=grad_needed)
                for train_set, test_set in folds
            ]
            for metric in self.metrics
        ]
        return np.mean(results, axis=1)

    @staticmethod
    def measure(model, train_set, test_set=None, grad_needed=False):
        """

        :param model:
        :type model:
        :param train_set:
        :type train_set:
        :param test_set:
        :type test_set:
        :param grad_needed:
        :type grad_needed:
        :return:
        :rtype:
        """

        pass
