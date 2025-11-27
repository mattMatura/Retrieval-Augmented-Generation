📈 Financial 10-K Analyst (RAG Pipeline)

A Production-Grade Retrieval-Augmented Generation (RAG) System for analyzing complex SEC Financial Filings.

📖 Overview

The Financial 10-K Analyst is an AI-powered tool designed to solve the "context window" problem standard LLMs face when analyzing massive financial documents. By ingesting, chunking, and indexing SEC 10-K filings (specifically Apple's 2023 report), this system allows users to ask complex financial questions and receive accurate, citation-backed answers.

Unlike a standard chatbot, this system features a "Glass Box" UI, allowing users to verify the AI's answer by inspecting the exact text chunks retrieved from the original PDF.

🎥 Demo

<img width="1438" height="776" alt="image" src="https://github.com/user-attachments/assets/20a44fba-296f-4ce3-b089-83f6747a7612" />


🏗️ Architecture

The system follows a standard ETL (Extract, Transform, Load) and Retrieval pipeline:

graph LR

    A[SEC 10-K PDF] -->|PyPDFLoader| B(Raw Text)
    B -->|Recursive Splitter| C[Text Chunks]
    C -->|OpenAI Embeddings| D[Vector Embeddings]
    D -->|Upsert| E[(Pinecone Vector DB)]
    
    U[User Question] -->|Vector Search| E
    E -->|Top 3 Chunks| L[LLM Context]
    L -->|GPT-4o-mini| R[Final Answer]


🚀 Key Features

Smart Ingestion: Automated fetching of 10-K filings using the sec-edgar-downloader.

Semantic Search: Utilizes Cosine Similarity via Pinecone to find relevant financial context, even if exact keywords don't match.

Recursive Chunking: Documents are split into 1000-character chunks with a 200-character overlap to preserve context across sentence boundaries.

Hallucination Guardrails: System prompt enforces strict "I don't know" policies if data is missing.

Source Citations: The UI provides an expandable "View Source Documents" section for trust and verification.


🛠️ Technical Decisions

Component

Choice

Rationale

LLM

gpt-4o-mini

Chosen for its high speed and low cost ($0.15/1M tokens) while maintaining strong reasoning for retrieval tasks.

Vector DB

Pinecone

Selected for its serverless architecture, low maintenance overhead, and industry-standard API.

Embeddings

text-embedding-3-small

OpenAI's latest efficient model (1536 dimensions) provides an optimal balance of cost vs. semantic capture.

Framework

LangChain (LCEL)

Used specifically for the RunnablePassthrough logic to build cleaner, composable chains without "black box" abstractions.

💻 Setup & Installation

1. Clone the Repository

git clone [https://github.com/yourusername/Retrieval-Augmented-Generation.git](https://github.com/yourusername/Retrieval-Augmented-Generation.git)
cd Retrieval-Augmented-Generation


2. Install Dependencies

pip install -r requirements.txt


3. Configure Secrets

Create a .env file in the root directory:

OPENAI_API_KEY=sk-proj-xxxx...
PINECONE_API_KEY=pcsk-xxxx...


4. Run the Ingestion Pipeline

This downloads the data and builds the vector database.

python ingest.py


5. Launch the App

streamlit run app.py


🔮 Future Improvements

Hybrid Search: Implement keyword-based search (BM25) alongside vector search to better handle specific acronyms (e.g., "EBITDA").

Metadata Filtering: Allow users to filter by "Fiscal Year" or "Company" before searching.

Evaluation: Implement RAGAS (Retrieval Augmented Generation Assessment) to programmatically score "Answer Faithfulness" and "Context Precision."
