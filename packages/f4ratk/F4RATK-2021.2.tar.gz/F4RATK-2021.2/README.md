# F4RATK

[![Version: PyPi](https://img.shields.io/pypi/v/F4RATK?cacheSeconds=2592000)](https://pypi.org/project/F4RATK/)
[![Python Version: PyPi](https://img.shields.io/pypi/pyversions/F4RATK?cacheSeconds=2592000)](https://pypi.org/project/F4RATK/)
[![License: AGPL](https://img.shields.io/badge/license-AGPL--3.0--only-informational.svg?cacheSeconds=31536000)](https://spdx.org/licenses/AGPL-3.0-only.html)
[![Build Status: Azure](https://img.shields.io/azure-devops/build/toroettg/F4RATK/1?cacheSeconds=86400)](https://dev.azure.com/toroettg/F4RATK/_build/latest?definitionId=1&branchName=main)
[![Coverage: Azure](https://img.shields.io/azure-devops/coverage/toroettg/F4RATK/1?cacheSeconds=86400)](https://dev.azure.com/toroettg/F4RATK/_build/latest?definitionId=1&branchName=main)
[![Downloads: PyPi](https://img.shields.io/pypi/dm/F4RATK?cacheSeconds=86400)](https://pypistats.org/packages/f4ratk)

A Fama/French Finance Factor Regression Analysis Toolkit.

## Here be dragons

This project is experimental: it does not provide any guarantees and its
results are not rigorously tested. It should not be used by itself as a
basis for decision‐making.

If you would like to join, please see [CONTRIBUTING] for guidelines.

## Features

The following lists some main use cases, this software can assist you.

- Analyze stock quotes of a ticker symbol.
- Analyze arbitrary performance data from file.
- Display historic factor returns.
- Estimate excess returns based on regression results.

## Quickstart

### Installation

Obtain the latest released version of F4RATK using pip:

`pip install f4ratk`

### Usage

Run the program to see an interactive help. Note that each listed
command also provides an individual help.

`f4ratk --help`

```lang-none
Usage: f4ratk [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  Increase output verbosity.
  --about        Display program information and exit.
  --help         Show this message and exit.

Commands:
  convert    Convert files to the 'file' command format.
  file       Analyze a CSV file.
  history    Display historic factor returns.
  portfolio  Analyze a portfolio file.
  ticker     Analyze a ticker symbol.

```

Adjust the program arguments according to your problem.
Then run your regression analysis similar to the following.

#### Examples

```lang-sh
f4ratk ticker USSC.L US USD
f4ratk file ./input.csv DEVELOPED EUR PRICE --frequency=MONTHLY

```

## License

This project is licensed under the GNU Affero General Public License
version 3 (only). See [LICENSE] for more information and [COPYING]
for the full license text.

## Notice

Based on the works of [Rand Low] and [DD].

[CONTRIBUTING]: https://codeberg.org/toroettg/F4RATK/src/branch/main/CONTRIBUTING.md
[LICENSE]: https://codeberg.org/toroettg/F4RATK/src/branch/main/LICENSE
[COPYING]: https://codeberg.org/toroettg/F4RATK/src/branch/main/COPYING

[Rand Low]: https://randlow.github.io/posts/finance-economics/asset-pricing-regression
[DD]: https://www.codingfinance.com/post/2019-07-01-analyze-ff-factor-python
