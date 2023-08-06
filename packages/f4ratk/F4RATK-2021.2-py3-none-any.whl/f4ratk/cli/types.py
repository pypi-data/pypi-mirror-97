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

from datetime import date, datetime
from typing import Optional

from click import Choice, DateTime

from f4ratk.domain import Region


class Date(DateTime):
    name = "date"

    def __init__(self, formats=None):
        formats = formats or ["%Y-%m-%d"]
        super().__init__(formats)

    def convert(self, value, param, ctx) -> Optional[date]:
        converted: Optional[datetime] = super().convert(value, param, ctx)
        return converted.date() if converted else None

    def __repr__(self):
        return 'Date'


class RegionChoice(Choice):
    name = "regionchoice"

    def __init__(self):
        super().__init__(
            choices=('DEVELOPED', 'DEVELOPED-EX-US', 'US', 'EU', 'EMERGING'),
            case_sensitive=False,
        )

    def convert(self, value, param, ctx) -> Optional[Region]:
        converted: Optional[str] = super().convert(value, param, ctx)
        return Region[converted.replace('-', '_')] if converted else None
