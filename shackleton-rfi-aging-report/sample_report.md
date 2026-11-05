# RFI & Submittal Aging Report

> **SYNTHETIC DATA.** Generated offline from a seeded fictional dataset. Prototype only; not Shackleton AI's real data.

## Headline metrics

- Dataset: SYNTHETIC (seed 2026, as of 2026-11-05): 12 projects, 255 RFIs, 178 submittals, 77 change orders, 129 field reports
- RFI turnaround: median 7.0 d, mean 11.03 d (n=187 answered)
- Open RFIs: 68 (overdue >14 d: 60)
- Aging buckets: 0-7 d=3, 8-14 d=5, 15-30 d=13, 30+ d=47
- Top bottleneck: E. Brandt (MEP Engineer) (10 overdue)
- Submittal review lag: median 9.0 d, mean 12.51 d (n=150 reviewed)
- Change-order dollars pending approval: $2,045,000

## RFI turnaround by discipline

| Discipline | Answered | Median d | Mean d |
|---|---|---|---|
| Architectural | 22 | 5.0 | 10.27 |
| Civil | 37 | 9.0 | 12.35 |
| Electrical | 20 | 2.5 | 5.85 |
| Fire Protection | 36 | 7.0 | 9.64 |
| Mechanical | 24 | 15.5 | 13.62 |
| Plumbing | 27 | 9.0 | 12.37 |
| Structural | 21 | 7.0 | 12.1 |

## RFI turnaround by project

| Project | Answered | Median d | Mean d |
|---|---|---|---|
| SYNTHETIC Alder Row Lofts | 17 | 7.0 | 12.12 |
| SYNTHETIC Birchfield Clinic | 10 | 5.0 | 9.6 |
| SYNTHETIC Cedar Quay Tower | 17 | 7.0 | 9.41 |
| SYNTHETIC Dunmore Logistics Hub | 18 | 7.0 | 9.67 |
| SYNTHETIC Elmstead School | 15 | 9.0 | 11.87 |
| SYNTHETIC Fairhaven Library | 19 | 7.0 | 11.53 |
| SYNTHETIC Granite Pass Hotel | 12 | 13.0 | 16.58 |
| SYNTHETIC Harbor Light Labs | 18 | 9.0 | 12.06 |
| SYNTHETIC Ironwood Parking Deck | 8 | 9.5 | 11 |
| SYNTHETIC Juniper Court Apartments | 20 | 6.0 | 10.1 |
| SYNTHETIC Kestrel Data Hall | 17 | 7.0 | 8.88 |
| SYNTHETIC Larkspur Hospital Wing | 16 | 6.0 | 10.75 |

## Open RFI aging

| Bucket (days open) | Open RFIs |
|---|---|
| 0-7 | 3 |
| 8-14 | 5 |
| 15-30 | 13 |
| 30+ | 47 |

## Bottleneck owners (most overdue RFIs)

| Owner | Overdue RFIs |
|---|---|
| E. Brandt (MEP Engineer) | 10 |
| G. Novak (Civil Engineer) | 10 |
| A. Okafor (Architect) | 8 |
| B. Lindqvist (Engineer) | 8 |
| D. Tanaka (Architect) | 8 |

## Submittal review lag

Median 9.0 d, mean 12.51 d over 150 reviewed submittals.

Slowest reviewers (min 3 reviews):

| Reviewer | Median lag d | Reviews |
|---|---|---|
| U. Haldane | 12.0 | 33 |
| R. Abara | 9.0 | 25 |
| V. Petrov | 9.0 | 23 |
| T. Vasquez | 7.5 | 22 |
| W. Osei | 7.5 | 24 |

## Budget-drift signals

Change-order dollars pending approval: **$2,045,000**

Drift = (approved + pending CO $) / baseline budget. Top projects:

| Project | Pending $ | Approved $ | Drift % | Zero-$ COs | Open field items |
|---|---|---|---|---|---|
| SYNTHETIC Alder Row Lofts | 715,000 | 180,000 | 3.89 | 1 | 50 |
| SYNTHETIC Harbor Light Labs | 106,000 | 440,000 | 1.52 | 2 | 25 |
| SYNTHETIC Dunmore Logistics Hub | 0 | 702,500 | 0.96 | 3 | 47 |
| SYNTHETIC Birchfield Clinic | 456,000 | 0 | 0.95 | 0 | 58 |
| SYNTHETIC Larkspur Hospital Wing | 375,000 | 180,000 | 0.91 | 0 | 41 |
