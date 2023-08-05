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

import deap.gp

from gplib.parameters.parameter import Parameter
from gplib.parameters.log_parameter_transformation \
    import LogParameterTransformation
from gplib.kernel_functions.kernel_function import KernelFunction


class GenProgKernel(deap.gp.PrimitiveTree, KernelFunction):
    """

    """

    def __init__(self, content):
        deap.gp.PrimitiveTree.__init__(self, content)

        self.complied_function = deap.gp.compile(self, self.pset)
        individual_args = [
            item.value
            for item in self
            if item.arity == 0 and item.conv_fct == str
        ]
        has_hps = [
            hp if hp in individual_args else None
            for hp in self.pset.arguments
            if 'hp' in hp
        ]

        hyperparams = []
        hp_arg = []

        for hp in has_hps:
            if hp:
                hyperparam = Parameter(
                    name=hp,
                    transformation=LogParameterTransformation,
                    default_value=1.0
                )
                hyperparams.append(hyperparam)
            else:
                hyperparam = None

            hp_arg.append(hyperparam)
        self.hp_arg = hp_arg

        KernelFunction.__init__(self, hyperparams)

        self.log.prim_count = sum([
            1
            for item in self
            if isinstance(item, deap.gp.Primitive)
        ])

        self.log.hp_count = self.get_param_n()

    def __hash__(self):
        hp_hashes = [hash(self.complied_function)]
        for hp in self.hyperparameters:
            if isinstance(hp, Parameter):
                if hp.is_array():
                    hp_hashes.extend(hash(tuple(hp.current_value)))
                else:
                    hp_hashes.append(hash(hp.current_value))
            else:
                raise Exception("Incorrect covariance structure")
        return hash(tuple(hp_hashes))

    def function(self, mat_a, mat_b=None, only_diagonal=False):
        """
        Measures the distance matrix between solutions of A and B, and
        applies the kernel function element-wise to the distance matrix.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :param only_diagonal:
        :type only_diagonal:
        :return: Result matrix with kernel function applied element-wise.
        :rtype:
        """
        variables = [(mat_a, mat_b), only_diagonal] + [
            hp.get_param_values()[0] if hp else 0.0 for hp in self.hp_arg]

        return self.complied_function(*variables)

    def dk_dx(self, mat_a, mat_b=None):
        """
        Measures gradient of the distance between solutions of A and B in X.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :return: 3D array with the gradient in every dimension of X.
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")

    def dk_dtheta(self, mat_a, mat_b=None, trans=False):
        """
        Measures gradient of the distance between solutions of A and B in the
        hyper-parameter space.

        :param mat_a: List of solutions in lines and dimensions in columns.
        :type mat_a:
        :param mat_b: List of solutions in lines and dimensions in columns.
        :type mat_b:
        :param trans: Return results in the transformed space.
        :type trans:
        :return: 3D array with the gradient in every
         dimension the length-scale hyper-parameter space.
        :rtype:
        """

        raise NotImplementedError("Not Implemented. This is an interface.")
