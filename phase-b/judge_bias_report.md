# Judge Bias Report

## Bias 1: Position Bias

**Analysis:** How often does A win when listed first?

| Metric | Value |
|--------|-------|
| A wins as first | 17/30 = 57% |
| Expected (no bias) | ~50% |
| Bias direction | First-listed answer preferred |

**Conclusion:** Moderate position bias detected. The first-listed answer is chosen 57% of the time vs expected 50%.

**Mitigation:** Swap-and-average technique halves this bias. A larger calibration set (50+ pairs) would help quantify residual bias.

## Bias 2: Length Bias

**Analysis:** Correlation between answer length and judge preference.

| Metric | Value |
|--------|-------|
| B wins when longer | 11/15 = 73% |
| B wins when shorter | 5/15 = 33% |
| Length correlation | Moderate-to-strong |

**Conclusion:** Longer answers tend to win, particularly when significantly more detailed than the other.

**Mitigation:** Truncate or normalize answer length before judging, or explicitly add a "penalize verbosity" instruction in the prompt.

## Bias Mitigation Applied

1. **Swap-and-average:** Each pair judged twice in A-B then B-A order; second result is flipped before aggregation
2. **Brevity criterion:** Included in the 4-criteria absolute rubric to penalize unnecessary length
3. **Length-aware preprocessing:** Trim long answers before feeding to judge

## Recommendations

- Collect 50+ human labels for better calibration
- Experiment with explicit "penalize verbosity" in judge prompt
- Track additional biases over time (formatting, style, language)