# -*- coding:utf-8 -*-
from trdb2py.config import loadConfig
from trdb2py.trdb2 import simTradings, getAssetCandles, simTrading, getAssetCandles2
from trdb2py.utils import str2asset, nextWeekDay, asset2str
from trdb2py.timeutils import str2timestamp, getDayInYear, getYearDays
from trdb2py.pdutils import (buildPNLReport, getPNLLastTs, getPNLValueWithTimestamp, mergePNL, mergePNLEx,
                             rmPNLValuesWithTimestamp, getPNLTimestampLowInMonth, getPNLTimestampHighInMonth,
                             countTradingDays4Year, calcAnnualizedVolatility, rebuildPNL, rebuildDrawdown,
                             calcAnnualizedReturns, calcSharpe)
from trdb2py.statistics import (calcPNLWinRateInYear, buildPNLWinRateInYears,
                                buildPNLWinRateInMonths, buildPNLListWinRateInYears2,
                                buildPNLListWinRateInMonths2, buildPNLListWinRate4Month,
                                buildPNLListResponseRateInYears2)
from trdb2py.plotly import (showAssetCandles, showHeatmap, showHeatmapWinRateInYears,
                            showWinRateInYears, showHeatmapWinRateInMonths, showWinRateInMonths,
                            showBarWinRateInMonths, showBarWinRateInYears, showBarWinRate4Month,
                            showPNL, showPNLs, showPNLs2, showBarResponseRateInYears,
                            showAssetCandles2)
from trdb2py.trdb2utils import analysisResult, getIndicatorInResult, getFirstCtrlTs, buildPNLDataFrame
import trdb2py.trading2_pb2
