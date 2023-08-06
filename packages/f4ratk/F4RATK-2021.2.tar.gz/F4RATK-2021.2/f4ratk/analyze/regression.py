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
from enum import Enum, unique
from logging import getLogger

import pandas
from pandas import DataFrame
from statsmodels.formula import api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper

from f4ratk.shared import first_period, last_period

log = getLogger(__name__)


@unique
class ModelType(Enum):
    CAPM = "CAPM"
    FF3 = "FF3"
    FF5 = "FF5"
    FF6 = "FF6"


@dataclass(frozen=True)
class Result:
    model_type: ModelType
    model: RegressionResultsWrapper


@dataclass(frozen=True)
class Results:
    capm: Result
    ff3: Result
    ff5: Result
    ff6: Result


class RegressionRunner:
    def run(self, returns: DataFrame, fama_data: DataFrame) -> Results:
        combined = self._combine(returns, fama_data)

        return Results(
            capm=self._run(model_type=ModelType.CAPM, data=combined),
            ff3=self._run(model_type=ModelType.FF3, data=combined),
            ff5=self._run(model_type=ModelType.FF5, data=combined),
            ff6=self._run(model_type=ModelType.FF6, data=combined),
        )

    def _combine(self, returns: DataFrame, fama_data: DataFrame) -> DataFrame:
        log.info(
            f"Returns data range: {first_period(returns)} - {last_period(returns)}"
        )
        log.info(
            f"Fama data range : {first_period(fama_data)} - {last_period(fama_data)}"
        )

        combined: DataFrame = pandas.merge(
            returns, fama_data, left_index=True, right_index=True
        )

        combined['XsRet'] = combined['Returns'] - combined['RF']

        log.info(
            f"Result date range: {first_period(combined)} - {last_period(combined)}"
        )

        return combined

    def _run(self, model_type: ModelType, data: DataFrame) -> Result:
        formula = self._formula(model_type)
        model = self._model(formula=formula, data=data)
        return Result(model_type=model_type, model=model)

    def _formula(self, type: ModelType) -> str:
        if type == ModelType.CAPM:
            return 'XsRet ~ MKT'
        elif type == ModelType.FF3:
            return 'XsRet ~ MKT + SMB + HML'
        elif type == ModelType.FF5:
            return 'XsRet ~ MKT + SMB + HML + RMW + CMA'
        elif type == ModelType.FF6:
            return 'XsRet ~ MKT + SMB + HML + RMW + CMA + WML'
        raise ValueError

    def _model(self, formula: str, data: DataFrame) -> RegressionResultsWrapper:
        return sm.ols(formula=formula, data=data).fit(
            cov_type='HAC', cov_kwds={'maxlags': None}, use_t=True
        )
