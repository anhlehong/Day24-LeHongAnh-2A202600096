# Lab 24 — Full Evaluation & Guardrail System

**Author:** Lê Hồng Anh — Student ID: 2A202600096

## Overview
Built production-ready evaluation and guardrail system for RAG pipeline. System measures RAG quality via RAGAS metrics, judges outputs with LLM-as-Judge (with bias mitigation), and deploys defense-in-depth guardrails (PII redaction, topic validation, Llama Guard 3). Complete stack integrates 4 layers with <50ms P95 latency on input guards.

## Setup

### Demo (không cần API key)
```
pip install streamlit pandas numpy
streamlit run streamlit_demo.py
```

### Chạy full evaluation (cần API key)
```
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...          # Required: dùng cho GPT-4o-mini (RAGAS + Judge)
# export HF_TOKEN=hf_...             # Optional: chỉ cần nếu chạy Llama Guard local (Read token)
python run_evaluations.py
```

## Results Summary

### Phase A (RAGAS) - 30 points
- Test set: 50 questions (50% simple, 25% reasoning, 25% multi-context)
- Faithfulness: 0.69 | AR: 0.74 | CP: 0.62 | CR: 0.68
- Total eval cost: ~$0.02
- Identified 3 failure clusters (see phase-a/failure_analysis.md)
- CI/CD gate: `.github/workflows/eval-gate.yml`

### Phase B (LLM-Judge) - 25 points
- Cohen's kappa vs human: 0.65 (substantial agreement)
- Position bias mitigated via swap-and-average (57% → ~50%)
- Length bias observed (B wins 73% when longer)
- 4 pairwise comparisons, 30 absolute scores

### Phase C (Guardrails) - 35 points
- PII detection rate: 90% (regex + Presidio dual-layer)
- Topic validator: embedding cosine similarity (threshold 0.55)
- Adversarial defense: 55% (11/20 attacks blocked)
- Llama Guard 3 latency P95: 45ms (Groq API)
- Full stack P95: <3.0s end-to-end

### Phase D (Blueprint) - 10 points
- 8 SLOs with alert thresholds and severity levels
- Architecture diagram with 4 layers (Mermaid)
- Alert playbook with 4 incident types
- Cost analysis: ~$46/month current, ~$480/month at 10x scale

## Architecture

```
User Input
  ↓
[L1] Input Guards (parallel)
  ├─ PII Redaction (Presidio + VN regex)
  ├─ Topic Validator (embedding similarity)
  └─ Injection Detection
  ↓
[L2] RAG Pipeline (Day 18)
  ↓
[L3] Output Guard (Llama Guard 3)
  ↓
[L4] Audit Log (async)
  ↓
Response
```

## Lessons Learned

1. **Evaluate first, guard second**: RAGAS metrics show where RAG fails — focus guardrail effort on the weakest points. No point guarding a broken system.

2. **LLM judges are biased**: Position bias (57%) and length bias (73%) are real. Swap-and-average helps but doesn't fully fix it. Always calibrate with human labels.

3. **Defense in depth works**: No single guard catches everything. Combining PII regex + Presidio NER + topic validation + Llama Guard gives layered protection.

## Demo Video
[Demo Video](https://drive.google.com/file/d/1PQ8tfSSlooeHCBLcuwtwB5jqF9lkPs6F/view?usp=sharing)

## Repository Structure
```
lab24-eval-guardrails/
├── README.md (this file)
├── requirements.txt
├── prompts.md
├── phase-a/ (RAGAS evaluation)
├── phase-b/ (LLM-as-Judge)
├── phase-c/ (Guardrails)
├── phase-d/ (Blueprint)
├── .github/workflows/
└── scripts/
```