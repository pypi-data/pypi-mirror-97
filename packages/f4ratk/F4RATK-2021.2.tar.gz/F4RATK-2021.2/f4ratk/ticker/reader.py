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
from logging import getLogger
from typing import Optional

from pandas import DataFrame, merge

from f4ratk.data_reader import yahoo_reader
from f4ratk.domain import Currency, Frame, Frequency
from f4ratk.exchange import ExchangeReader
from f4ratk.shared import Downsampler, Normalizer, QualityChecker

log = getLogger(__name__)


@dataclass(frozen=True)
class Stock:
    ticker_symbol: str
    currency: Currency = Currency.USD


def read_ticker(stock: Stock, frame: Frame) -> DataFrame:
    ticker_reader = TickerReader(
        ExchangeReader(frame.frequency), Normalizer(), Downsampler(), QualityChecker()
    )

    return ticker_reader.data(stock, frame.frequency, frame.start, frame.end)


class TickerReader:
    ADJUSTED_CLOSE_COLUMN = 'Adj Close'

    def __init__(
        self,
        exchange_reader: ExchangeReader,
        normalizer: Normalizer,
        downsampler: Downsampler,
        checker: Optional[QualityChecker] = None,
    ):
        self._exchange_reader = exchange_reader
        self._normalizer = normalizer
        self._downsampler = downsampler
        self._checker = checker

    def data(
        self,
        stock: Stock,
        frequency: Frequency,
        start: Optional[date] = None,
        end: Optional[date] = None,
    ) -> DataFrame:
        data = self._read_stock_data(stock, start, end)
        data = self._normalize_date_range(data, frequency)

        if stock.currency is not Currency.USD:
            data = self._convert_currency(data, stock.currency, start, end)

        data['Returns'] = self._calculate_returns_as_relative_percentage(data)

        log.debug(
            f"Stock data of symbol '{stock.ticker_symbol}' starts at: \n%s", data.head()
        )

        return data[['Returns']].dropna()

    def _read_stock_data(
        self, stock: Stock, start: Optional[date], end: Optional[date]
    ) -> DataFrame:
        data: DataFrame = yahoo_reader(stock.ticker_symbol, start, end).read()
        return data

    def _convert_currency(
        self,
        data: DataFrame,
        currency: Currency,
        start: Optional[date],
        end: Optional[date],
    ) -> DataFrame:
        exchange_data = self._exchange_reader.exchange_data(currency, start, end)

        data = merge(data, exchange_data, left_index=True, right_index=True)

        source_currency_close_column = f"{self.ADJUSTED_CLOSE_COLUMN} ({currency.name})"

        data = data.rename(
            columns={self.ADJUSTED_CLOSE_COLUMN: source_currency_close_column}
        )

        data[self.ADJUSTED_CLOSE_COLUMN] = (
            data[source_currency_close_column]
            * data[ExchangeReader.EXCHANGE_RATE_COLUMN]
        )

        return data

    def _calculate_returns_as_relative_percentage(self, data: DataFrame) -> DataFrame:
        return data[[self.ADJUSTED_CLOSE_COLUMN]].pct_change() * 100

    def _normalize_date_range(self, data: DataFrame, frequency: Frequency) -> DataFrame:
        data = self._normalizer.index_to_periods(data=data, frequency=Frequency.DAILY)

        if self._checker:
            self._checker.investigate(data)

        if frequency == Frequency.MONTHLY:
            data = self._down_sample(data)

        return data

    def _down_sample(self, data: DataFrame) -> DataFrame:
        log.info("Downsampling ticker data to monthly rate")
        data = self._downsampler.monthly_sample(data=data)
        return data
