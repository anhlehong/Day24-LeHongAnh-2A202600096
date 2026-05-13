# src/phase_c/topic_guard.py
"""Topic-scope guardrail using embedding cosine similarity."""
from langchain_openai import OpenAIEmbeddings
import numpy as np
from typing import Tuple


class TopicGuard:
    """Validates whether user query falls within allowed topics."""

    def __init__(self, allowed_topics: list[str]):
        self.embeddings = OpenAIEmbeddings()
        self.topic_vectors = [self.embeddings.embed_query(t) for t in allowed_topics]
        self.topics = allowed_topics

    def check(self, text: str, threshold: float = 0.55) -> Tuple[bool, str]:
        """Return (is_on_topic, explanation) based on cosine similarity."""
        q_vec = self.embeddings.embed_query(text)
        sims = [
            np.dot(q_vec, tv) / (np.linalg.norm(q_vec) * np.linalg.norm(tv))
            for tv in self.topic_vectors
        ]
        max_sim = max(sims)
        best_topic = self.topics[sims.index(max_sim)]

        if max_sim > threshold:
            return True, f"On topic: {best_topic}"
        return False, f"Off topic. Closest: {best_topic} ({max_sim:.2f})"

    def check_llm(self, text: str, llm, allowed_topics: list[str]) -> bool:
        """LLM-based topic check (alternative method)."""
        from langchain.prompts import PromptTemplate
        prompt = PromptTemplate.from_template(
            "Is this question about one of these topics: {topics}?\nQuestion: {text}\nAnswer YES or NO only."
        )
        response = llm.invoke(prompt.format(topics=allowed_topics, text=text)).content.strip()
        return response.upper().startswith("YES")