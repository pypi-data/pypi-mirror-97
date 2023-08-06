##############################################################################
# Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from textwrap import dedent
from typing import TextIO

from statsmodels.iolib.summary2 import summary_col

from f4ratk.analyze.evaluation import EvaluatedResult, EvaluatedResults


class ResultsWriter:
    def __init__(self, file: TextIO):
        self._file = file

    def write(self, results: EvaluatedResults) -> None:
        self._write_summary(results)
        print(file=self._file)
        self._write_forecast(results.ff6)
        print(file=self._file)
        self._write_ff6_details(results.ff6)

    def _write_summary(self, results: EvaluatedResults) -> None:
        summary = summary_col(
            results=list(result.model for result in results),
            stars=True,
            model_names=list(result.model_type.value for result in results),
            info_dict={
                'N': lambda x: "{0:d}".format(int(x.nobs)),
            },
            regressor_order=['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA', 'WML'],
        )

        print(summary, file=self._file)

    def _write_forecast(self, result: EvaluatedResult) -> None:
        print(
            dedent(
                f"""\
                Expected excess return before cost: {result.evaluation:.3}%

                Notes:
                  Based on the determined factor loadings and historic
                  factor returns. Past performance is not a guarantee of
                  future results nor an indicator of future performance.

                """
            ),
            file=self._file,
        )

    def _write_ff6_details(self, ff6: EvaluatedResult) -> None:
        print(ff6.model.summary(), file=self._file)
