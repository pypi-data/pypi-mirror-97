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
from datetime import date
from enum import Enum, unique
from pathlib import Path
from typing import Optional

from pandas import DataFrame, merge

from f4ratk.data_reader import CsvFileReader
from f4ratk.domain import Currency, Frame, Frequency
from f4ratk.exchange import ExchangeReader
from f4ratk.shared import Normalizer


@unique
class ValueFormat(Enum):
    PRICE = 'Prices'
    RETURN = 'Returns'


@dataclass(frozen=True)
class FileConfig:
    path: Path
    currency: Currency
    value_format: ValueFormat


def read_file(file_config: FileConfig, frame: Frame) -> DataFrame:
    file_reader = FileReader(
        csv_reader=CsvFileReader(path=file_config.path),
        exchange_reader=ExchangeReader(frame.frequency),
        currency=file_config.currency,
        value_format=file_config.value_format,
        normalizer=Normalizer(),
    )

    return file_reader.read(start=frame.start, end=frame.end, frequency=frame.frequency)


class FileReader:
    def __init__(
        self,
        csv_reader: CsvFileReader,
        exchange_reader: ExchangeReader,
        currency: Currency,
        value_format: ValueFormat,
        normalizer: Normalizer,
    ):
        self._csv_reader = csv_reader
        self._exchange_reader = exchange_reader
        self._currency = currency
        self._value_format = value_format
        self._normalizer = normalizer

    def read(
        self, start: Optional[date], end: Optional[date], frequency: Frequency
    ) -> DataFrame:
        data = self._csv_reader.read().sort_index()

        data = self._normalizer.index_to_periods(data=data, frequency=frequency)

        if self._currency is not Currency.USD:
            data = self._convert_currency(
                data=data, currency=self._currency, start=start, end=end
            )

        if self._value_format == ValueFormat.PRICE:
            data = data[['Returns']].pct_change() * 100

        return data.dropna()

    def _convert_currency(
        self, data: DataFrame, currency: Currency, start: date, end: date
    ) -> DataFrame:
        exchange_data = self._exchange_reader.exchange_data(currency, start, end)

        data = merge(data, exchange_data, left_index=True, right_index=True)

        data['Returns'] = data['Returns'] * data[ExchangeReader.EXCHANGE_RATE_COLUMN]

        return data[['Returns']]
