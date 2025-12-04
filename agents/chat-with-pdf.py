import streamlit as st
import os
import time
from pathlib import Path
import pandas as pd
from typing import List, Dict
import tempfile

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import our RAG components
from RAG_QnA.rag_chain import QueryProcessor
from RAG_QnA.vector_store import VectorStore
from RAG_QnA.document_processor import DocumentProcessor
from RAG_QnA.document_loader import PDFDocumentLoader
from config import GROQ_API_KEY

# Configure Streamlit page
st.set_page_config(
    page_title="PDF Q&A with RAG",
    page_icon="📚",
    layout="centered",  # Change layout to centered to avoid wide layout
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    
    LEARNING NOTE: Session state maintains data across Streamlit reruns
    - Keeps conversation history
    - Stores uploaded documents
    - Maintains system configuration
    """
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    
    if 'query_processor' not in st.session_state:
        st.session_state.query_processor = None
    
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

def load_default_documents():
    """Load sample documents if no custom documents are uploaded."""
    try:
        # Try to load existing vector store
        vector_store = VectorStore()
        vector_store.load_vector_store("data/vector_store")
        return vector_store, "Loaded existing sample documents"
    except FileNotFoundError:
        # Create sample documents
        loader = PDFDocumentLoader()
        documents = loader.create_sample_documents()
        
        processor = DocumentProcessor()
        chunks = processor.process_documents(documents)
        
        vector_store = VectorStore()
        vector_store.create_vector_store(chunks)
        vector_store.save_vector_store("data/vector_store")
        
        return vector_store, "Created sample documents"

def process_uploaded_files(uploaded_files, chunk_size=1000, chunk_overlap=200):
    """
    Process uploaded PDF files.
    
    LEARNING NOTE: This handles the full document processing pipeline:
    1. Save uploaded files temporarily
    2. Extract text from PDFs
    3. Process into chunks
    4. Create vector store
    """
    if not uploaded_files:
        return None, "No files uploaded"
    
    loader = PDFDocumentLoader()
    all_documents = []
    
    # Process each uploaded file
    for uploaded_file in uploaded_files:
        
        try:
            # Load document from PDF
            pdf_bytes = uploaded_file.getvalue()
            document = loader.load_from_pdf_bytes(pdf_bytes, uploaded_file.name)
            
            if document:
                all_documents.append(document)

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
            continue  # Skip this file, continue with others
    
    if not all_documents:
        return None, "No valid documents found"
    
    # Process documents into chunks
    processor = DocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = processor.process_documents(all_documents)
    
    # Create vector store
    vector_store = VectorStore()
    vector_store.create_vector_store(chunks)
    
    return vector_store, f"Processed {len(all_documents)} documents into {len(chunks)} chunks"

def main():
    """Main Streamlit application."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header for PDF upload
    st.title("📚 PDF Q&A with RAG")
    st.markdown("Upload PDFs and ask questions about their content using AI!")
    
    # Document upload
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Upload PDF documents to ask questions about"
    )
    
    # Automatically process documents as soon as uploaded
    if uploaded_files:
        with st.spinner("Processing uploaded documents..."):
            st.session_state.vector_store = None
            st.session_state.query_processor = None
            st.session_state.documents_processed = False
            st.session_state.messages = [] 
                    
            vector_store, message = process_uploaded_files(
                uploaded_files, chunk_size=1000, chunk_overlap=200
            )
            
            if vector_store:
                st.session_state.vector_store = vector_store
                st.session_state.documents_processed = True
                st.session_state.uploaded_files = [f.name for f in uploaded_files]
                st.success(message)
            else:
                st.error(message)
    
    # Main chat interface
    st.header("💬 Chat Interface")
        
    # Initialize query processor if documents are processed
    if (st.session_state.documents_processed and 
        st.session_state.vector_store and 
        not st.session_state.query_processor):
        
        try:
            query_processor = QueryProcessor(GROQ_API_KEY)
            query_processor.load_vector_store(st.session_state.vector_store)
            st.session_state.query_processor = query_processor
            st.success("🚀 RAG system ready!")
        except Exception as e:
            st.error(f"Error initializing RAG system: {e}")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source['title']}**")
                        st.markdown(f"*Similarity: {source['similarity_score']:.3f}*")
                        st.markdown(f"```\n{source['content_preview']}\n```")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        if not st.session_state.query_processor:
            st.error("Please process documents first using the sidebar")
        else:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = st.session_state.query_processor.process_query(
                        prompt, k=3
                    )
                
                # Display answer
                st.markdown(result["answer"])
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result.get("sources", [])
                })

if __name__ == "__main__":
    main()
