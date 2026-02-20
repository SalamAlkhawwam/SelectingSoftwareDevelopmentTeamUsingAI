import os
import pandas as pd
import chromadb
from chromadb.config import Settings
from ollama import embeddings

# --------------------------
# 1️⃣ Paths
# --------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CHROMA_PATHS = {
    "Nomic": os.path.join(BASE_DIR, "chroma_db_nomic"),
    "BGE": os.path.join(BASE_DIR, "chroma_db_bge"),
}

# --------------------------
# 2️⃣ Metrics
# --------------------------
def precision_at_k(predicted, ground_truth, k):
    return len(set(predicted[:k]) & set(ground_truth)) / k

def recall_at_k(predicted, ground_truth, k):
    return len(set(predicted[:k]) & set(ground_truth)) / len(ground_truth) if ground_truth else 0

def mean_reciprocal_rank(predicted, ground_truth):
    for i, p in enumerate(predicted, start=1):
        if p in ground_truth:
            return 1 / i
    return 0

# --------------------------
# 3️⃣ Embedding functions
# --------------------------
def get_nomic_embedding(text):
    return embeddings(
        model="nomic-embed-text",
        prompt=text
    )["embedding"]

def get_bge_embedding(text):
    return embeddings(
        model="bge-m3",
        prompt=text
    )["embedding"]

embedding_models = {
    "Nomic": get_nomic_embedding,
    "BGE": get_bge_embedding
}

# --------------------------
# 4️⃣ Evaluate one model
# --------------------------
def evaluate_model(role, seniority, skills, ground_truth_ids, model_name, embed_func, top_k=5):
    # ✅ افتح Chroma الصحيح
    client = chromadb.PersistentClient(
        path=CHROMA_PATHS[model_name],
        settings=Settings(anonymized_telemetry=False)
    )

    # ✅ تأكد أن collection موجودة
    collections = [c.name for c in client.list_collections()]
    if "developers" not in collections:
        raise RuntimeError(f"Collection 'developers' غير موجودة في {CHROMA_PATHS[model_name]}")

    collection = client.get_collection("developers")

    query_text = f"{role} {seniority} {' '.join(skills)}"
    query_embedding = embed_func(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["metadatas", "distances"]
    )

    predicted_ids = [m["id"] for m in results["metadatas"][0]]

    return {
        "model": model_name,
        "precision@k": precision_at_k(predicted_ids, ground_truth_ids, top_k),
        "recall@k": recall_at_k(predicted_ids, ground_truth_ids, top_k),
        "MRR": mean_reciprocal_rank(predicted_ids, ground_truth_ids),
        "predicted_ids": predicted_ids
    }

# --------------------------
# 5️⃣ Run evaluation
# --------------------------
role = "DevOps Engineer"
seniority = "Senior"
skills = ["cloud", "security", "kubernetes"]
ground_truth_ids = ["devops_001", "devops_006", "devops_010"]

results = []

for model_name, embed_func in embedding_models.items():
    print(f"\n🔍 Evaluating {model_name}")
    results.append(
        evaluate_model(
            role,
            seniority,
            skills,
            ground_truth_ids,
            model_name,
            embed_func,
            top_k=3
        )
    )

df = pd.DataFrame(results)
print("\n📊 Results:")
print(df)