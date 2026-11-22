"""Deterministic midpoint integration of a centered Gaussian over a disk, w=1."""
import json
from math import exp, expm1, fsum


def enclosed(radius, intervals):
    step = radius / intervals
    points = ((i + 0.5) * step for i in range(intervals))
    return step * fsum(4 * r * exp(-2 * r * r) for r in points)


if __name__ == "__main__":
    rows = []
    for radius in (0.5, 1.0):
        exact = -expm1(-2 * radius * radius)
        for n in (32, 64, 128):
            estimate = enclosed(radius, n)
            rows.append({"a_over_w": radius, "intervals": n, "numeric": estimate,
                         "exact": exact, "absolute_error": abs(estimate - exact)})
    small, large = [row for row in rows if row["intervals"] == 128]
    difference = large["numeric"] - small["numeric"]
    exact_difference = large["exact"] - small["exact"]
    rows.append({"kind": "between_apertures", "numeric_difference": difference,
                 "analytic_difference": exact_difference,
                 "difference_error": abs(difference - exact_difference),
                 "error_bound": large["absolute_error"] + small["absolute_error"]})
    print(json.dumps(rows, indent=2))
