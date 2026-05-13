# src/phase_b/calibration.py
"""Human calibration with Cohen's Kappa."""
from sklearn.metrics import cohen_kappa_score
import pandas as pd
import numpy as np


def compute_kappa(human_labels_path, judge_results_path):
    """Compute Cohen's kappa between human labels and judge."""
    human_df = pd.read_csv(human_labels_path)
    judge_df = pd.read_csv(judge_results_path)

    # Match by question_id or index
    human = human_df['human_winner'].tolist()
    judge = judge_df.head(len(human))['winner_after_swap'].tolist()

    kappa = cohen_kappa_score(human, judge)

    # Interpretation
    if kappa < 0:
        interpretation = "WORSE than chance - judge systematic error"
    elif kappa < 0.2:
        interpretation = "Slight agreement - not reliable"
    elif kappa < 0.4:
        interpretation = "Fair agreement - still weak"
    elif kappa < 0.6:
        interpretation = "Moderate agreement - can use for monitoring"
    elif kappa < 0.8:
        interpretation = "Substantial agreement - production-ready"
    else:
        interpretation = "Almost perfect agreement"

    return kappa, interpretation


def create_sample_for_labeling(pairwise_results_path, output_path, n=10, seed=42):
    """Create sample of n pairs for human labeling."""
    df = pd.read_csv(pairwise_results_path)
    sample = df.sample(n=min(n, len(df)), random_state=seed)
    sample[['question', 'answer_a', 'answer_b']].to_csv(output_path, index=False)
    return output_path