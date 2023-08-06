from unittest import TestCase
from contracting.stdlib.bridge.time import Datetime, Timedelta
from datetime import datetime as dt
from datetime import timedelta


class TestDatetime(TestCase):
    def test_datetime_variables_set(self):
        now = dt.now()

        d = Datetime(now.year, now.month, now.day)

        self.assertEqual(0, d.microsecond)
        self.assertEqual(0, d.second)
        self.assertEqual(0, d.minute)
        self.assertEqual(0, d.hour)
        self.assertEqual(now.day, d.day)
        self.assertEqual(now.month, d.month)
        self.assertEqual(now.year, d.year)

    ###
    # ==
    ###
    def test_datetime_eq_true(self):
        now = dt.now()

        d = Datetime(now.year, now.month, now.day)
        e = Datetime(now.year, now.month, now.day)

        self.assertTrue(d == e)

    def test_datetime_eq_false(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertFalse(d == e)

    ###
    # !=
    ###
    def test_datetime_ne_false(self):
        now = dt.now()

        d = Datetime(now.year, now.month, now.day)
        e = Datetime(now.year, now.month, now.day)

        self.assertFalse(d != e)

    def test_datetime_ne_true(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertTrue(d != e)

    ###
    # <
    ###
    def test_datetime_lt_true(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertTrue(d < e)

    def test_datetime_lt_false(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertFalse(e < d)

    ###
    # >
    ###
    def test_datetime_gt_true(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertTrue(e > d)

    def test_datetime_gt_false(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertFalse(d > e)

    ###
    # >=
    ###
    def test_datetime_ge_true_g(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertTrue(e >= d)

    def test_datetime_ge_true_eq(self):
        now = dt.now()

        d = Datetime(now.year, now.month, now.day)
        e = Datetime(now.year, now.month, now.day)

        self.assertTrue(d >= e)

    def test_datetime_ge_false_g(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertFalse(d >= e)

    ###
    # <=
    ###
    def test_datetime_le_true(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertTrue(d <= e)

    def test_datetime_le_true_eq(self):
        now = dt.now()

        d = Datetime(now.year, now.month, now.day)
        e = Datetime(now.year, now.month, now.day)

        self.assertTrue(d <= e)

    def test_datetime_le_false(self):
        now = dt.now()
        d = Datetime(now.year, now.month, now.day)

        then = now + timedelta(days=1)
        e = Datetime(then.year, then.month, then.day)

        self.assertFalse(e <= d)

    def test_datetime_subtraction_to_proper_timedelta(self):
        d = Datetime(2019, 1, 1)
        e = Datetime(2018, 1, 1)

        self.assertEqual((d - e), Timedelta(days=365))