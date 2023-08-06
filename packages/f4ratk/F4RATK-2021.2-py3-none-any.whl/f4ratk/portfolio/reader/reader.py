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
from pathlib import Path
from typing import Iterable, List, Optional

from f4ratk.domain import AnalysisConfig, Currency, Frame, Frequency, Region
from f4ratk.file.reader import FileConfig, ValueFormat
from f4ratk.portfolio.analyze import PortfolioConfiguration
from f4ratk.portfolio.ports import Source
from f4ratk.portfolio.reader.nodes import Analysis, File, Root, Ticker
from f4ratk.ticker.reader import Stock

log = getLogger(__name__)


class TickerSourceReader:
    @staticmethod
    def sources(ticker_nodes: Iterable[dict]) -> List[Source]:
        return [TickerSourceReader._read_ticker_node(node) for node in ticker_nodes]

    @staticmethod
    def _read_ticker_node(ticker_node: dict) -> Source:
        ticker = Ticker(ticker_node)

        log.info(
            "Found ticker source '%s' with %d%% weight.",
            ticker.description,
            ticker.weight,
        )

        source = Source(
            origin=Stock(
                ticker_symbol=ticker.symbol, currency=Currency[ticker.currency]
            ),
            weight=ticker.weight,
        )

        return source


class FileSourceReader:
    @staticmethod
    def sources(file_nodes: Iterable[dict]) -> List[Source]:
        return [FileSourceReader._read_file_node(node) for node in file_nodes]

    @staticmethod
    def _read_file_node(file_node: dict) -> Source:
        file = File(file_node)

        log.info(
            "Found file source '%s' with %d%% weight.",
            file.description,
            file.weight,
        )

        return Source(
            origin=FileConfig(
                path=Path(file.path),
                currency=Currency[file.currency],
                value_format=ValueFormat[file.format],
            ),
            weight=file.weight,
        )


class AnalysisReader:
    @staticmethod
    def analysis(analysis_node: dict) -> AnalysisConfig:
        analysis = Analysis(analysis_node)

        log.info(
            "Found analysis configuration: [%s, %s]",
            analysis.region,
            analysis.frequency,
        )

        config = AnalysisConfig(
            region=Region[analysis.region],
            frame=Frame(frequency=Frequency[analysis.frequency], start=None, end=None),
        )

        return config


def read_requested_document(
    document: dict, name: Optional[str]
) -> Optional[PortfolioConfiguration]:
    root = Root(document)

    if name and name != root.name:
        log.debug("Skipping portfolio configuration '%s'", root.name)
        return

    return _read_document(root)


def _read_document(root: Root) -> Optional[PortfolioConfiguration]:
    log.info("Reading portfolio configuration '%s'", root.name)

    config = AnalysisReader.analysis(root.analysis)

    sources = tuple(
        TickerSourceReader.sources(root.ticker) + FileSourceReader.sources(root.file)
    )

    portfolio = PortfolioConfiguration(sources=sources, config=config)

    _verify_weight(portfolio)

    return portfolio


def _verify_weight(portfolio: PortfolioConfiguration) -> None:
    weight = portfolio.total_weight()
    if weight != 100:
        log.warning("Total portfolio weight of '%d %%' should be 100%%.", weight)
