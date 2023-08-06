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


from pathlib import Path

from appdirs import AppDirs

_appdirs = AppDirs(appname='F4RATK')


class Cache:
    def __init__(self, directory: Path):
        self._location = directory

    def file(self, name: str) -> Path:
        return self._location.joinpath(name)

    @staticmethod
    def register(location: str) -> 'Cache':
        cache_location = Path(location)
        cache_location.mkdir(parents=True, exist_ok=True)
        return Cache(directory=cache_location)


cache = Cache.register(_appdirs.user_cache_dir)
