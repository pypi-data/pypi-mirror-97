#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damescipy; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from unittest import TestCase
import numpy as np
import scipy as sp
from scipy import integrate
from scipy import spatial
from scipy import stats
from scipy.stats import poisson
from scipy.interpolate import interp1d
from scipy.optimize import fmin

class TestBasics(TestCase):

    def test_arange(self):
        x1 = sp.arange(0,10,1)
        self.assertTrue(np.array_equal(x1, np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])))

    def test_descriptives(self):
        x = np.array([1,2,3,1,2,1,1,1,3,2,2,1,7,7,7,7,7,7,7,7,7,7,7,7,7])
        self.assertEqual(x.min(), 1)         # equivalent to np.min(x)
        self.assertEqual(x.max(), 7)         # equivalent to np.max(x)
        self.assertEqual(x.mean(), 4.44)     # equivalent to np.mean(x)
        self.assertEqual(x.var(), 7.3664)    # equivalent to np.var(x)

    def test_distance(self):
        dataSetI = [3, 45, 7, 2]
        dataSetII = [2, 54, 13, 15]
        self.assertEqual(spatial.distance.cosine(dataSetI, dataSetII), 0.02771574828765)

    def test_roots(self):
        polinomio = [1.3,4,.6,-1]   # polinomio = 1.3 x^3 + 4 x^2 + 0.6 x - 1
        x = sp.arange(-4,1,.05)
        y = sp.polyval(polinomio,x)
        raices = sp.roots(polinomio)
        self.assertEqual(raices[0], -2.816023020827658)
        self.assertEqual(raices[1], -0.6691329703979497)
        self.assertEqual(raices[2], 0.4082329143025312)

    def test_poisson(self):
        mu = 0.6
        mean, var, skew, kurt = poisson.stats(mu, moments='mvsk')
        self.assertEqual(mean, 0.6)
        self.assertEqual(var, 0.6)
        self.assertEqual(skew, 1.2909944487358056)
        self.assertEqual(kurt, 1.6666666666666667)
        n = np.array([0., 1., 2.])
        x = np.arange(poisson.ppf(0.01, mu),
                                    poisson.ppf(0.99, mu))
        self.assertTrue(np.array_equal(n, x))

    def test_integrate(self):
        limite_inferior = 0
        limite_superior = 5
        exponencial_decreciente = lambda x: sp.exp(-x)
        integrate.quad(exponencial_decreciente ,limite_inferior,limite_superior)
        self.assertEqual(integrate.quad(exponencial_decreciente ,limite_inferior,limite_superior), (0.9932620530009145, 1.102742400728068e-14))

    def test_interpolate(self):
        x = np.linspace(0, 10, num=11, endpoint=True)
        y = np.cos(-x**2/9.0)
        f = interp1d(x, y)
        f2 = interp1d(x, y, kind='cubic')

    def test_fmin(self):
        rsinc = lambda x: -1 * np.sin(x)/x
        # Empezamos a partir de x = -5
        x0 = -5
        xmin0 = fmin(rsinc,x0)
        self.assertEqual(-7.72528076171875, xmin0[0])

        # mu = 0.6
        # prob = poisson.cdf(x, mu)
        # self.assertTrue(np.array_equal(prob, np.array([0.54881164, 0.87809862, 0.97688471])))

        # print(x.min())
        # print(x.max())   # equivalent to np.max(x)
        # print(x.mean())  # equivalent to np.mean(x)
        # print(x.var())   # equivalent to np.var(x))
        # prob = poisson.cdf(x, mu)
        # self.assertTrue(np.array_equal(prob, np.array([0.54881164, 0.87809862, 0.97688471])))

        # def test_stats(self):
    #     rvs1 = stats.norm.rvs(loc=5, scale=10, size=500)
    #     rvs2 = stats.norm.rvs(loc=5, scale=10, size=500)
    #     self.assertEqual("Ttest_indResult(statistic=0.4207285367232999, pvalue=0.6740439005034364)", stats.ttest_ind(rvs1, rvs2))
