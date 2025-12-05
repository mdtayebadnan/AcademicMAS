import streamlit as st
from agents.paraphrase_agent import paraphrase_text

# Center the title using HTML
st.markdown("<h1 style='text-align: center;'>AI Assistant to Automate Everyday Research Tasks</h1>", unsafe_allow_html=True)

# Initialize the session state to store conversation history if not already initialized
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Create a form with 'clear_on_submit' to clear the input after submission
with st.form(key='my_text_form', clear_on_submit=True):
    user_input = st.text_input("Enter your text here:", placeholder="Ask me anything")
    submit_button = st.form_submit_button(label='Submit')

# After form submission, update conversation history
if submit_button:
    # Append user input to conversation history
    st.session_state.conversation.append(f"You: {user_input}")
    
    # Get the response from the assistant
    response = paraphrase_text(user_input)
    
    # Append the assistant's response to the conversation history
    st.session_state.conversation.append(f"AI Assistant: {response}")
    
    # Display the entire conversation history in order (most recent message last)
    for message in st.session_state.conversation:
        if message.startswith("You:"):
            # Display user message aligned to the right, removing "You:" prefix
            st.markdown(f"<p style='text-align: right;'>{message[4:]}</p>", unsafe_allow_html=True)
        elif message.startswith("AI Assistant:"):
            # Display AI response aligned to the left, removing "AI Assistant:" prefix
            st.markdown(f"<p style='text-align: left;'>{message[14:]}</p>", unsafe_allow_html=True)
