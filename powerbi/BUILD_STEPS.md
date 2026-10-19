# Building this dashboard in Power BI

The web version of this dashboard is plain HTML so anyone can open it without a licence.
These steps rebuild the same report in Power BI Desktop (free, Windows), using the same data and the measures in [`measures.dax`](measures.dax).

## 1. Load the data

1. Open Power BI Desktop and choose **Get data > Text/CSV**.
2. Pick `data/finance_monthly.csv` and click **Transform Data**.
3. In Power Query, rename the query to `Finance`.
4. Add a date column: **Add Column > Custom Column**, name `month_date`, formula `Date.FromText([month] & "-01")`, then set its type to **Date**.
5. Check the number columns are **Decimal number**, then click **Close & Apply**.

## 2. Add a calendar table

1. Go to **Modeling > New table** and paste:

   ```DAX
   Date =
   ADDCOLUMNS (
       CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2025, 12, 31 ) ),
       "Year", YEAR ( [Date] ),
       "Month", FORMAT ( [Date], "mmm yy" ),
       "MonthNo", YEAR ( [Date] ) * 100 + MONTH ( [Date] )
   )
   ```

2. Select the new table, choose **Table tools > Mark as date table**, and pick `Date`.
3. Sort the `Month` column by `MonthNo` (**Column tools > Sort by column**).
4. In **Model view**, drag `Date[Date]` onto `Finance[month_date]` to create a one-to-many relationship.

## 3. Create the measures

Select the `Finance` table, click **New measure** and paste each measure from [`measures.dax`](measures.dax), one at a time.
Format the `%` measures as **Percentage** with 1 decimal place, and the amounts as **Whole number** with a `$` prefix.

## 4. Build the page

| Visual | Fields |
|---|---|
| Slicer (dropdown) | `Finance[region]` |
| Slicer (between) | `Date[Date]`, or a button-style slicer on `Date[Year]` |
| 5 Card visuals | `Revenue`, `Variance to Budget %`, `Gross Margin %`, `EBITDA Margin %`, `DSO (days)` |
| Line chart: revenue vs budget | X: `Date[Month]`; Y: `Revenue`, `Budget Revenue` (budget as a dashed line under **Format > Lines**) |
| Column chart: monthly variance | X: `Date[Month]`; Y: `Variance to Budget %`; **Format > Columns > fx**: colour by rules on `Variance Is Positive` (1 = blue, 0 = red) |
| Line chart: margins | X: `Date[Month]`; Y: `Gross Margin %`, `EBITDA Margin %`; Y axis starts at 0 |
| Bar chart: revenue by region | Y: `Finance[region]`; X: `Revenue`; tooltip: `Budget Revenue`, `Revenue Share of Total` |

For the subtitle under each card, use **Format > Callout value > Reference label** (newer versions) or a second card showing `Revenue YoY %`, `Gross Margin Change (pts)` and `EBITDA Margin Change (pts)`.

## 5. Publish (optional)

**Home > Publish** sends the report to the Power BI service. Free accounts cannot embed publicly, so for a portfolio either share screenshots or upload the `.pbix` to this repository.

## Checking the numbers

With all regions and the last 12 months (Nov 2024 to Oct 2025) selected, the cards should show:
revenue $13.97m, variance to budget +0.7%, gross margin 40.6%, EBITDA margin 20.8% and DSO 40.4 days.
These are the same figures the web dashboard shows, so they are a quick check that the model is built correctly.
