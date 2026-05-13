# src/phase_a/testset_generator.py
"""Synthetic test set generator for RAG evaluation."""
from ragas.testset import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pandas as pd


def load_documents(path="./docs", glob="**/*.md"):
    """Load documents from directory."""
    loader = DirectoryLoader(path, glob=glob)
    return loader.load()


def generate_testset(documents, test_size=50, distributions=None):
    """Generate test set with specified distribution."""
    if distributions is None:
        distributions = {simple: 0.5, reasoning: 0.25, multi_context: 0.25}

    generator = TestsetGenerator.from_langchain(
        generator_llm=ChatOpenAI(model="gpt-4o-mini"),
        critic_llm=ChatOpenAI(model="gpt-4o-mini"),
        embeddings=OpenAIEmbeddings(),
    )

    testset = generator.generate_with_langchain_docs(
        documents=documents,
        test_size=test_size,
        distributions=distributions
    )

    return testset.to_pandas()


def save_testset(df, path="testset_v1.csv"):
    """Save test set to CSV."""
    df.to_csv(path, index=False)
    return path