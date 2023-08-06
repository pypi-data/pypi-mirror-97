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
from scipy.stats import bernoulli
import scipy.stats as stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TestBasics(TestCase):

    def test_bernoulli(self):
        fig, ax = plt.subplots(1, 1)

        p = 0.3
        mean, var, skew, kurt = bernoulli.stats(p, moments='mvsk')

        x = np.arange(bernoulli.ppf(0.01, p),
                      bernoulli.ppf(0.99, p))

        ax.plot(x, bernoulli.pmf(x, p), 'bo', ms=8, label='bernoulli pmf')
        ax.vlines(x, 0, bernoulli.pmf(x, p), colors='b', lw=5, alpha=0.5)

        rv = bernoulli(p)

        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1, label='frozen pmf')
        ax.legend(loc='best', frameon=False)

        self.assertEqual("AxesSubplot(0.125,0.11;0.775x0.77)", str(ax))

    def test_betabinom(self):
        from scipy.stats import betabinom
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        n, a, b = 5, 2.3, 0.63
        mean, var, skew, kurt = betabinom.stats(n, a, b, moments='mvsk')

        x = np.arange(betabinom.ppf(0.01, n, a, b),
                      betabinom.ppf(0.99, n, a, b))
        ax.plot(x, betabinom.pmf(x, n, a, b), 'bo', ms=8, label='betabinom pmf')
        ax.vlines(x, 0, betabinom.pmf(x, n, a, b), colors='b', lw=5, alpha=0.5)

        rv = betabinom(n, a, b)
        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
                  label='frozen pmf')
        ax.legend(loc='best', frameon=False)
#        plt.show()
        self.assertEqual("AxesSubplot(0.125,0.11;0.775x0.77)", str(ax))
        
    def test_boltzman(self):
        from scipy.stats import boltzmann
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        lambda_, N = 1.4, 19
        mean, var, skew, kurt = boltzmann.stats(lambda_, N, moments='mvsk')

        x = np.arange(boltzmann.ppf(0.01, lambda_, N),
                      boltzmann.ppf(0.99, lambda_, N))
        ax.plot(x, boltzmann.pmf(x, lambda_, N), 'bo', ms=8, label='boltzmann pmf')
        ax.vlines(x, 0, boltzmann.pmf(x, lambda_, N), colors='b', lw=5, alpha=0.5)

        rv = boltzmann(lambda_, N)
        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
                  label='frozen pmf')
        ax.legend(loc='best', frameon=False)
        self.assertEqual("AxesSubplot(0.125,0.11;0.775x0.77)", str(ax))

    def test_laplace(self):
        from scipy.stats import dlaplace
        import matplotlib.pyplot as plt
        import numpy as np
        fig, ax = plt.subplots(1, 1)

        a = 0.8
        mean, var, skew, kurt = dlaplace.stats(a, moments='mvsk')

        x = np.arange(dlaplace.ppf(0.01, a),
                      dlaplace.ppf(0.99, a))
        ax.plot(x, dlaplace.pmf(x, a), 'bo', ms=8, label='dlaplace pmf')
        ax.vlines(x, 0, dlaplace.pmf(x, a), colors='b', lw=5, alpha=0.5)

        rv = dlaplace(a)
        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
                  label='frozen pmf')
        ax.legend(loc='best', frameon=False)
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")
        
    def test_geom(self):
        from scipy.stats import geom
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        p = 0.5
        mean, var, skew, kurt = geom.stats(p, moments='mvsk')

        x = np.arange(geom.ppf(0.01, p),
                      geom.ppf(0.99, p))
        ax.plot(x, geom.pmf(x, p), 'bo', ms=8, label='geom pmf')
        ax.vlines(x, 0, geom.pmf(x, p), colors='b', lw=5, alpha=0.5)

        rv = geom(p)
        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
                  label='frozen pmf')
        ax.legend(loc='best', frameon=False)
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")

    def test_hypergeom(self):
        from scipy.stats import hypergeom
        import matplotlib.pyplot as plt
        import numpy as np

        [M, n, N] = [20, 7, 12]
        rv = hypergeom(M, n, N)
        x = np.arange(0, n+1)
        pmf_dogs = rv.pmf(x)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, pmf_dogs, 'bo')
        ax.vlines(x, 0, pmf_dogs, lw=2)
        ax.set_xlabel('# of dogs in our group of chosen animals')
        ax.set_ylabel('hypergeom PMF')
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")


    def test_poisson(self):
        from scipy.stats import poisson
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        mu = 0.6
        mean, var, skew, kurt = poisson.stats(mu, moments='mvsk')

        x = np.arange(poisson.ppf(0.01, mu),
                      poisson.ppf(0.99, mu))
        ax.plot(x, poisson.pmf(x, mu), 'bo', ms=8, label='poisson pmf')
        ax.vlines(x, 0, poisson.pmf(x, mu), colors='b', lw=5, alpha=0.5)

        rv = poisson(mu)
        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
                  label='frozen pmf')
        ax.legend(loc='best', frameon=False)        
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")

        
