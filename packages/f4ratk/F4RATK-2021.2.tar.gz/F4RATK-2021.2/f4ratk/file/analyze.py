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

from f4ratk.analyze.api import DataAnalyzer
from f4ratk.domain import AnalysisConfig
from f4ratk.fama import FamaReader
from f4ratk.file.reader import FileConfig, read_file
from f4ratk.history import History
from f4ratk.infrastructure import di
from f4ratk.shared import Normalizer


def analyze_file(
    file_config: FileConfig,
    analysis_config: AnalysisConfig,
) -> None:
    fama_reader = FamaReader(Normalizer())
    analyzer: DataAnalyzer = di[DataAnalyzer]
    history: History = di[History]

    data = read_file(
        file_config=file_config,
        frame=analysis_config.frame,
    )

    historic_returns = history.annualized_returns(region=analysis_config.region)

    analyzer.analyze(
        data,
        fama_reader.fama_data(
            region=analysis_config.region, frequency=analysis_config.frame.frequency
        ),
        historic_returns=historic_returns,
    )
