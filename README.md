# Legal AI Assistant for Ethiopia: Rooted in the Constitution, Civil and Criminal Codes

A conversational AI system designed to make Ethiopian law accessible, explainable, and actionable. Built using modern retrieval-augmented generation (RAG) techniques and grounded in Ethiopia’s Constitution, Civil Code, and Criminal Code, the assistant enables users to ask natural language legal questions and receive clear, article-based answers.

---

## 🚀 Features

- ⚖️ Understands and explains articles from Ethiopia’s **Constitution**, **Civil Code**, and **Criminal Code**
- 🧠 Answers freeform user questions with grounded legal citations
- 🧾 Interprets real-life criminal case scenarios and outlines potential consequences
- 💡 Handles irrelevant or vague queries with graceful fallbacks
- 💬 Offers both **CLI** and **Streamlit UI** for interaction

---

## 🗂 Repository Structure

```
├── app/
│   ├── extract_and_store.py     # Builds ChromaDB vector store from PDF law documents
│   ├── query_and_answer.py      # CLI interface to test the system
│   ├── qa_engine.py             # Core retrieval, prompt assembly, and LLM reasoning
│   └── main.py                  # FastAPI app backend

├── frontend/
│   └── streamlit_app.py         # Streamlit-based user interface

├── legal_db/                    # Precomputed ChromaDB vector artifacts (29MB)
│   └── index files and embeddings

├── data/                        # Legal PDF documents (publicly sourced)
│   ├── Ethiopia_Constitution.pdf
│   ├── Ethiopia_Civil_Code.pdf
│   └── Ethiopia_Criminal_Code.pdf

├── UI_Screenshots/              # Example interactions
│   ├── constitutionBased.png
│   ├── civilCodeBased.png
│   ├── criminalCodeBased.png
│   ├── outOfContext.png
│   ├── caseBased.png
│   └── CLI.png

├── requirements.txt             # Installation requirements
├── .env                         # API keys and environment variables
├── README.md                    # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Abenezer-Baheru/Legal_AI_Assistant.git
cd Legal_AI_Assistant
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🧪 Quick Start

### A. Run From the Command Line (CLI)

```bash
python app/query_and_answer.py
```

This allows you to interact with the legal assistant in the terminal.

---

### B. Launch API and UI

#### 1. Start the FastAPI backend (for LLM-powered legal QA)

```bash
uvicorn app.main:app --reload
```

This runs the API server at http://localhost:8000 — used by the frontend.

#### 2. Launch the Streamlit UI

In a separate terminal:

```bash
streamlit run frontend/streamlit_app.py
```

The UI will open in your browser (typically at http://localhost:8501) and let you chat with the assistant using a clean interface.

---

## 🔗 Technologies

- **LLM Inference**: LLaMA 3 (8B) via `langchain_groq.ChatGroq`
- **Embeddings**: `all-MiniLM-L6-v2`
- **Retrieval**: ChromaDB
- **Frameworks**: LangChain, FastAPI, Streamlit

---

## 📚 Legal Sources

All legal texts are publicly accessible and sourced from:

- **FDRE Constitution of Ethiopia (1995)**
- **Ethiopian Civil Code (1960)**
- **Ethiopian Criminal Code (2004)**

Main source: [LawEthiopia.com](https://www.lawethiopia.com/)

---

## 🛣️ Future Plans

- 🌍 Amharic language support
- 📜 Proclamation and precedent interpretation
- 🧪 Sentencing benchmark evaluation
- 👩🏽‍🏫 Educational walkthrough mode for training
- 🔐 Public/role-based deployments

---

## 🧾 License

This project is distributed under the **MIT License** — free to use, share, and build upon with attribution.

---

## 🙌 Acknowledgments

Crafted with purpose to democratize legal access in Ethiopia. This project is a step toward making statutory law more transparent, understandable, and empowering for all citizens.

---

## 🛠 Support

For questions, issues, or ideas:

- GitHub Issues: [Open an issue](https://github.com/Abenezer-Baheru/Legal_AI_Assistant/issues)
- Contact: abenezer7baheru@gmail.com

---

## 📖 Citation

If you use or reference this project in your work, please cite the ReadyTensor publication:

**Abenezer Baheru** (2025). _Legal AI Assistant for Ethiopia: Rooted in the Constitution, Civil and Criminal Codes_. ReadyTensor.  
Available at: [https://app.readytensor.ai/publications/pHZqtw8lp7Ul](https://app.readytensor.ai/publications/pHZqtw8lp7Ul)

📝 For academic use  
📚 For legal education  
🌍 For civic and AI research impact

---

## 👤 Author

**Abenezer Baheru**
