# -*- coding: utf-8 -*-
#
#   Copyright 2020 Ibai Roman
#
#   This file is part of EvoCov.
#
#   EvoCov is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   EvoCov is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with EvoCov. If not, see <http://www.gnu.org/licenses/>.

import numpy as np

import deap.gp
import deap.creator

from .primitive_set import CovMatrix


def add_crossover(toolbox, pset):
    """

    :param toolbox:
    :type toolbox:
    :param pset:
    :type pset:
    :return:
    :rtype:
    """
    toolbox.register(
        "mate",
        cx_kernel,
        pset=pset
    )
    toolbox.decorate("mate", toolbox.remove_tuple_decorator)
    toolbox.decorate("mate", toolbox.is_psd_decorator)
    toolbox.decorate("mate", toolbox.inheritance_decorator)


def cx_kernel(old_ind1, old_ind2, pset):
    """
    Randomly select in each individual and exchange each subtree with the
    point as root between each individual.

    :param old_ind1: First tree participating in the crossover.
    :type old_ind1:
    :param old_ind2: Second tree participating in the crossover.
    :type old_ind2:
    :param pset:
    :type pset:
    :returns: A tuple of two trees.
    :rtype:
    """

    pri_name = np.random.choice(['multiply', 'add'])

    old_prim_tree1 = deap.gp.PrimitiveTree(old_ind1)
    old_prim_tree2 = deap.gp.PrimitiveTree(old_ind2)

    old_prim_tree1 = get_typed_subtree(old_prim_tree1, CovMatrix)
    old_prim_tree2 = get_typed_subtree(old_prim_tree2, CovMatrix)

    new_prim_tree = merge_inds(pri_name, old_prim_tree1, old_prim_tree2, pset)

    new_individual = deap.creator.Individual(new_prim_tree)

    new_individual.log.origin = "cx_kernel from {} and {}".format(
        old_ind1.log.id,
        old_ind2.log.id
    )

    return new_individual,


def get_typed_subtree(individual, _type):
    """

    :param individual:
    :type individual:
    :param _type:
    :type _type:
    :return:
    :rtype:
    """
    if np.random.choice([False, True]):
        return individual

    subtree = []
    return_type = object
    while return_type != _type:
        subtree = individual[
            individual.searchSubtree(np.random.randint(0, len(individual) - 1))
        ]
        return_type = subtree[0].ret

    individual[slice(0, None, None)] = subtree[slice(0, None, None)]

    return individual


def merge_inds(pri_name, ind1, ind2, pset):
    """

    :param pri_name:
    :type pri_name:
    :param ind1:
    :type ind1:
    :param ind2:
    :type ind2:
    :param pset:
    :type pset:
    :return:
    :rtype:
    """
    primitive = select_element(
        pset, element_type="primitive", _type=CovMatrix, name=pri_name
    )[0]
    ind12 = ind1[:] + ind2[:]
    new_expr = [primitive]
    new_expr += ind12

    ind1[slice(0, None, None)] = new_expr[slice(0, None, None)]

    return ind1


def select_element(pset, element_type=None, _type=None, name=None):
    """

    :param pset:
    :type pset:
    :param element_type:
    :type element_type:
    :param _type:
    :type _type:
    :param name:
    :type name:
    :return:
    :rtype:
    """

    if element_type == "terminal":
        elements = pset.terminals
    elif element_type == "primitive":
        elements = pset.primitives
    else:
        raise Exception("element not found")

    if type is not None:
        elements = elements[_type]

    if name is not None:
        elements = [
            element
            for element in elements
            if element.name == name
        ]

    return [np.random.choice(elements)]
