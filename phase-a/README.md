# Phase A: RAGAS Evaluation

## testset_v1.csv
See: testset_v1.csv (50 questions with evolution_type)

## testset_review_notes.md
Manual review of 10 questions:
- Q3: Edited to be more specific about retention period
- Q12: Simplified complex multi-hop to single-hop
- Q23: Added domain context for finance banking
- Q31: Removed ambiguous reference
- Q42: Adjusted to match ground truth format
- Q8: Changed to Vietnamese context
- Q15: Added clarification on document scope
- Q27: Fixed entity reference
- Q38: Adjusted question length
- Q49: Corrected cross-document dependency

## ragas_summary.json
```json
{
  "faithfulness": 0.69,
  "answer_relevancy": 0.74,
  "context_precision": 0.62,
  "context_recall": 0.68
}
```

## failure_analysis.md
See: failure_analysis.md (bottom 10 + clusters)