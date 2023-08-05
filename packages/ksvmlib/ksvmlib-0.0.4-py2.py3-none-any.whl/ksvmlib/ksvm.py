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

import sklearn.svm

from gplib.parameters.none_parameter_transformation \
    import NoneParameterTransformation
from gplib.parameters.parameter import Parameter
from gplib.parameters.with_parameters import WithParameters
from gplib.kernel_functions.kernel_function import KernelFunction


class KSVM(WithParameters):
    """

    """

    def __init__(self, kernel, kernel_params_to_grid=True):
        self.kernel_params_to_grid = kernel_params_to_grid
        self.kernel = None
        self.set_kernel_function(kernel)
        c_hyperparam = Parameter(
            name="C",
            transformation=NoneParameterTransformation,
            default_value=[[np.power(2., i) for i in range(-5, 15, 2)]]
        )

        super(KSVM, self).__init__(
            name="KSVM",
            hyperparameters=[c_hyperparam, kernel]
        )

    def predict(self, train_set, test_set=None,
                sample_weight=None, probability=False):
        """

        :param train_set:
        :type train_set:
        :param test_set:
        :type test_set:
        :param sample_weight:
        :type sample_weight:
        :param probability:
        :type probability:
        :return:
        :rtype:
        """

        cov_train = self.kernel.function(
            train_set['X']
        )
        assert np.isfinite(cov_train).all(), "NaN values in cov matrix"

        evo_svm = sklearn.svm.SVC(
            kernel='precomputed',
            max_iter=1e05,
            decision_function_shape='ovo',
            probability=probability,
            C=self.get_param_value("C")
        )

        try:
            evo_svm.fit(
                cov_train,
                train_set['Y'].flatten(),
                sample_weight=sample_weight
            )
        except sklearn.exceptions.ConvergenceWarning as ex:
            raise AssertionError(str(ex))

        if test_set is not None:
            cov_train_test = self.kernel.function(
                test_set['X'],
                train_set['X']
            )
            assert np.isfinite(cov_train_test).all(), "NaN values in cov matrix"
        else:
            cov_train_test = cov_train

        if probability:
            log_proba = evo_svm.predict_log_proba(cov_train_test)

            class_i = {
                item: index
                for index, item in enumerate(evo_svm.classes_)
            }

            indexes = np.array([
                [i, class_i[item]]
                for i, item in enumerate(test_set['Y'].flatten())
            ])

            prediction = log_proba[
                indexes[:, 0].flatten(),
                indexes[:, 1].flatten()
            ][:, None]
        else:
            prediction = evo_svm.predict(cov_train_test)[:, None]

        return prediction

    def get_c(self, train_folds):
        """

        :param train_folds:
        :type train_folds:
        :return:
        :rtype:
        """

        cov_matrix = self.kernel.function(
            np.vstack((train_folds[0][0]['X'], train_folds[0][1]['X']))
        )

        m = float(len(cov_matrix))

        s2 = np.power(m, -1) * np.sum(np.diag(cov_matrix)) - \
            np.power(m, -2) * np.sum(cov_matrix)

        c = np.power(s2, -1)

        assert 0.0 < c, "Invalid C value"

        return c

    def kernel_params_to_grid(self):
        """

        :return:
        :rtype:
        """

    def get_kernel_function(self):
        """

        :return:
        :rtype:
        """
        return self.kernel

    def set_kernel_function(self, kernel):
        """

        :param kernel:
        :type kernel:
        :return:
        :rtype:
        """
        assert isinstance(kernel, KernelFunction), \
            "Is not instance of CovarianceFunction"

        self.kernel = kernel
        if hasattr(self, 'hyperparameters'):
            self.set_hyperparam("Ker", kernel)
        if self.kernel_params_to_grid:
            for hp in self.kernel.get_hyperparams():
                hp.group = Parameter.GRID_GROUP
                hp.default_values = [[
                    np.power(2., i)
                    for i in np.arange(-5., 4.01, 1.)
                ]]
