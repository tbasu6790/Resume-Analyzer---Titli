# Resume-Analyzer---Titli
==========================
<!-- AI-Powered Resume Analysis & Ranking System
An intelligent, LLM-driven backend system that analyzes multiple resumes against a job description (JD) and produces a ranked list of candidates based on semantic relevance and comparative strength.
This project is designed as a production-ready FastAPI service, suitable for integration with any frontend (React, Angular, etc.).

🚀 Key Features
1. Job Description (JD) Pointwise Summary
Converts raw job descriptions into clear, structured bullet points
Makes job requirements transparent and UI-friendly
Powered by an LLM for semantic understanding
2. Resume Upload & Text Extraction
Supports single or multiple PDF resumes
Extracts raw text using robust PDF parsing
Handles multi-page resumes gracefully
3. Resume Summarization & Skill Extraction
Generates:
Candidate overview (2–3 lines)
Skill list
Candidate name (when possible)
Converts unstructured resumes into structured, analyzable data
4. Resume vs Job Description Scoring (JD Score)
Each resume is evaluated independently against the job description to produce:
JD match score (0–100)
Matched skills
Missing skills
Short professional analysis
This ensures absolute job relevance is always considered.
5. Automatic Baseline Selection (Strategy 2)
The resume with the highest JD match score is automatically selected as the baseline
Prevents upload-order bias
Ensures fair and meaningful comparisons
6. Pairwise Resume Comparison (LLM-based)
All resumes are compared relative to the baseline resume
The LLM generates a continuous relative score (0–100)
No hardcoded buckets like 30/50/70
Produces natural score differentiation
7. Final Scoring & Ranking
**Final score formula:
Final Score = 0.6 × JD Score + 0.4 × Pairwise Score**
JD relevance remains dominant
Pairwise comparison refines ranking
Produces stable, explainable results
8. Clean, UI-Safe Output
The API response exposes only:
Candidate name
Resume name
Final score
Matched skills
Missing skills
Short analysis
Internal signals (JD score, pairwise score, baseline identity) are hidden from UI.
9. Mock LLM Support (Development & Testing)
Includes a MockLLM to simulate LLM responses
Enables Swagger testing when real LLM is unavailable
Industry-standard practice for backend testing

System Architecture :
Client / UI
   ↓
FastAPI Backend
   ↓
Resume Text Extraction (PDF)
   ↓
LLM-based Resume & JD Analysis
   ↓
Baseline-Anchored Pairwise Comparison
   ↓
Final Scoring & Ranking
   ↓
JSON Output for UI

🛠️ Tech Stack
Backend
FastAPI – High-performance Python API framework
Python 3.10+ – Core language
AI / NLP
Large Language Models (LLMs) via Ollama or server-based inference
Used for:
Resume summarization
Skill extraction
JD analysis
Pairwise resume comparison
PDF Processing
PyMuPDF (fitz) – Reliable PDF text extraction
Data Format
JSON – API communication and output storage
Development & Testing
MockLLM – Simulated LLM for offline testing
Swagger UI – API testing & documentation

Project Structure :
FastAPI/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── pipeline.py        # Core analysis pipeline
│   └── mock_llm.py        # Mock LLM for testing
│
├── core/
│   ├── fextractor.py      # Resume text extraction
│   ├── fsummarizer.py     # Resume summarization
│   ├── fcompare_jd.py     # Resume vs JD comparison
│   ├── fpairwise_compare.py # Pairwise comparison logic
│   └── futils.py          # Utilities (LLM, JSON safety)
│
├── uploads/               # Uploaded resumes & outputs
├── requirements.txt
└── README.md

▶️ How to Run the Project
1. Create Virtual Environment
python -m venv analyze
source analyze/bin/activate

2. Install Dependencies
pip install -r requirements.txt

3. Start FastAPI Server
uvicorn app.main:app --reload

4. Open Swagger UI
http://127.0.0.1:8000/docs

🧪 Testing Without a Real LLM
Use MockLLM for testing:
export USE_MOCK_LLM=1
uvicorn app.main:app --reload

🎯 Why This Project Is Different from Traditional ATS
Traditional ATS	This System
Keyword matching	Semantic understanding
Rigid rules	Adaptive LLM reasoning
High false negatives	Context-aware evaluation
No explanation	Explainable analysis -->
>>>>>>> e821224 (Initial commit: Resume Analyzer FastAPI project)
