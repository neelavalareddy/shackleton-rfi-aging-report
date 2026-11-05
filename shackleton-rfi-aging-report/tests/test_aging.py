import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rfi_aging import analysis as A  # noqa: E402
from rfi_aging.generator import generate  # noqa: E402
from rfi_aging.report import compute, render_markdown  # noqa: E402

AS_OF = "2026-11-05"


def rfi(raised, resp=None, owner="o", disc="D", proj="P1"):
    return {"id": "x", "raised_date": raised, "response_date": resp, "owner": owner,
            "discipline": disc, "project": proj}


class Bucketing(unittest.TestCase):
    def test_boundaries(self):
        for age, b in [(0, "0-7"), (7, "0-7"), (8, "8-14"), (14, "8-14"), (15, "15-30"),
                       (30, "15-30"), (31, "30+"), (200, "30+")]:
            self.assertEqual(A.bucket_for_age(age), b)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            A.bucket_for_age(-1)

    def test_aging_counts_only_open(self):
        rs = [rfi("2026-11-05"), rfi("2026-10-29"), rfi("2026-10-20"), rfi("2026-09-01"),
              rfi("2026-09-01", "2026-09-05")]
        self.assertEqual(A.aging_buckets(rs, AS_OF), {"0-7": 2, "8-14": 0, "15-30": 1, "30+": 1})


class Turnaround(unittest.TestCase):
    def test_same_day(self):
        self.assertEqual(A.turnaround_days(rfi("2026-10-01", "2026-10-01")), 0)

    def test_missing_response(self):
        self.assertIsNone(A.turnaround_days(rfi("2026-10-01")))

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            A.turnaround_days(rfi("2026-10-02", "2026-10-01"))

    def test_median_mean(self):
        rs = [rfi("2026-10-01", "2026-10-01"), rfi("2026-10-01", "2026-10-03"),
              rfi("2026-10-01", "2026-10-11"), rfi("2026-10-01")]
        s = A.turnaround_stats(rs)
        self.assertEqual((s["count"], s["median"], s["mean"]), (3, 2.0, 4.0))

    def test_empty(self):
        self.assertEqual(A.turnaround_stats([])["median"], None)

    def test_by_discipline(self):
        rs = [rfi("2026-10-01", "2026-10-05", disc="A"), rfi("2026-10-01", "2026-10-03", disc="B"),
              rfi("2026-10-01", "2026-10-07", disc="A")]
        g = A.turnaround_stats(rs, "discipline")
        self.assertEqual(g["A"]["median"], 5.0)
        self.assertEqual(g["B"]["count"], 1)


class Ranking(unittest.TestCase):
    def test_bottlenecks_ranked_and_overdue_only(self):
        rs = [rfi("2026-09-01", owner="B")] * 2 + [rfi("2026-09-01", owner="A")] * 2 + \
             [rfi("2026-09-01", owner="C")] + [rfi("2026-11-01", owner="Z")] * 5 + \
             [rfi("2026-09-01", "2026-09-02", owner="Y")] * 9
        self.assertEqual(A.bottleneck_owners(rs, AS_OF), [("A", 2), ("B", 2), ("C", 1)])

    def test_overdue_threshold(self):
        self.assertFalse(A.is_overdue(rfi("2026-10-22"), AS_OF))  # 14 days
        self.assertTrue(A.is_overdue(rfi("2026-10-21"), AS_OF))   # 15 days

    def test_slowest_reviewers(self):
        subs = [{"reviewer": "A", "submitted_date": "2026-10-01", "review_date": "2026-10-11"},
                {"reviewer": "B", "submitted_date": "2026-10-01", "review_date": "2026-10-03"},
                {"reviewer": "B", "submitted_date": "2026-10-01"}]
        self.assertEqual(A.slowest_reviewers(subs), [("A", 10.0, 1), ("B", 2.0, 1)])
        self.assertEqual(A.submittal_lag_stats(subs)["count"], 2)


class Budget(unittest.TestCase):
    def cos(self):
        return [{"project": "P1", "cost_impact": 1000, "status": "pending"},
                {"project": "P1", "cost_impact": 0, "status": "pending"},
                {"project": "P1", "cost_impact": 500, "status": "approved"},
                {"project": "P1", "cost_impact": 9999, "status": "rejected"},
                {"project": "P2", "cost_impact": 0, "status": "pending"}]

    def test_drift(self):
        d = A.budget_drift(self.cos(), {"P1": 10000, "P2": 0})
        self.assertEqual(d["P1"]["pending"], 1000)
        self.assertEqual(d["P1"]["approved"], 500)
        self.assertEqual(d["P1"]["drift_pct"], 15.0)
        self.assertEqual(d["P1"]["zero_dollar"], 1)

    def test_zero_dollar_and_zero_baseline(self):
        d = A.budget_drift(self.cos(), {"P1": 10000, "P2": 0})
        self.assertEqual(d["P2"]["pending"], 0)
        self.assertIsNone(d["P2"]["drift_pct"])
        self.assertEqual(A.rank_drift(d)[0][0], "P1")  # None drift ranks last

    def test_total_pending(self):
        self.assertEqual(A.total_pending(self.cos()), 1000)


class Pipeline(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(generate(7), generate(7))
        self.assertNotEqual(generate(7), generate(8))

    def test_synthetic_marked_and_shape(self):
        d = generate(1)
        self.assertTrue(d["synthetic"])
        self.assertEqual(len(d["projects"]), 12)
        self.assertTrue(all(p["name"].startswith("SYNTHETIC") for p in d["projects"]))

    def test_generated_data_valid(self):
        d = generate(2026)
        for r in d["rfis"]:
            A.turnaround_days(r)  # no negative lags
            if r["status"] == "answered":
                self.assertTrue(r["response_date"])
        for s in d["submittals"]:
            A.submittal_lag_days(s)

    def test_report_renders(self):
        md = render_markdown(compute(generate(2026)))
        self.assertIn("SYNTHETIC", md)
        self.assertIn("Open RFI aging", md)


if __name__ == "__main__":
    unittest.main()
