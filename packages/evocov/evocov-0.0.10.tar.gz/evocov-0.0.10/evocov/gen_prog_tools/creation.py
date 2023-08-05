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

import operator
import random
from inspect import isclass
from functools import wraps

import deap.tools
import deap.base
import deap.creator
import deap.gp

import numpy as np

import gplib

from .primitive_set import CovMatrix, HyperParameter
from ..kernel_functions.gen_prog_kernel import GenProgKernel


def add_creation(toolbox, pset, max_depth, dims):
    """
    
    :param toolbox: 
    :type toolbox: 
    :param pset: 
    :type pset: 
    :param max_depth: 
    :type max_depth: 
    :param dims: 
    :type dims: 
    :return: 
    :rtype: 
    """

    deap.creator.create(
        "FitnessMin",
        deap.base.Fitness,
        weights=tuple(-1.0 for _ in range(20))
    )

    deap.creator.create(
        "Log",
        object,
        id=0,
        evals=0,
        creation=0,
        hp_count=0,
        prim_count=0,
        origin=""
    )

    deap.creator.create(
        "Individual",
        GenProgKernel,
        pset=pset,
        fitness=deap.creator.FitnessMin,
        log=deap.creator.Log,
        nested=None
    )

    toolbox.register(
        "is_psd_decorator",
        is_psd_decorator,
        key=operator.attrgetter("height"),
        max_value=max_depth,
        dims=dims,
        check_noise_con=True,
        verbose=False
    )

    toolbox.register(
        "is_noise_con_psd_cov_decorator",
        is_psd_decorator,
        key=operator.attrgetter("height"),
        max_value=max_depth,
        dims=dims,
        check_noise_con=False,
        verbose=False
    )

    toolbox.register(
        "inheritance_decorator",
        inheritance_decorator,
        pset=pset
    )

    toolbox.register(
        "remove_tuple_decorator",
        remove_tuple_decorator
    )

    toolbox.register(
        "individual_from_string",
        deap.gp.PrimitiveTree.from_string,
        pset=pset
    )
    toolbox.decorate("individual_from_string", init_ind_decorator)
    toolbox.decorate(
        "individual_from_string",
        toolbox.is_noise_con_psd_cov_decorator
    )
    toolbox.decorate("individual_from_string", hps_decorator)

    toolbox.register(
        "random_expr",
        gen_typed,
        pset=pset,
        min_=3,
        max_=15
    )
    toolbox.register(
        "random_mini_expr",
        gen_typed,
        pset=pset,
        min_=3,
        max_=6
    )
    toolbox.register(
        "random_individual",
        toolbox.random_expr
    )
    toolbox.decorate("random_individual", init_ind_decorator)
    toolbox.decorate(
        "random_individual",
        toolbox.is_psd_decorator
    )

    toolbox.register(
        "random_population",
        deap.tools.initRepeat,
        list,
        toolbox.random_individual
    )


def is_psd_decorator(func, key, max_value, dims,
                     check_noise_con=True, verbose=True):
    """

    :param func:
    :type func:
    :param key:
    :type key:
    :param max_value:
    :type max_value:
    :param dims:
    :type dims:
    :param check_noise_con:
    :type check_noise_con:
    :param verbose:
    :type verbose:
    :return:
    :rtype:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        trial = 0
        while trial < 600:
            trial += 1
            candidate_individual = func(*args, **kwargs)
            if not candidate_individual:
                continue
            candidate_individual = is_psd(
                candidate_individual,
                dims,
                check_noise_con=check_noise_con,
                verbose=verbose
            )
            if not candidate_individual:
                continue
            if key(candidate_individual) <= max_value:
                return candidate_individual
        return None

    return wrapper


def is_psd(individual, dims, items=200, n_data_sets=50,
           check_noise_con=True, verbose=True):
    """

    :param individual:
    :type individual:
    :param dims:
    :type dims:
    :param items:
    :type items:
    :param n_data_sets:
    :type n_data_sets:
    :param check_noise_con:
    :type check_noise_con:
    :param verbose:
    :type verbose:
    :return:
    :rtype:
    """

    if verbose:
        print("s) {0}".format(str(individual)))

    saved_params = individual.get_param_values(trans=False)
    n_hp_trials = (10 * individual.get_param_n()) + 1

    i_hp_trials = 0
    individual_is_psd = False
    def_opt_values = individual.get_param_values(
        only_group=gplib.hp.parameter.Parameter.OPT_GROUP,
        trans=True
    )
    def_grid_values = individual.get_grid(
        only_group=gplib.hp.parameter.Parameter.GRID_GROUP,
        trans=False
    )
    while not individual_is_psd and i_hp_trials < n_hp_trials:
        if 0 < len(def_grid_values):
            individual.set_param_values(
                random.choice(def_grid_values),
                only_group=gplib.hp.parameter.Parameter.GRID_GROUP,
                trans=False
            )
        current_value = def_opt_values + np.array(
            np.random.normal(
                loc=0.0,
                scale=1.,
                size=len(def_opt_values)
            )
        )
        individual.set_param_values(
            current_value,
            only_group=gplib.hp.parameter.Parameter.OPT_GROUP,
            trans=True
        )
        individual_is_psd = True
        i_data_set = 0
        while individual_is_psd and i_data_set < n_data_sets:
            data = np.vstack((
                np.zeros(dims),
                np.random.rand(1, dims) +
                np.random.randn(int(items / 2.0), dims) * 1e-3,
                np.random.rand(int(items / 2.0), dims)
            ))
            cov_matrix = individual.function(data)
            try:
                if check_noise_con:
                    is_noise_con(cov_matrix)
                gplib.MGD._chol(cov_matrix)
            except np.linalg.LinAlgError:
                individual_is_psd = False
            i_data_set += 1
        i_hp_trials += 1

    individual.set_param_values(saved_params, trans=False)

    if not individual_is_psd:
        if verbose:
            print("\t[FAIL] Is not PSD")
        return None

    if verbose:
        print("\t[OK]")

    return individual


def is_noise_con(cov_matrix):
    """

    :param cov_matrix:
    :type cov_matrix:
    :return:
    :rtype:
    """

    # Cov matrix is Noise + Constant
    diag_index = np.eye(cov_matrix.shape[0], dtype=bool)
    diag_matrix = cov_matrix[diag_index]
    diagless_matrix = cov_matrix[np.logical_not(diag_index)]
    diag_diff = np.max(diag_matrix) - np.min(diag_matrix)
    diagless_diff = np.max(diagless_matrix) - np.min(diagless_matrix)
    if diag_diff < 1e-20 and diagless_diff < 1e-20:
        raise np.linalg.LinAlgError("Cov matrix is Noise + Constant")


def inheritance_decorator(func, pset):
    """

    :param func:
    :type func:
    :param pset:
    :type pset:
    :return:
    :rtype:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        old_inds = [
            ind
            for ind in args
            if isinstance(ind, deap.creator.Individual)
        ]
        if len(old_inds) == 2:
            change_ind2(old_inds[0], old_inds[1], pset)
        hps_to_inherit = {
            cov_hp.get_param_keys(recursive=False): cov_hp.get_param_values()[0]
            for old_ind in old_inds
            for cov_hp in old_ind.get_hyperparams()
        }

        candidate_individual = func(*args, **kwargs)

        new_inds = []
        if candidate_individual:
            load_hyperparams_to_cov(
                candidate_individual,
                hps_to_inherit
            )
            new_inds.append(candidate_individual)

        new_inds += old_inds[len(new_inds):]
        return tuple(new_inds)

    return wrapper


def change_ind2(ind1, ind2, pset):
    """

    :param ind1:
    :type ind1:
    :param ind2:
    :type ind2:
    :param pset:
    :type pset:
    :return:
    :rtype:
    """
    hps_in_ind1 = set(
        terminal.value for terminal in ind1[:]
        if type(terminal) == deap.gp.Terminal and 'hp' in str(terminal.value)
    )
    hps_in_ind2 = set(
        terminal.value for terminal in ind2[:]
        if type(terminal) == deap.gp.Terminal and 'hp' in str(terminal.value)
    )
    avaiable_hps = list(
        terminal.value
        for terminal in pset.terminals[HyperParameter]
        if terminal.value not in hps_in_ind1 and
        terminal.value not in hps_in_ind2 and 'hp' in str(terminal.value)
    )
    avaiable_hps.sort()
    random.shuffle(avaiable_hps)
    hps_to_remove = list(hps_in_ind1.intersection(hps_in_ind2))
    hps_to_remove.sort()
    random.shuffle(hps_to_remove)

    # Replace from ind2 the parameters that are also in ind1
    # Add them also to the new parameter dict
    for hp_to_remove in hps_to_remove:
        if avaiable_hps:
            hp_to_put = avaiable_hps.pop()
        else:
            hp_to_put = hp_to_remove
            print("No HPS left")
        for i in range(len(ind2[:])):
            if type(ind2[i]) == deap.gp.Terminal and \
                    ind2[i].value == hp_to_remove:
                ind2[i] = [
                    terminal
                    for terminal in pset.terminals[HyperParameter]
                    if hp_to_put == str(terminal.value)
                ][0]
        for hyperparam in ind2.get_hyperparams():
            if hyperparam.name == hp_to_remove:
                hyperparam.name = hp_to_put


def remove_tuple_decorator(func):
    """

    :param func:
    :type func:
    :return:
    :rtype:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret_tuple = func(*args, **kwargs)

        individual = ret_tuple[0]

        return individual
    return wrapper


def init_ind_decorator(func):
    """

    :param func:
    :type func:
    :return:
    :rtype:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        expr = func(*args, **kwargs)
        individual = deap.creator.Individual(expr)
        individual.log.origin = func.__name__
        return individual
    return wrapper


def hps_decorator(func):
    """

    :param func:
    :type func:
    :return:
    :rtype:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        hps = {}
        if 'hps' in kwargs:
            hps.update(kwargs['hps'])
            del kwargs['hps']

        individual = func(*args, **kwargs)

        load_hyperparams_to_cov(individual, hps)

        return individual
    return wrapper


def load_hyperparams_to_cov(individual, hps_to_inherit):
    """

    :param individual:
    :type individual:
    :param hps_to_inherit:
    :type hps_to_inherit:
    :return:
    :rtype:
    """

    if hps_to_inherit:
        for cov_hp in individual.get_hyperparams():
            name = cov_hp.get_param_keys(recursive=False)
            if name in hps_to_inherit:
                cov_hp.set_param_values(
                    [hps_to_inherit[name]]
                )


def gen_typed(pset, min_, max_, type_=None):
    """

    :param pset:
    :type pset:
    :param min_:
    :type min_:
    :param max_:
    :type max_:
    :param type_:
    :type type_:
    :return:
    :rtype:
    """
    if type_ is None:
        type_ = CovMatrix

    options = []
    desirable_options = []
    if len(pset.terminals[type_]) > 0:
        options.append('add_terminal')
        if 2 >= min_:
            desirable_options.append('add_terminal')
    if len(pset.cont_primitives[type_]) > 0:
        options.append('add_cont_primitive')
        if max_ >= 2:
            desirable_options.append('add_cont_primitive')
    if len(pset.end_primitives[type_]) > 0:
        options.append('add_end_primitive')
        if 2 >= min_:
            desirable_options.append('add_end_primitive')

    if len(options) == 1:
        result = options[0]
    elif len(options) < 1:
        raise Exception("No options left")
    else:
        if len(desirable_options) == 1:
            result = desirable_options[0]
        elif len(desirable_options) < 1:
            result = np.random.choice(options)
        else:
            result = np.random.choice(desirable_options)

    expr = []
    if result == 'add_terminal':
        term = np.random.choice(
            pset.terminals[type_]
        )

        if isclass(term):
            term = term()
        expr.append(term)
    if result in ['add_cont_primitive', 'add_end_primitive']:
        if result == 'add_cont_primitive':
            prim = np.random.choice(
                pset.cont_primitives[type_]
            )
        else:
            prim = np.random.choice(
                pset.end_primitives[type_]
            )
        expr.append(prim)
        for arg_type in prim.args:
            arg = gen_typed(
                pset, min_ - 1, max_ - 1, type_=arg_type
            )
            expr.extend(arg)

    return expr
