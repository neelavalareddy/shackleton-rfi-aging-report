"""Demo: generate SYNTHETIC data, print headline metrics, write sample_report.md."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfi_aging.report import build, headline, render_markdown  # noqa: E402

m = build(2026)
print("=== RFI & Submittal Aging: headline metrics (SYNTHETIC DATA) ===")
print("\n".join(headline(m)))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_report.md")
with open(out, "w") as f:
    f.write(render_markdown(m))
print("Wrote " + out)
