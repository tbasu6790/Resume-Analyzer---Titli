# core/fcompare_jd.py

from core.futils import force_json
from langchain_ollama import OllamaLLM

def compare_with_jd(llm: OllamaLLM, resume_summary: dict, jd_text: str) -> dict:
    prompt = f"""
You are a senior technical recruiter.

Evaluate how well the resume matches the job description.

Consider:
- Skill overlap
- Depth of experience
- Role relevance

Return ONLY JSON:
{{
  "match_score": 0-100,
  "matched_skills": [],
  "missing_skills": [],
  "analysis": "2-3 sentence explanation"
}}

Resume Summary:
{resume_summary}

Job Description:
{jd_text}
"""
    resp = llm.invoke(prompt)
    data = force_json(resp)

    return {
        "match_score": int(data.get("match_score", 0)),
        "matched_skills": data.get("matched_skills", []),
        "missing_skills": data.get("missing_skills", []),
        "analysis": data.get("analysis", "")
    }





# import json
# from core.futils import force_json
# from langchain_ollama import OllamaLLM

# def compare_with_jd(llm: OllamaLLM, overview: str, jd_text: str) -> dict:
#     """
#     Compares a resume overview with a job description.

#     Returns keys:
#       - effective_match_percentage (0-100)
#       - match_skills (list)
#       - missing_skills (list)
#       - jd_required_skills (list)
#       - analysis (str)
#       - skill_rating (0-10)  # compatibility field
#     """
#     prompt = f"""
# You are an experienced technical recruiter.

# Tasks:
# 1. From the Resume Overview, extract the candidate's skills.
# 2. From the Job Description, extract the REQUIRED skills for the role.
# 3. Identify which required skills are matched by the resume (match_skills)
#    and which required skills are missing (missing_skills).
# 4. Estimate an overall effective match percentage (0-100) between the resume and JD.
# 5. Provide a short 1-3 line analysis.

# Return ONLY JSON in this exact shape:
# {{
#   "effective_match_percentage": 0,
#   "jd_required_skills": ["skill1", "skill2"],
#   "match_skills": ["skill1"],
#   "missing_skills": ["skill2"],
#   "analysis": "short explanation"
# }}

# Resume Overview:
# {overview}

# Job Description:
# {jd_text}
# """

#     resp = llm.invoke(prompt)
#     data = force_json(resp)

#     # Ensure fields exist and have sensible defaults
#     jd_required = data.get("jd_required_skills", []) or []
#     match_skills = data.get("match_skills", []) or []
#     missing_skills = data.get("missing_skills", []) or []
#     effective = data.get("effective_match_percentage", 0)
#     analysis = data.get("analysis", "")

#     # Compute a skill_rating (0-10) for backward compatibility:
#     total_required = len(jd_required)
#     if total_required == 0:
#         skill_rating = 0.0
#     else:
#         # Prefer using match over jd_required length to avoid divide-by-zero issues
#         skill_rating = round((len(match_skills) / total_required) * 10, 1)

#     return {
#         "effective_match_percentage": int(effective) if isinstance(effective, (int, float)) else 0,
#         "jd_required_skills": jd_required,
#         "match_skills": match_skills,
#         "missing_skills": missing_skills,
#         "analysis": analysis,
#         "skill_rating": skill_rating
#     }


