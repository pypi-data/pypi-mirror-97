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

from typing import List


class Node:
    def __init__(self, node: dict):
        self._node = node

    @staticmethod
    def _normalize(value: str) -> str:
        uppercase = value.upper()
        return uppercase.replace('-', '_')

    def _read(self, key: str) -> str:
        return self._node[key]

    def _read_normalized(self, key: str) -> str:
        raw = self._read(key)
        return self._normalize(raw)


class Root(Node):
    @property
    def name(self) -> str:
        return self._read('name')

    @property
    def file(self) -> List[dict]:
        return self._node.get('files', [])

    @property
    def ticker(self) -> List[dict]:
        return self._node.get('tickers', [])

    @property
    def analysis(self) -> dict:
        return self._node['analysis']


class Source(Node):
    @property
    def description(self) -> str:
        return self._read('description')

    @property
    def currency(self) -> str:
        return self._read_normalized('currency')

    @property
    def weight(self) -> int:
        return int(self._node['weight'])


class Ticker(Source):
    @property
    def symbol(self) -> str:
        return self._read_normalized('symbol')


class File(Source):
    @property
    def path(self) -> str:
        return self._read('path')

    @property
    def format(self) -> str:
        return self._read_normalized('format')


class Analysis(Node):
    @property
    def region(self) -> str:
        return self._read_normalized('region')

    @property
    def frequency(self) -> str:
        return self._read_normalized('frequency')
