"""Compute metrics and render the Markdown report from them."""
from . import analysis as A
from .generator import generate


def compute(data):
    as_of = data["as_of"]
    rfis, subs, cos = data["rfis"], data["submittals"], data["change_orders"]
    names = {p["id"]: p["name"] for p in data["projects"]}
    budgets = {p["id"]: p["baseline_budget"] for p in data["projects"]}
    drift = A.budget_drift(cos, budgets)
    return {
        "as_of": as_of, "names": names, "seed": data["seed"],
        "counts": {"projects": len(data["projects"]), "rfis": len(rfis), "submittals": len(subs),
                   "change_orders": len(cos), "field_reports": len(data["field_reports"])},
        "rfi_overall": A.turnaround_stats(rfis),
        "rfi_by_discipline": A.turnaround_stats(rfis, "discipline"),
        "rfi_by_project": A.turnaround_stats(rfis, "project"),
        "open_rfis": sum(1 for r in rfis if A.is_open(r)),
        "aging": A.aging_buckets(rfis, as_of),
        "overdue_rfis": sum(1 for r in rfis if A.is_overdue(r, as_of)),
        "bottlenecks": A.bottleneck_owners(rfis, as_of, 5),
        "submittal_lag": A.submittal_lag_stats(subs),
        "slowest_reviewers": A.slowest_reviewers(subs, 5, 3),
        "pending_co_dollars": A.total_pending(cos),
        "drift": drift, "top_drift": A.rank_drift(drift, 5),
        "open_items": A.open_items_by_project(data["field_reports"]),
    }


def headline(m):
    return [
        "Dataset: SYNTHETIC (seed %d, as of %s): %d projects, %d RFIs, %d submittals, %d change orders, %d field reports" % (
            m["seed"], m["as_of"], m["counts"]["projects"], m["counts"]["rfis"], m["counts"]["submittals"],
            m["counts"]["change_orders"], m["counts"]["field_reports"]),
        "RFI turnaround: median %s d, mean %s d (n=%d answered)" % (
            m["rfi_overall"]["median"], m["rfi_overall"]["mean"], m["rfi_overall"]["count"]),
        "Open RFIs: %d (overdue >%d d: %d)" % (m["open_rfis"], A.RFI_DUE_DAYS, m["overdue_rfis"]),
        "Aging buckets: " + ", ".join("%s d=%d" % (b, m["aging"][b]) for b in A.BUCKETS),
        "Top bottleneck: %s" % ("%s (%d overdue)" % m["bottlenecks"][0] if m["bottlenecks"] else "none"),
        "Submittal review lag: median %s d, mean %s d (n=%d reviewed)" % (
            m["submittal_lag"]["median"], m["submittal_lag"]["mean"], m["submittal_lag"]["count"]),
        "Change-order dollars pending approval: $%s" % format(m["pending_co_dollars"], ","),
    ]


def _t(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def _f(x):
    return "n/a" if x is None else x


def render_markdown(m):
    L = ["# RFI & Submittal Aging Report", "",
         "> **SYNTHETIC DATA.** Generated offline from a seeded fictional dataset. "
         "Prototype only; not Shackleton AI's real data.", "",
         "## Headline metrics", ""]
    L += ["- " + h for h in headline(m)]
    L += ["", "## RFI turnaround by discipline", "",
          _t(["Discipline", "Answered", "Median d", "Mean d"],
             [(k, v["count"], v["median"], v["mean"]) for k, v in m["rfi_by_discipline"].items()]),
          "", "## RFI turnaround by project", "",
          _t(["Project", "Answered", "Median d", "Mean d"],
             [(m["names"][k], v["count"], v["median"], v["mean"]) for k, v in m["rfi_by_project"].items()]),
          "", "## Open RFI aging", "",
          _t(["Bucket (days open)", "Open RFIs"], [(b, m["aging"][b]) for b in A.BUCKETS]),
          "", "## Bottleneck owners (most overdue RFIs)", "",
          _t(["Owner", "Overdue RFIs"], m["bottlenecks"]),
          "", "## Submittal review lag", "",
          "Median %s d, mean %s d over %d reviewed submittals." % (
              m["submittal_lag"]["median"], m["submittal_lag"]["mean"], m["submittal_lag"]["count"]),
          "", "Slowest reviewers (min 3 reviews):", "",
          _t(["Reviewer", "Median lag d", "Reviews"], m["slowest_reviewers"]),
          "", "## Budget-drift signals", "",
          "Change-order dollars pending approval: **$%s**" % format(m["pending_co_dollars"], ","), "",
          "Drift = (approved + pending CO $) / baseline budget. Top projects:", "",
          _t(["Project", "Pending $", "Approved $", "Drift %", "Zero-$ COs", "Open field items"],
             [(m["names"][p], format(r["pending"], ","), format(r["approved"], ","), _f(r["drift_pct"]),
               r["zero_dollar"], m["open_items"].get(p, 0)) for p, r in m["top_drift"]]),
          ""]
    return "\n".join(L)


def build(seed=2026):
    return compute(generate(seed))
