# -*- coding: utf-8 -*-
#
#    Copyright 2019 Ibai Roman
#
#    This file is part of BOlib.
#
#    BOlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    BOlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BOlib. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import scipy.optimize as spo

from .optimization_method import OptimizationMethod


class RandomGrid(OptimizationMethod):
    """

    """

    def minimize(self, fun, x0, args=(),
                 bounds=(), maxiter=200,
                 square_size=1e-02, square_samples=0.1,
                 **unknown_options):
        """

        :param fun:
        :type fun:
        :param x0:
        :type x0:
        :param args:
        :type args:
        :param bounds:
        :type bounds:
        :param maxiter:
        :type maxiter:
        :param square_size:
        :type square_size:
        :param square_samples:
        :type square_samples:
        :param unknown_options:
        :type unknown_options:
        :return:
        :rtype:
        """

        # Main sample
        x_main = self.random_sample(
            bounds,
            int(maxiter * (1.0 - square_samples))
        )

        y_main = fun(x_main)

        # Fine tuning sample
        best_main = np.argmin(y_main)
        x_best_main = x_main[best_main, :]

        x_fine = self.random_sample(
            [
                (
                    x_best_main_i - (square_size * (bounds_i[1] - bounds_i[0])),
                    x_best_main_i + (square_size * (bounds_i[1] - bounds_i[0]))
                )
                for x_best_main_i, bounds_i in zip(x_best_main, bounds)
            ],
            int(maxiter * square_samples)
        )

        y_fine = fun(x_fine)

        # Selection
        x_total = np.vstack((x_main, x_fine))
        y_total = np.vstack((y_main, y_fine))

        best = np.argmin(y_total)

        x_best = x_total[best, :][None, :]
        y_best = y_total[best, 0]

        return spo.OptimizeResult(
            fun=y_best,
            x=x_best,
            nit=1,
            nfev=maxiter,
            success=True
        )
