# src/phase_b/pairwise_judge.py
"""Pairwise comparison judge with position-bias mitigation via swap-and-average."""
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json
import pandas as pd

JUDGE_PROMPT = PromptTemplate.from_template("""
You are a fair and neutral judge. Given a question and two candidate answers, determine which answer is better.
Question: {question}
Answer A: {answer_a}
Answer B: {answer_b}
Evaluate on: correctness, relevance, and brevity.
Return JSON only: {{"winner": "A" or "B" or "tie", "reason": "..."}}
""")


def parse_judge_output(text):
    """Parse judge JSON output, fallback to tie on failure."""
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        return {"winner": "tie", "reason": "Parse error"}


def pairwise_judge_with_swap(question, ans1, ans2, judge_llm):
    """Run judge twice with swapped order to reduce position bias."""
    results = []

    # Run 1: ans1 first, ans2 second
    prompt = JUDGE_PROMPT.format(question=question, answer_a=ans1, answer_b=ans2)
    out = judge_llm.invoke(prompt)
    r1 = parse_judge_output(out.content)
    results.append(r1)

    # Run 2: swap order
    prompt = JUDGE_PROMPT.format(question=question, answer_a=ans2, answer_b=ans1)
    out = judge_llm.invoke(prompt)
    r2 = parse_judge_output(out.content)

    # Flip winner for run 2
    if r2['winner'] == 'A':
        r2['winner'] = 'B'
    elif r2['winner'] == 'B':
        r2['winner'] = 'A'
    results.append(r2)

    # Aggregate: both agree -> that. Disagree -> tie.
    if results[0]['winner'] == results[1]['winner']:
        return results[0]['winner']
    return 'tie'


def run_pairwise_evaluation(questions, answers_a, answers_b, judge_llm):
    """Run pairwise evaluation on multiple question pairs."""
    results = []
    for q, a, b in zip(questions, answers_a, answers_b):
        winner = pairwise_judge_with_swap(q, a, b, judge_llm)
        results.append({
            'question': q,
            'winner_after_swap': winner
        })
    return pd.DataFrame(results)