import pytest
from app.query_and_answer import search_legal_docs
from app.config import TOP_K, MAX_CONTEXT_CHARS

def test_search_returns_context_and_metadata():
    query = "What does the Constitution say about human rights?"
    context, metadata = search_legal_docs(query)
    assert isinstance(context, str)
    assert isinstance(metadata, dict)
    assert len(context) <= MAX_CONTEXT_CHARS
    assert len(metadata) <= TOP_K

def test_metadata_keys_are_titles():
    query = "Explain criminal procedure"
    _, metadata = search_legal_docs(query)
    for key in metadata:
        assert isinstance(key, str)
        assert "doc" in metadata[key]