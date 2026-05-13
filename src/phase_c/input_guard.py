# src/phase_c/input_guard.py
"""Input-layer guardrails: detect and redact PII from user queries."""
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import re
import time
from typing import Tuple, Dict

VN_PII = {
    "cccd": r"\b\d{12}\b",
    "phone_vn": r"(\+84|0)\d{9,10}",
    "tax_code": r"\b\d{10}(-\d{3})?\b",
    "email": r"\b[\w.-]+@[\w.-]+\.\w+\b",
}


class InputGuard:
    """Dual-layer PII guard: VN regex patterns + Presidio NER."""

    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.vn_patterns = VN_PII

    def scrub_vn(self, text: str) -> str:
        """First pass: Vietnamese PII patterns (CCCD, phone, tax, email)."""
        for name, pattern in self.vn_patterns.items():
            text = re.sub(pattern, f"[{name.upper()}]", text)
        return text

    def scrub_ner(self, text: str) -> str:
        """Second pass: Presidio NER engine for English entities."""
        results = self.analyzer.analyze(text=text, language="en")
        return self.anonymizer.anonymize(text=text, analyzer_results=results).text

    def sanitize(self, text: str) -> Tuple[str, float]:
        """Run full PII pipeline and return (clean_text, latency_ms)."""
        start = time.perf_counter()
        out = self.scrub_ner(self.scrub_vn(text))
        latency_ms = (time.perf_counter() - start) * 1000
        return out, latency_ms

    def detect_pii(self, text: str) -> Dict[str, int]:
        """Detect PII types in text."""
        counts = {}
        for name, pattern in self.vn_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                counts[name] = len(matches)

        # Presidio NER
        results = self.analyzer.analyze(text=text, language="en")
        for r in results:
            entity_type = r.entity_type
            counts[entity_type] = counts.get(entity_type, 0) + 1

        return counts