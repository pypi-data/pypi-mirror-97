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
from typing import Any, Dict, Generator, Hashable, List, Optional, Union

from yaml import safe_load_all

from f4ratk.portfolio.ports import (
    PortfolioConfiguration,
    PortfolioReader,
    PortfolioRequest,
)
from f4ratk.portfolio.reader.reader import read_requested_document

log = getLogger(__name__)


class PortfolioReaderAdapter(PortfolioReader):
    def read(self, request: PortfolioRequest) -> PortfolioConfiguration:
        documents = self._load_file_content(request.path)

        configurations = (
            read_requested_document(document, request.name) for document in documents
        )

        configuration = self._find_first(configurations)

        return configuration

    @staticmethod
    def _load_file_content(
        path: Path,
    ) -> List[Union[Dict[Hashable, Any], list]]:
        with open(path, 'r') as handle:
            content = list(safe_load_all(handle))
            content = list(content) if isinstance(content, dict) else content
        return content

    @staticmethod
    def _find_first(
        configurations: Generator[Optional[PortfolioConfiguration], None, None],
    ) -> PortfolioConfiguration:
        try:
            return next(config for config in configurations if config is not None)
        except StopIteration:
            raise SystemExit("Unable to read requested portfolio configuration.")
