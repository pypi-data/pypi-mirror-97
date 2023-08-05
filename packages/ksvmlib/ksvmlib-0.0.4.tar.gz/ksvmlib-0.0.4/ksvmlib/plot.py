# -*- coding: utf-8 -*-
#
#    Copyright 2019 Ibai Roman
#
#    This file is part of kSVMlib.
#
#    kSVMlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    kSVMlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with kSVMlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt

import gplib.plot

plt.style.use('ggplot')


def kernel_sort_data(svm, test_data=None, file_name=None):
    """

    :param svm:
    :type svm:
    :param test_data:
    :type test_data:
    :param file_name:
    :type file_name:
    :return:
    :rtype:
    """
    kernel = svm.get_kernel_function()

    covar = np.hstack((
        np.sum(
            kernel.function(
                test_data['X'],
                test_data['X']
            ),
            axis=0
        )[:, None],
        test_data['Y']
    )).T
    ordered_data = test_data['X'][np.lexsort(covar), :]
    gplib.plot.kernel(
        kernel_function=kernel,
        data=ordered_data,
        file_name=file_name
    )