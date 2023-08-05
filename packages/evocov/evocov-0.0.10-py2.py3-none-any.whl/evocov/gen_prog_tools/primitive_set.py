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

import collections

import numpy as np

import deap.gp


class InputX(object):
    pass


class OnlyDiagonal(object):
    pass


class HyperParameter(object):
    pass


# class Dimension(object):
#     pass


class ShapeX(object):
    pass


class TransX(object):
    pass


class CovMatrix(object):
    pass


def get_primitive_set(arg_num):
    """

    :param arg_num:
    :type arg_num:
    :return:
    :rtype:
    """
    pset = deap.gp.PrimitiveSetTyped(
        "MAIN",
        [InputX, OnlyDiagonal] + ([HyperParameter] * arg_num),
        CovMatrix
    )
    pset.renameArguments(ARG0='x')
    pset.renameArguments(ARG1='onlyvar')
    for i in range(arg_num):
        pset.renameArguments(**{'ARG{}'.format(i+2): 'hp{}'.format(i)})
    # for i in range(20):
    #     pset.addEphemeralConstant(
    #         'ec{}'.format(i),
    #         lambda: np.exp(np.random.uniform(-10, 10)),
    #         HyperParameter
    #     )

    #  TERMNINALS  #

    # HyperParameter Type
    pset.addTerminal(0.5, HyperParameter)
    pset.addTerminal(1.0, HyperParameter)
    pset.addTerminal(2.0, HyperParameter)
    pset.addTerminal(3.0, HyperParameter)
    pset.addTerminal(5.0, HyperParameter)

    # Dimension Type
    # for i in range(dims):
    #     pset.addTerminal(i, Dimension)

    #  PRIMITIVES  #

    # ShapeX Type
    pset.addPrimitive(
        x_shape,
        [InputX],
        ShapeX,
        "x_shape"
    )

    # TransX Type
    pset.addPrimitive(
        lambda x: x,
        [InputX],
        TransX,
        "map"
    )
    # pset.addPrimitive(
    #     x_mask,
    #     [InputX, Dimension],
    #     TransX,
    #     "x_mask"
    # )
    pset.addPrimitive(
        x_div,
        [TransX, HyperParameter],
        TransX,
        "x_div"
    )
    pset.addPrimitive(
        x_sub,
        [TransX, HyperParameter],
        TransX,
        "x_sub"
    )
    pset.addPrimitive(
        spectral,
        [TransX],
        TransX,
        "spectral"
    )

    # CovMatrix Type
    pset.addPrimitive(
        sq_distance,
        [TransX, OnlyDiagonal],
        CovMatrix,
        "sq_distance"
    )
    pset.addPrimitive(
        dot_product,
        [TransX, OnlyDiagonal],
        CovMatrix,
        "dot_product"
    )
    pset.addPrimitive(
        constant,
        [ShapeX, HyperParameter, OnlyDiagonal],
        CovMatrix,
        "constant"
    )
    pset.addPrimitive(
        noise,
        [ShapeX, HyperParameter, OnlyDiagonal],
        CovMatrix,
        "noise"
    )
    # pset.addPrimitive(
    #     polynomial,
    #     [CovMatrix, HyperParameter, Dimension],
    #     CovMatrix,
    #     "polynomial"
    # )
    # pset.addPrimitive(
    #     comp_fun,
    #     [TransX, OnlyDiagonal],
    #     CovMatrix,
    #     "comp_fun"
    # )
    # pset.addPrimitive(
    #     change_window,
    #     [
    #         MaskedX,
    #         CovMatrix, CovMatrix,
    #         HyperParameter, HyperParameter, HyperParameter, OnlyDiagonal
    #     ],
    #     CovMatrix,
    #     "cw"
    # )
    # pset.addPrimitive(
    #     change_point,
    #     [
    #         MaskedX,
    #         CovMatrix, CovMatrix,
    #         HyperParameter, HyperParameter, OnlyDiagonal
    #     ],
    #     CovMatrix,
    #     "cp"
    # )
    pset.addPrimitive(np.add, [CovMatrix, CovMatrix], CovMatrix)
    pset.addPrimitive(np.multiply, [CovMatrix, CovMatrix], CovMatrix)
    pset.addPrimitive(np.exp, [CovMatrix], CovMatrix)
    pset.addPrimitive(np.negative, [CovMatrix], CovMatrix)
    pset.addPrimitive(np.tanh, [CovMatrix], CovMatrix)
    pset.addPrimitive(np.power, [CovMatrix, HyperParameter], CovMatrix)
    pset.addPrimitive(
        lambda x: np.power(x, -1.0),
        [CovMatrix],
        CovMatrix,
        "div"
    )
    pset.addPrimitive(np.sqrt, [CovMatrix], CovMatrix)
    pset.addPrimitive(np.square, [CovMatrix], CovMatrix)

    pset.cont_primitives = collections.defaultdict(list)
    pset.end_primitives = collections.defaultdict(list)
    for type_, primitives in pset.primitives.items():
        pset.cont_primitives[type_] = []
        pset.end_primitives[type_] = []
        for prim in primitives:
            if np.any([arg == type_ for arg in prim.args]):
                pset.cont_primitives[type_].append(prim)
            else:
                pset.end_primitives[type_].append(prim)

    return pset


def x_shape(x):
    """

    :param x:
    :type x:
    :return:
    :rtype:
    """

    mat_a, mat_b = x

    len_a = len(mat_a)
    if mat_b is None:
        len_b = None
    else:
        len_b = len(mat_b)

    return len_a, len_b


def x_div(x, ls):
    """

    :param x:
    :type x:
    :param ls:
    :type ls:
    :return:
    :rtype:
    """
    mat_a, mat_b = x

    t_mat_a = mat_a / ls
    if mat_b is not None:
        t_mat_b = mat_b / ls
    else:
        t_mat_b = None

    return t_mat_a, t_mat_b


def x_sub(x, shift):
    """

    :param x:
    :type x:
    :param shift:
    :type shift:
    :return:
    :rtype:
    """
    mat_a, mat_b = x

    t_mat_a = mat_a - shift
    if mat_b is not None:
        t_mat_b = mat_b - shift
    else:
        t_mat_b = None

    return t_mat_a, t_mat_b


# def x_mask(x, dim):
#     """
#
#     :param x:
#     :type x:
#     :param dim:
#     :type dim:
#     :return:
#     :rtype:
#     """
#     mat_a, mat_b = x
#     total_dims = mat_a.shape[1]
#     masked_dim = int(dim)
#     mask = np.full(total_dims, np.nan)
#     mask[masked_dim] = 1.0
#     t_mat_a = mat_a * mask
#     if mat_b is not None:
#         t_mat_b = mat_b * mask
#     else:
#         t_mat_b = None
#
#     return t_mat_a, t_mat_b


def spectral(transformed_x):
    """

    :param transformed_x:
    :type transformed_x: tuple
    :return:
    :rtype: tuple
    """
    mat_a, mat_b = transformed_x

    a_param = 2.0 * np.pi

    spectral_mat_a = np.hstack((
        np.sin(a_param * mat_a),
        np.cos(a_param * mat_a)
    ))

    spectral_mat_b = None
    if mat_b is not None:
        spectral_mat_b = np.hstack((
            np.sin(a_param * mat_b),
            np.cos(a_param * mat_b)
        ))

    spectral_x = (spectral_mat_a, spectral_mat_b)

    return spectral_x


def sq_distance(transformed_x, only_diagonal):
    """

    :param transformed_x:
    :type transformed_x: tuple
    :param only_diagonal:
    :type only_diagonal:
    :return:
    :rtype: np.ndarray
    """
    mat_a, mat_b = transformed_x

    mat_a = np.nan_to_num(mat_a)
    if mat_b is None:
        if only_diagonal:
            return np.zeros((len(mat_a), 1))

        center = np.mean(mat_a, axis=0)
        mat_a = mat_a - center
        mat_a_sq = np.sum(np.square(mat_a), 1)

        r2 = mat_a_sq[:, None] + mat_a_sq[None, :]

        r2 -= 2. * np.dot(mat_a, mat_a.T)

        np.lib.stride_tricks.as_strided(
            r2, shape=(r2.shape[0], ),
            strides=((r2.shape[0] + 1) * r2.itemsize, )
        )[:, ] = 0
    else:
        mat_b = np.nan_to_num(mat_b)
        center = np.mean(np.vstack((mat_a, mat_b)), axis=0)
        mat_a = mat_a - center
        mat_b = mat_b - center
        mat_a_sq = np.sum(np.square(mat_a), 1)
        mat_b_sq = np.sum(np.square(mat_b), 1)

        r2 = mat_a_sq[:, None] + mat_b_sq[None, :]

        r2 -= 2. * np.dot(mat_a, mat_b.T)

    r2 = r2.clip(min=0.0)
    return r2


def dot_product(transformed_x, only_diagonal):
    """

    :param transformed_x:
    :type transformed_x: tuple
    :param only_diagonal:
    :type only_diagonal: bool
    :return:
    :rtype: np.ndarray
    """
    mat_a, mat_b = transformed_x

    mat_a = np.nan_to_num(mat_a)
    if mat_b is None:
        if only_diagonal:
            return np.sum(np.square(mat_a), axis=1)[:, None]
        mat_b = mat_a
    else:
        mat_b = np.nan_to_num(mat_b)
    return np.dot(mat_a, mat_b.T)


def constant(shape_x, ov, only_diagonal):
    """

    :param shape_x:
    :type shape_x: tuple
    :param ov:
    :type ov: float
    :param only_diagonal:
    :type only_diagonal:
    :return:
    :rtype: np.ndarray
    """

    len_a, len_b = shape_x

    if len_b is None:
        len_b = len_a
        if only_diagonal:
            len_b = 1

    return ov * np.ones((len_a, len_b))


def noise(shape_x, ov, only_diagonal):
    """

    :param shape_x:
    :type shape_x: tuple
    :param ov:
    :type ov: float
    :param only_diagonal:
    :type only_diagonal:
    :return:
    :rtype: np.ndarray
    """

    len_a, len_b = shape_x

    if len_b is not None:
        return np.zeros((len_a, len_b))

    if only_diagonal:
        return ov * np.ones((len_a, 1))

    return ov * np.eye(len_a)


# def polynomial(cov, coef, dim):
#     """
#
#     :param cov:
#     :type cov:
#     :param coef:
#     :type coef:
#     :param dim:
#     :type dim:
#     :return:
#     :rtype:
#     """
#
#     return np.multiply(coef, np.power(cov, dim))
#
#
# def comp_fun(transformed_x, only_diagonal):
#     """
#
#     :param transformed_x:
#     :type transformed_x: tuple
#     :param only_diagonal:
#     :type only_diagonal:
#     :return:
#     :rtype: np.ndarray
#     """
#     mat_a, mat_b = transformed_x
#
#     if mat_b is None:
#         if only_diagonal:
#             return np.ones((len(mat_a), 1))
#
#         center = np.mean(mat_a, axis=0)
#         mat_a = mat_a - center
#         mat_a_sq = -0.5 * np.sum(np.square(mat_a), 1)
#
#         r2 = mat_a_sq[:, None] + mat_a_sq[None, :]
#
#         r2 += np.dot(mat_a, mat_a.T)
#
#     else:
#         center = np.mean(np.vstack((mat_a, mat_b)), axis=0)
#         mat_a = mat_a - center
#         mat_b = mat_b - center
#         mat_a_sq = -0.5 * np.sum(np.square(mat_a), 1)
#         mat_b_sq = -0.5 * np.sum(np.square(mat_b), 1)
#
#         r2 = mat_a_sq[:, None] + mat_b_sq[None, :]
#
#         r2 += np.dot(mat_a, mat_b.T)
#
#     return np.exp(r2)
#
#
# def change_window(masked_x, cov1, cov2,
#                   location, steepness, width, only_diagonal):
#     """
#
#     :param masked_x:
#     :type masked_x:
#     :param cov1:
#     :type cov1:
#     :param cov2:
#     :type cov2:
#     :param location:
#     :type location:
#     :param steepness:
#     :type steepness:
#     :param width:
#     :type width:
#     :param only_diagonal:
#     :type only_diagonal:
#     :return:
#     :rtype:
#     """
#     mat_a, mat_b = masked_x
#
#     tx1 = np.tanh(
#         (mat_a - (location - 0.5 * width)) * steepness
#     )
#     tx2 = np.tanh(
#         -(mat_a - (location + 0.5 * width)) * steepness
#     )
#     ax = np.multiply((0.5 + 0.5 * tx1), (0.5 + 0.5 * tx2))
#     if mat_b is not None:
#         tz1 = np.tanh(
#             (mat_b - (location - 0.5 * width)) * steepness
#         )
#         tz2 = np.tanh(
#             -(mat_b - (location + 0.5 * width)) * steepness
#         )
#         az = np.multiply((0.5 + 0.5 * tz1), (0.5 + 0.5 * tz2)).T
#     else:
#         if only_diagonal:
#             az = ax
#         else:
#             az = ax.T
#
#     k_matrix = np.multiply(np.multiply(ax, cov2), az) + \
#         np.multiply(np.multiply((1 - ax), cov1), (1 - az))
#
#     return k_matrix
#
#
# def change_point(masked_x, cov1, cov2, location, steepness, only_diagonal):
#     """
#
#     :param masked_x:
#     :type masked_x:
#     :param cov1:
#     :type cov1:
#     :param cov2:
#     :type cov2:
#     :param location:
#     :type location:
#     :param steepness:
#     :type steepness:
#     :param only_diagonal:
#     :type only_diagonal:
#     :return:
#     :rtype:
#     """
#     mat_a, mat_b = masked_x
#
#     tx = np.tanh(
#         (mat_a - location) * steepness
#     )
#     ax = 0.5 + 0.5 * tx
#     if mat_b is not None:
#         tz = np.tanh(
#             (mat_b - location) * steepness
#         )
#         az = (0.5 + 0.5 * tz).T
#     else:
#         if only_diagonal:
#             az = ax
#         else:
#             az = ax.T
#
#     ax = 1 - ax
#     az = 1 - az
#
#     k_matrix = np.multiply(np.multiply(ax, cov1), az) + \
#         np.multiply(np.multiply((1 - ax), cov2), (1 - az))
#
#     return k_matrix
