# RFI & Submittal Aging Report (prototype)

**Prototype on SYNTHETIC data. Not Shackleton AI's real data.** Every project, person and number is fictional and produced by a seeded generator.

## The gap
Shackleton AI's homepage says: "Project managers spend 40% of their time on admin... RFIs fall through the cracks. Budgets drift without anyone noticing." This prototype shows the kind of measurement that makes those two problems visible: which RFIs are aging, who holds them, how slow submittal review is, and how much change-order money is waiting on approval.

## What it computes
- RFI turnaround (median/mean days) overall, by discipline and by project
- Open-RFI aging buckets: 0-7 / 8-14 / 15-30 / 30+ days
- Bottleneck owners: most overdue RFIs (open and older than 14 days)
- Submittal review lag: median/mean, slowest reviewers
- Budget drift: pending change-order dollars, (approved + pending) / baseline budget by project, open field-report items

## Synthetic data
`rfi_aging/generator.py` builds ~12 fictional projects with RFIs, submittals, change orders and field reports from `random.Random(seed)` (default seed 2026, fixed as-of date 2026-11-05). Same seed = identical data and report. No network, no third-party packages (Python 3.8+ stdlib).

## Run
```
python3 -m unittest discover -s tests -v   # tests
python3 demo.py                             # prints headline metrics, writes sample_report.md
python3 -m rfi_aging --out report.md        # CLI; also --seed N, --headline, --dump-data FILE.json
```
`sample_report.md` is only ever written by `demo.py` from computed output; none is hand-written.

## Limits
Overdue = no response and more than 14 days since raised (a fixed assumption). Drift is a simple signal against a synthetic baseline budget, not a forecast.
