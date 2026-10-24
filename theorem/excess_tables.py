"""Reproduce the Earth-scale tables on the Theorema Egregium background page.

Spherical model with the Gaussian mean radius R_G = sqrt(M N) of the WGS84 ellipsoid.
  - spherical excess of an equilateral triangle: eps = A / R_G^2  (arcsec)
  - circumference deficit of a geodesic circle: 2 pi r - C ~ (pi/3) K r^3,
    relative deficit ~ K r^2 / 6  (leading term of Bertrand-Diguet-Puiseux)
Writes excess_tables.json and excess_tables.csv next to this script.
"""
import csv, json, math, pathlib

A_WGS84 = 6378.137            # km
F_WGS84 = 1 / 298.257223563
E2 = F_WGS84 * (2 - F_WGS84)
RHO = 180 / math.pi * 3600    # arcsec per radian

def gauss_radius(lat_deg):
    s = math.sin(math.radians(lat_deg)) ** 2
    M = A_WGS84 * (1 - E2) / (1 - E2 * s) ** 1.5
    N = A_WGS84 / math.sqrt(1 - E2 * s)
    return math.sqrt(M * N)

def heron(a, b, c):
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))

LAT = 50.2                    # Nanton, AB
RG = gauss_radius(LAT)
K = 1 / RG ** 2               # km^-2

out = {"lat_deg": LAT, "R_G_km": round(RG, 1),
       "R_G_range_km": [round(gauss_radius(0), 1), round(gauss_radius(90), 1)],
       "excess": [], "circle": []}
rows = []
for side in (10, 30, 55, 100):
    A = math.sqrt(3) / 4 * side ** 2
    eps = A * K * RHO
    out["excess"].append({"side_km": side, "area_km2": round(A, 1), "eps_arcsec": round(eps, 3)})
    rows.append(["excess", f"equilateral {side} km", round(A, 1), round(eps, 3), ""])

# Inselsberg-Brocken-Hohenhagen, rounded sides, R_G at 51.5 N
a, b, c = 69, 85, 107
A = heron(a, b, c)
eps = A / gauss_radius(51.5) ** 2 * RHO
out["gauss_triangle"] = {"sides_km": [a, b, c], "area_km2": round(A, 1), "eps_arcsec": round(eps, 2)}
rows.append(["excess", "Gauss triangle 69/85/107 km", round(A, 1), round(eps, 2), ""])

for r in (1, 10, 25, 55):
    d_m = math.pi / 3 * K * r ** 3 * 1000
    ppm = K * r ** 2 / 6 * 1e6
    out["circle"].append({"r_km": r, "deficit_m": round(d_m, 6), "ppm": round(ppm, 3)})
    rows.append(["circle", f"geodesic radius {r} km", "", round(d_m, 6), round(ppm, 3)])

here = pathlib.Path(__file__).parent
(here / "excess_tables.json").write_text(json.dumps(out, indent=2) + "\n")
with open(here / "excess_tables.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["table", "case", "area_km2", "excess_arcsec_or_deficit_m", "relative_deficit_ppm"])
    w.writerows(rows)
print(json.dumps(out, indent=2))
