import json
import os
import chromadb
from chromadb.config import Settings
from ollama import embeddings

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "developers.json")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db_bge")

# -----------------------------
# Load developers data
# -----------------------------
with open(DATA_PATH, "r", encoding="utf-8") as f:
    developers = json.load(f)

print(f"Loaded {len(developers)} developer profiles")

# -----------------------------
# Initialize Chroma
# -----------------------------
client = chromadb.PersistentClient(
    path=CHROMA_PATH,
    settings=Settings(
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(
    name="developers"
)

collections = client.list_collections()
print("Available collections:")
for c in collections:
    print("-", c.name)
# -----------------------------
# Helper: build embedding text
# -----------------------------
def build_embedding_text(dev):
    return f"""
Name: {dev['name']}
Role: {dev['role']}
Seniority: {dev['seniority']}
Years of Experience: {dev['years_experience']}
Availability: {dev['availability']}
Timezone: {dev['timezone']}
Languages: {', '.join(dev['languages'])}
Skills: {', '.join(dev['skills'])}
Frameworks: {', '.join(dev['frameworks'])}
Domains: {', '.join(dev['domains'])}
Tools: {', '.join(dev['tools'])}
Project Types: {', '.join(dev['project_types'])}

Summary:
{dev['summary']}
""".strip()

# -----------------------------
# Insert into Chroma
# -----------------------------
for dev in developers:
    text = build_embedding_text(dev)

    embedding = embeddings(
        model="bge-m3",
        prompt=text
    )["embedding"]

    metadata = {
        "id": dev["id"],
        "role": dev["role"],
        "seniority": dev["seniority"],
        "availability": dev["availability"],
        "timezone": dev["timezone"],
        "years_experience": dev["years_experience"]
    }

    collection.add(
        ids=[dev["id"]],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )

print("✅ Chroma Vector DB built successfully!")