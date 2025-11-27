import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Page Config (Must be first)
st.set_page_config(
    page_title="Financial Analyst Pro", 
    page_icon="🍏", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUPERTINO CSS OVERRIDE
# This block injects custom CSS to override Streamlit's default look
st.markdown("""
    <style>
    /* Main Background - Midnight */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #1c1c1e 100%);
        color: #f5f5f7;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sidebar - Frosted Glass */
    [data-testid="stSidebar"] {
        background-color: rgba(28, 28, 30, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f5f5f7 !important;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    /* Chat Input - Floating Pill */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    .stChatInputContainer textarea {
        background-color: #2c2c2e !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
    }
    
    /* User Message Bubble (Blue) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(10, 132, 255, 0.1);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid rgba(10, 132, 255, 0.2);
    }

    /* AI Message Bubble (Gray) */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Expander (Source Docs) */
    .streamlit-expanderHeader {
        background-color: #2c2c2e !important;
        color: #f5f5f7 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logic Setup
load_dotenv(override=True)

@st.cache_resource
def get_rag_chain():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    embeddings = OpenAIEmbeddings()
    vectorstore = PineconeVectorStore(
        index_name="financial-10k", 
        embedding=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    template = """You are a senior financial analyst at Apple.
    Answer the question based ONLY on the following context.
    Keep answers professional, concise, and data-driven.
    
    Context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever

chain, retriever = get_rag_chain()

# 4. Sidebar (Settings)
with st.sidebar:
    st.title("🍏 Analyst Pro")
    st.markdown("---")
    st.caption("DATA SOURCE")
    st.info("Apple Inc. (AAPL)\n10-K Filing (2023)")
    
    st.markdown("---")
    st.caption("CONFIGURATION")
    year = st.selectbox("Fiscal Year", ["2023", "2022", "2021"])
    strict_mode = st.toggle("Strict Citation Mode", value=True)
    
    st.markdown("---")
    st.caption("STATUS")
    st.markdown("🟢 **System Online**")
    st.markdown("⚡ **Latency:** 1.2s")

# 5. Main Chat Interface
st.header("Financial Intelligence Unit")
st.markdown("Analyzing 2023 SEC Filings for **Apple Inc.**")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🍏"):
        st.markdown(message["content"])

# Chat Input
if query := st.chat_input("Ask about Revenue, Risks, or R&D..."):
    
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    # 2. AI Response
    with st.chat_message("assistant", avatar="🍏"):
        message_placeholder = st.empty()
        
        # Retrieve & Generate
        with st.spinner("Analyzing documents..."):
            docs = retriever.invoke(query)
            response = chain.invoke(query)
        
        message_placeholder.markdown(response)
        
        # 3. Glass Box Source Viewer (Styled)
        with st.expander("🔍 Verified Sources"):
            for i, doc in enumerate(docs):
                st.markdown(f"**Document Fragment {i+1}**")
                # Clean up newlines for better display
                clean_content = doc.page_content.replace("\n", " ")
                st.caption(f"...{clean_content[:300]}...")
                st.markdown("---")

    # Save history
    st.session_state.messages.append({"role": "assistant", "content": response})