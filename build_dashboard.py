"""Builds dashboard/index.html: embeds data/finance_monthly.csv into src/template.html.

The output is one self-contained HTML file with no external libraries, so it can be
opened straight from disk or hosted on GitHub Pages.
Run:  python build_dashboard.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).parent
NUMERIC = ["units", "revenue", "budget_revenue", "cost_of_sales", "operating_expenses", "receivables"]


def main():
    with open(ROOT / "data" / "finance_monthly.csv", newline="") as f:
        rows = [{**r, **{k: float(r[k]) for k in NUMERIC}} for r in csv.DictReader(f)]
    template = (ROOT / "src" / "template.html").read_text()
    html = template.replace("/*__DATA__*/[]", json.dumps(rows, separators=(",", ":")))
    out = ROOT / "dashboard" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html)
    print(f"Wrote {out.relative_to(ROOT)} ({len(rows)} rows embedded)")


if __name__ == "__main__":
    main()
