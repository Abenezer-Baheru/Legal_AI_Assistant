import os
import re
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

# 1. Initialize ChromaDB client and collection
client = chromadb.PersistentClient(path="./legal_db")
collection = client.get_or_create_collection(
    name="ethiopian_law",
    metadata={"hnsw:space": "cosine"}
)

# 2. Set up embedding model
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. Extract PDF content
def load_legal_documents(data_dir="data"):
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

# 4. Chunking rules
def chunk_constitution(text):
    chunks = []
    articles = re.split(r"(?=Article\s+\d+)", text)
    for i, article in enumerate(articles):
        title_match = re.match(r"Article\s+\d+", article.strip())
        title = title_match.group() if title_match else f"Article_{i}"
        chunks.append({
            "content": article.strip(),
            "metadata": {
                "source": "constitution",
                "article": title
            }
        })
    return chunks

def chunk_civil_code(text):
    chunks = []
    titles = re.split(r"(?=Title\s+[IVXLCDM]+)", text)
    for section in titles:
        title_match = re.search(r"(Title\s+[IVXLCDM]+.*)", section)
        title = title_match.group(1).strip() if title_match else "Untitled"
        articles = re.findall(r"Article\s+(\d+)", section)
        if articles:
            article_range = f"{articles[0]}–{articles[-1]}"
            chunks.append({
                "content": section.strip(),
                "metadata": {
                    "source": "civil_code",
                    "title": title,
                    "articles": article_range
                }
            })
    return chunks

def chunk_criminal_code(text):
    chunks = []
    parts = re.split(r"(?=PART\s+[A-Z]+)", text)
    for section in parts:
        title_match = re.search(r"PART\s+[A-Z]+\s*[:\-]?\s*(.+)", section)
        title = title_match.group(1).strip() if title_match else "Untitled Offense"
        articles = re.findall(r"Article\s+(\d+)", section)
        if articles:
            article_range = f"{articles[0]}–{articles[-1]}"
            chunks.append({
                "content": section.strip(),
                "metadata": {
                    "source": "criminal_code",
                    "offense": title,
                    "articles": article_range
                }
            })
    return chunks

# 5. Embedding & indexing
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

# 6. Run the pipeline
if __name__ == "__main__":
    all_chunks = []
    docs = load_legal_documents()

    all_chunks += chunk_constitution(docs["constitution"])
    all_chunks += chunk_civil_code(docs["civil_code"])
    all_chunks += chunk_criminal_code(docs["criminal_code"])

    insert_documents(collection, all_chunks)
    print("✅ Legal documents successfully embedded into ChromaDB.")