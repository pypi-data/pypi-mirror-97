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

import deap.gp
import deap.creator


def add_mutation(toolbox, pset, mutation_method='all'):
    """

    :param toolbox:
    :type toolbox:
    :param pset:
    :type pset:
    :param mutation_method:
    :type mutation_method:
    :return:
    :rtype:
    """

    toolbox.register(
        "mutate_uniform",
        deap.gp.mutUniform,
        expr=toolbox.random_mini_expr,
        pset=pset
    )
    toolbox.register(
        "mutate_replacement",
        deap.gp.mutNodeReplacement,
        pset=pset
    )
    toolbox.register(
        "mutate_shrink",
        deap.gp.mutShrink
    )
    toolbox.register(
        "mutate_insert",
        deap.gp.mutInsert,
        pset=pset
    )

    if mutation_method == "all":
        mutate_functions = [
            toolbox.mutate_uniform,
            toolbox.mutate_replacement,
            toolbox.mutate_shrink,
            # TODO toolbox.mutate_insert,
        ]
    else:
        raise Exception("This mutation method is not available")

    toolbox.register(
        "mutate",
        mut_kernel,
        mutate_functions=mutate_functions
    )
    toolbox.decorate("mutate", toolbox.remove_tuple_decorator)
    toolbox.decorate("mutate", toolbox.is_psd_decorator)
    toolbox.decorate("mutate", toolbox.inheritance_decorator)


def mut_kernel(old_individual, mutate_functions):
    """
    Replaces a randomly chosen primitive from *individual* by a randomly
    chosen primitive with the same number of arguments from the :attr:`pset`
    attribute of the individual.

    :param old_individual: The normal or typed tree to be mutated.
    :type old_individual:
    :param mutate_functions: mutate_functions:
    :type mutate_functions:
    :return: A tuple of one tree.
    :rtype:
    """

    mutate_function = np.random.choice(mutate_functions)

    old_prim_tree = deap.gp.PrimitiveTree(old_individual)

    new_prim_tree = mutate_function(old_prim_tree)[0]

    new_individual = deap.creator.Individual(new_prim_tree)

    new_individual.log.origin = "{} from {}".format(
        mutate_function.func.__name__,
        old_individual.log.id
    )

    if str(new_individual) == str(old_individual):
        return None,

    return new_individual,
