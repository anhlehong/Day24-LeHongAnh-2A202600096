# src/phase_a/ragas_evaluator.py
"""RAGAS evaluation pipeline for RAG systems."""
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset
import pandas as pd
import json


def evaluate_rag_pipeline(test_df, rag_pipeline_fn=None):
    """
    Evaluate RAG pipeline using RAGAS metrics.
    rag_pipeline_fn: callable that takes question returns (answer, contexts)
    """
    dataset = Dataset.from_list(test_df.to_dict('records'))

    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ChatOpenAI(model="gpt-4o-mini")
    )
    return scores


def save_results(scores, results_path="ragas_results.csv", summary_path="ragas_summary.json"):
    """Save evaluation results to CSV and JSON."""
    scores.to_pandas().to_csv(results_path, index=False)
    summary = {k: float(scores[k]) for k in scores.keys()}
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    return results_path, summary_path