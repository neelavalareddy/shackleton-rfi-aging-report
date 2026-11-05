"""Seeded SYNTHETIC data generator. All projects/people are fictional."""
import random
from datetime import date, timedelta

SYNTHETIC = True
AS_OF = date(2026, 11, 5)
DISCIPLINES = ["Structural", "Mechanical", "Electrical", "Plumbing", "Civil", "Architectural", "Fire Protection"]
PROJECT_NAMES = ["Alder Row Lofts", "Birchfield Clinic", "Cedar Quay Tower", "Dunmore Logistics Hub",
                 "Elmstead School", "Fairhaven Library", "Granite Pass Hotel", "Harbor Light Labs",
                 "Ironwood Parking Deck", "Juniper Court Apartments", "Kestrel Data Hall", "Larkspur Hospital Wing"]
OWNERS = ["A. Okafor (Architect)", "B. Lindqvist (Engineer)", "C. Moreau (Owner Rep)", "D. Tanaka (Architect)",
          "E. Brandt (MEP Engineer)", "F. Castillo (Structural EOR)", "G. Novak (Civil Engineer)", "H. Singh (Owner Rep)"]
REVIEWERS = ["R. Abara", "S. Whitcombe", "T. Vasquez", "U. Haldane", "V. Petrov", "W. Osei"]


def generate(seed=2026, as_of=AS_OF):
    rng = random.Random(seed)
    d = lambda n: (as_of - timedelta(days=n)).isoformat()
    projects = []
    for i, name in enumerate(PROJECT_NAMES):
        projects.append({"id": "P%02d" % (i + 1), "name": "SYNTHETIC " + name,
                         "baseline_budget": rng.randrange(8, 120) * 1_000_000})
    rfis, subs, cos, frs = [], [], [], []
    for p in projects:
        pid = p["id"]
        for k in range(rng.randint(14, 26)):
            age = rng.randint(1, 120)
            answered = rng.random() < 0.72
            resp = None
            if answered:
                lag = min(age, rng.choice([0, 1, 2, 3, 5, 7, 9, 12, 16, 21, 28, 40]))
                resp = d(age - lag)
            if resp:
                status = "answered"
            else:
                status = "overdue" if age > 14 else "open"
            rfis.append({"id": "%s-RFI-%03d" % (pid, k + 1), "project": pid,
                         "discipline": rng.choice(DISCIPLINES), "owner": rng.choice(OWNERS),
                         "raised_date": d(age), "response_date": resp, "status": status})
        for k in range(rng.randint(10, 20)):
            age = rng.randint(1, 100)
            done = rng.random() < 0.8
            rd, st = None, "pending"
            if done:
                rd = d(max(0, age - rng.choice([2, 4, 6, 9, 12, 15, 20, 28, 35])))
                st = rng.choice(["approved", "approved", "revise_resubmit", "rejected"])
            subs.append({"id": "%s-SUB-%03d" % (pid, k + 1), "project": pid,
                         "reviewer": rng.choice(REVIEWERS), "submitted_date": d(age),
                         "review_date": rd, "review_status": st})
        for k in range(rng.randint(3, 9)):
            age = rng.randint(1, 110)
            amt = rng.choice([0, 0, 2500, 8000, 15000, 42000, 90000, 180000, 350000])
            st = rng.choice(["approved", "pending", "pending", "rejected"])
            ad = None
            if st != "pending":
                ad = d(max(0, age - rng.randint(3, 45)))
            cos.append({"id": "%s-CO-%03d" % (pid, k + 1), "project": pid, "cost_impact": amt,
                        "status": st, "submitted_date": d(age), "decision_date": ad})
        for k in range(rng.randint(8, 14)):
            frs.append({"id": "%s-FR-%03d" % (pid, k + 1), "project": pid,
                        "date": d(rng.randint(0, 60)), "open_items": rng.randint(0, 9)})
    return {"synthetic": True, "as_of": as_of.isoformat(), "seed": seed, "projects": projects,
            "rfis": rfis, "submittals": subs, "change_orders": cos, "field_reports": frs}
