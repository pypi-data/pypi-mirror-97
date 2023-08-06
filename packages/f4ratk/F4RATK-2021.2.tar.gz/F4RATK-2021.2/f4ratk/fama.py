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

import logging as log
from dataclasses import dataclass
from enum import Enum, unique

from pandas import NA, DataFrame, DatetimeIndex, merge

from f4ratk.data_reader import fama_french_reader
from f4ratk.domain import Frequency, Region
from f4ratk.shared import Normalizer


@unique
class ReturnsData(Enum):
    DEVELOPED_5_DAILY = 'Developed_5_Factors_Daily'
    DEVELOPED_5_MONTHLY = 'Developed_5_Factors'
    DEVELOPED_MOM_DAILY = 'Developed_Mom_Factor_Daily'
    DEVELOPED_MOM_MONTHLY = 'Developed_Mom_Factor'

    DEVELOPED_EX_US_5_DAILY = 'Developed_ex_US_5_Factors_Daily'
    DEVELOPED_EX_US_5_MONTHLY = 'Developed_ex_US_5_Factors'
    DEVELOPED_EX_US_MOM_DAILY = 'Developed_ex_US_Mom_Factor_Daily'
    DEVELOPED_EX_US_MOM_MONTHLY = 'Developed_ex_US_Mom_Factor'

    US_5_DAILY = 'F-F_Research_Data_5_Factors_2x3_daily'
    US_5_MONTHLY = 'F-F_Research_Data_5_Factors_2x3'
    US_MOM_DAILY = 'F-F_Momentum_Factor_daily'
    US_MOM_MONTHLY = 'F-F_Momentum_Factor'

    EU_5_DAILY = 'Europe_5_Factors_Daily'
    EU_5_MONTHLY = 'Europe_5_Factors'
    EU_MOM_DAILY = 'Europe_Mom_Factor_Daily'
    EU_MOM_MONTHLY = 'Europe_Mom_Factor'

    EMERGING_5_MONTHLY = 'Emerging_5_Factors'
    EMERGING_MOM_MONTHLY = 'Emerging_MOM_Factor'


@dataclass
class ReturnsRequest:
    frequency: Frequency
    five: ReturnsData
    momentum: ReturnsData

    @staticmethod
    def _source_for(region: Region, frequency: Frequency) -> (ReturnsData, ReturnsData):
        if region == Region.DEVELOPED:
            if frequency == Frequency.DAILY:
                return (
                    ReturnsData.DEVELOPED_5_DAILY,
                    ReturnsData.DEVELOPED_MOM_DAILY,
                )
            elif frequency == Frequency.MONTHLY:
                return (
                    ReturnsData.DEVELOPED_5_MONTHLY,
                    ReturnsData.DEVELOPED_MOM_MONTHLY,
                )
        if region == Region.DEVELOPED_EX_US:
            if frequency == Frequency.DAILY:
                return (
                    ReturnsData.DEVELOPED_EX_US_5_DAILY,
                    ReturnsData.DEVELOPED_EX_US_MOM_DAILY,
                )
            elif frequency == Frequency.MONTHLY:
                return (
                    ReturnsData.DEVELOPED_EX_US_5_MONTHLY,
                    ReturnsData.DEVELOPED_EX_US_MOM_MONTHLY,
                )
        elif region == Region.US:
            if frequency == Frequency.DAILY:
                return (ReturnsData.US_5_DAILY, ReturnsData.US_MOM_DAILY)
            elif frequency == Frequency.MONTHLY:
                return (ReturnsData.US_5_MONTHLY, ReturnsData.US_MOM_MONTHLY)
        elif region == Region.EU:
            if frequency == Frequency.DAILY:
                return (ReturnsData.EU_5_DAILY, ReturnsData.EU_MOM_DAILY)
            elif frequency == Frequency.MONTHLY:
                return (ReturnsData.EU_5_MONTHLY, ReturnsData.EU_MOM_MONTHLY)
        elif region == Region.EMERGING:
            if frequency == Frequency.MONTHLY:
                return (
                    ReturnsData.EMERGING_5_MONTHLY,
                    ReturnsData.EMERGING_MOM_MONTHLY,
                )

        raise ValueError(
            f"'{frequency.name}' data unvailable for '{region.name}' region."
        )

    @staticmethod
    def of(region: Region, frequency: Frequency) -> 'ReturnsRequest':
        five, momentum = ReturnsRequest._source_for(region, frequency)

        return ReturnsRequest(frequency=frequency, five=five, momentum=momentum)


class FamaReader:
    def __init__(self, normalizer: Normalizer):
        self._normalizer = normalizer

    def fama_data(self, region: Region, frequency: Frequency) -> DataFrame:
        sources = ReturnsRequest.of(region, frequency)
        return self._fama_data(sources)

    def _fama_data(
        self,
        request: ReturnsRequest,
    ) -> DataFrame:
        data_ff = self._fama_ff_data(request.five, request.frequency)
        data_mom = self._fama_momentum_data(request.momentum, request.frequency)

        combined: DataFrame = merge(
            data_ff, data_mom, left_index=True, right_index=True
        )

        log.debug(f"Fama data of set '{combined}' ends at\n%s", combined.tail())

        return combined

    def _fama_ff_data(self, source: ReturnsData, frequency: Frequency) -> DataFrame:
        data = self._load_fama_data(source, frequency)
        data = data.rename(columns={'Mkt-RF': 'MKT'})
        return data

    def _fama_momentum_data(
        self, source: ReturnsData, frequency: Frequency
    ) -> DataFrame:
        data: DataFrame = self._load_fama_data(source, frequency)

        if source == ReturnsData.US_MOM_DAILY or source == ReturnsData.US_MOM_MONTHLY:
            data = data.rename(columns={'Mom   ': 'WML'})

        return data

    def _load_fama_data(self, source: ReturnsData, frequency: Frequency) -> DataFrame:
        data: DataFrame = fama_french_reader(returns_data=source.value).read()[0]

        if isinstance(data.index, DatetimeIndex):
            data = self._normalizer.index_to_periods(data, frequency)
            log.debug(
                f"Fama reader returned DatetimeIndex for source '{source}', converted to frequency '{frequency}'"  # noqa: E501
            )

        data = data.replace(-99.99, NA)
        data = data.dropna()

        return data
