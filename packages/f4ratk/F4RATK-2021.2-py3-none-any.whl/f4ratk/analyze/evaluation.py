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

from dataclasses import dataclass
from logging import getLogger
from typing import Iterator

from pandas import Series
from statsmodels.regression.linear_model import RegressionResultsWrapper

from f4ratk.analyze.regression import ModelType, Result
from f4ratk.history import AnnualizedReturns

log = getLogger(__name__)


@dataclass(frozen=True)
class EvaluatedResult:
    model_type: ModelType
    model: RegressionResultsWrapper
    evaluation: float

    @staticmethod
    def of(result: Result, evaluation: float) -> "EvaluatedResult":
        return EvaluatedResult(
            model_type=result.model_type, model=result.model, evaluation=evaluation
        )


@dataclass(frozen=True)
class EvaluatedResults:
    capm: Result
    ff3: Result
    ff5: Result
    ff6: EvaluatedResult

    def __iter__(self) -> Iterator[Result]:
        yield from (self.capm, self.ff3, self.ff5, self.ff6)


class Critic:
    _TARGET_FACTORS = ['MKT', 'SMB', 'HML', 'RMW', 'CMA', 'WML']

    def evaluate(
        self, result: Result, historic_returns: AnnualizedReturns
    ) -> EvaluatedResult:
        log.debug(f"Evaluating with: {historic_returns}")

        factors = self._normalize(self._significant_factors(result.model))
        expectation = self._expectation(historic_returns)

        forecast = factors.mul(expectation).sum()

        return EvaluatedResult.of(result=result, evaluation=forecast)

    def _significant_factors(self, model: RegressionResultsWrapper) -> Series:
        targeted = model.params[Critic._TARGET_FACTORS]
        return targeted[model.pvalues < 0.1]

    def _normalize(self, factors: Series) -> Series:
        if 'MKT' in factors:
            factors['MKT'] -= 1
        return factors

    def _expectation(self, historic_returns: AnnualizedReturns) -> Series:
        return historic_returns.all().div(2)
