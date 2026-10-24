# The Remarkable Theorem: background to the report

## 📄 [Read the page](https://rooster-ninja.github.io/TheoremaEgregium_CurvatureMeasuredFromSurveyorsTriangles/theorem/)

A companion to the [report](../README.md). The report measures the Earth's Gaussian curvature from surveyors' triangles; this page explains the theorem that makes that possible. Gauss's *Theorema Egregium* (1827, Art. 12) says a surface's curvature K depends only on distances measured within the surface, so it can be found from the inside, with no third dimension.

## What it covers

| § | Card | Contents |
| --- | --- | --- |
| 1 | The statement | Gauss's Latin text of Art. 12 with translation; K = κ₁κ₂ and the intrinsic form in geodesic polar coordinates; worked check for sphere and plane |
| 2 | History | Girard 1629 → Euler 1775 → Legendre 1787 → Delambre–Méchain 1792–98 → Gauss's Hanover survey and the *Disquisitiones* (presented 8 Oct 1827) → Bonnet and Bertrand–Diguet–Puiseux 1848 → Riemann 1854. The Brocken–Inselsberg–Hohenhagen "test of Euclid" story is marked as contested |
| 3 | The words | *theorema* (Greek, a sight to look at) and *egregium* (Latin, out of the flock); why English "egregious" is a false friend |
| 4 | What makes a theorem | Axiom, definition, lemma, theorem, corollary, conjecture; theorems are relative to their axioms |
| 5 | Among other theorems | Pythagoras, Girard, Legendre, quadratic reciprocity, Gauss's Art. 20 triangle theorem, Bertrand–Diguet–Puiseux, Gauss–Bonnet |
| 6 | Sphere versus plane | Constant-curvature geometries compared: angle sums, parallels, circle circumference, similar triangles, flattening |
| 7 | How big is the effect on Earth | Spherical excess of triangles and circumference deficit of geodesic circles, R_G = 6 382.0 km at 50.2° N |
| 8 | Back to the distance-only test | What the theorem promises a ranging network; ppm signal sizes and rough 3σ / 5σ error targets |

## Key numbers

Spherical model, R_G = √(MN) on WGS84 at 50.2° N = 6 382.0 km (6 356.8 km at the equator to 6 399.6 km at the pole). The report's measured K = 2.450 ± 0.012 × 10⁻¹⁴ m⁻² gives R = 6 388.8 km; the difference is under 0.3%.

| Equilateral side | Area, km² | Excess, arcsec |
| --- | ---: | ---: |
| 10 km | 43.3 | 0.219 |
| 30 km | 389.7 | 1.974 |
| 55 km | 1 309.9 | 6.633 |
| 100 km | 4 330.1 | 21.929 |
| Gauss triangle, 69 / 85 / 107 km (rounded) | 2 929.4 | 14.83 ± 0.1 |

| Geodesic radius | 2πr − C | Relative deficit, ppm |
| --- | ---: | ---: |
| 1 km | 0.03 mm | 0.004 |
| 10 km | 2.57 cm | 0.409 |
| 25 km | 40.2 cm | 2.558 |
| 55 km | 4.28 m | 12.378 |

Planning estimate, not a result: detecting the 55 km circle signal at 3σ needs an effective combined ranging error near 4 ppm or better; 5σ needs about 2.5 ppm, before refraction and chord-to-geodesic reduction errors.

## Files

| File | What it is |
| --- | --- |
| [`index.html`](index.html) | The page (GitHub Pages) |
| [`excess_tables.py`](excess_tables.py) | Reproduces both tables from WGS84 constants |
| [`excess_tables.json`](excess_tables.json), [`excess_tables.csv`](excess_tables.csv) | Script output; the CSV opens in any spreadsheet |

## Sources

Primary and scholarly sources only.

- Gauss, C. F., *Disquisitiones generales circa superficies curvas* (1827), Arts. 12, 16, 20, 26–28. English: *General Investigations of Curved Surfaces of 1827 and 1825*, tr. J. C. Morehead & A. M. Hiltebeitel, Princeton, 1902 ([Project Gutenberg #36856](https://www.gutenberg.org/ebooks/36856)).
- Legendre, A.-M., "Mémoire sur les opérations trigonométriques, dont les résultats dépendent de la figure de la terre", *Mém. Acad. Roy. Sci. Paris* (1787, publ. 1789), 352–383 ([scan](https://books.google.com/books?id=0uIEAAAAQAAJ&pg=PA352)).
- Delambre, J.-B. J. & Legendre, A.-M., *Méthodes analytiques pour la détermination d'un arc du méridien*, Paris: Crapelet, An VII (1798–99) ([scan](https://books.google.com/books?id=DBAOAAAAQAAJ)).
- Obituary of Legendre, *Journal of the Royal Astronomical Society* 3:4 (1834), 24–26 ([MacTutor](https://mathshistory.st-andrews.ac.uk/Obituaries/Legendre_RAS/)).
- Bertrand, J., "Démonstration d'un théorème de M. Gauss", *J. Math. Pures Appl.* (1) 13 (1848), 80–82 ([Numdam](https://www.numdam.org/item/JMPA_1848_1_13__80_0/)); Puiseux, V., "Sur le même théorème", ibid., 87 ([Numdam](https://www.numdam.org/item/JMPA_1848_1_13__87_0/)).
- Reventós, A. & Rodríguez, C., *L'Esfera Imaginària: comentaris al Disquisitiones*, Societat Catalana de Matemàtiques, 2004 ([PDF](https://mat.uab.cat/~agusti/esferaImaginaria.pdf)), pp. 14–18, 61–62.
- Merker, J., "Le Theorema Egregium de Gauss", [arXiv:1402.1018](https://arxiv.org/abs/1402.1018).
- Petrunin, A. & Zamora Barrera, S., *What is differential geometry: curves and surfaces*, [arXiv:2012.11814](https://arxiv.org/abs/2012.11814), Theorem 16.14.
- Gouvêa, F. Q., review of Gauss, *General Investigations of Curved Surfaces*, ed. P. Pesic (Dover, 2005), [MAA Reviews](https://old.maa.org/node/105949).
- Etymology: [Etymonline, "egregious"](https://www.etymonline.com/word/egregious) and ["theorem"](https://www.etymonline.com/word/theorem); Lanczos (1970) on the name, via [That's Maths](https://thatsmaths.com/2018/12/27/gaussian-curvature-the-theorema-egregium/).
