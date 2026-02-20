import os
import json
import chromadb
from chromadb.config import Settings
from ollama import embeddings

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# -----------------------------
# Paths (اختر DB واحد بوضوح)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db_bge")  # ✅ نفس مسار build
EMBED_MODEL = "bge-m3"

# -----------------------------
# Lazy Chroma loader (مهم جدًا)
# -----------------------------
def get_collection():
    client = chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False)
    )

    collection = client.get_or_create_collection("developers")
    return collection

# -----------------------------
# Retrieve candidates
# -----------------------------
def retrieve_candidates(role, top_k=5):
    collection = get_collection()

    query_text = f"""
Role: {role.role}
Seniority: {role.seniority}
Required skills: {', '.join(role.skills)}
""".strip()

    query_embedding = embeddings(
        model=EMBED_MODEL,
        prompt=query_text
    )["embedding"]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    candidates = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        candidates.append({
            "id": meta["id"],
            "name": doc.split("\n")[0].replace("Name:", "").strip(),
            "role": meta["role"],
            "seniority": meta["seniority"],
            "availability": meta["availability"],
            "years_experience": meta["years_experience"],
        })

    return candidates

# -----------------------------
# LLM
# -----------------------------
llm = OllamaLLM(model="llama3", temperature=0.4)

prompt_template = PromptTemplate(
    input_variables=["project_analysis", "candidates"],
    template="""You are a senior engineering manager.

Return ONLY valid JSON.
Each team member MUST include a non-empty "reason" field.
If reason is missing, the response is invalid.

{{
  "team": [
    {{
      "id": string,
      "name": string,
      "role": string,
      "seniority": string,
      "reason": string
    }}
  ]
}}

Project:
{project_analysis}

Candidates:
{candidates}
"""
)

parser = JsonOutputParser()

def llm_select_team(project_analysis, candidates_by_role):
    prompt = prompt_template.format(
        project_analysis=json.dumps(project_analysis.model_dump(), indent=2),
        candidates=json.dumps(candidates_by_role, indent=2)
    )
    raw = llm.invoke(prompt)
    return parser.parse(raw[raw.find("{"): raw.rfind("}") + 1])

# -----------------------------
# Public API
# -----------------------------
def run_team_matching(project_analysis):
    candidates_by_role = {}

    for role in project_analysis.required_roles:
        candidates_by_role[role.role] = retrieve_candidates(role)

    final_team = llm_select_team(project_analysis, candidates_by_role)

    # ✅ طباعة النتيجة في الـ command line
    print("\n🤖 Final Team Selected:\n")
    print(json.dumps(final_team, indent=2, ensure_ascii=False))

    return final_team