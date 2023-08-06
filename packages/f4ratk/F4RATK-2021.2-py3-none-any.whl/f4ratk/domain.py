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
from typing import Optional


@unique
class Region(Enum):
    DEVELOPED = 'Developed'
    DEVELOPED_EX_US = 'Developed excluding United States'
    EMERGING = 'Emerging'
    US = 'United States'
    EU = 'Europe'


@unique
class Frequency(Enum):
    DAILY = 'Daily'
    MONTHLY = 'Monthly'


@unique
class Currency(Enum):
    EUR = 'Euro'
    USD = 'US Dollar'


@dataclass(frozen=True)
class Frame:
    frequency: Frequency
    start: Optional[date]
    end: Optional[date]


@dataclass(frozen=True)
class AnalysisConfig:
    region: Region
    frame: Frame
