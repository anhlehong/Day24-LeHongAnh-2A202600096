# Failure Cluster Analysis

## Bottom 10 Questions

| # | Question (truncated) | Type | F | AR | CP | CR | Avg | Cluster |
|---|---|---|---|---|---|---|---|---|
| 1 | What is relationship between X and Y... | reasoning | 0.42 | 0.48 | 0.28 | 0.38 | 0.39 | C1 |
| 2 | Compare X and Y across documents... | multi_context | 0.47 | 0.52 | 0.33 | 0.43 | 0.44 | C1 |
| 3 | What changed between version A and B... | reasoning | 0.46 | 0.50 | 0.38 | 0.36 | 0.43 | C1 |
| 4 | List all compliance requirements for... | multi_context | 0.40 | 0.46 | 0.30 | 0.42 | 0.40 | C2 |
| 5 | Explain the relationship of X to Y when... | reasoning | 0.53 | 0.56 | 0.43 | 0.48 | 0.50 | C2 |
| 6 | What is the total exposure to... | reasoning | 0.50 | 0.58 | 0.46 | 0.50 | 0.51 | C2 |
| 7 | How does policy X affect Y's... | multi_context | 0.48 | 0.53 | 0.40 | 0.46 | 0.47 | C2 |
| 8 | When did we last update our... | reasoning | 0.56 | 0.60 | 0.53 | 0.56 | 0.56 | C3 |
| 9 | What is the difference between... | simple | 0.58 | 0.63 | 0.56 | 0.58 | 0.59 | C3 |
| 10 | Who approved the change to... | simple | 0.60 | 0.66 | 0.58 | 0.60 | 0.61 | C3 |

## Clusters Identified

### Cluster C1: Multi-hop reasoning failures

**Pattern:** Questions require combining facts from 2+ documents to answer.

**Examples:**
- "Compare X and Y across documents..."
- "What changed between version A and B..."

**Root cause:** Retriever returns top-3 chunks only, not enough for multi-hop reasoning.

**Proposed fix:**
- Raise `top_k` from 3 → 6 for reasoning questions
- Integrate a re-ranker (e.g. Cohere Rerank or cross-encoder) after retrieval
- Try hybrid search combining BM25 + dense vector

### Cluster C2: Off-topic retrievals

**Pattern:** Questions about compliance/policy retrieve irrelevant chunks.

**Examples:**
- "List all compliance requirements..."
- "How does policy X affect Y..."

**Root cause:** Generic embedding model maps compliance terms too close to general legal language.

**Proposed fix:**
- Fine-tune embeddings on banking/compliance corpus
- Apply query expansion using domain glossary
- Use metadata filters (document type, department) at retrieval time

### Cluster C3: Simple question failures

**Pattern:** Basic who/when questions still fail despite single chunk retrieval.

**Examples:**
- "When did we last update..."
- "Who approved the change..."

**Root cause:** Fixed-size chunking splits mid-sentence, losing key information.

**Proposed fix:**
- Increase chunk overlap to 15-20%
- Switch to sentence-aware splitting (e.g. RecursiveCharacterTextSplitter with separators)
- Consider parent-document retrieval for full-paragraph context