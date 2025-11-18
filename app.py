import streamlit as st
from agents import home

# # Set page config
# st.set_page_config(page_title="AI Assistant", page_icon="🏠")

# Define pages using st.navigation
home_page = st.Page("agents/home.py", title="Home", icon="🏠")
summarizer_page = st.Page("agents/chat-with-pdf.py", title="Chat With PDF", icon="💬")
pdf_chat_page = st.Page("agents/summarizer-page.py", title="Summarizer", icon="📊")
literature_page = st.Page("agents/literature_page.py", title="Literature", icon="📚")
citation_page = st.Page("agents/citation_page.py", title="Citation Generator", icon="📎")


pg = st.navigation([home_page, summarizer_page, pdf_chat_page, literature_page, citation_page])


pg.run()
