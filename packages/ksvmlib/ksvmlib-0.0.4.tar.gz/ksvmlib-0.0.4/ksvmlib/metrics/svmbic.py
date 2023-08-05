# -*- coding: utf-8 -*-
#
#    Copyright 2020 Ibai Roman
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

from gplib.metrics.metric import Metric


class SVMBIC(Metric):
    """

    """

    @staticmethod
    def measure(model, train_set, test_set=None, grad_needed=False):
        """

        :param model:
        :type model:
        :param train_set:
        :type train_set:
        :param test_set:
        :type test_set:
        :param grad_needed:
        :type grad_needed:
        :return:
        :rtype:
        """

        if test_set is None:
            raise TypeError("Test set should be provided")

        if grad_needed:
            raise NotImplementedError("Accuracy gradient")

        prediction = model.predict(train_set, test_set, probability=True)

        proba = np.sum(prediction)

        n = train_set['X'].shape[0]
        m = model.get_kernel_function().get_param_n()
        bic = -2 * proba + m * np.log(n)

        return bic
