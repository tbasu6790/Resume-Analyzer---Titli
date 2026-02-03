# app/pipeline.py

from pathlib import Path
import json

from core.fextractor import extract_resume_text
from core.fsummarizer import summarize_resume
from core.fcompare_jd import compare_with_jd
from core.fpairwise_compare import compare_two_resumes
from core.futils import ensure_llm, force_json


def run_resume_analysis(resume_paths, jd_text: str, output_dir: Path):
    llm = ensure_llm()
    internal_data = []

    # ----------------------------
    # STEP 0: JD Pointwise Summary
    # ----------------------------
    jd_prompt = f"""
You are a professional recruiter.

Summarize the job description into concise bullet points.

Return ONLY valid JSON:
{{
  "points": ["point 1", "point 2"]
}}

Job Description:
{jd_text}
"""
    jd_points = force_json(llm.invoke(jd_prompt)).get("points", [])

    # ----------------------------
    # STEP 1: Resume → JD Evaluation
    # ----------------------------
    for path in resume_paths:
        raw_text = extract_resume_text(path)

        if not raw_text.strip():
            internal_data.append({
                "resume_name": path.name,
                "candidate_name": path.stem.replace("_", " ").title(),
                "overview": "",
                "jd_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "analysis": "No readable text found in the resume."
            })
            continue

        summary = summarize_resume(llm, raw_text)

        candidate_name = summary.get(
            "candidate_name",
            path.stem.replace("_", " ").title()
        )

        jd_result = compare_with_jd(
            llm,
            summary.get("overview", ""),
            jd_text
        )

        internal_data.append({
            "resume_name": path.name,
            "candidate_name": candidate_name,
            "overview": summary.get("overview", ""),
            "jd_score": jd_result.get("match_score", 0),
            "matched_skills": jd_result.get("matched_skills", []),
            "missing_skills": jd_result.get("missing_skills", []),
            "analysis": jd_result.get("analysis", "")
        })

    # ----------------------------
    # STEP 2: Auto-select BASELINE
    # ----------------------------
    baseline_resume = max(
        internal_data,
        key=lambda x: x["jd_score"]
    )

    # ----------------------------
    # STEP 3: Pairwise Comparison
    # ----------------------------
    for resume in internal_data:
        if resume["resume_name"] == baseline_resume["resume_name"]:
            resume["pairwise_score"] = baseline_resume["jd_score"]
            continue

        pairwise = compare_two_resumes(
            llm,
            baseline_resume,
            resume
        )

        resume["pairwise_score"] = pairwise["pairwise_score"]

    # ----------------------------
    # STEP 4: Final Score (NO HARDCODING)
    # ----------------------------
    for resume in internal_data:
        resume["final_score"] = int(
            0.6 * resume["jd_score"] +
            0.4 * resume["pairwise_score"]
        )

    # ----------------------------
    # STEP 5: UI-safe Ranked Output
    # ----------------------------
    ranked_resumes = sorted(
        internal_data,
        key=lambda x: x["final_score"],
        reverse=True
    )

    public_resumes = [
        {
            "resume_name": r["resume_name"],
            "candidate_name": r["candidate_name"],
            "final_score": r["final_score"],
            "matched_skills": r["matched_skills"],
            "missing_skills": r["missing_skills"],
            "analysis": r["analysis"]
        }
        for r in ranked_resumes
    ]

    result = {
        "total_resumes": len(public_resumes),
        "job_description_points": jd_points,
        "ranked_resumes": public_resumes
    }

    # ----------------------------
    # STEP 6: Save Output
    # ----------------------------
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return result






# # app/pipeline.py

# from pathlib import Path
# import json

# from core.fextractor import extract_resume_text
# from core.fsummarizer import summarize_resume
# from core.fcompare_jd import compare_with_jd
# from core.fpairwise_compare import compare_two_resumes
# from core.futils import ensure_llm, force_json


# def run_resume_analysis(resume_paths, jd_text: str, output_dir: Path):
#     llm = ensure_llm()
#     internal_data = []

#     # ----------------------------
#     # STEP 0: JD Pointwise Summary
#     # ----------------------------
#     jd_prompt = f"""
# You are a professional recruiter.

# Summarize the following job description into clear, concise bullet points.

# Rules:
# - Return ONLY valid JSON
# - No explanations
# - Each point should represent a key requirement or responsibility

# JSON format:
# {{
#   "points": [
#     "point 1",
#     "point 2",
#     "point 3"
#   ]
# }}

# Job Description:
# {jd_text}
# """
#     jd_summary_resp = llm.invoke(jd_prompt)
#     jd_summary_json = force_json(jd_summary_resp)
#     jd_points = jd_summary_json.get("points", [])

#     # ----------------------------
#     # STEP 1: Extract + JD Scoring
#     # ----------------------------
#     for path in resume_paths:
#         raw_text = extract_resume_text(path)

#         if not raw_text or not raw_text.strip():
#             internal_data.append({
#                 "resume_name": path.name,
#                 "candidate_name": path.stem.replace("_", " ").replace("-", " ").title(),
#                 "overview": "",
#                 "jd_score": 0,
#                 "matched_skills": [],
#                 "missing_skills": [],
#                 "analysis": "No readable text found in the resume."
#             })
#             continue

#         summary = summarize_resume(llm, raw_text)

#         candidate_name = summary.get("candidate_name", "Unknown")
#         if not candidate_name or candidate_name.lower() == "unknown":
#             candidate_name = path.stem.replace("_", " ").replace("-", " ").title()

#         jd_result = compare_with_jd(llm, summary.get("overview", ""), jd_text)

#         internal_data.append({
#             "resume_name": path.name,
#             "candidate_name": candidate_name,
#             "overview": summary.get("overview", ""),
#             "jd_score": jd_result.get("match_score", 0),
#             "matched_skills": jd_result.get("matched_skills", []),
#             "missing_skills": jd_result.get("missing_skills", []),
#             "analysis": jd_result.get("analysis", "")
#         })

#     # ----------------------------
#     # STEP 2: Pairwise vs Base Resume
#     # ----------------------------
#     base_resume = internal_data[0]
#     base_text = base_resume["overview"]

#     for i, resume in enumerate(internal_data):
#         if i == 0:
#             resume["pairwise_score"] = 50
#             continue

#         pairwise = compare_two_resumes(
#             llm,
#             base_resume["resume_name"], base_text,
#             resume["resume_name"], resume["overview"]
#         )

#         if pairwise["better_resume"] == resume["resume_name"]:
#             resume["pairwise_score"] = 70
#         elif pairwise["better_resume"] == base_resume["resume_name"]:
#             resume["pairwise_score"] = 30
#         else:
#             resume["pairwise_score"] = 50

#     # ----------------------------
#     # STEP 3: Final Score (internal)
#     # ----------------------------
#     for resume in internal_data:
#         resume["final_score"] = int(
#             0.6 * resume["jd_score"] +
#             0.4 * resume["pairwise_score"]
#         )

#     # ----------------------------
#     # STEP 4: Clean Output (UI-safe)
#     # ----------------------------
#     ranked_resumes = sorted(
#         internal_data,
#         key=lambda x: x["final_score"],
#         reverse=True
#     )

#     public_resumes = []
#     for r in ranked_resumes:
#         public_resumes.append({
#             "resume_name": r["resume_name"],
#             "candidate_name": r["candidate_name"],
#             "final_score": r["final_score"],
#             "matched_skills": r["matched_skills"],
#             "missing_skills": r["missing_skills"],
#             "analysis": r["analysis"]
#         })

#     result = {
#         "total_resumes": len(public_resumes),
#         "job_description_points": jd_points,
#         "ranked_resumes": public_resumes
#     }

#     # ----------------------------
#     # STEP 5: Save Output
#     # ----------------------------
#     output_dir.mkdir(parents=True, exist_ok=True)
#     with open(output_dir / "analysis_result.json", "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2)

#     return result











# from pathlib import Path
# import itertools
# import json

# from core.fextractor import extract_resume_text
# from core.fsummarizer import summarize_resume
# from core.fcompare_jd import compare_with_jd
# from core.fpairwise_compare import compare_two_resumes
# from core.futils import ensure_llm, force_json

# def jd_to_pointwise(llm, jd_text: str):
#     """
#     Convert Job Description into clean bullet points.
#     Returns a list of strings.
#     """
#     prompt = f"""
# Convert the following Job Description into clear and brief bullet points. Mention 2 sentences of the Job description first then continue with the bullet points.
# Each bullet should represent a key requirement, skill, or responsibility.
# Return ONLY bullet points, nothing else.

# Job Description:
# {jd_text}
# """

#     try:
#         response = llm.invoke(prompt)
#         points = [
#             line.strip("-• ").strip()
#             for line in response.split("\n")
#             if line.strip()
#         ]
#         return points
#     except Exception:
#         return []


# def run_resume_analysis(resume_paths, jd_text: str, output_dir: Path):
#     llm = ensure_llm()
#     jd_points = jd_to_pointwise(llm, jd_text)

#     summaries = {}
#     jd_evaluations = []

#     # ----------------------------
#     # STEP 1: Extract + Summarize
#     # ----------------------------
#     for path in resume_paths:
#         raw_text = extract_resume_text(path)
#         summary = summarize_resume(llm, raw_text)
#         summaries[path.name] = summary

#         jd_result = compare_with_jd(llm, summary, jd_text)
#         jd_evaluations.append({
#             "resume_name": path.name,
#             **jd_result
#         })

#     # ----------------------------
#     # STEP 2: Pairwise (Hidden)
#     # ----------------------------
#     pairwise_results = []
#     if len(resume_paths) > 1:
#         for a, b in itertools.combinations(resume_paths, 2):
#             r = compare_two_resumes(
#                 llm,
#                 a.name, json.dumps(summaries[a.name]),
#                 b.name, json.dumps(summaries[b.name])
#             )
#             pairwise_results.append(r)

#     # ----------------------------
#     # STEP 3: FINAL LLM DECISION
#     # ----------------------------
#     decision_prompt = f"""
# You are selecting the best candidate for the job.

# Inputs:
# 1. Resume vs JD evaluations
# 2. Optional resume-to-resume comparisons

# Decide:
# - Which resume is the best overall
# - Final suitability score (0-100)
# - 2-3 sentence explanation

# Return ONLY JSON:
# {{
#     "job_description_points": jd_points,
#     "winner_resume": decision.get("winner_resume"),
#     "final_score": decision.get("final_score"),
#     "reason": decision.get("reason")
# }}

# Resume vs JD Results:
# {jd_evaluations}

# Pairwise Results (optional signal):
# {pairwise_results}
# """

#     decision = force_json(llm.invoke(decision_prompt))

#     result = {
#         "job_description_points": jd_points,
#         "winner_resume": decision.get("winner_resume"),
#         "final_score": decision.get("final_score"),
#         "reason": decision.get("reason"),
#         "resume_breakdown": jd_evaluations
#     }

#     # ----------------------------
#     # SAVE OUTPUT FILE
#     # ----------------------------
#     output_dir.mkdir(exist_ok=True)

#     with open(output_dir / "analysis_result.json", "w", encoding="utf-8") as f:
#         json.dump(result, f, indent=2)

#     return result

