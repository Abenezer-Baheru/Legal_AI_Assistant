import os
import re
import chromadb
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize the LLM
llm = ChatGroq(
    api_key=api_key,
    model="llama3-8b-8192",
    temperature=0.3
)

# Session memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Structured conversational prompt
prompt = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template="""
You are a legal AI assistant trained on the Ethiopian Constitution, Civil Code, and Criminal Code.

Instructions:
- Base your answer strictly on the provided legal context.
- Think step-by-step: identify the relevant law → interpret it clearly → communicate it naturally.
- Avoid speculation or outside sources. If the context is insufficient, say:
  "The provided context does not contain a definitive answer."
- Use an insightful, warm, and professional tone — like a knowledgeable legal peer guiding someone.

Structure your response seamlessly:
- Begin with a smooth, topic-aware opening that flows into the explanation. Avoid generic phrases like “great question.”
- Explain the law in clear, accessible English, citing article numbers when possible.
- Close with a concise insight that reinforces the legal takeaway.
- End with a subtle, natural follow-up prompt to keep the conversation active.
- Conclude with a clear source reference like: “📘 Source: Article 93, Ethiopian Constitution”

Do not label sections or format headers like “Summary” or “Insight.” The response should feel cohesive, human, and conversational — not robotic or templated.

Chat History:
{chat_history}

Legal Context:
{context}

User Question: {question}

Answer:
"""
)

# Vector store + embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./legal_db")
collection = client.get_or_create_collection("ethiopian_law")

# Retrieve relevant context
def search_legal_docs(query, top_k=5, max_chars=4000):
    query_vector = embeddings.embed_query(query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    grouped = {}
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        title = meta.get("article") or meta.get("title") or meta.get("offense") or "Unknown"
        if title not in grouped:
            grouped[title] = {"doc": [], "summary": meta.get("summary_title", "")}
        grouped[title]["doc"].append(doc.strip())

    context = "\n\n".join(
        f"{title}\n" + "\n".join(grouped[title]["doc"]) for title in grouped
    )

    return context[:max_chars], grouped

# Build reasoning pipeline
qa_chain = (
    RunnableMap({
        "context": lambda x: x["context"],
        "question": lambda x: x["question"],
        "chat_history": lambda x: x.get("chat_history", "")
    })
    | prompt
    | llm
    | StrOutputParser()
)

# Primary callable from API
def ask_question(query: str):
    context, grouped = search_legal_docs(query)
    chat_history = memory.load_memory_variables({}).get("chat_history", "")
    response = qa_chain.invoke({
        "context": context,
        "question": query,
        "chat_history": chat_history
    })
    memory.save_context({"input": query}, {"output": response})
    return response, grouped