# Lab 24 Prompts Used

## Phase A: RAGAS Test Set Generation
```python
# TestsetGenerator config:
generator_llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
critic_llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25}
test_size=50
```

## Phase B: LLM-as-Judge

### Pairwise Judge Prompt
```
You are a fair and neutral judge. Given a question and two candidate answers, determine which answer is better.
Question: {question}
Answer A: {answer_a}
Answer B: {answer_b}
Evaluate on: correctness, relevance, and brevity.
Return JSON only: {"winner": "A" or "B" or "tie", "reason": "..."}
```

### Absolute Scoring Rubric
```
Rate the following answer on 4 criteria, each on a 1-5 scale:
1. Correctness (1=incorrect, 5=completely accurate)
2. Relevance (1=unrelated, 5=directly addresses the question)
3. Brevity (1=too long, 5=concise and clear)
4. Usefulness (1=not helpful, 5=very actionable)
Question: {question}
Answer: {answer}
Return JSON only: {"accuracy": int, "relevance": int, "conciseness": int, "helpfulness": int, "overall": float}
```

## Phase C: Guardrails

### Topic Validator (Option 1 - Embedding Similarity)
Cosine similarity between query embedding and allowed topic embeddings, threshold=0.55

### Llama Guard 3 (API Mode)
Groq API inference with llama-guard-3-8b for safety classification