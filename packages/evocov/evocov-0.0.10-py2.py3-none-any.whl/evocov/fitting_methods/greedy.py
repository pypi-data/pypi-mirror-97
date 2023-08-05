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

from .kernel_fitting_method import KernelFittingMethod

from ..gen_prog_tools import selection
from ..gen_prog_tools import mutation


class Greedy(KernelFittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None):

        super(Greedy, self).__init__(
            obj_fun,
            max_fun_call=max_fun_call,
            dims=dims,
            nested_fit_method=nested_fit_method
        )

        selection.add_selection(
            toolbox=self.toolbox,
            selection_method='best'
        )

        mutation.add_mutation(
            toolbox=self.toolbox,
            pset=self.pset,
            mutation_method='all'
        )

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

        _, max_fun_call = self.get_max_eval(budget)

        best_state, initial_state = self.model_to_state(model)
        best_state['restarts'] = 0
        individual = model.get_kernel_function()

        base_id = int(individual.log.id * 1e5)
        best = individual
        population = []
        while best_state['fun_calls'] < max_fun_call:
            individual.log.id = base_id + best_state['restarts']
            # run optimization
            eval_population = [individual]
            self.evaluate_population(
                model,
                best_state,
                initial_state,
                max_fun_call,
                folds,
                eval_population,
                verbose=verbose
            )
            individual = eval_population[0]
            best_state['restarts'] += 1

            population.append(individual)
            best = self.toolbox.select(population, 1)[0]
            population = [best]
            individual = self.toolbox.mutate(best)[0]

        self.best_to_model(model, best_state, best)

        return best_state
