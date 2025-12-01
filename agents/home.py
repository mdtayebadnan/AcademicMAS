import ollama

# Initialize Ollama client
client = ollama.Client()

def home_chat(input_text):
    # Define the prompt to ask Ollama to summarize the input text
    prompt = f"You are a helpful assistant. Keep responses concise and friendly to the question:\n\n{input_text}"

    # Generate the response from Ollama
    response = client.generate(model="llama3.2", prompt=prompt)

    # Return the summary
    return response.response.strip()

