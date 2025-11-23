# AcademicMAS -  A Multi-Agent Research Assistant 
AcademicMAS is a multi-agent system developed as part of the course requirements for "Agent-Based Software Engineering" (SENG 696) at the University of Calgary. 

## Prepared by:
- <span style="font-size:20px"> **Name:** Md Tayeb Adnan </span> <br> 
- <span style="font-size:20px"> **UCID#** 30292333 </span> <br>
- **Course Title:** Agent-Based Software Engineering  <br>
- **Course Code:** SENG 696  <br>
- **Instructor:** Professor Behrouz Far  <br>
- University of Calgary | Fall 2025

## Overview 
This project presents a Multi-Agent Research Assistant System designed to automate key research tasks, such as literature review, data analysis, and report writing. The system uses specialized agents for PDF parsing, literature search, summarization, knowledge management, analysis, citation generation, and report writing. A central Orchestrator Agent detects the input type (text query or PDF) and delegates tasks to the appropriate agents, streamlining the research process. By automating repetitive tasks, the system enhances efficiency, ensures consistency, and reduces manual workload, ultimately supporting more productive and accurate research. This framework showcases the potential of multi-agent systems to improve academic and industry research workflows.

## Technology Stack

- **Agent Framework:** SPADE (Smart Python Multi-Agent Development Environment)
- **Backend:** Python (Flask/FastAPI) with MySQL 8.0
- **Frontend:** Streamlit
- **Communication:** FIPA-ACL via REST API
- **Natural Language Processing:** Langchain (for LLM integration and natural language tasks)
- **Retrieval-Augmented Generation (RAG):** For combining language models with external knowledge retrieval systems

## 🚀 Quick Start
### Prerequisites
- Python 3.11+
- SPADE 3.3.0+
- SPADE_LLM
- Docker (optional)
- Groq API Key

### 1. Clone and Setup
```bash
git clone https://github.com/mdtayebadnan/AcademicMAS.git
cd academicmas

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Create environment file
cp .env.example .env

# Add your API key to .env
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
```
### 3. Run the Application
```bash
streamlit run app.py
```

## Documentation
<a href="https://github.com/mdtayebadnan/AcademicMAS/blob/main/reports/First_Report.pdf">First Assignment</a> <br>
<a href="https://github.com/mdtayebadnan/AcademicMAS/blob/main/reports/Second_Report.pdf">Second Assignment</a>

