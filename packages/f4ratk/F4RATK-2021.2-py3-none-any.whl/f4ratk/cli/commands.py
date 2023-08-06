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

from datetime import date
from pathlib import Path
from textwrap import dedent
from typing import Optional

from click import Choice, Context, Option, Path as PathArg, argument, group, option

from f4ratk import __VERSION__
from f4ratk.cli.types import Date, RegionChoice
from f4ratk.converter import SourceType, convert_file
from f4ratk.domain import AnalysisConfig, Currency, Frame, Frequency, Region
from f4ratk.file.analyze import analyze_file
from f4ratk.file.reader import FileConfig, ValueFormat
from f4ratk.history import History
from f4ratk.infrastructure import configure_logging, di, instantiate_dependencies
from f4ratk.portfolio.api import PortfolioAnalyzer, PortfolioRequest
from f4ratk.ticker.analyze import analyze_ticker_symbol
from f4ratk.ticker.reader import Stock


def _print_program_info_and_exit(context: Context, _: Option, value: bool) -> None:
    if not value:
        return

    print(
        dedent(
            f"""\
            F4RATK, version {__VERSION__}
            Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>

            https://codeberg.org/toroettg/F4RATK

            F4RATK is free software: you can redistribute it and/or modify
            it under the terms of the GNU Affero General Public License version 3
            as published by the Free Software Foundation.

            This program is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU Affero General Public License for more details.
            """
        )
    )
    context.exit()


@group()
@option('-v', '--verbose', is_flag=True, help="Increase output verbosity.")
@option(
    '--about',
    callback=_print_program_info_and_exit,
    is_flag=True,
    expose_value=False,
    help="Display program information and exit.",
)
def main(verbose: bool):
    configure_logging(verbose)
    instantiate_dependencies()


@main.command(name="ticker", help="Analyze a ticker symbol.")
@argument('symbol')
@argument('region', type=RegionChoice())
@argument('currency', type=Choice(('USD', 'EUR'), case_sensitive=False))
@option(
    '--start', type=Date(formats=('%Y-%m-%d',)), help="Start of period under review."
)
@option('--end', type=Date(formats=('%Y-%m-%d',)), help="End of period under review.")
@option(
    '--frequency',
    type=Choice(('DAILY', 'MONTHLY'), case_sensitive=False),
    default='MONTHLY',
    show_default=True,
    help="Conduct analysis with given sample frequency.",
)
def ticker(
    symbol: str,
    currency: str,
    region: Region,
    start: Optional[date],
    end: Optional[date],
    frequency: str = 'MONTHLY',
):
    stock = Stock(ticker_symbol=symbol, currency=Currency[currency])

    analysis_config = AnalysisConfig(
        region=region, frame=Frame(frequency=Frequency[frequency], start=start, end=end)
    )

    analyze_ticker_symbol(
        stock=stock,
        analysis_config=analysis_config,
    )


@main.command(
    name="file",
    short_help="Analyze a CSV file.",
    help="""
         Analyze a CSV file.

         Expects a row to be formatted in ISO 8601 with optional day for monthly input
         at the first column; and percentage in US notation with arbitrary-precision
         decimal number value at the second column, where the value may represent
         either prices or returns in percentage:

         'YYYY-MM[-DD],####.####', e.g.,

         '2020-09-11,3.53'
         '2020-09,-0.282'
         """,
)
@argument('path', type=PathArg(dir_okay=False))
@argument('region', type=RegionChoice())
@argument('currency', type=Choice(('USD', 'EUR'), case_sensitive=False))
@argument('value_format', type=Choice(('PRICE', 'RETURN'), case_sensitive=False))
@option(
    '--start', type=Date(formats=('%Y-%m-%d',)), help="Start of period under review."
)
@option('--end', type=Date(formats=('%Y-%m-%d',)), help="End of period under review.")
@option(
    '--frequency',
    type=Choice(('DAILY', 'MONTHLY'), case_sensitive=False),
    default='MONTHLY',
    show_default=True,
    help="Conduct analysis with given sample frequency.",
)
def file(
    path: str,
    currency: str,
    region: Region,
    value_format: ValueFormat,
    start: Optional[date],
    end: Optional[date],
    frequency: str = 'MONTHLY',
):
    target_frequency = Frequency[frequency]

    file_config = FileConfig(
        path=Path(path),
        currency=Currency[currency],
        value_format=ValueFormat[value_format],
    )

    analysis_config = AnalysisConfig(
        region=region, frame=Frame(frequency=target_frequency, start=start, end=end)
    )

    analyze_file(file_config=file_config, analysis_config=analysis_config)


@main.command(name="convert", help="Convert files to the 'file' command format.")
@argument('type', type=Choice(('MSCI',), case_sensitive=False))
@argument('source', type=PathArg(dir_okay=False, exists=True))
def convert(source: str, type: str):
    source_path = Path(source)
    target_path = source_path.with_suffix('.csv')

    convert_file(source=source_path, target=target_path, source_type=SourceType[type])


@main.command(name="history", help="Display historic factor returns.")
@argument('region', type=RegionChoice())
def history(region: Region):
    di[History].display_history(region=region)


@main.command(
    name="portfolio",
    short_help="Analyze a portfolio file.",
    help="""
         Analyze a portfolio file.

         A portfolio consists of a set of multiple sources (e.g.,
         files or ticker symbols) and their respective weights.
         The data for each source is being read, aggregated and
         finally tested against a given analysis configuration.

         Each of those parameters is being read from a file at
         the given path parameter. For details of the required
         format of this file, please see the documentation.
         """,
)
@argument('path', type=PathArg(dir_okay=False, exists=True))
@option(
    '--name',
    type=str,
    help=(
        "Name of the portfolio to analyze in the file at the given path."
        " [default: the first portfolio of the file]"
    ),
)
def portfolio(path: str, name: Optional[str] = None):
    request = PortfolioRequest(path=Path(path), name=name)
    di[PortfolioAnalyzer].analyze_portfolio_file(request=request)
