import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import fitz  # PyMuPDF
import pdfplumber

class PDFParserAgent(Agent):
    class PDFParserBehaviour(CyclicBehaviour):
        async def run(self):
            # Check if the agent has received a message with a PDF file
            msg = await self.receive()
            if msg:
                # Extract PDF path from the received message
                pdf_path = msg.body
                print(f"Processing PDF: {pdf_path}")

                # Parse the PDF using PyMuPDF (or pdfplumber, unstructured, etc.)
                pdf_data = self.extract_pdf_data(pdf_path)

                # Send extracted data back to the orchestrator or relevant agent
                response = spade.message.Message(to="orchestrator_agent@yourdomain.com")
                response.set_metadata("performative", "inform")
                response.body = str(pdf_data)
                await self.send(response)
        
        def extract_pdf_data(self, pdf_path):
            """ Function to extract metadata and text from a PDF """
            pdf_data = {}

            # Extracting text and metadata using PyMuPDF
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            pdf_data['title'] = metadata.get('title', '')
            pdf_data['author'] = metadata.get('author', '')
            pdf_data['keywords'] = metadata.get('keywords', '')

            # Extract text and segment sections using pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text()

            # Segment the document into sections (e.g., abstract, introduction)
            sections = self.segment_document(text)
            pdf_data['sections'] = sections

            return pdf_data

        def segment_document(self, text):
            """ Function to segment the document into logical sections """
            sections = {
                "abstract": "",
                "introduction": "",
                "methods": "",
                "results": "",
                "discussion": "",
                "conclusion": ""
            }
            # You can use basic regex or more sophisticated NLP techniques to extract sections
            lines = text.split('\n')
            current_section = None
            for line in lines:
                if "abstract" in line.lower():
                    current_section = "abstract"
                elif "introduction" in line.lower():
                    current_section = "introduction"
                elif "methodology" in line.lower():
                    current_section = "methods"
                elif "results" in line.lower():
                    current_section = "results"
                elif "discussion" in line.lower():
                    current_section = "discussion"
                elif "conclusion" in line.lower():
                    current_section = "conclusion"
                
                if current_section:
                    sections[current_section] += line + "\n"
            
            return sections

    async def setup(self):
        print(f"PDFParserAgent {self.name} started.")
        # Set up the behaviour for the agent
        behaviour = self.PDFParserBehaviour()
        self.add_behaviour(behaviour)

# Start the SPADE agent
if __name__ == "__main__":
    # Set up the agent with the desired XMPP connection (e.g., "username@yourdomain.com")
    agent = PDFParserAgent("pdfparser_agent@yourdomain.com", "password")
    agent.start()
