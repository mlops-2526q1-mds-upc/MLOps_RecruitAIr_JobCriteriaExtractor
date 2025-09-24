#!/usr/bin/env python3
"""
Preprocess match_X.json / mismatch_X.json JSONs into Parquet + JSON files.

Defaults:
 - input dir:  data/raw/raw_jsons
 - output dir: data/processed
 - output parquet: data/processed/preprocessed_resumes.parquet
 - output json:    data/processed/preprocessed_resumes.json

Columns:
 - resume (str)
 - job_description (str)
 - score (float, may be NaN)
 - match (int: 1=match, 0=mismatch)
"""

import os
import re
import json
import math
import argparse
import sys
from typing import Optional, Tuple, List

import pandas as pd

FNAME_RE = re.compile(r'^(?P<label>match|mismatch)_(?P<num>\d+)\.json$', re.IGNORECASE)


def find_target_json_files(input_dir: str) -> List[str]:
    matches = []
    for root, _, files in os.walk(input_dir):
        for fn in files:
            if FNAME_RE.match(fn):
                matches.append(os.path.join(root, fn))
    return sorted(matches)


def extract_text(d: dict, path: List[str]) -> Optional[str]:
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def compute_score_from_aggregated(agg: dict) -> Optional[float]:
    if not isinstance(agg, dict):
        return None
    macro = agg.get("macro_scores")
    micro = agg.get("micro_scores")
    vals = []
    if isinstance(macro, (int, float)):
        vals.append(float(macro))
    if isinstance(micro, (int, float)):
        vals.append(float(micro))
    return sum(vals) / len(vals) if vals else None


def avg_of_scores_list(scores_list) -> Optional[float]:
    if not isinstance(scores_list, list) or not scores_list:
        return None
    vals = []
    for el in scores_list:
        if isinstance(el, dict) and "score" in el:
            try:
                v = float(el["score"])
                if math.isfinite(v):
                    vals.append(v)
            except Exception:
                continue
    return sum(vals) / len(vals) if vals else None


def compute_score(output: dict) -> Optional[float]:
    if not isinstance(output, dict):
        return None
    scores = output.get("scores") or {}
    agg = scores.get("aggregated_scores")
    s = compute_score_from_aggregated(agg)
    if s is not None:
        return s
    macro_avg = avg_of_scores_list(scores.get("macro_scores"))
    micro_avg = avg_of_scores_list(scores.get("micro_scores"))
    vals = [v for v in (macro_avg, micro_avg) if v is not None]
    return sum(vals) / len(vals) if vals else None


def process_file(path: str) -> Optional[Tuple[str, str, Optional[float], int]]:
    fn = os.path.basename(path)
    m = FNAME_RE.match(fn)
    if not m:
        return None
    label = m.group("label").lower()
    match_flag = 1 if label == "match" else 0

    try:
        with open(path, "r", encoding="utf-8") as fh:
            obj = json.load(fh)
    except Exception as e:
        print(f"WARNING: Failed to parse {path}: {e}", file=sys.stderr)
        return None

    resume = extract_text(obj, ["input", "resume"]) or ""
    job_description = extract_text(obj, ["input", "job_description"]) or ""
    score = compute_score(obj.get("output"))

    return (resume.strip(), job_description.strip(), score, match_flag)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def main():
    p = argparse.ArgumentParser(description="Preprocess resume JSONs into Parquet + JSON")
    p.add_argument("--input-dir", "-i", default="data/raw/raw_jsons",
                   help="Directory containing JSON files (default: data/raw/raw_jsons)")
    p.add_argument("--output-dir", "-d", default="data/processed",
                   help="Directory for processed outputs (default: data/processed)")
    p.add_argument("--output-parquet", default=None,
                   help="Output Parquet file (default: data/processed/preprocessed_resumes.parquet)")
    p.add_argument("--output-json", default=None,
                   help="Output JSON file (default: data/processed/preprocessed_resumes.json)")
    args = p.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    out_parquet = args.output_parquet or os.path.join(output_dir, "preprocessed_resumes.parquet")
    out_json = args.output_json or os.path.join(output_dir, "preprocessed_resumes.json")

    if not os.path.isdir(input_dir):
        print(f"ERROR: input directory does not exist: {input_dir}", file=sys.stderr)
        sys.exit(2)

    files = find_target_json_files(input_dir)
    if not files:
        print(f"No files matching match_X.json or mismatch_X.json found under {input_dir}", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(files)} JSON files. Processing...")

    rows = []
    for idx, fp in enumerate(files, start=1):
        res = process_file(fp)
        if res is not None:
            rows.append(res)
        if idx % 100 == 0 or idx == len(files):
            print(f"Progress: {idx}/{len(files)} processed.")

    df = pd.DataFrame(rows, columns=["resume", "job_description", "score", "match"])

    ensure_dir(output_dir)
    df.to_parquet(out_parquet, index=False)
    df.to_json(out_json, orient="records", lines=False, force_ascii=False, indent=2)

    print(f"✅ Done. {len(df)} rows written to:")
    print(f" - Parquet: {out_parquet}")
    print(f" - JSON:    {out_json}")


if __name__ == "__main__":
    main()