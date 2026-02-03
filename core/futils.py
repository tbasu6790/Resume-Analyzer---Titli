import json
import re
import io
import zipfile
import matplotlib.pyplot as plt
import pandas as pd

from langchain_ollama import OllamaLLM


# -------------------------------------------------------------------
# LLM INITIALIZER (OLLAMA SERVER)
# -------------------------------------------------------------------

def ensure_llm():
    """
    Connects to remote Ollama server running LLaMA.
    """
    try:
        return OllamaLLM(
            model="llama3.1:8b",
            base_url="http://192.168.11.97:11434",
            temperature=0.0,
            top_p=1.0,
            top_k=1,
            num_predict=512
        )
    except Exception as e:
        raise RuntimeError(f"Ollama server not reachable: {e}")


# -------------------------------------------------------------------
# JSON SAFETY
# -------------------------------------------------------------------

def force_json(txt: str):
    try:
        return json.loads(txt)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", txt)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    return {}


# -------------------------------------------------------------------
# OPTIONAL BACKEND HELPERS
# -------------------------------------------------------------------

def make_heatmap(pairwise_results, names):
    import numpy as np

    n = len(names)
    idx = {n: i for i, n in enumerate(names)}
    M = np.zeros((n, n))

    for p in pairwise_results:
        i = idx[p["resume_a"]]
        j = idx[p["resume_b"]]
        M[i][j] = p["match_score"]
        M[j][i] = p["match_score"]

    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.imshow(M, cmap="viridis")
    plt.colorbar(cax)

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_yticklabels(names)

    plt.close(fig)
    return fig


def create_zip(jd_ranked, pairwise_results, final_ranking, summaries):
    files = []

    for r in jd_ranked:
        name = r["resume_name"]
        data = {
            "resume_name": name,
            "summary": summaries.get(name, {}),
            "jd_result": r
        }
        files.append((f"{name}_analysis.json", json.dumps(data, indent=2)))

    files.append(("pairwise.json", json.dumps(pairwise_results, indent=2)))
    files.append(("final_ranking.json", json.dumps(final_ranking, indent=2)))

    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as z:
        for fname, content in files:
            z.writestr(fname, content)

    mem.seek(0)
    return mem.read()



# #FOR SERVER LLM 
# import json
# import re
# import io
# import zipfile
# import matplotlib.pyplot as plt
# import pandas as pd
# from langchain_ollama import OllamaLLM

# # import streamlit as st   #REMOVED (Streamlit not used)

# def ensure_llm():
#     try:
#         return OllamaLLM(
#             model="llama3.1",
#             base_url="http://192.168.10.80:11434",
#             temperature=0.0,
#             top_p=1.0,
#             top_k=1,
#             num_predict=512
#         )
#     except Exception as e:
#         # st.error(f"Ollama remote server not reachable: {e}")
#         # st.stop()
#         raise RuntimeError(f"Ollama remote server not reachable: {e}")

# def force_json(txt: str):
#     try:
#         return json.loads(txt)
#     except:
#         pass

#     m = re.search(r"\{[\s\S]*\}", txt)
#     if m:
#         try:
#             return json.loads(m.group(0))
#         except:
#             pass

#     return {}

# # ---- OPTIONAL UI HELPERS (LEFT INTACT, UNUSED BY FASTAPI) ----

# def make_heatmap(pairwise_results, names):
#     import numpy as np
#     n = len(names)
#     idx = {n: i for i, n in enumerate(names)}
#     M = np.zeros((n, n))

#     for p in pairwise_results:
#         i = idx[p["resume_a"]]
#         j = idx[p["resume_b"]]
#         M[i][j] = p["match_score"]
#         M[j][i] = p["match_score"]

#     fig, ax = plt.subplots(figsize=(6, 5))
#     cax = ax.imshow(M, cmap="viridis")
#     plt.colorbar(cax)
#     ax.set_xticks(range(n))
#     ax.set_yticks(range(n))
#     ax.set_xticklabels(names, rotation=45, ha="right")
#     ax.set_yticklabels(names)
#     plt.close(fig)
#     return fig  # backend-safe (no st.pyplot)

# def create_zip(jd_ranked, pairwise_results, final_ranking, summaries):
#     files = []

#     for r in jd_ranked:
#         name = r["resume_name"]
#         data = {
#             "resume_name": name,
#             "summary": summaries[name],
#             "jd_result": r
#         }
#         files.append((f"{name}_analysis.json", json.dumps(data, indent=2)))

#     files.append(("pairwise.json", json.dumps(pairwise_results, indent=2)))
#     files.append(("final_ranking.json", json.dumps(final_ranking, indent=2)))

#     mem = io.BytesIO()
#     with zipfile.ZipFile(mem, "w") as z:
#         for fname, content in files:
#             z.writestr(fname, content)

#     mem.seek(0)
#     return mem.read()
