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

import deap.tools


def add_selection(toolbox, selection_method):
    """

    :param toolbox:
    :type toolbox:
    :param selection_method:
    :type selection_method:
    :return:
    :rtype:
    """
    if selection_method == 'best':
        toolbox.register("select", deap.tools.selBest)
    elif selection_method == 'NSGA2':
        toolbox.register("select", deap.tools.selNSGA2)
    else:
        raise Exception("This selection method is not available")

    toolbox.register("get_nondominated", get_nondominated)

def get_nondominated(population):
    """

    :param population:
    :type population:
    :return:
    :rtype:
    """
    return deap.tools.sortNondominated(
        population,
        len(population),
        first_front_only=True
    )[0]
