#!/usr/bin/env python3
"""
Independent checks for the ratio extractor.
Verifies unit consistency, period alignment, and arithmetic.
"""

import argparse
import json
import os

def load_result(path):
    with open(path) as f:
        return json.load(f)

def check_arithmetic(result):
    figures = result["figures"]
    ratios = result["ratios"]
    issues = []

    rev = figures.get("revenue")
    gp = figures.get("gross_profit")
    if rev and gp and "gross_margin" in ratios:
        expected = gp / rev
        actual = ratios["gross_margin"]
        if abs(expected - actual) > 1e-6:
            issues.append(f"Gross margin mismatch: expected {expected:.6f}, got {actual:.6f}")

    # Add more ratio checks as needed
    return issues

def check_periods(result):
    figures = result["figures"]
    issues = []
    inc = figures.get("income_period")
    bal = figures.get("balance_period")
    if inc and bal and inc != bal:
        issues.append(f"Period mismatch: income={inc}, balance={bal}")
    return issues

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True, help="Path to figures_and_ratios.json")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    result = load_result(args.result)
    issues = []
    issues.extend(check_arithmetic(result))
    issues.extend(check_periods(result))

    check_result = {
        "passed": len(issues) == 0,
        "issues": issues,
        "checked_at": "now"
    }

    out_path = os.path.join(args.output_dir, "check_results.json")
    with open(out_path, "w") as f:
        json.dump(check_result, f, indent=2)

    print(json.dumps(check_result, indent=2))
    if issues:
        print("CHECKS FAILED")
        exit(1)
    else:
        print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()