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


class GoWithTheFirst(KernelFittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None):

        super(GoWithTheFirst, self).__init__(
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

        max_eval, max_fun_call = self.get_max_eval(budget)
        nmut = max(3, int(max_eval * 0.01))
        hof_size = 1
        npop = self.get_npop(
            hof_size,
            int(float(max_eval) / (nmut + 1))
        )

        best_state, initial_state = self.model_to_state(model)

        population = self.toolbox.random_population(n=npop)
        id_i = 0
        for ind in population:
            ind.log.id = id_i
            id_i += 1

        # Evaluate the individuals with an invalid fitness
        self.evaluate_population(
            model,
            best_state,
            initial_state,
            max_fun_call,
            folds,
            population,
            verbose=verbose
        )

        for gen_i in range(npop - hof_size + 1):
            best_pop = []
            pop_size = npop - gen_i
            pop_j = 0
            while pop_j < pop_size:
                best = population[pop_j]
                mut_k = 0
                while mut_k < nmut:
                    mutated_individual = self.toolbox.mutate(best)[0]
                    best.log.id = id_i
                    best.log.creation = gen_i + 1
                    id_i += 1
                    eval_population = [mutated_individual]
                    self.evaluate_population(
                        model,
                        best_state,
                        initial_state,
                        max_fun_call,
                        folds,
                        eval_population,
                        verbose=verbose
                    )
                    mutated_individual = eval_population[0]
                    best = self.toolbox.select([best, mutated_individual], 1)[0]
                    mut_k += 1
                best_pop.append(best)
                pop_j += 1

            population[:] = self.toolbox.select(
                best_pop,
                max(1, pop_size - 1)
            )

        best = population[0]

        self.best_to_model(model, best_state, best)

        return best_state

    @staticmethod
    def get_npop(hof_size, max_eval):
        """

        :param hof_size:
        :type hof_size:
        :param max_eval:
        :type max_eval:
        :return:
        :rtype:
        """
        n_pop = hof_size
        n_eval = hof_size
        while n_eval <= max_eval:
            n_pop += 1
            n_eval += n_pop

        return n_pop - 1
