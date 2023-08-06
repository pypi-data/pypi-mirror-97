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
from sys import stdout
from typing import Any, Dict, Type

from f4ratk.analyze.analyze import DataAnalyzerAdapter
from f4ratk.analyze.api import DataAnalyzer
from f4ratk.analyze.evaluation import Critic
from f4ratk.analyze.output import ResultsWriter
from f4ratk.analyze.regression import RegressionRunner
from f4ratk.fama import FamaReader
from f4ratk.history import Historian, History
from f4ratk.portfolio.analyze import PortfolioAnalyzerAdapter
from f4ratk.portfolio.api import PortfolioAnalyzer
from f4ratk.portfolio.reader.api import PortfolioReaderAdapter
from f4ratk.shared import Normalizer


def configure_logging(verbose: bool) -> None:
    log.basicConfig(level=log.DEBUG if verbose else log.INFO)
    log.getLogger("urllib3").setLevel(log.INFO)


di: Dict[Type[Any], Any] = dict()


def instantiate_dependencies() -> None:
    log.debug("Bootstrapping application dependencies")
    global di

    fama_reader: FamaReader = FamaReader(Normalizer())

    data_analyer: DataAnalyzer = DataAnalyzerAdapter(
        regression_runner=RegressionRunner(),
        critic=Critic(),
        writer=ResultsWriter(file=stdout),
    )

    history: History = History(historian=Historian(fama_reader=fama_reader))

    di.update(
        {
            DataAnalyzer: data_analyer,
            History: history,
            PortfolioAnalyzer: PortfolioAnalyzerAdapter(
                portfolio_reader=PortfolioReaderAdapter(),
                fama_reader=fama_reader,
                analyzer=data_analyer,
                history=history,
            ),
        }
    )
