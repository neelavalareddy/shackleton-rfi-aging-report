"""Pure analysis functions. Stdlib only. Inputs are plain dicts (see generator)."""
from datetime import date
from statistics import mean, median

RFI_DUE_DAYS = 14
BUCKETS = ("0-7", "8-14", "15-30", "30+")


def parse(d):
    return d if isinstance(d, date) else date.fromisoformat(d)


def days_between(a, b):
    return (parse(b) - parse(a)).days


def turnaround_days(rfi):
    """Days raised -> response. None if no response date. Same-day = 0."""
    if not rfi.get("response_date"):
        return None
    n = days_between(rfi["raised_date"], rfi["response_date"])
    if n < 0:
        raise ValueError("response before raised: %s" % rfi.get("id"))
    return n


def bucket_for_age(age):
    if age < 0:
        raise ValueError("negative age")
    if age <= 7:
        return "0-7"
    if age <= 14:
        return "8-14"
    if age <= 30:
        return "15-30"
    return "30+"


def is_open(rfi):
    return not rfi.get("response_date")


def is_overdue(rfi, as_of, due_days=RFI_DUE_DAYS):
    return is_open(rfi) and days_between(rfi["raised_date"], as_of) > due_days


def _stats(values):
    if not values:
        return {"count": 0, "median": None, "mean": None}
    return {"count": len(values), "median": float(median(values)),
            "mean": round(mean(values), 2)}


def turnaround_stats(rfis, key=None):
    """Overall stats (key=None) or dict group->stats. Open RFIs are excluded."""
    if key is None:
        return _stats([t for t in map(turnaround_days, rfis) if t is not None])
    groups = {}
    for r in rfis:
        t = turnaround_days(r)
        if t is not None:
            groups.setdefault(r[key], []).append(t)
    return {k: _stats(groups[k]) for k in sorted(groups)}


def aging_buckets(rfis, as_of):
    out = {b: 0 for b in BUCKETS}
    for r in rfis:
        if is_open(r):
            out[bucket_for_age(days_between(r["raised_date"], as_of))] += 1
    return out


def bottleneck_owners(rfis, as_of, top=5):
    """[(owner, overdue_count)] ranked desc by count, ties by owner name."""
    counts = {}
    for r in rfis:
        if is_overdue(r, as_of):
            counts[r["owner"]] = counts.get(r["owner"], 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:top]


def submittal_lag_days(s):
    if not s.get("review_date"):
        return None
    n = days_between(s["submitted_date"], s["review_date"])
    if n < 0:
        raise ValueError("review before submission: %s" % s.get("id"))
    return n


def submittal_lag_stats(subs):
    return _stats([x for x in map(submittal_lag_days, subs) if x is not None])


def slowest_reviewers(subs, top=5, min_reviews=1):
    """[(reviewer, median_lag, n)] ranked by median lag desc, then name."""
    g = {}
    for s in subs:
        n = submittal_lag_days(s)
        if n is not None:
            g.setdefault(s["reviewer"], []).append(n)
    rows = [(k, float(median(v)), len(v)) for k, v in g.items() if len(v) >= min_reviews]
    return sorted(rows, key=lambda r: (-r[1], r[0]))[:top]


def budget_drift(change_orders, budgets):
    """Per project: pending $, approved $, drift_pct vs baseline budget.

    drift_pct = (approved + pending) / baseline * 100; None if baseline <= 0.
    Zero-dollar COs are counted but add no dollars. Rejected COs are ignored.
    """
    rows = {}
    for co in change_orders:
        r = rows.setdefault(co["project"], {"pending": 0, "approved": 0,
                                            "co_count": 0, "zero_dollar": 0})
        r["co_count"] += 1
        if co["cost_impact"] == 0:
            r["zero_dollar"] += 1
        if co["status"] == "pending":
            r["pending"] += co["cost_impact"]
        elif co["status"] == "approved":
            r["approved"] += co["cost_impact"]
    for p, r in rows.items():
        base = budgets.get(p, 0)
        r["drift_pct"] = round((r["approved"] + r["pending"]) / base * 100, 2) if base > 0 else None
    return rows


def total_pending(change_orders):
    return sum(c["cost_impact"] for c in change_orders if c["status"] == "pending")


def rank_drift(drift, top=5):
    """Projects ranked by drift_pct desc (None last), then name."""
    items = list(drift.items())
    return sorted(items, key=lambda kv: (kv[1]["drift_pct"] is None,
                                         -(kv[1]["drift_pct"] or 0), kv[0]))[:top]


def open_items_by_project(field_reports):
    out = {}
    for f in field_reports:
        out[f["project"]] = out.get(f["project"], 0) + f["open_items"]
    return dict(sorted(out.items()))
