import json
import os

# Agents
from chains.project_analysis_chain import run_project_analysis
from chains.team_matching_chain import run_team_matching
from chains.coordinator_chain import run_coordinator_report

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
PROJECT_ANALYSIS_PATH = os.path.join(BASE_DIR, "project_analysis.json")
FINAL_TEAM_PATH = os.path.join(BASE_DIR, "final_team.json")
REPORT_PATH = os.path.join(BASE_DIR, "coordinator_report.txt")

# -----------------------------
# Orchestrator
# -----------------------------
def run_orchestrator(project_idea: str):
    print("\n🚀 Starting AI Team Builder Pipeline...\n")

    # 1️⃣ Project Analysis
    print("🧠 Running Project Analysis Agent...")
    project_analysis = run_project_analysis(project_idea)
    project_analysis_dict = project_analysis.model_dump()  # ✅ تحويل لكائن dict

    # Save project analysis
    with open(PROJECT_ANALYSIS_PATH, "w", encoding="utf-8") as f:
        json.dump(project_analysis_dict, f, indent=2)

    # 2️⃣ Team Matching
    print("\n🧩 Running Team Matching Agent...")
    final_team = run_team_matching(project_analysis)  # يمكن تمرير كائن Pydantic مباشرة
    with open(FINAL_TEAM_PATH, "w", encoding="utf-8") as f:
        json.dump(final_team, f, indent=2)

    print("\n🤖 Running Coordinator Agent...")
    report = run_coordinator_report(project_analysis, final_team)  # تحويل داخلي
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print("\n✅ Pipeline completed successfully!\n")
    return {
        "project_analysis": project_analysis_dict,
        "final_team": final_team,
        "report": report
    }


# -----------------------------
# Run (CLI test)
# -----------------------------
if __name__ == "__main__":
    idea = """
    I want to build a SaaS platform for managing online payments
    for small businesses. The system needs to be scalable,
    secure, and API-first.
    """
    result = run_orchestrator(idea)

    print("\n📌 FINAL OUTPUT SUMMARY:\n")
    print(json.dumps(result["final_team"], indent=2))