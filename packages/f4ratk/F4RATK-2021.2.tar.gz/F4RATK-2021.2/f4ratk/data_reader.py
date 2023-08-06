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

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import requests_cache
from pandas import DataFrame, read_csv
from pandas_datareader.famafrench import FamaFrenchReader
from pandas_datareader.fred import FredReader
from pandas_datareader.yahoo.daily import YahooDailyReader

from f4ratk.directories import cache


def _cached_session() -> requests_cache.CachedSession:
    cache_duration = timedelta(days=14)
    cache_location = str(cache.file(name='requests'))

    # noinspection PyTypeChecker
    session = requests_cache.CachedSession(
        cache_name=cache_location, backend='sqlite', expire_after=cache_duration
    )
    session.cache.remove_old_entries(datetime.utcnow() - cache_duration)

    return session


_session = _cached_session()


def fama_french_reader(returns_data: str) -> FamaFrenchReader:
    return FamaFrenchReader(symbols=returns_data, session=_session, start='1920')


def yahoo_reader(
    ticker_symbol: str, start: Optional[date], end: Optional[date]
) -> YahooDailyReader:
    return YahooDailyReader(
        symbols=ticker_symbol,
        start=start if start else '1970',
        end=end,
        session=_session,
    )


def fred_reader(
    exchange_symbol: str, start: Optional[date], end: Optional[date]
) -> FredReader:
    return FredReader(
        symbols=exchange_symbol,
        start=start if start else '1970',
        end=end,
        session=_session,
    )


class CsvFileReader:
    _HEADER = ('Dates', 'Returns')

    def __init__(self, path: Path):
        self._path = path

    def read(self) -> DataFrame:
        return read_csv(self._path, parse_dates=True, index_col=0, names=self._HEADER)


def csv_reader(path: Path) -> CsvFileReader:
    return CsvFileReader(path=path)
