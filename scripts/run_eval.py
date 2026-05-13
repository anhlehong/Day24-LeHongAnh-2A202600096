# scripts/run_eval.py
"""Evaluation script for CI/CD gate."""
import argparse
import json
import sys


def run_eval_with_threshold(thresholds: dict):
    """
    Run RAGAS evaluation with threshold checks.
    Exit 1 if any metric is below threshold.
    """
    try:
        with open('ragas_summary.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        print("ERROR: ragas_summary.json not found")
        sys.exit(1)

    failed = []
    for metric, threshold in thresholds.items():
        if metric in scores:
            if scores[metric] < threshold:
                failed.append(f"{metric}: {scores[metric]:.3f} < {threshold}")

    if failed:
        print("EVALUATION FAILED - Metrics below threshold:")
        for f in failed:
            print(f"  - {f}")
        sys.exit(1)

    print("EVALUATION PASSED")
    print(json.dumps(scores, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run RAGAS evaluation with threshold gate')
    parser.add_argument('--threshold', action='append',
                       help='Threshold in format metric=value, e.g., faithfulness=0.85')
    args = parser.parse_args()

    thresholds = {}
    if args.threshold:
        for t in args.threshold:
            if '=' in t:
                metric, value = t.split('=')
                thresholds[metric] = float(value)

    run_eval_with_threshold(thresholds)