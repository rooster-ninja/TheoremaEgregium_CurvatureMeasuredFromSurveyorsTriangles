# Scripts

Python 3. Dependencies: `numpy`, `pyproj`, `matplotlib`, `shapely`, `mpmath`, `basemap` (globe only), `openpyxl` (workbook), `pymupdf` (source extracts).

Run from a working directory; each step writes JSON the next one reads.

| Order | Script | Does |
| --- | --- | --- |
| 1 | `parse.py ../data/arcs_parallel_master.kml` | KML → `data.json` |
| 2 | `analyse.py` | Observed excess per triangle, QC, the three source-verified corrections, first-pass fit → `rows.json`, `summary.json` |
| 3 | `sides.py` | Printed side lengths → metres → `rows_s.json` |
| 4 | `fit2.py` | Areas from printed sides, law-of-sines check, tiers → `rows_t.json` |
| 5 | `rule_fit.py` | The declared rule (`RULE.md`): main result, sensitivity runs, per-survey results → `rule_results.json` |
| 6 | `angle_err.py` | Per-angle error from closures; Helmert's printed corrections |
| 7 | `chain.py` | Whole-chain sums over non-overlapping triangles → `chain_results.json` |
| — | `snr_charts.py`, `forest.py`, `signal_noise.py`, `chain_fig.py`, `chain_curve.py`, `chain_section.py`, `chain_section_true.py`, `globe_lab.py`, `detail.py`, `rebuild.py`, `timeline.py`, `shasta.py`, `shasta_true.py` | Charts in `figures/` |
| — | `quad.py` | Distance-only curvature from quadrilaterals (shows why printed sides cannot test curvature) |
| — | `build_xlsx.py` | `supplemental/Curvature_from_triangles.xlsx` |
| — | `annotate.py`, `gallery.py` | Source extracts and the plate gallery (need the scanned PDFs, not included) |
