import argparse
import json
import sys

from .generator import generate
from .report import compute, headline, render_markdown


def main(argv=None):
    ap = argparse.ArgumentParser(prog="rfi_aging", description="RFI & submittal aging report (SYNTHETIC data)")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out", help="write Markdown report to this path (default: stdout)")
    ap.add_argument("--headline", action="store_true", help="print headline metrics only")
    ap.add_argument("--dump-data", help="write the synthetic dataset as JSON to this path")
    a = ap.parse_args(argv)
    data = generate(a.seed)
    if a.dump_data:
        with open(a.dump_data, "w") as f:
            json.dump(data, f, indent=1)
    m = compute(data)
    if a.headline:
        print("\n".join(headline(m)))
        return 0
    md = render_markdown(m)
    if a.out:
        with open(a.out, "w") as f:
            f.write(md)
        print("wrote " + a.out)
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
