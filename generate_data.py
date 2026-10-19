"""Generates the illustrative monthly finance data used by the dashboard.

Output: data/finance_monthly.csv, one row per month and region, $ thousands.
Run:  python generate_data.py
"""
import csv
import math
import random
from pathlib import Path

random.seed(42)
REGIONS = {"North": 420, "South": 310, "West": 250}   # base monthly revenue
MONTHS = [f"{2023 + (10 + i) // 12}-{(10 + i) % 12 + 1:02d}" for i in range(24)]  # Nov 2023 .. Oct 2025


def main():
    rows = []
    for region, base in REGIONS.items():
        growth = {"North": 0.010, "South": 0.006, "West": 0.014}[region]
        for i, month in enumerate(MONTHS):
            m = int(month[5:])
            season = 1 + 0.08 * math.sin((m - 3) / 12 * 2 * math.pi)        # spring/summer peak
            revenue = base * (1 + growth) ** i * season * random.uniform(0.95, 1.05)
            budget = base * (1 + growth * 0.9) ** i * season * 1.01
            gm = 0.38 + 0.0015 * i + random.uniform(-0.01, 0.01)           # gross margin creeps up
            cogs = revenue * (1 - gm)
            opex = base * 0.22 * (1 + 0.004) ** i * random.uniform(0.97, 1.03)
            dso = {"North": 44, "South": 52, "West": 47}[region] - 0.25 * i + random.uniform(-2, 2)
            receivables = revenue * 12 / 365 * dso
            rows.append({"month": month, "region": region, "revenue": round(revenue, 1), "budget_revenue": round(budget, 1),
                         "cost_of_sales": round(cogs, 1), "operating_expenses": round(opex, 1),
                         "receivables": round(receivables, 1)})
    Path("data").mkdir(exist_ok=True)
    with open("data/finance_monthly.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} rows to data/finance_monthly.csv")


if __name__ == "__main__":
    main()
