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
from pprint import pprint
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

    def test_binom(self):
        from scipy.stats import binom
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        n, p = 5, 0.4
        mean, var, skew, kurt = binom.stats(n, p, moments='mvsk')

        x = np.arange(binom.ppf(0.01, n, p),
                      binom.ppf(0.99, n, p))
        ax.plot(x, binom.pmf(x, n, p), 'bo', ms=8, label='binom pmf')
        ax.vlines(x, 0, binom.pmf(x, n, p), colors='b', lw=5, alpha=0.5)

        rv = binom(n, p)
        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
                  label='frozen pmf')
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

    def test_tstudent(self):
        from scipy.stats import t
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        df = 2.74
        mean, var, skew, kurt = t.stats(df, moments='mvsk')

        x = np.linspace(t.ppf(0.01, df),
                        t.ppf(0.99, df), 100)
        ax.plot(x, t.pdf(x, df),
                'r-', lw=5, alpha=0.6, label='t pdf')

        rv = t(df)
        ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

        vals = t.ppf([0.001, 0.5, 0.999], df)
        np.allclose([0.001, 0.5, 0.999], t.cdf(vals, df))

        r = t.rvs(df, size=1000)

        ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
        ax.legend(loc='best', frameon=False)
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")


    def test_chi(self):
        from scipy.stats import chi
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        df = 78
        mean, var, skew, kurt = chi.stats(df, moments='mvsk')

        x = np.linspace(chi.ppf(0.01, df),
                        chi.ppf(0.99, df), 100)
        ax.plot(x, chi.pdf(x, df),
                'r-', lw=5, alpha=0.6, label='chi pdf')

        rv = chi(df)
        ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

        vals = chi.ppf([0.001, 0.5, 0.999], df)
        np.allclose([0.001, 0.5, 0.999], chi.cdf(vals, df))

        r = chi.rvs(df, size=1000)

        ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
        ax.legend(loc='best', frameon=False)
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")


    def test_chi2(self):
        from scipy.stats import chi2
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        df = 55
        mean, var, skew, kurt = chi2.stats(df, moments='mvsk')

        x = np.linspace(chi2.ppf(0.01, df),
                        chi2.ppf(0.99, df), 100)
        ax.plot(x, chi2.pdf(x, df),
                'r-', lw=5, alpha=0.6, label='chi2 pdf')

        rv = chi2(df)
        ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

        vals = chi2.ppf([0.001, 0.5, 0.999], df)
        np.allclose([0.001, 0.5, 0.999], chi2.cdf(vals, df))

        r = chi2.rvs(df, size=1000)

        ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
        ax.legend(loc='best', frameon=False)
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")


    def test_cosine(self):
        from scipy.stats import cosine
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        mean, var, skew, kurt = cosine.stats(moments='mvsk')

        x = np.linspace(cosine.ppf(0.01),
                        cosine.ppf(0.99), 100)
        ax.plot(x, cosine.pdf(x),
                'r-', lw=5, alpha=0.6, label='cosine pdf')

        rv = cosine()
        ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

        vals = cosine.ppf([0.001, 0.5, 0.999])
        np.allclose([0.001, 0.5, 0.999], cosine.cdf(vals))

        r = cosine.rvs(size=1000)

        ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
        ax.legend(loc='best', frameon=False)
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")

    def test_expon(self):
        from scipy.stats import expon
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 1)

        mean, var, skew, kurt = expon.stats(moments='mvsk')

        x = np.linspace(expon.ppf(0.01),
                        expon.ppf(0.99), 100)
        ax.plot(x, expon.pdf(x),
                'r-', lw=5, alpha=0.6, label='expon pdf')

        rv = expon()
        ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

        vals = expon.ppf([0.001, 0.5, 0.999])
        np.allclose([0.001, 0.5, 0.999], expon.cdf(vals))
        self.assertEqual(str(ax), "AxesSubplot(0.125,0.11;0.775x0.77)")

    def test_pearson(self):
        a = np.array([0, 0, 0, 1, 1, 1, 1])
        b = np.arange(7)
        val = stats.pearsonr(a, b)
        self.assertEqual(val, (0.8660254037844386, 0.011724811003954649))

    def test_spearmanr(self):
        from scipy import stats
        stats.spearmanr([1,2,3,4,5], [5,6,7,8,7])
        np.random.seed(1234321)
        x2n = np.random.randn(100, 2)
        y2n = np.random.randn(100, 2)
        stats.spearmanr(x2n)
        stats.spearmanr(x2n[:,0], x2n[:,1])
        rho, pval = stats.spearmanr(x2n, y2n)
        rho, pval = stats.spearmanr(x2n.T, y2n.T, axis=1)
        stats.spearmanr(x2n, y2n, axis=None)
        stats.spearmanr(x2n.ravel(), y2n.ravel())
        xint = np.random.randint(10, size=(100, 2))
        variable = stats.spearmanr(xint)
        self.assertEqual("SpearmanrResult(correlation=0.05276092702971021, pvalue=0.6021304583706234)", str(variable))
