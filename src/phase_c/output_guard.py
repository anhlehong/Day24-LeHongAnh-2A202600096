# src/phase_c/output_guard.py
"""Output-layer safety check powered by Llama Guard 3 (local or API)."""
import torch
import time
from typing import Tuple, Dict
import requests


class OutputGuard:
    """Safety classifier for RAG output using Llama Guard 3."""

    def __init__(self, use_api=False, api_key=None, model_id="meta-llama/Llama-Guard-3-8B"):
        self.use_api = use_api
        self.api_key = api_key
        self.model_id = model_id

        if not use_api:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, torch_dtype=torch.bfloat16, device_map="auto"
            )

    def check(self, user_input: str, agent_response: str) -> Tuple[bool, str, float]:
        """Classify response safety. Returns (is_safe, raw_result, latency_ms)."""
        if self.use_api:
            return self._check_api(user_input, agent_response)
        return self._check_local(user_input, agent_response)

    def _check_local(self, user_input: str, agent_response: str) -> Tuple[bool, str, float]:
        """Local inference with Llama Guard."""
        from transformers import AutoTokenizer, AutoModelForCausalLM

        chat = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": agent_response}
        ]
        input_ids = self.tokenizer.apply_chat_template(chat, return_tensors="pt").to(self.model.device)

        start = time.perf_counter()
        output = self.model.generate(input_ids=input_ids, max_new_tokens=100, pad_token_id=0)
        latency_ms = (time.perf_counter() - start) * 1000

        result = self.tokenizer.decode(output[0][input_ids.shape[-1]:])
        is_safe = "safe" in result.lower() and "unsafe" not in result.lower()

        return is_safe, result, latency_ms

    def _check_api(self, user_input: str, agent_response: str) -> Tuple[bool, str, float]:
        """API-based inference (Groq)."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": "llama-guard-3-8b",
            "messages": [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": agent_response}
            ]
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        start = time.perf_counter()
        resp = requests.post(url, json=payload, headers=headers)
        latency_ms = (time.perf_counter() - start) * 1000

        result = resp.json()['choices'][0]['message']['content']
        is_safe = "safe" in result.lower() and "unsafe" not in result.lower()

        return is_safe, result, latency_ms