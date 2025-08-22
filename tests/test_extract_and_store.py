import pytest
from app.extract_and_store import load_legal_documents, chunk_constitution, chunk_civil_code, chunk_criminal_code

def test_load_documents_structure():
    docs = load_legal_documents(data_dir="data")
    assert isinstance(docs, dict)
    assert "constitution" in docs and "civil_code" in docs and "criminal_code" in docs
def test_chunk_constitution_structure():
    sample_text = "Article 1\nThis is the first article.\nArticle 2\nThis is the second article."
    chunks = chunk_constitution(sample_text)
    assert len(chunks) == 3
    assert all("content" in c and "metadata" in c for c in chunks)
    assert all("article" in c["metadata"] for c in chunks)

def test_chunk_civil_code_structure():
    sample_text = "Title I\nArticle 1\nText.\nArticle 2\nText.\nTitle II\nArticle 3\nText."
    chunks = chunk_civil_code(sample_text)
    assert len(chunks) == 2
    assert all("title" in c["metadata"] and "articles" in c["metadata"] for c in chunks)

def test_chunk_criminal_code_structure():
    sample_text = "PART A: Theft\nArticle 1\nText.\nArticle 2\nText.\nPART B: Assault\nArticle 3\nText."
    chunks = chunk_criminal_code(sample_text)
    assert len(chunks) == 2
    assert all("offense" in c["metadata"] and "articles" in c["metadata"] for c in chunks)