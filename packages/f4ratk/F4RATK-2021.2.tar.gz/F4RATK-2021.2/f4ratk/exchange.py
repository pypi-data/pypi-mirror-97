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

from datetime import date
from logging import getLogger

from pandas import DataFrame

from f4ratk.data_reader import fred_reader
from f4ratk.domain import Currency, Frequency
from f4ratk.shared import first_period, last_period

log = getLogger(__name__)


class ExchangeReader:
    EXCHANGE_RATE_COLUMN = 'Exchange Rate'

    def __init__(self, frequency: Frequency):
        self._frequency = frequency

    def exchange_data(
        self, currency: Currency, start: date = None, end: date = None
    ) -> DataFrame:
        symbol = self._symbol(currency)

        data: DataFrame = fred_reader(
            exchange_symbol=symbol, start=start, end=end
        ).read()

        data = data.rename(columns={symbol: self.EXCHANGE_RATE_COLUMN})

        data = self._convert_index_to_periods(data)

        data = data.dropna()

        log.info(f"Exchange data range : {first_period(data)} - {last_period(data)}")

        return data

    def _symbol(self, currency: Currency):
        if currency == Currency.EUR:
            if self._frequency == Frequency.DAILY:
                return 'DEXUSEU'
            elif self._frequency == Frequency.MONTHLY:
                return 'EXUSEU'

        raise NotImplementedError

    def _convert_index_to_periods(self, data):
        frequency = 'B' if self._frequency == Frequency.DAILY else 'M'
        return data.to_period(freq=frequency)
