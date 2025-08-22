import os
import re
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from config import (
    EMBEDDING_MODEL_NAME, CHROMA_DB_PATH, COLLECTION_NAME,
    SIMILARITY_METRIC, DATA_DIR
)

# Initialize ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={f"hnsw:space": SIMILARITY_METRIC}
)

# Embedding model
embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# Load PDFs
def load_legal_documents(data_dir=DATA_DIR):
    docs_by_type = {"constitution": "", "civil_code": "", "criminal_code": ""}
    for file in os.listdir(data_dir):
        if file.endswith(".pdf"):
            file_path = os.path.join(data_dir, file)
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            full_text = "\n".join(p.page_content for p in pages)
            filename = file.lower()
            if "constitution" in filename:
                docs_by_type["constitution"] = full_text
            elif "civil" in filename:
                docs_by_type["civil_code"] = full_text
            elif "criminal" in filename:
                docs_by_type["criminal_code"] = full_text
            print(f"✅ Loaded: {file}")
    return docs_by_type

# Semantic chunking
def chunk_constitution(text):
    return [
        {
            "content": article.strip(),
            "metadata": {"source": "constitution", "article": re.match(r"Article\s+\d+", article.strip()).group() if re.match(r"Article\s+\d+", article.strip()) else f"Article_{i}"}
        }
        for i, article in enumerate(re.split(r"(?=Article\s+\d+)", text))
    ]

def chunk_civil_code(text):
    chunks = []
    for section in re.split(r"(?=Title\s+[IVXLCDM]+)", text):
        title_match = re.search(r"(Title\s+[IVXLCDM]+.*)", section)
        title = title_match.group(1).strip() if title_match else "Untitled"
        articles = re.findall(r"Article\s+(\d+)", section)
        if articles:
            chunks.append({
                "content": section.strip(),
                "metadata": {
                    "source": "civil_code",
                    "title": title,
                    "articles": f"{articles[0]}–{articles[-1]}"
                }
            })
    return chunks

def chunk_criminal_code(text):
    chunks = []
    for section in re.split(r"(?=PART\s+[A-Z]+)", text):
        title_match = re.search(r"PART\s+[A-Z]+\s*[:\-]?\s*(.+)", section)
        title = title_match.group(1).strip() if title_match else "Untitled Offense"
        articles = re.findall(r"Article\s+(\d+)", section)
        if articles:
            chunks.append({
                "content": section.strip(),
                "metadata": {
                    "source": "criminal_code",
                    "offense": title,
                    "articles": f"{articles[0]}–{articles[-1]}"
                }
            })
    return chunks

# Index chunks
def insert_documents(collection, chunks):
    next_id = collection.count()
    for i, chunk in enumerate(chunks):
        try:
            vector = embeddings_model.embed_documents([chunk["content"]])[0]
            collection.add(
                ids=[f"chunk_{next_id + i}"],
                documents=[chunk["content"]],
                embeddings=[vector],
                metadatas=[chunk["metadata"]]
            )
        except Exception as e:
            print(f"⚠️ Error indexing chunk {i}: {e}")
    print(f"📚 Stored {next_id + len(chunks)} total chunks.")

# Run
if __name__ == "__main__":
    docs = load_legal_documents()
    all_chunks = (
        chunk_constitution(docs["constitution"]) +
        chunk_civil_code(docs["civil_code"]) +
        chunk_criminal_code(docs["criminal_code"])
    )
    insert_documents(collection, all_chunks)
    print("✅ Legal documents successfully embedded into ChromaDB.")