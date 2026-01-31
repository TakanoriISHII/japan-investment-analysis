#!/usr/bin/env python3
"""
validate_scores.py - 5軸スコアリングフレームワーク自動検証スクリプト
Usage: python scripts/validate_scores.py [--file PATH] [--strict]

Graham分類体系統合版 v2.0.0/v3.0.0 準拠
"""

import json
import sys
import os
from pathlib import Path

# 5-axis maximum scores
AXIS_LIMITS = {
    "structural_advantage": 20,
    "intrinsic_value": 20,
    "future_value": 25,
    "information_asymmetry": 20,
    "policy_catalyst": 15
}

INVESTMENT_AXES = ["structural_advantage", "intrinsic_value"]
SPECULATIVE_AXES = ["future_value", "information_asymmetry", "policy_catalyst"]
MAX_INVESTMENT = 40
MAX_SPECULATIVE = 60
MAX_TOTAL = 100

VALID_QUADRANTS = {"prime", "stable", "stable_growth", "speculative", "avoid"}
VALID_CONFIDENCE = {"A", "A+", "A-", "B", "B+", "B-", "C", "C+", "C-", "D", "E"}

# Deprecated field names (should NOT exist)
DEPRECATED_FIELDS = {"monopoly", "resilience", "synergy", "asymmetry", "capital",
                     "monopoly_score", "capital_efficiency"}


def find_top30_file():
    """Auto-detect the top30 file based on current directory."""
    candidates = [
        "data/analysis/japan_top30.json",
        "data/analysis/top30.json",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def validate_company(company, strict=False):
    """Validate a single company's scoring data."""
    errors = []
    warnings = []

    ticker = company.get("ticker", "UNKNOWN")
    rank = company.get("rank", "?")
    prefix = f"Rank {rank} ({ticker})"

    # 1. Check required fields
    required_top = ["rank", "ticker", "total", "investment_factors", "speculative_factors"]
    for field in required_top:
        if field not in company:
            errors.append(f"{prefix}: Missing required field '{field}'")

    # Check for scores object
    scores = company.get("scores", {})

    # 2. Axis score validation
    for axis, max_val in AXIS_LIMITS.items():
        if axis in scores:
            score_obj = scores[axis]
            score = score_obj.get("score", 0) if isinstance(score_obj, dict) else score_obj
            if score < 0:
                errors.append(f"{prefix}: {axis} score {score} is negative")
            if score > max_val:
                errors.append(f"{prefix}: {axis} score {score} exceeds max {max_val}")

            # Confidence check
            if isinstance(score_obj, dict):
                conf = score_obj.get("confidence", "")
                if conf and conf not in VALID_CONFIDENCE:
                    warnings.append(f"{prefix}: {axis} confidence '{conf}' not in standard set")
        elif strict:
            errors.append(f"{prefix}: Missing axis score '{axis}'")

    # 3. Investment/Speculative sum validation
    inv = company.get("investment_factors", 0)
    spec = company.get("speculative_factors", 0)
    total = company.get("total", 0)

    if inv > MAX_INVESTMENT:
        errors.append(f"{prefix}: investment_factors {inv} exceeds max {MAX_INVESTMENT}")
    if spec > MAX_SPECULATIVE:
        errors.append(f"{prefix}: speculative_factors {spec} exceeds max {MAX_SPECULATIVE}")
    if total > MAX_TOTAL:
        errors.append(f"{prefix}: total {total} exceeds max {MAX_TOTAL}")

    # 4. Sum consistency
    if inv + spec != total:
        errors.append(f"{prefix}: investment({inv}) + speculative({spec}) = {inv+spec} != total({total})")

    # Axis sum vs investment/speculative
    if scores:
        calc_inv = sum(
            (scores[a].get("score", 0) if isinstance(scores[a], dict) else scores[a])
            for a in INVESTMENT_AXES if a in scores
        )
        calc_spec = sum(
            (scores[a].get("score", 0) if isinstance(scores[a], dict) else scores[a])
            for a in SPECULATIVE_AXES if a in scores
        )
        if calc_inv != inv:
            warnings.append(f"{prefix}: Calculated investment({calc_inv}) != stated({inv})")
        if calc_spec != spec:
            warnings.append(f"{prefix}: Calculated speculative({calc_spec}) != stated({spec})")

    # 5. Quadrant validation
    quadrant = company.get("quadrant", "")
    if quadrant and quadrant not in VALID_QUADRANTS:
        warnings.append(f"{prefix}: Quadrant '{quadrant}' not in standard set")

    # 6. Deprecated fields check
    for dep in DEPRECATED_FIELDS:
        if dep in company:
            errors.append(f"{prefix}: Deprecated field '{dep}' found (should be removed)")
        if dep in scores:
            errors.append(f"{prefix}: Deprecated score '{dep}' found (should be removed)")

    # 7. Graham-Buffett note
    if "graham_buffett_note" not in company and strict:
        warnings.append(f"{prefix}: Missing graham_buffett_note")

    # 8. Confidence summary
    if "confidence" not in company and strict:
        warnings.append(f"{prefix}: Missing confidence summary")

    return errors, warnings


def validate_metadata(data):
    """Validate the metadata section."""
    errors = []
    meta = data.get("metadata", {})

    if not meta:
        errors.append("Missing metadata section")
        return errors

    # Check Graham classification
    graham = meta.get("graham_classification", {})
    axes = meta.get("axes", {})

    if axes:
        for axis_name, max_val in AXIS_LIMITS.items():
            if axis_name in axes:
                stated_max = axes[axis_name].get("max", 0)
                if stated_max != max_val:
                    errors.append(f"Metadata: {axis_name} max stated as {stated_max}, expected {max_val}")

    return errors


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate 5-axis scoring framework")
    parser.add_argument("--file", "-f", help="Path to top30.json file")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation")
    args = parser.parse_args()

    filepath = args.file or find_top30_file()
    if not filepath or not os.path.exists(filepath):
        print(f"ERROR: Cannot find top30 file. Use --file to specify path.")
        sys.exit(1)

    print(f"Validating: {filepath}")
    print(f"Mode: {'STRICT' if args.strict else 'STANDARD'}")
    print("=" * 60)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_errors = []
    all_warnings = []

    # Metadata validation
    meta_errors = validate_metadata(data)
    all_errors.extend(meta_errors)

    # Find companies list
    companies = data.get("top30", data.get("japan_top30", []))
    if not companies:
        # Try snapshot format
        companies = data.get("top30_rankings", [])

    if not companies:
        print("ERROR: No companies found in file")
        sys.exit(1)

    print(f"Companies found: {len(companies)}")
    print()

    # Validate each company
    for company in companies:
        errors, warnings = validate_company(company, strict=args.strict)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    # Print results
    if all_errors:
        print("ERRORS:")
        for e in all_errors:
            print(f"  [FAIL] {e}")
        print()

    if all_warnings:
        print("WARNINGS:")
        for w in all_warnings:
            print(f"  [WARN] {w}")
        print()

    # Summary
    print("=" * 60)
    print(f"Total companies: {len(companies)}")
    print(f"Errors: {len(all_errors)}")
    print(f"Warnings: {len(all_warnings)}")

    if len(all_errors) == 0:
        print("\n✓ VALIDATION PASSED")
        sys.exit(0)
    else:
        print("\n✗ VALIDATION FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
