#!/usr/bin/env python

import unittest

import lsst.daf.persistence as dafPersist

class TimeFuncTestCase(unittest.TestCase):
    """A test case for SQL time functions."""

    def setUp(self):
        self.db = dafPersist.DbStorage()
        self.db.setRetrieveLocation(dafPersist.LogicalLocation(
            "mysql://lsst10.ncsa.uiuc.edu:3306/ktl"))
        self.db.startTransaction()
        self.db.setTableForQuery("test")

    def tearDown(self):
        self.db.endTransaction()

    def testMJD(self):
        mjdUtc = 45205.125
        self.db.outColumn("taiToUtc(mjdUtcToTai(%f))" % mjdUtc)
        self.db.outColumn("mjdUtcToTai(%f)" % mjdUtc)
        self.db.outColumn("taiToMjdUtc(mjdUtcToTai(%f))" % mjdUtc)
        self.db.outColumn("taiToMjdTai(mjdUtcToTai(%f))" % mjdUtc)
        self.db.query()
        haveRow = self.db.next()
        self.assert_(haveRow)
        self.assertEqual(self.db.getColumnByPosInt64(0), 399006000000000000L)
        self.assertEqual(self.db.getColumnByPosInt64(1), 399006021000000000L)
        self.assertAlmostEqual(self.db.getColumnByPosDouble(2), 45205.125)
        self.assertAlmostEqual(self.db.getColumnByPosDouble(3),
                45205.125 + 21.0 / 86400.0)
        haveRow = self.db.next()
        self.assert_(not haveRow)

    def testNsecs(self):
        nsecsUtc = 1192755473000000000L
        self.db.outColumn("taiToUtc(utcToTai(%d))" % nsecsUtc)
        self.db.outColumn("utcToTai(%d)" % nsecsUtc)
        self.db.outColumn("taiToMjdUtc(utcToTai(%d))" % nsecsUtc)
        self.db.query()
        haveRow = self.db.next()
        self.assert_(haveRow)
        self.assertEqual(self.db.getColumnByPosInt64(0), 1192755473000000000L)
        self.assertEqual(self.db.getColumnByPosInt64(1), 1192755506000000000L)
        self.assertAlmostEqual(self.db.getColumnByPosDouble(2), 54392.040196759262)
        haveRow = self.db.next()
        self.assert_(not haveRow)

    def testBoundaryMJD(self):
        mjdUtc = 47892.0
        self.db.outColumn("taiToUtc(mjdUtcToTai(%f))" % mjdUtc)
        self.db.outColumn("mjdUtcToTai(%f)" % mjdUtc)
        self.db.outColumn("taiToMjdUtc(mjdUtcToTai(%f))" % mjdUtc)
        self.db.query()
        haveRow = self.db.next()
        self.assert_(haveRow)
        self.assertEqual(self.db.getColumnByPosInt64(0), 631152000000000000L)
        self.assertEqual(self.db.getColumnByPosInt64(1), 631152025000000000L)
        self.assertEqual(self.db.getColumnByPosDouble(2), 47892.0)
        haveRow = self.db.next()
        self.assert_(not haveRow)

    def testCrossBoundaryNsecs(self):
        nsecsUtc = 631151998000000000L
        self.db.outColumn("taiToUtc(utcToTai(%d))" % nsecsUtc)
        self.db.outColumn("utcToTai(%d)" % nsecsUtc)
        self.db.query()
        haveRow = self.db.next()
        self.assert_(haveRow)
        self.assertEqual(self.db.getColumnByPosInt64(0), 631151998000000000L)
        self.assertEqual(self.db.getColumnByPosInt64(1), 631152022000000000L)
        haveRow = self.db.next()
        self.assert_(not haveRow)

    def testNsecsTAI(self):
        nsecsTai = 1192755506000000000L
        self.db.outColumn("taiToUtc(%d)" % nsecsTai)
        self.db.outColumn("utcToTai(taiToUtc(%d))" % nsecsTai)
        self.db.outColumn("taiToMjdUtc(%d)" % nsecsTai)
        self.db.query()
        haveRow = self.db.Next()
        self.assert_(haveRow)
        self.assertEqual(self.db.getColumnByPosInt64(0), 1192755473000000000L)
        self.assertEqual(self.db.getColumnByPosInt64(1), 1192755506000000000L)
        self.assertAlmostEqual(self.db.getColumnByPosDouble(2), 54392.040196759262)
        haveRow = self.db.next()
        self.assert_(not haveRow)

if __name__ == '__main__':
    unittest.main()
