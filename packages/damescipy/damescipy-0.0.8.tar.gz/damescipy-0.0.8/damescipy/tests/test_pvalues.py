#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright (C) 2021 David Arroyo Menéndez

#  Author: David Arroyo Menéndez <davidam@gmail.com>
#  Maintainer: David Arroyo Menéndez <davidam@gmail.com>
#  This file is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
#
#  This file is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with damescipy; see the file LICENSE.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301 USA,

from unittest import TestCase
from scipy.stats import chisquare
import scipy.stats as stats
import pandas as pd
import numpy as np

class TestBasics(TestCase):

    def test_chisquare(self):
        self.assertEqual("Power_divergenceResult(statistic=2.0, pvalue=0.7357588823428847)", str(chisquare([16, 18, 16, 14, 12, 12], ddof=1)))
        self.assertEqual("Power_divergenceResult(statistic=2.0, pvalue=array([0.84914504, 0.73575888, 0.5724067 ]))", str(chisquare([16, 18, 16, 14, 12, 12], ddof=[0,1,2])))

    def test_fisher(self):
        oddsratio, pvalue = stats.fisher_exact([[8, 2], [1, 5]])
        self.assertEqual(pvalue, 0.03496503496503495)
        self.assertEqual(oddsratio, 20)

    def test_pearsonr(self):
        a = np.array([0, 0, 0, 1, 1, 1, 1])
        b = np.arange(7)
        pvalue1, pvalue2 = stats.pearsonr(a, b)
        self.assertEqual((0.8660254037844386, 0.011724811003954649), (pvalue1, pvalue2))
        pvalue3, pvalue4 = stats.pearsonr([1,2,3,4,5], [5,6,7,8,7])
        self.assertEqual((0.8320502943378436, 0.08050957329849862), (pvalue3, pvalue4))

    def test_anova(self):
        np.random.seed(12)
        races =   ["asian","black","hispanic","other","white"]

        # Generate random data
        voter_race = np.random.choice(a= races,
                              p = [0.05, 0.15 ,0.25, 0.05, 0.5],
                              size=1000)

        voter_age = stats.poisson.rvs(loc=18,
                              mu=30,
                              size=1000)

        # Group age data by race
        voter_frame = pd.DataFrame({"race":voter_race,"age":voter_age})
        groups = voter_frame.groupby("race").groups

        # Extract individual groups
        asian = voter_age[groups["asian"]]
        black = voter_age[groups["black"]]
        hispanic = voter_age[groups["hispanic"]]
        other = voter_age[groups["other"]]
        white = voter_age[groups["white"]]

        # Perform the ANOVA
        self.assertEqual(str(stats.f_oneway(asian, black, hispanic, other, white)), "F_onewayResult(statistic=1.7744689357329695, pvalue=0.13173183201930463)")
