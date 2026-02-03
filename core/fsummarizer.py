#core/fsummarizer.py

from core.futils import force_json
from langchain_ollama import OllamaLLM

# def summarize_resume(llm: OllamaLLM, raw_text: str) -> dict:
#     prompt = f"""
# You are a professional resume analyst.

# Summarize the resume and extract skills.

# Return ONLY valid JSON:
# {{
#   "overview": "2-3 line professional summary",
#   "skills": ["skill1", "skill2", "skill3"]
# }}

# Resume:
# {raw_text}
# """
#     resp = llm.invoke(prompt)
#     return force_json(resp)




def summarize_resume(llm: OllamaLLM, raw_text: str) -> dict:
    prompt = f"""
You are a professional resume analyst.

From the resume text below, extract:

1. Candidate full name (if clearly mentioned at the top)
2. A 2–3 line professional summary
3. A list of key technical skills

Rules:
- If candidate name is not found, return "Unknown"
- Return ONLY valid JSON
- No explanations, no markdown

JSON format:
{{
  "candidate_name": "string",
  "overview": "2-3 line professional summary",
  "skills": ["skill1", "skill2", "skill3"]
}}

Resume:
{raw_text}
"""
    resp = llm.invoke(prompt)
    return force_json(resp)








# import re #regex parsing
# from langchain_ollama import OllamaLLM

# def summarize_resume(llm: OllamaLLM, raw_text: str) -> str:
#     prompt = f"""
# Summarize this resume into one paragraph titled 'Overview' 
# and extract skills in comma-separated form.

# Format:
# Overview: ...
# Skills: skill1, skill2, skill3

# Resume:
# {raw_text}
# """
#     return llm.invoke(prompt)

# def parse_summary(summary: str):
#     over = re.search(r"Overview:(.*)", summary, re.DOTALL)
#     skl = re.search(r"Skills:(.*)", summary, re.DOTALL)

#     overview = over.group(1).strip() if over else ""
#     skills = [s.strip() for s in skl.group(1).split(",")] if skl else []

#     return overview, skills

