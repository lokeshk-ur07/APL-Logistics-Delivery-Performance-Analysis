# APL Logistics Delivery Performance Project

## Files
- `APL_Logistics_EDA.ipynb` — reproducible analysis notebook.
- `app.py` — interactive Streamlit dashboard.
- `APL_Logistics_Research_Report.docx` — full research/analysis report.
- `APL_Logistics_Executive_Summary.docx` — concise stakeholder summary.
- `APL_Logistics_Project_Presentation.pptx` — presentation/viva slides.
- `apl_logistics_analysis_data.csv.zip` — analysis-ready data with direct customer identifiers removed.
- PNG files — report/dashboard supporting charts.

## Run the dashboard
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.
5. Open the local URL shown by Streamlit.

## Run the notebook
Open `APL_Logistics_EDA.ipynb` in Jupyter Notebook, JupyterLab or Google Colab. Keep the notebook and `apl_logistics_analysis_data.csv.zip` in the same folder.

## Metric definitions
`Delay Gap = Days for shipping (real) - Days for shipment (scheduled)`.
- Positive: Delayed
- Zero: On-time
- Negative: Early

The strict on-time rate counts only zero-gap records. Do not confuse this measure with the source `Delivery Status` or `Late_delivery_risk` field.

## Important limitations
The source CSV has no order/dispatch/delivery date, carrier, route, facility or delay-reason fields. Consequently, date filtering, time trends, seasonality and definitive root-cause attribution are not possible. The dashboard intentionally does not provide a date filter. Cancelled shipments should be separated from completed-delivery SLA denominators.

## Submission checklist
- Review the report cover page and add your name, institution, course and submission date if required.
- Confirm your institution's citation/formatting requirements.
- Run the notebook from top to bottom and the Streamlit app locally before submission.
- If your instructor requires the original dataset, submit it separately through the institution's approved secure channel; it contains personal customer information.

## Dataset provenance note
The dataset was supplied by the project user for the APL Logistics case study. The files do not independently verify that it is an internal APL Logistics system extract. Do not describe it as audited company data unless you have a source document confirming provenance.


Dataset upload note: the analysis CSV is stored as a ZIP archive to remain below GitHub's browser upload limit. The notebook and dashboard read the ZIP directly with Pandas.
