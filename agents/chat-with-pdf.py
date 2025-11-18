import streamlit as st

st.markdown("## 📄 Chat with PDF")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded:
    st.success("PDF uploaded!")
    st.write("**File:**", uploaded.name)
    st.write("### Ask a question:")
    q = st.text_input("Your question")

    if q:
        st.info("AI answer will go here...")

if st.button("Back to Home"):
    st.switch_page("agents/home.py")
