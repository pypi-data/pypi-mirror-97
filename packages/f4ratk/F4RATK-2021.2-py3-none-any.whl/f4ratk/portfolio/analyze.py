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
from typing import Iterable

from pandas import DataFrame

from f4ratk.analyze.api import DataAnalyzer
from f4ratk.domain import Frame, Frequency, Region
from f4ratk.fama import FamaReader
from f4ratk.file.reader import FileConfig, read_file
from f4ratk.history import History
from f4ratk.portfolio.api import PortfolioAnalyzer
from f4ratk.portfolio.ports import (
    Origin,
    PortfolioConfiguration,
    PortfolioReader,
    PortfolioRequest,
    Source,
)
from f4ratk.shared import format_range
from f4ratk.ticker.reader import Stock, read_ticker

log = getLogger(__name__)


class PortfolioAnalyzerAdapter(PortfolioAnalyzer):
    def __init__(
        self,
        portfolio_reader: PortfolioReader,
        fama_reader: FamaReader,
        analyzer: DataAnalyzer,
        history: History,
    ):
        self._portfolio_reader = portfolio_reader
        self._fama_reader = fama_reader
        self._analyzer = analyzer
        self._history = history

    def analyze_portfolio_file(self, request: PortfolioRequest) -> None:
        portfolio = self._portfolio_reader.read(request=request)

        self._analyze_portfolio(portfolio)

    def _analyze_portfolio(self, portfolio: PortfolioConfiguration) -> None:
        frame = portfolio.config.frame
        region = portfolio.config.region

        portfolio_data = self._read_combined_sources(portfolio.sources, frame)

        fama_data = self._read_fama_data(region, frame.frequency)

        historic_returns = self._history.annualized_returns(region=region)

        self._analyzer.analyze(
            portfolio_data,
            fama_data,
            historic_returns,
        )

    def _read_combined_sources(
        self, sources: Iterable[Source], frame: Frame
    ) -> DataFrame:
        combined = sum(self._read_weighted_data(source, frame) for source in sources)
        return combined.dropna()

    def _read_weighted_data(self, source: Source, frame: Frame) -> DataFrame:
        data = self._read_data(source.origin, frame)
        log.debug("Source data range: %s", format_range(data))
        return data.mul(source.weight / 100)

    @staticmethod
    def _read_data(origin: Origin, frame: Frame) -> DataFrame:
        if isinstance(origin, Stock):
            return read_ticker(stock=origin, frame=frame)
        elif isinstance(origin, FileConfig):
            return read_file(file_config=origin, frame=frame)

        raise ValueError

    def _read_fama_data(self, region: Region, frequency: Frequency) -> DataFrame:
        return self._fama_reader.fama_data(region=region, frequency=frequency)
