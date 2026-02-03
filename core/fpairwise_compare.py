# core/fpairwise_compare.py

from core.futils import force_json


def compare_two_resumes(llm, base_resume: dict, other_resume: dict) -> dict:
    """
    Compare OTHER resume relative to BASE resume and return
    a continuous relative score (0-100).
    """

    prompt = f"""
You are a professional technical recruiter.

You are given a BASE resume which is already known to be a strong match
for the job description.

Your task:
- Evaluate the SECOND resume relative to the BASE resume
- Assign a numeric score between 0 and 100
- 50 means comparable to base
- Higher than 50 means stronger than base
- Lower than 50 means weaker than base

Return ONLY valid JSON:
{{
  "relative_score": 0-100,
  "reason": "1-2 sentence explanation"
}}

BASE RESUME:
JD Match Score: {base_resume["jd_score"]}
Matched Skills: {base_resume["matched_skills"]}
Missing Skills: {base_resume["missing_skills"]}
Summary: {base_resume["overview"]}

SECOND RESUME:
Summary: {other_resume["overview"]}
"""

    resp = llm.invoke(prompt)
    data = force_json(resp)

    score = data.get("relative_score", 50)

    try:
        score = int(score)
    except Exception:
        score = 50

    # Safety clamp
    score = max(0, min(score, 100))

    return {
        "pairwise_score": score,
        "reason": data.get("reason", "")
    }













# from core.futils import force_json

# def compare_two_resumes(llm, name_a, text_a, name_b, text_b):
#     """
#     Compare two resumes using LLM. Returns a dict with:
#       - resume_a
#       - resume_b
#       - better_resume (name)
#       - match_score (0-100)
#       - key_points (list)
#       - analysis (str)
#     """
#     prompt = f"""
# Compare two resumes.

# Return STRICT JSON only:

# {{
#   "better_resume": "A" or "B",
#   "match_score": 0,
#   "key_points": ["point1","point2"],
#   "analysis": "3-5 sentences"
# }}

# Resume A ({name_a}):
# {text_a}

# Resume B ({name_b}):
# {text_b}
# """
#     resp = llm.invoke(prompt)
#     data = force_json(resp)

#     # Normalize
#     winner_key = (data.get("better_resume", "A") or "A").strip().upper()
#     winner = name_a if winner_key == "A" else name_b

#     # Safe values
#     match_score = data.get("match_score", 0)
#     try:
#         match_score = int(match_score)
#     except:
#         try:
#             match_score = int(float(match_score))
#         except:
#             match_score = 0

#     return {
#         "resume_a": name_a,
#         "resume_b": name_b,
#         "better_resume": winner,
#         "match_score": match_score,
#         "key_points": data.get("key_points", []),
#         "analysis": data.get("analysis", "")
#     }


# def compute_strength_scores(pairwise_list, resumes):
#     """
#     Compute wins and weighted scores per resume.

#     Returns:
#       wins: {resume: number_of_wins}
#       weighted: {resume: sum_of_match_scores_for_wins}
#     """
#     wins = {r: 0 for r in resumes}
#     weighted = {r: 0 for r in resumes}

#     for p in pairwise_list:
#         winner = p.get("better_resume")
#         if not winner:
#             continue
#         if winner not in wins:
#             # ignore unknown winners
#             continue
#         wins[winner] += 1
#         try:
#             weighted[winner] += int(p.get("match_score", 0))
#         except:
#             weighted[winner] += 0

#     return wins, weighted


