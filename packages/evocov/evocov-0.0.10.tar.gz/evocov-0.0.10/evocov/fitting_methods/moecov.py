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

import numpy as np

import deap.algorithms

from .kernel_fitting_method import KernelFittingMethod
from ..gen_prog_tools import selection
from ..gen_prog_tools import mutation
from ..gen_prog_tools import crossover


class MOECov(KernelFittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None,
                 cxpb=0.4, mutpb=0.6, beta=1e-4):

        super(MOECov, self).__init__(
            obj_fun,
            max_fun_call=max_fun_call,
            dims=dims,
            nested_fit_method=nested_fit_method
        )

        selection.add_selection(
            toolbox=self.toolbox,
            selection_method='NSGA2'
        )

        mutation.add_mutation(
            toolbox=self.toolbox,
            pset=self.pset,
            mutation_method='all'
        )

        crossover.add_crossover(
            toolbox=self.toolbox,
            pset=self.pset
        )

        self.cxpb = cxpb
        self.mutpb = mutpb
        self.beta = beta

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
        ngen = int(np.power(max_eval, 0.535))
        npop = int(float(max_eval)/ngen)
        mu = max(3, int(npop * 0.25))

        best_state, initial_state = self.model_to_state(model)

        population = self.toolbox.random_population(n=npop)
        id_i = 0
        for ind in population:
            ind.log.id = id_i
            id_i += 1
        best_fitness_m2 = np.inf
        best_fitness_m1 = np.inf
        all_population = population

        # Begin the generational process
        for gen in range(0, ngen-1):

            # Evaluate the individuals with an invalid fitness
            self.evaluate_population(
                model,
                best_state,
                initial_state,
                max_fun_call,
                folds,
                population,
                all_population=all_population,
                verbose=verbose
            )

            # Measure improvement
            best_fitness = np.min(np.array([
                best.fitness.getValues()
                for best in population
            ]), axis=0)

            relative_improvement = \
                (0.5 * (best_fitness_m2 + best_fitness_m1) - best_fitness) / \
                np.abs(best_fitness)

            if verbose:
                print("\nrelative improvement: {}\n".format(
                    relative_improvement
                ))

            # Restart condition
            if self.beta < np.max(relative_improvement):
                # Select the next generation population
                selection = self.toolbox.select(population, mu)
                # Vary the population
                offspring = deap.algorithms.varOr(
                    selection,
                    self.toolbox,
                    npop-mu,
                    self.cxpb,
                    self.mutpb
                )
            else:
                if verbose:
                    print("\nRestart...\n")
                selection = []
                offspring = self.toolbox.random_population(n=npop)
                best_fitness_m1 = np.inf
                best_fitness = np.inf

            for ind in offspring:
                ind.log.creation = gen + 1
                ind.log.id = id_i
                id_i += 1

            population = offspring + selection
            all_population += offspring
            best_fitness_m2 = best_fitness_m1
            best_fitness_m1 = best_fitness

        # Evaluate the individuals with an invalid fitness
        self.evaluate_population(
            model,
            best_state,
            initial_state,
            max_fun_call,
            folds,
            population,
            all_population=all_population,
            verbose=verbose
        )

        front = self.toolbox.get_nondominated(population)
        best = front[0]

        self.best_to_model(model, best_state, best)

        return best_state
