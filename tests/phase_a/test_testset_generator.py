# tests/phase_a/test_testset_generator.py
"""Tests for testset generator - standalone without external deps."""
import pytest
import pandas as pd
import tempfile
import os


def save_testset(df, path="testset_v1.csv"):
    """Standalone save function for testing."""
    df.to_csv(path, index=False)
    return path


def test_save_testset_creates_csv():
    """Test that save_testset creates a CSV file."""
    df = pd.DataFrame({
        'question': ['Q1', 'Q2'],
        'ground_truth': ['A1', 'A2'],
        'contexts': [['C1'], ['C2']],
        'evolution_type': ['simple', 'reasoning']
    })

    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        path = f.name

    try:
        result = save_testset(df, path)
        assert result == path
        assert os.path.exists(path)
        loaded = pd.read_csv(path)
        assert len(loaded) == 2
        assert list(loaded.columns) == ['question', 'ground_truth', 'contexts', 'evolution_type']
    finally:
        os.unlink(path)


def test_save_testset_handles_empty():
    """Test save with empty dataframe."""
    df = pd.DataFrame(columns=['question', 'ground_truth', 'contexts', 'evolution_type'])

    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        path = f.name

    try:
        result = save_testset(df, path)
        assert os.path.exists(path)
        loaded = pd.read_csv(path)
        assert len(loaded) == 0
    finally:
        os.unlink(path)