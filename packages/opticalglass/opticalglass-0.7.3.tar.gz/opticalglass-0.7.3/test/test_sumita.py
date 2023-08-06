#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2020 Michael J. Hayford
""" unit test for Sumita optical glass catalog

.. Created on Wed Aug 26 14:46:13 2020

.. codeauthor: Michael J. Hayford
"""

import unittest
import opticalglass.sumita as su


class SumitaTestCase(unittest.TestCase):
    catalog = su.SumitaCatalog()

    def compare_indices(self, glass, tol=5e-6):
        nC = glass.rindex(656.27)
        nd = glass.rindex(587.56)
        ne = glass.rindex(546.07)
        nF = glass.rindex(486.13)
        ng = glass.rindex(435.84)
        nh = glass.rindex(404.66)
        nI = glass.rindex(365.01)
        nline = self.catalog.nline_str
        indxC = glass.glass_item(nline['C'])
        indxd = glass.glass_item(nline['d'])
        indxe = glass.glass_item(nline['e'])
        indxF = glass.glass_item(nline['F'])
        indxg = glass.glass_item(nline['g'])
        indxh = glass.glass_item(nline['h'])
        indxI = glass.glass_item(nline['i'])
        self.assertAlmostEqual(nC, indxC, delta=tol)
        self.assertAlmostEqual(nd, indxd, delta=tol)
        self.assertAlmostEqual(ne, indxe, delta=tol)
        self.assertAlmostEqual(nF, indxF, delta=tol)
        self.assertAlmostEqual(ng, indxg, delta=tol)
        self.assertAlmostEqual(nh, indxh, delta=tol)
        self.assertAlmostEqual(nI, indxI, delta=tol)

    def test_ohara_catalog_glass_index(self):
        cafk95 = self.catalog.glass_index('K-CaFK95')  # first in list
        self.assertEqual(cafk95, 1)
        pbk40 = self.catalog.glass_index('K-PBK40')
        self.assertEqual(pbk40, 7)
        sk16 = self.catalog.glass_index('K-SK16')
        self.assertEqual(sk16, 64)
        laskn1 = self.catalog.glass_index('K-LaSKn1')
        self.assertEqual(laskn1, 101)
        fir100uv = self.catalog.glass_index('K-FIR100UV')  # last in list
        self.assertEqual(fir100uv, 134)

    def test_sumita_catalog_data_index(self):
        nd = self.catalog.data_index('nd')
        self.assertEqual(nd, 16)
        vd = self.catalog.data_index('vd')
        self.assertEqual(vd, 4)
        B1 = self.catalog.data_index('A4')
        self.assertEqual(B1, 52)
        glasscode = self.catalog.data_index('GTYPE')
        self.assertEqual(glasscode, 2)
        date = self.catalog.data_index('T1_550')
        self.assertEqual(date, 97)

    def test_sumita_glass_pbk40(self):
        glass = su.SumitaGlass('K-PBK40')
        self.assertIsNotNone(glass.gindex)
        self.assertEqual(glass.name(), 'K-PBK40')
        self.compare_indices(glass, tol=1.1e-5)

    def test_sumita_glass_sk16(self):
        glass = su.SumitaGlass('K-SK16')
        self.assertIsNotNone(glass.gindex)
        self.assertEqual(glass.name(), 'K-SK16')
        self.compare_indices(glass, tol=2.5e-6)

    def test_sumita_glass_laskn1(self):
        glass = su.SumitaGlass('K-LaSKn1')
        self.assertIsNotNone(glass.gindex)
        self.assertEqual(glass.name(), 'K-LaSKn1')
        self.compare_indices(glass, tol=7.5e-6)


if __name__ == '__main__':
    unittest.main(verbosity=2)
