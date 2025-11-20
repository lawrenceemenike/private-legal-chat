import streamlit as st
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Private Legal Chat", layout="wide")

st.title("⚖️ Private Legal Chat Assistant")
st.markdown("---")

# Sidebar for Document Upload
with st.sidebar:
    st.header("Document Knowledge Base")
    uploaded_files = st.file_uploader(
        "Upload Legal Documents (PDF/TXT)", 
        accept_multiple_files=True,
        type=['pdf', 'txt']
    )
    
    if uploaded_files and st.button("Ingest Documents"):
        with st.spinner("Ingesting documents..."):
            files = [
                ('files', (file.name, file, file.type)) for file in uploaded_files
            ]
            try:
                response = requests.post(f"{API_URL}/ingest", files=files)
                if response.status_code == 200:
                    st.success("Ingestion Complete!")
                else:
                    st.error(f"Ingestion Failed: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['source']}** (Page {source['page']})")
                    st.caption(source['content'])

# User Input
if prompt := st.chat_input("Ask a question about your legal documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/chat", json={"query": prompt})
                if response.status_code == 200:
                    data = response.json()
                    answer = data["result"]
                    sources = data["source_documents"]
                    
                    st.markdown(answer)
                    with st.expander("View Sources"):
                        for source in sources:
                            st.markdown(f"**{source['source']}** (Page {source['page']})")
                            st.caption(source['content'])
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
