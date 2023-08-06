# Copyright 2019 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To run: python -m unittest discover -s tests/ -p test*.py -t .

import unittest
import os
import pandas as pd
from quantrocket.moonshot import read_moonshot_csv

EOD_AGGREGATE_RESULTS = {
    'dma-tech': {
        ('AbsExposure', '2016-03-17'): 1.0,
        ('AbsExposure', '2016-03-18'): 1.0,
        ('AbsWeight', '2016-03-17'): 1.0,
        ('AbsWeight', '2016-03-18'): 1.0,
        ('Commission', '2016-03-17'): 0.0,
        ('Commission', '2016-03-18'): 0.0,
        ('NetExposure', '2016-03-17'): 1.0,
        ('NetExposure', '2016-03-18'): 1.0,
        ('Return', '2016-03-17'): -0.006873687065956036,
        ('Return', '2016-03-18'): -0.0010547573032254989,
        ('Slippage', '2016-03-17'): 0.0,
        ('Slippage', '2016-03-18'): 0.0,
        ('TotalHoldings', '2016-03-17'): 3.0,
        ('TotalHoldings', '2016-03-18'): 3.0,
        ('Turnover', '2016-03-17'): 0.0,
        ('Turnover', '2016-03-18'): 0.0}}

EOD_DETAILED_RESULTS = {
    'AAPL(FI265598)': {
        ('AbsExposure', '2016-03-17'): 0.0,
        ('AbsExposure', '2016-03-18'): 0.0,
        ('AbsWeight', '2016-03-17'): 0.0,
        ('AbsWeight', '2016-03-18'): 0.0,
        ('Commission', '2016-03-17'): 0.0,
        ('Commission', '2016-03-18'): 0.0,
        ('LMavg', '2016-03-17'): 116.45881666666641,
        ('LMavg', '2016-03-18'): 116.43891666666642,
        ('NetExposure', '2016-03-17'): 0.0,
        ('NetExposure', '2016-03-18'): 0.0,
        ('Return', '2016-03-17'): -0.0,
        ('Return', '2016-03-18'): 0.0,
        ('Signal', '2016-03-17'): 0.0,
        ('Signal', '2016-03-18'): 0.0,
        ('Slippage', '2016-03-17'): 0.0,
        ('Slippage', '2016-03-18'): 0.0,
        ('TotalHoldings', '2016-03-17'): 0.0,
        ('TotalHoldings', '2016-03-18'): 0.0,
        ('Turnover', '2016-03-17'): 0.0,
        ('Turnover', '2016-03-18'): 0.0,
        ('Weight', '2016-03-17'): 0.0,
        ('Weight', '2016-03-18'): 0.0},
    'AMZN(FI3691937)': {
        ('AbsExposure', '2016-03-17'): 0.3333333333333333,
        ('AbsExposure', '2016-03-18'): 0.3333333333333333,
        ('AbsWeight', '2016-03-17'): 0.3333333333333333,
        ('AbsWeight', '2016-03-18'): 0.3333333333333333,
        ('Commission', '2016-03-17'): 0.0,
        ('Commission', '2016-03-18'): 0.0,
        ('LMavg', '2016-03-17'): 495.75341666666606,
        ('LMavg', '2016-03-18'): 496.5921499999994,
        ('NetExposure', '2016-03-17'): 0.3333333333333333,
        ('NetExposure', '2016-03-18'): 0.3333333333333333,
        ('Return', '2016-03-17'): -0.008608029904632497,
        ('Return', '2016-03-18'): -0.0043853377186710745,
        ('Signal', '2016-03-17'): 1.0,
        ('Signal', '2016-03-18'): 1.0,
        ('Slippage', '2016-03-17'): 0.0,
        ('Slippage', '2016-03-18'): 0.0,
        ('TotalHoldings', '2016-03-17'): 1.0,
        ('TotalHoldings', '2016-03-18'): 1.0,
        ('Turnover', '2016-03-17'): 0.0,
        ('Turnover', '2016-03-18'): 0.0,
        ('Weight', '2016-03-17'): 0.3333333333333333,
        ('Weight', '2016-03-18'): 0.3333333333333333}
}

INTRADAY_AGGREGATE_RESULTS = {
    'fx-revert': {
        ('AbsExposure', '2018-12-18', '09:00:00'): 0.0,
        ('AbsExposure', '2018-12-18', '10:00:00'): 0.0,
        ('AbsExposure', '2018-12-18', '11:00:00'): 0.0,
        ('AbsExposure', '2018-12-19', '09:00:00'): 0.0,
        ('AbsExposure', '2018-12-19', '10:00:00'): 1.0,
        ('AbsExposure', '2018-12-19', '11:00:00'): 1.0,
        ('AbsWeight', '2018-12-18', '09:00:00'): 0.0,
        ('AbsWeight', '2018-12-18', '10:00:00'): 0.0,
        ('AbsWeight', '2018-12-18', '11:00:00'): 0.0,
        ('AbsWeight', '2018-12-19', '09:00:00'): 1.0,
        ('AbsWeight', '2018-12-19', '10:00:00'): 1.0,
        ('AbsWeight', '2018-12-19', '11:00:00'): 0.0,
        ('Benchmark', '2018-12-18', '09:00:00'): 1.136,
        ('Benchmark', '2018-12-18', '10:00:00'): 1.136465,
        ('Benchmark', '2018-12-18', '11:00:00'): 1.13606,
        ('Benchmark', '2018-12-19', '09:00:00'): 1.142945,
        ('Benchmark', '2018-12-19', '10:00:00'): 1.142125,
        ('Benchmark', '2018-12-19', '11:00:00'): 1.142185,
        ('Commission', '2018-12-18', '09:00:00'): 0.0,
        ('Commission', '2018-12-18', '10:00:00'): 0.0002,
        ('Commission', '2018-12-18', '11:00:00'): 0.00002,
        ('Commission', '2018-12-19', '09:00:00'): 0.0001,
        ('Commission', '2018-12-19', '10:00:00'): 0.0,
        ('Commission', '2018-12-19', '11:00:00'): 0.0,
        ('NetExposure', '2018-12-18', '09:00:00'): 0.0,
        ('NetExposure', '2018-12-18', '10:00:00'): 0.0,
        ('NetExposure', '2018-12-18', '11:00:00'): 0.0,
        ('NetExposure', '2018-12-19', '09:00:00'): 1.0,
        ('NetExposure', '2018-12-19', '10:00:00'): 1.5,
        ('NetExposure', '2018-12-19', '11:00:00'): 2.0,
        ('Return', '2018-12-18', '09:00:00'): 0.0,
        ('Return', '2018-12-18', '10:00:00'): 0.0,
        ('Return', '2018-12-18', '11:00:00'): 0.0,
        ('Return', '2018-12-19', '09:00:00'): 0.0010389911773893924,
        ('Return', '2018-12-19', '10:00:00'): -0.0004370168394709274,
        ('Return', '2018-12-19', '11:00:00'): -1.9934242843433506e-05,
        ('Slippage', '2018-12-18', '09:00:00'): 0.00001,
        ('Slippage', '2018-12-18', '10:00:00'): 0.00002,
        ('Slippage', '2018-12-18', '11:00:00'): 0.00001,
        ('Slippage', '2018-12-19', '09:00:00'): 0.00002,
        ('Slippage', '2018-12-19', '10:00:00'): 0.00001,
        ('Slippage', '2018-12-19', '11:00:00'): 0.00002,
        ('TotalHoldings', '2018-12-18', '09:00:00'): 0.0,
        ('TotalHoldings', '2018-12-18', '10:00:00'): 0.0,
        ('TotalHoldings', '2018-12-18', '11:00:00'): 0.0,
        ('TotalHoldings', '2018-12-19', '09:00:00'): 5.0,
        ('TotalHoldings', '2018-12-19', '10:00:00'): 5.0,
        ('TotalHoldings', '2018-12-19', '11:00:00'): 3.0,
        ('Turnover', '2018-12-18', '09:00:00'): 0.1,
        ('Turnover', '2018-12-18', '10:00:00'): 0.0,
        ('Turnover', '2018-12-18', '11:00:00'): 0.0,
        ('Turnover', '2018-12-19', '09:00:00'): 0.1,
        ('Turnover', '2018-12-19', '10:00:00'): 0.1,
        ('Turnover', '2018-12-19', '11:00:00'): 0.1}
}

INTRADAY_DETAILED_RESULTS = {
    'EUR.USD(FXEURUSD)': {
        ('AbsExposure', '2018-12-18', '09:00:00'): 0.0,
        ('AbsExposure', '2018-12-18', '10:00:00'): 0.0,
        ('AbsExposure', '2018-12-18', '11:00:00'): 0.0,
        ('AbsExposure', '2018-12-19', '09:00:00'): 0.2,
        ('AbsExposure', '2018-12-19', '10:00:00'): 0.2,
        ('AbsExposure', '2018-12-19', '11:00:00'): 0.2,
        ('AbsWeight', '2018-12-18', '09:00:00'): 0.0,
        ('AbsWeight', '2018-12-18', '10:00:00'): 0.0,
        ('AbsWeight', '2018-12-18', '11:00:00'): 0.0,
        ('AbsWeight', '2018-12-19', '09:00:00'): 0.2,
        ('AbsWeight', '2018-12-19', '10:00:00'): 0.2,
        ('AbsWeight', '2018-12-19', '11:00:00'): 0.2,
        ('Benchmark', '2018-12-18', '09:00:00'): 1.136,
        ('Benchmark', '2018-12-18', '10:00:00'): 1.136465,
        ('Benchmark', '2018-12-18', '11:00:00'): 1.13606,
        ('Benchmark', '2018-12-19', '09:00:00'): 1.142945,
        ('Benchmark', '2018-12-19', '10:00:00'): 1.142125,
        ('Benchmark', '2018-12-19', '11:00:00'): 1.142185,
        ('Commission', '2018-12-18', '09:00:00'): 0.0,
        ('Commission', '2018-12-18', '10:00:00'): 0.0,
        ('Commission', '2018-12-18', '11:00:00'): 0.00001,
        ('Commission', '2018-12-19', '09:00:00'): 0.0,
        ('Commission', '2018-12-19', '10:00:00'): 0.00002,
        ('Commission', '2018-12-19', '11:00:00'): 0.0,
        ('Mavg', '2018-12-18', '09:00:00'): None,
        ('Mavg', '2018-12-18', '10:00:00'): None,
        ('Mavg', '2018-12-18', '11:00:00'): None,
        ('Mavg', '2018-12-19', '09:00:00'): 1.1369470000000004,
        ('Mavg', '2018-12-19', '10:00:00'): 1.1370885000000004,
        ('Mavg', '2018-12-19', '11:00:00'): 1.1372462000000003,
        ('NetExposure', '2018-12-18', '09:00:00'): 0.0,
        ('NetExposure', '2018-12-18', '10:00:00'): 0.0,
        ('NetExposure', '2018-12-18', '11:00:00'): 0.0,
        ('NetExposure', '2018-12-19', '09:00:00'): 0.2,
        ('NetExposure', '2018-12-19', '10:00:00'): 0.2,
        ('NetExposure', '2018-12-19', '11:00:00'): 0.2,
        ('Return', '2018-12-18', '09:00:00'): -0.0,
        ('Return', '2018-12-18', '10:00:00'): -0.0,
        ('Return', '2018-12-18', '11:00:00'): -0.0,
        ('Return', '2018-12-19', '09:00:00'): 0.0004902863658290624,
        ('Return', '2018-12-19', '10:00:00'): -0.00014348896928548794,
        ('Return', '2018-12-19', '11:00:00'): 1.0506730874437764e-05,
        ('Signal', '2018-12-18', '09:00:00'): 0.0,
        ('Signal', '2018-12-18', '10:00:00'): 0.0,
        ('Signal', '2018-12-18', '11:00:00'): 0.0,
        ('Signal', '2018-12-19', '09:00:00'): 1.0,
        ('Signal', '2018-12-19', '10:00:00'): 1.0,
        ('Signal', '2018-12-19', '11:00:00'): 1.0,
        ('Slippage', '2018-12-18', '09:00:00'): 0.0,
        ('Slippage', '2018-12-18', '10:00:00'): 0.0,
        ('Slippage', '2018-12-18', '11:00:00'): 0.0,
        ('Slippage', '2018-12-19', '09:00:00'): 0.0,
        ('Slippage', '2018-12-19', '10:00:00'): 0.00002,
        ('Slippage', '2018-12-19', '11:00:00'): 0.00002,
        ('TotalHoldings', '2018-12-18', '09:00:00'): 0.0,
        ('TotalHoldings', '2018-12-18', '10:00:00'): 0.0,
        ('TotalHoldings', '2018-12-18', '11:00:00'): 0.0,
        ('TotalHoldings', '2018-12-19', '09:00:00'): 1.0,
        ('TotalHoldings', '2018-12-19', '10:00:00'): 2.0,
        ('TotalHoldings', '2018-12-19', '11:00:00'): 1.0,
        ('Turnover', '2018-12-18', '09:00:00'): 0.0,
        ('Turnover', '2018-12-18', '10:00:00'): 0.0,
        ('Turnover', '2018-12-18', '11:00:00'): 0.0,
        ('Turnover', '2018-12-19', '09:00:00'): 0.1,
        ('Turnover', '2018-12-19', '10:00:00'): 0.1,
        ('Turnover', '2018-12-19', '11:00:00'): 0.1,
        ('Weight', '2018-12-18', '09:00:00'): 0.0,
        ('Weight', '2018-12-18', '10:00:00'): 0.0,
        ('Weight', '2018-12-18', '11:00:00'): 0.0,
        ('Weight', '2018-12-19', '09:00:00'): 0.1,
        ('Weight', '2018-12-19', '10:00:00'): 0.15,
        ('Weight', '2018-12-19', '11:00:00'): 0.2},
    'GBP.USD(FXGBPUSD)': {
        ('AbsExposure', '2018-12-18', '09:00:00'): 0.0,
        ('AbsExposure', '2018-12-18', '10:00:00'): 0.0,
        ('AbsExposure', '2018-12-18', '11:00:00'): 0.0,
        ('AbsExposure', '2018-12-19', '09:00:00'): 0.2,
        ('AbsExposure', '2018-12-19', '10:00:00'): 0.2,
        ('AbsExposure', '2018-12-19', '11:00:00'): 0.2,
        ('AbsWeight', '2018-12-18', '09:00:00'): 0.0,
        ('AbsWeight', '2018-12-18', '10:00:00'): 0.0,
        ('AbsWeight', '2018-12-18', '11:00:00'): 0.0,
        ('AbsWeight', '2018-12-19', '09:00:00'): 0.2,
        ('AbsWeight', '2018-12-19', '10:00:00'): 0.2,
        ('AbsWeight', '2018-12-19', '11:00:00'): 0.2,
        ('Benchmark', '2018-12-18', '09:00:00'): None,
        ('Benchmark', '2018-12-18', '10:00:00'): None,
        ('Benchmark', '2018-12-18', '11:00:00'): None,
        ('Benchmark', '2018-12-19', '09:00:00'): None,
        ('Benchmark', '2018-12-19', '10:00:00'): None,
        ('Benchmark', '2018-12-19', '11:00:00'): None,
        ('Commission', '2018-12-18', '09:00:00'): 0.0,
        ('Commission', '2018-12-18', '10:00:00'): 0.0,
        ('Commission', '2018-12-18', '11:00:00'): 0.0,
        ('Commission', '2018-12-19', '09:00:00'): 0.0,
        ('Commission', '2018-12-19', '10:00:00'): 0.00001,
        ('Commission', '2018-12-19', '11:00:00'): 0.00002,
        ('Mavg', '2018-12-18', '09:00:00'): None,
        ('Mavg', '2018-12-18', '10:00:00'): None,
        ('Mavg', '2018-12-18', '11:00:00'): None,
        ('Mavg', '2018-12-19', '09:00:00'): 1.2640600000000104,
        ('Mavg', '2018-12-19', '10:00:00'): 1.2641065000000105,
        ('Mavg', '2018-12-19', '11:00:00'): 1.2642211000000103,
        ('NetExposure', '2018-12-18', '09:00:00'): 0.0,
        ('NetExposure', '2018-12-18', '10:00:00'): 0.0,
        ('NetExposure', '2018-12-18', '11:00:00'): 0.0,
        ('NetExposure', '2018-12-19', '09:00:00'): 0.1,
        ('NetExposure', '2018-12-19', '10:00:00'): 0.2,
        ('NetExposure', '2018-12-19', '11:00:00'): 0.3,
        ('Return', '2018-12-18', '09:00:00'): -0.0,
        ('Return', '2018-12-18', '10:00:00'): -0.0,
        ('Return', '2018-12-18', '11:00:00'): 0.0,
        ('Return', '2018-12-19', '09:00:00'): 0.0007272756081426303,
        ('Return', '2018-12-19', '10:00:00'): -0.0004057355535645791,
        ('Return', '2018-12-19', '11:00:00'): 0.0003899498918343625,
        ('Signal', '2018-12-18', '09:00:00'): 0.0,
        ('Signal', '2018-12-18', '10:00:00'): 0.0,
        ('Signal', '2018-12-18', '11:00:00'): 0.0,
        ('Signal', '2018-12-19', '09:00:00'): 1.0,
        ('Signal', '2018-12-19', '10:00:00'): 1.0,
        ('Signal', '2018-12-19', '11:00:00'): 1.0,
        ('Slippage', '2018-12-18', '09:00:00'): 0.0,
        ('Slippage', '2018-12-18', '10:00:00'): 0.0,
        ('Slippage', '2018-12-18', '11:00:00'): 0.0,
        ('Slippage', '2018-12-19', '09:00:00'): 0.00001,
        ('Slippage', '2018-12-19', '10:00:00'): 0.0,
        ('Slippage', '2018-12-19', '11:00:00'): 0.00002,
        ('TotalHoldings', '2018-12-18', '09:00:00'): 0.0,
        ('TotalHoldings', '2018-12-18', '10:00:00'): 0.0,
        ('TotalHoldings', '2018-12-18', '11:00:00'): 0.0,
        ('TotalHoldings', '2018-12-19', '09:00:00'): 1.0,
        ('TotalHoldings', '2018-12-19', '10:00:00'): 1.0,
        ('TotalHoldings', '2018-12-19', '11:00:00'): 1.0,
        ('Turnover', '2018-12-18', '09:00:00'): 0.0,
        ('Turnover', '2018-12-18', '10:00:00'): 0.0,
        ('Turnover', '2018-12-18', '11:00:00'): 0.0,
        ('Turnover', '2018-12-19', '09:00:00'): 0.0,
        ('Turnover', '2018-12-19', '10:00:00'): 0.0,
        ('Turnover', '2018-12-19', '11:00:00'): 0.0,
        ('Weight', '2018-12-18', '09:00:00'): 0.0,
        ('Weight', '2018-12-18', '10:00:00'): 0.0,
        ('Weight', '2018-12-18', '11:00:00'): 0.0,
        ('Weight', '2018-12-19', '09:00:00'): 0.2,
        ('Weight', '2018-12-19', '10:00:00'): 0.2,
        ('Weight', '2018-12-19', '11:00:00'): 0.2}
 }

class ReadMoonshotCsvTestCase(unittest.TestCase):
    """
    Test cases for `quantrocket.moonshot.read_moonshot_csv`.
    """

    def tearDown(self):
        if os.path.exists("results.csv"):
            os.remove("results.csv")

    def test_eod_aggregate(self):

        results = pd.DataFrame.from_dict(EOD_AGGREGATE_RESULTS)
        results.index.set_names(["Field","Date"], inplace=True)
        results.to_csv("results.csv")

        results = read_moonshot_csv("results.csv")

        results = results.reset_index()
        results.loc[:, "Date"] = results.Date.dt.strftime("%Y-%m-%d")
        results = results.set_index(["Field", "Date"])

        self.assertDictEqual(
            results.to_dict(),
            EOD_AGGREGATE_RESULTS
        )

    def test_eod_detailed(self):

        results = pd.DataFrame.from_dict(EOD_DETAILED_RESULTS)
        results.index.set_names(["Field","Date"], inplace=True)
        results.to_csv("results.csv")

        results = read_moonshot_csv("results.csv")

        results = results.reset_index()
        results.loc[:, "Date"] = results.Date.dt.strftime("%Y-%m-%d")
        results = results.set_index(["Field", "Date"])

        self.assertDictEqual(
            results.to_dict(),
            EOD_DETAILED_RESULTS
        )

    def test_intraday_aggregate(self):

        results = pd.DataFrame.from_dict(INTRADAY_AGGREGATE_RESULTS)
        results.index.set_names(["Field","Date", "Time"], inplace=True)
        results.to_csv("results.csv")

        results = read_moonshot_csv("results.csv")

        results = results.reset_index()
        results.loc[:, "Date"] = results.Date.dt.strftime("%Y-%m-%d")
        results = results.set_index(["Field", "Date", "Time"])

        self.assertDictEqual(
            results.to_dict(),
            INTRADAY_AGGREGATE_RESULTS
        )

    def test_intraday_detailed(self):

        results = pd.DataFrame.from_dict(INTRADAY_DETAILED_RESULTS)
        results.index.set_names(["Field","Date", "Time"], inplace=True)
        results.to_csv("results.csv")

        results = read_moonshot_csv("results.csv")

        results = results.reset_index()
        results.loc[:, "Date"] = results.Date.dt.strftime("%Y-%m-%d")
        results = results.set_index(["Field", "Date", "Time"])

        results = results.where(results.notnull(), None)

        self.assertDictEqual(
            results.to_dict(),
            INTRADAY_DETAILED_RESULTS
        )

