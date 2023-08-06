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

from pandas import DataFrame

from f4ratk.analyze.api import DataAnalyzer
from f4ratk.analyze.evaluation import Critic, EvaluatedResults
from f4ratk.analyze.output import ResultsWriter
from f4ratk.analyze.regression import RegressionRunner, Results
from f4ratk.history import AnnualizedReturns


class DataAnalyzerAdapter(DataAnalyzer):
    def __init__(
        self, regression_runner: RegressionRunner, critic: Critic, writer: ResultsWriter
    ):
        self._regression_runner = regression_runner
        self._critic = critic
        self._writer = writer

    def analyze(
        self,
        returns: DataFrame,
        fama_data: DataFrame,
        historic_returns: AnnualizedReturns,
    ) -> None:
        regression_results = self._regression_runner.run(
            returns=returns, fama_data=fama_data
        )

        evaluated_results = self._evaluate(regression_results, historic_returns)

        self._writer.write(evaluated_results)

    def _evaluate(
        self, regression: Results, historic_returns: AnnualizedReturns
    ) -> EvaluatedResults:
        evaluated_ff6 = self._critic.evaluate(regression.ff6, historic_returns)

        return EvaluatedResults(
            capm=regression.capm,
            ff3=regression.ff3,
            ff5=regression.ff5,
            ff6=evaluated_ff6,
        )
