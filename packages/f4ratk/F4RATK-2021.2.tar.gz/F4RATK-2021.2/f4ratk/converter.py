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

from enum import Enum, unique
from logging import getLogger
from pathlib import Path

from pandas import DataFrame, ExcelFile

from f4ratk.domain import Frequency
from f4ratk.shared import Normalizer, first_period, last_period

log = getLogger(__name__)


@unique
class SourceType(Enum):
    MSCI = "MSCI Index History"


class MSCIConverter:
    _HEADER = ('Dates', 'Returns')

    def __init__(self, normalizer: Normalizer):
        self._normalizer = normalizer

    def convert(self, source: Path, target: Path):
        data = self._read_msci_file(source)

        log.info(
            f"Content date ranges from '{first_period(data)}' to '{last_period(data)}'"
        )

        self._write_file(target, data)

    def _read_msci_file(self, path: Path) -> DataFrame:
        log.info(f"Reading input file'{path}'")
        document = ExcelFile(path)
        sheet = document.parse(
            parse_dates=True, names=self._HEADER, skiprows=6, skipfooter=18, index_col=0
        )

        data = self._normalizer.index_to_periods(sheet, Frequency.MONTHLY)
        return data

    @staticmethod
    def _write_file(target: Path, data: DataFrame) -> None:
        log.info(f"Writing output file'{target}'")
        data.to_csv(target, header=False)


def convert_file(source: Path, target: Path, source_type: SourceType) -> None:
    MSCIConverter(normalizer=Normalizer()).convert(source, target)
