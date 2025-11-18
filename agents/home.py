import streamlit as st

# Center the title using HTML
st.markdown("<h1 style='text-align: center;'>AI Assistant to Automate Everyday Research Tasks</h1>", unsafe_allow_html=True)

# Create a form with 'clear_on_submit' to clear the input after submission
with st.form(key='my_form', clear_on_submit=True):
    user_input = st.text_input("Enter your text here:")
    submit_button = st.form_submit_button(label='Submit')

# After form submission, display the text entered
if submit_button:
    st.write(f"You submitted: {user_input}")
