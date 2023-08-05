# -*- coding: utf-8 -*-
#
#    Copyright 2020 Ibai Roman
#
#    This file is part of EvoCov.
#
#    EvoCov is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    EvoCov is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with EvoCov. If not, see <http://www.gnu.org/licenses/>.

import time

import numpy as np

import deap.base
import deap.creator

from gplib.fitting_methods.fitting_method import FittingMethod
from ..gen_prog_tools import primitive_set, creation


class KernelFittingMethod(FittingMethod):
    """

    """
    MAX_SIGMA = 10.0 ** 20

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None):

        self.max_fun_call = max_fun_call

        self.obj_fun = obj_fun

        self.toolbox = deap.base.Toolbox()

        self.pset = primitive_set.get_primitive_set(
            arg_num=20
        )

        creation.add_creation(
            toolbox=self.toolbox,
            pset=self.pset,
            max_depth=30,
            dims=dims
        )

        super(KernelFittingMethod, self).__init__(
            nested_fit_method=nested_fit_method
        )

    def evaluate_population(self, model, best_state, initial_state,
                            max_fun_call, folds,
                            population, all_population=None, verbose=False):
        """

        :param model:
        :type model:
        :param best_state:
        :type best_state:
        :param initial_state:
        :type initial_state:
        :param max_fun_call:
        :type max_fun_call:
        :param folds:
        :type folds:
        :param population:
        :type population:
        :param all_population:
        :type all_population:
        :param verbose:
        :type verbose:
        :return:
        :rtype:
        """
        for pop_i in range(len(population)):
            # run optimization
            cur_individual = population[pop_i]
            all_pop_i = 0
            if all_population is not None:
                while all_population[all_pop_i] != cur_individual:
                    all_pop_i += 1
            self.load_state(model, initial_state)
            model.set_kernel_function(cur_individual)
            if verbose:
                print(model.get_kernel_function())

            nested_log = None
            best_state['fun_calls'] += 1
            try:
                if self.nested_fit_method is not None:
                    nested_log = self.nested_fit_method.fit(
                        model,
                        folds,
                        budget=max_fun_call - best_state['fun_calls'],
                        verbose=verbose
                    )
                    best_state['fun_calls'] += nested_log['fun_calls']
                fitness = self.obj_fun(
                    model=model,
                    folds=folds,
                    grad_needed=False
                )
                if not hasattr(fitness, "__len__"):
                    fitness = [fitness]
                if verbose:
                    print(fitness)
            except (AssertionError, np.linalg.linalg.LinAlgError) as ex:
                fitness = [KernelFittingMethod.MAX_SIGMA]
                if verbose:
                    print(ex)

            individual = model.get_kernel_function()
            individual.fitness.setValues(fitness)
            individual.nested = nested_log
            individual.log.evals += 1
            population[pop_i] = individual
            if all_population is not None:
                all_population[all_pop_i] = individual

    def model_to_state(self, model):
        """

        :param model:
        :type model:
        :return:
        :rtype:
        """
        start = time.time()

        best_state = {
            'name': self.__class__.__name__,
            'fun_calls': 0,
            'value': np.inf,
            'time': start,
            'creation': 0,
            'evals': 0,
            'id': 0,
            'origin': 0,
            'hp_count': 0,
            'prim_count': 0
        }
        best_state.update(self.save_state(model))
        initial_state = self.save_state(model)
        return best_state, initial_state

    def best_to_model(self, model, best_state, best):
        """

        :param model:
        :type model:
        :param best_state:
        :type best_state:
        :param best:
        :type best:
        :return:
        :rtype:
        """
        end = time.time()

        best_state['value'] = best.fitness.getValues()
        best_state['time'] = end - best_state['time']
        best_state['creation'] = best.log.creation
        best_state['evals'] = best.log.evals
        best_state['id'] = best.log.id
        best_state['origin'] = best.log.origin
        best_state['hp_count'] = best.log.hp_count
        best_state['prim_count'] = best.log.prim_count
        best_state['state'] = str(best)
        best_state['nested'] = best.nested

        self.load_state(model, best_state)

    def save_state(self, model):
        """

        :param model:
        :type model:
        :return:
        :rtype:
        """
        if not isinstance(model.get_kernel_function(), deap.creator.Individual):
            raise Exception("Kernel is not Individual")

        state = self.nested_save_state(model)
        state['state'] = str(model.get_kernel_function())

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
        kernel = state['state']
        if not isinstance(kernel, str):
            raise Exception("Kernel is not str")

        kernel = self.toolbox.individual_from_string(kernel)
        model.set_kernel_function(kernel)
        self.nested_load_state(model, state)

    def get_max_eval(self, budget):
        """

        :param budget:
        :type budget:
        :return:
        :rtype:
        """
        if budget is None or self.max_fun_call < budget:
            max_fun_call = self.max_fun_call
        else:
            max_fun_call = budget

        max_eval = max_fun_call
        if self.nested_fit_method is not None:
            max_eval = int(
                max_fun_call / (self.nested_fit_method.max_fun_call + 1)
            )

        return max_eval, max_fun_call

    def get_random_kernel(self):
        """

        :return:
        :rtype:
        """
        return self.toolbox.random_individual()

    def get_kernel_from_str(self, kernel_str):
        """

        :param kernel_str:
        :type kernel_str:
        :return:
        :rtype:
        """
        return self.toolbox.individual_from_string(kernel_str)

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
