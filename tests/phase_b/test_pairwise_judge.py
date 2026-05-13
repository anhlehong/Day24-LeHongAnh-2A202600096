# tests/phase_b/test_pairwise_judge.py
"""Tests for pairwise judge - standalone without external deps."""
import pytest
import json


def parse_judge_output(text):
    """Standalone parse function for testing."""
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        return {"winner": "tie", "reason": "Parse error"}


def test_parse_judge_output_valid_json():
    """Test JSON parsing with valid input."""
    result = parse_judge_output('{"winner": "A", "reason": "better"}')
    assert result['winner'] == 'A'
    assert result['reason'] == 'better'


def test_parse_judge_output_with_markdown():
    """Test JSON parsing with markdown fences."""
    result = parse_judge_output('```json\n{"winner": "B", "reason": "ok"}\n```')
    assert result['winner'] == 'B'
    assert result['reason'] == 'ok'


def test_parse_judge_output_invalid_json():
    """Test JSON parsing falls back to tie on invalid input."""
    result = parse_judge_output('not json at all')
    assert result['winner'] == 'tie'
    assert result['reason'] == 'Parse error'


def test_parse_judge_output_strips_whitespace():
    """Test that whitespace is stripped."""
    result = parse_judge_output('  {"winner": "A", "reason": "test"}  ')
    assert result['winner'] == 'A'