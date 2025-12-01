import sys
import os
import streamlit as st

# Add the directory of 'summary.py' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))

from agents.summarizer import summarize_text  # Import the summarize_text function
from PyPDF2 import PdfReader  

# Center the title using HTML
st.markdown("<h1 style='text-align: center;'>AI Assistant to Automate Everyday Research Tasks</h1>", unsafe_allow_html=True)

# Create a form with 'clear_on_submit' to clear the input after submission
with st.form(key='my_text_form', clear_on_submit=True):
    user_input = st.text_area("Enter your text here:", height=200)
    
    uploaded_file = st.file_uploader(
        "Or upload a PDF file:",
        type=["pdf"],
        help="If you upload a PDF, its text will be summarized."
    )

    submit_button = st.form_submit_button(label='Submit')

def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file-like object."""
    reader = PdfReader(file)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n".join(text)

# After form submission, call the summarize_text function from summarize.py
if submit_button:
    # Priority: if PDF is uploaded, use that; otherwise use text area
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text.strip():
            summary = summarize_text(pdf_text)
            st.write("**Summary of PDF:**")
            st.write(summary)
        else:
            st.write("Could not extract any text from the uploaded PDF.")
    elif user_input:
        summary = summarize_text(user_input)
        st.write("**Summary of text:**")
        st.write(summary)
    else:
        st.write("Please enter some text or upload a PDF to summarize.")

