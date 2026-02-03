from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from pathlib import Path
import shutil
import uuid

from app.pipeline import run_resume_analysis

app = FastAPI(title="Resume Analyzer API", version="1.0.0")

# -----------------------------
# GLOBAL UPLOAD ROOT
# -----------------------------
UPLOAD_ROOT = Path("uploads")
UPLOAD_ROOT.mkdir(exist_ok=True)


# # -----------------------------
# # ROOT CHECK
# # -----------------------------
# @app.get("/")
# def root():
#     return {"message": "Resume Analyzer API is running"}


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================================================
# 1️⃣ UPLOAD JOB DESCRIPTION
# =========================================================
@app.post("/upload/jd")
async def upload_job_description(
    job_description: UploadFile = File(...)
):
    if not job_description.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt JD files allowed")

    jd_id = str(uuid.uuid4())

    jd_dir = UPLOAD_ROOT / jd_id / "jd"
    jd_dir.mkdir(parents=True, exist_ok=True)

    jd_path = jd_dir / job_description.filename

    with open(jd_path, "wb") as f:
        shutil.copyfileobj(job_description.file, f)

    return {
        "message": "Job description uploaded successfully",
        "jd_id": jd_id,
        "jd_file": str(jd_path)
    }


# =========================================================
# 2️⃣ UPLOAD RESUMES (SINGLE OR MULTIPLE)
# =========================================================
@app.post("/upload/resumes")
async def upload_resumes(
    jd_id: str,
    resumes: List[UploadFile] = File(...)
):
    base_dir = UPLOAD_ROOT / jd_id

    if not base_dir.exists():
        raise HTTPException(status_code=404, detail="Invalid JD ID")

    resume_dir = base_dir / "resumes"
    resume_dir.mkdir(exist_ok=True)

    saved_files = []

    for resume in resumes:
        if not resume.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF resumes allowed")

        resume_path = resume_dir / resume.filename
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)

        saved_files.append(resume.filename)

    return {
        "message": "Resumes uploaded successfully",
        "jd_id": jd_id,
        "uploaded_resumes": saved_files
    }


# =========================================================
# 3️⃣ ANALYZE (CORE LOGIC RUNS HERE)
# =========================================================
@app.post("/analyze/{jd_id}")
def analyze(jd_id: str):
    base_dir = UPLOAD_ROOT / jd_id

    jd_dir = base_dir / "jd"
    resume_dir = base_dir / "resumes"
    output_dir = base_dir / "outputs"

    if not jd_dir.exists():
        raise HTTPException(status_code=400, detail="Job description not found")

    if not resume_dir.exists():
        raise HTTPException(status_code=400, detail="Resumes not uploaded")

    jd_files = list(jd_dir.glob("*.txt"))
    if not jd_files:
        raise HTTPException(status_code=400, detail="JD file missing")

    resume_files = list(resume_dir.glob("*.pdf"))
    if not resume_files:
        raise HTTPException(status_code=400, detail="No resumes found")

    jd_text = jd_files[0].read_text(encoding="utf-8")

    # 🔥 CALL YOUR EXISTING PIPELINE
    result = run_resume_analysis(
        resume_paths=resume_files,
        jd_text=jd_text,
        output_dir=output_dir
    )

    return {
        "message": "Analysis completed successfully",
        "jd_id": jd_id,
        "output_files": {
            "json": str(output_dir / "analysis_result.json")
        },
        "result_summary": result
    }










# #FOR SERVER LLM 
# from fastapi import FastAPI, UploadFile, File
# from typing import List
# from pathlib import Path

# from app.pipeline import run_resume_analysis



# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="Resume Analyzer API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],   # later restrict in prod
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # include your routers below



# app = FastAPI(title="Resume Analyzer API") #start app

# BASE_DIR = Path(__file__).resolve().parent.parent
# UPLOADS = BASE_DIR / "uploads"
# OUTPUTS = BASE_DIR / "outputs"

# (UPLOADS / "resumes").mkdir(parents=True, exist_ok=True)
# (UPLOADS / "job_descriptions").mkdir(parents=True, exist_ok=True)
# OUTPUTS.mkdir(exist_ok=True)

# @app.get("/")
# def root():
#     return {"message": "Resume Analyzer API is running"}


# @app.get("/health") #to check if server is running
# def health():
#     return {"status": "ok"}


# @app.post("/analyze") #post is used for actions that process data
# async def analyze_resumes( #async allows: Non-blocking file reads & Better performance with multiple users
#     resumes: List[UploadFile] = File(...),
#     job_description: UploadFile = File(...)
# ):
#     resume_paths = []

#     for file in resumes: #save uploaded resumes
#         save_path = UPLOADS / "resumes" / file.filename
#         with open(save_path, "wb") as f:
#             f.write(await file.read())
#         resume_paths.append(save_path)

#     jd_path = UPLOADS / "job_descriptions" / job_description.filename #save uploaded job description
#     with open(jd_path, "wb") as f:
#         f.write(await job_description.read())

#     jd_text = jd_path.read_text(encoding="utf-8", errors="ignore") #read job description text and converts to plain text

#     result = run_resume_analysis(resume_paths, jd_text, OUTPUTS) #run analysis pipeline

#     return {  #API response structure
#         "message": "Analysis completed successfully",
#         "output_files": {
#             "json": "outputs/analysis_result.json",
#             "text": "outputs/analysis_result.txt"
#         },
#         "result_summary": result
#     }
