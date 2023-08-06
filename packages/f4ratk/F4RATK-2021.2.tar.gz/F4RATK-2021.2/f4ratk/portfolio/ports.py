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

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

from f4ratk.domain import AnalysisConfig
from f4ratk.file.reader import FileConfig
from f4ratk.ticker.reader import Stock

Origin = Union[Stock, FileConfig]


@dataclass(frozen=True)
class PortfolioRequest:
    path: Path
    name: Optional[str]


@dataclass(frozen=True)
class Source:
    origin: Origin
    weight: int


@dataclass(frozen=True)
class PortfolioConfiguration:
    sources: Tuple[Source, ...]
    config: AnalysisConfig

    def total_weight(self) -> int:
        return sum(source.weight for source in self.sources)


class PortfolioReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, request: PortfolioRequest) -> PortfolioConfiguration:
        """Read the portfolio configuration matching the given request."""
