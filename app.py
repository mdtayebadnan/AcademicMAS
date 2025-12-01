import streamlit as st


# Create pages
home_page = st.Page("pages/home_page.py", title="Home", icon="🏠")
pdf_chat_page  = st.Page("agents/chat-with-pdf.py", title="Chat With PDF", icon="💬")
summarizer_page = st.Page("pages/summarizer_page.py", title="Summarizer", icon="📝")
literature_page = st.Page("agents/literature_page.py", title="Literature Review", icon="📚")
paraphraser_page = st.Page("pages/paraphraser_page.py", title="Paraphraser", icon="🔄")
citation_page = st.Page("pages/citation_page.py", title="Citation Generator", icon="📋")

# Add all pages to navigation
pg = st.navigation([home_page, pdf_chat_page, summarizer_page, literature_page, paraphraser_page, citation_page])

pg.run()
