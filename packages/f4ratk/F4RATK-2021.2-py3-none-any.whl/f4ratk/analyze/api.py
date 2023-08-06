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

from pandas import DataFrame

from f4ratk.history import AnnualizedReturns


class DataAnalyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze(
        self,
        returns: DataFrame,
        fama_data: DataFrame,
        historic_returns: AnnualizedReturns,
    ) -> None:
        """Analyze data in regards to fit for Fama / French models."""
