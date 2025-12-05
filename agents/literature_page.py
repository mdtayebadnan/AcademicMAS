
import spade
from spade_llm import LLMAgent, LLMProvider

# Initialize the Ollama LLM provider
provider = LLMProvider.create_ollama(
    model="llama3.2:latest",
    base_url="http://localhost:11434/v1"
)

# SPADE Summarization Agent
class SummarizationAgent(LLMAgent):
    async def handle_message(self, message):
        input_text = message.body  # Get input text from the message
        prompt = f"Summarize the following text in one sentence:\n\n{input_text}"
        
        # Use the LLM provider (Ollama) to generate a summary
        response = await self.provider.generate(prompt=prompt)
        
        # Send the summary back to the sender
        summary = response.response.strip()
        await message.reply(summary)

async def start_summarizer_agent(text):
    # Create the SummarizationAgent instance
    spade_server = "localhost"
    summarization_agent = SummarizationAgent(
        jid=f"summarizer@{spade_server}",
        password="password",  # Password for the agent
        provider=provider,
        system_prompt="You are an agent that summarizes text in one sentence."
    )
    
    # Start the agent
    await summarization_agent.start()

    # Send the text to the agent for summarization
    message = await summarization_agent.send_message(text)
    
    # Wait for the agent's response
    summary = message.body
    await summarization_agent.stop()
    
    return summary

import ollama

# Initialize Ollama client
client = ollama.Client()

def Literature_text(input_text):
    # Define the prompt to ask Ollama to summarize the input text
    prompt = f"Literature the following text in one sentence:\n\n{input_text}"
    
    # Generate the response from Ollama
    response = client.generate(model="llama3.2", prompt=prompt)

    # Return the summary
    return response.response.strip()
