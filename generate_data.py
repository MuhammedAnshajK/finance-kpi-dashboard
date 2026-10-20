"""Generates the illustrative monthly sales data used by the dashboard.

Output: data/finance_monthly.csv, one row per month, region and product line,
$ thousands (units in thousands). Run:  python generate_data.py
"""
import csv
import math
import random
from pathlib import Path

random.seed(42)
REGIONS = {"North": 420, "South": 310, "West": 250}   # base monthly revenue, all products
REGION_GROWTH = {"North": 0.010, "South": 0.006, "West": 0.014}
REGION_DSO = {"North": 44, "South": 52, "West": 47}
# product line: share of revenue, monthly growth, gross margin, average selling price ($), peak month
PRODUCTS = {
    "Running Shoes":   (0.34, 0.012, 0.44, 95, 4),
    "Lifestyle Shoes": (0.24, -0.002, 0.40, 80, 11),
    "Apparel":         (0.28, 0.006, 0.36, 40, 6),
    "Accessories":     (0.14, 0.010, 0.50, 25, 12),
}
MONTHS = [f"{2023 + (10 + i) // 12}-{(10 + i) % 12 + 1:02d}" for i in range(24)]  # Nov 2023 .. Oct 2025


def main():
    rows = []
    for region, base in REGIONS.items():
        for product, (share, pg, gm0, asp, peak) in PRODUCTS.items():
            pbase = base * share
            growth = REGION_GROWTH[region] + pg - 0.006
            for i, month in enumerate(MONTHS):
                m = int(month[5:])
                season = 1 + 0.10 * math.cos((m - peak) / 12 * 2 * math.pi)       # each line peaks in its own season
                revenue = pbase * (1 + growth) ** i * season * random.uniform(0.93, 1.07)
                target = pbase * (1 + (REGION_GROWTH[region] + 0.004) * 0.85) ** i * season
                price = asp * (1 + 0.002 * i) * random.uniform(0.98, 1.02)
                units = revenue / price
                gm = gm0 + 0.0015 * i + random.uniform(-0.012, 0.012)            # gross margin creeps up
                cogs = revenue * (1 - gm)
                opex = pbase * 0.22 * (1 + 0.004) ** i * random.uniform(0.97, 1.03)
                dso = REGION_DSO[region] - 0.25 * i + random.uniform(-2, 2)
                receivables = revenue * 12 / 365 * dso
                rows.append({"month": month, "region": region, "product": product, "units": round(units, 2),
                             "revenue": round(revenue, 1), "budget_revenue": round(target, 1),
                             "cost_of_sales": round(cogs, 1), "operating_expenses": round(opex, 1),
                             "receivables": round(receivables, 1)})
    rows.sort(key=lambda r: (r["month"], r["region"], r["product"]))
    Path("data").mkdir(exist_ok=True)
    with open("data/finance_monthly.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} rows to data/finance_monthly.csv")


if __name__ == "__main__":
    main()
