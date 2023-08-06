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
from math import sqrt

from pandas import DataFrame, Period, Series, concat

from f4ratk.domain import Frequency, Region
from f4ratk.fama import FamaReader
from f4ratk.shared import first_period, format_range, last_period

log = getLogger(__name__)


@dataclass(frozen=True)
class AnnualizedReturns:
    _data: DataFrame
    _first: Period
    _last: Period

    def all(self) -> Series:
        return self._data['Returns']

    def __str__(self) -> str:
        sep = f"\n{'#' * 25}\n"
        nl = '\n'

        header = "Annualized Returns (%)"
        period = f"Period: {self._first} - {self._last}"
        frequency = f"Frequency: {Frequency.MONTHLY.name}"

        content = self._data.to_string(col_space=10, float_format='{:0.3f}'.format)

        return "".join((header, sep, period, nl, frequency, nl * 2, content))


class Historian:
    def __init__(self, fama_reader: FamaReader):
        self._fama_reader = fama_reader

    def annualized_returns(self, region: Region) -> AnnualizedReturns:
        returns = self._historic_returns(region=region)
        annualized = self._monthly_annualized_returns(data=returns)

        log.info(f"Historic data range {format_range(returns)}")

        return annualized

    def _historic_returns(self, region: Region) -> DataFrame:
        return self._fama_reader.fama_data(region=region, frequency=Frequency.MONTHLY)

    @staticmethod
    def _monthly_annualized_returns(data: DataFrame) -> AnnualizedReturns:
        periods = 12 / len(data)

        annualized_returns: Series = Series(
            data.div(100).add(1).prod().pow(periods).sub(1).mul(100), name="Returns"
        )

        annualized_std: Series = Series(data.std().mul(sqrt(12)), name="SD")

        return AnnualizedReturns(
            _data=concat((annualized_returns, annualized_std), axis='columns'),
            _first=first_period(data),
            _last=last_period(data),
        )


class History:
    def __init__(self, historian: Historian):
        self._historian = historian

    def display_history(self, region: Region):
        returns = self.annualized_returns(region)
        print(returns)

    def annualized_returns(self, region: Region):
        return self._historian.annualized_returns(region=region)
