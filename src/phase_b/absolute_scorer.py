# src/phase_b/absolute_scorer.py
"""Multi-dimensional absolute scoring rubric for RAG answers."""
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json
import pandas as pd

ABSOLUTE_PROMPT = PromptTemplate.from_template("""
Rate the following answer on 4 criteria, each on a 1-5 scale:
1. Correctness (1=incorrect, 5=completely accurate)
2. Relevance (1=unrelated, 5=directly addresses the question)
3. Brevity (1=too long, 5=concise and clear)
4. Usefulness (1=not helpful, 5=very actionable)
Question: {question}
Answer: {answer}
Return JSON only: {{"accuracy": int, "relevance": int, "conciseness": int, "helpfulness": int, "overall": float}}
""")


def parse_judge_output(text):
    """Parse scoring JSON, return default mid-scores on failure."""
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        return {"accuracy": 3, "relevance": 3, "conciseness": 3, "helpfulness": 3, "overall": 3.0}


def absolute_score(question, answer, judge_llm):
    """Score one answer using the 4-criteria rubric."""
    prompt = ABSOLUTE_PROMPT.format(question=question, answer=answer)
    out = judge_llm.invoke(prompt)
    parsed = parse_judge_output(out.content)

    # Compute overall as average if not provided
    if 'overall' not in parsed:
        dims = ['accuracy', 'relevance', 'conciseness', 'helpfulness']
        parsed['overall'] = sum(parsed.get(d, 3) for d in dims) / 4

    return parsed


def run_absolute_scoring(questions, answers, judge_llm):
    """Run absolute scoring on multiple Q&A pairs."""
    results = []
    for q, a in zip(questions, answers):
        scores = absolute_score(q, a, judge_llm)
        scores['question'] = q
        scores['answer'] = a
        results.append(scores)
    return pd.DataFrame(results)