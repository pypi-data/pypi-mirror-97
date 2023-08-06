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

from logging import getLogger
from typing import Union

from pandas import DataFrame, Period, period_range
from pandas.tseries.offsets import BusinessDay, MonthEnd

from f4ratk.domain import Frequency

log = getLogger(__name__)


def format_range(df: DataFrame) -> str:
    return f"{first_period(df)} - {last_period(df)}"


def last_period(df: DataFrame) -> Period:
    return df.index.max()


def first_period(df: DataFrame) -> Period:
    return df.index.min()


class Downsampler:
    def monthly_sample(self, data: DataFrame) -> DataFrame:
        return data.resample(BusinessDay()).interpolate().resample(MonthEnd()).last()


class Normalizer:
    def index_to_periods(self, data: DataFrame, frequency: Frequency) -> DataFrame:
        offset = self._to_offset(frequency)
        return data.to_period(freq=offset)

    def _to_offset(self, frequency: Frequency) -> Union[BusinessDay, MonthEnd]:
        if frequency == Frequency.DAILY:
            return BusinessDay()
        elif frequency == Frequency.MONTHLY:
            return MonthEnd()

        raise NotImplementedError


class QualityChecker:
    def investigate(self, data: DataFrame):
        observation_pct = self._relative_observations(data)

        if observation_pct < 0.95:
            log.warning(
                f"Quote data contains only {observation_pct:.2%} of possible periods"
            )
        else:
            log.info(f"Quote data contains {observation_pct:.2%} of possible periods")

    @staticmethod
    def _relative_observations(data: DataFrame) -> float:
        return len(data) / len(
            period_range(start=first_period(data), end=last_period(data))
        )
