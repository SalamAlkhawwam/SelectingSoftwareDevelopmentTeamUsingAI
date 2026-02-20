import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

llm = OllamaLLM(model="llama3", temperature=0.6)

prompt_template = PromptTemplate(
    input_variables=["project", "team"],
    template="""
You are a senior project coordinator AI.

Project analysis:
{project}

Selected team:
{team}

Tasks:
1. Explain why each member was selected.
2. Highlight team strengths.
3. Point out weaknesses or risks.
4. Identify missing roles or seniority imbalance.
5. Provide short, actionable recommendations.

Do NOT return JSON. Do not overuse bullets.
"""
)

def run_coordinator_report(project_analysis, final_team):
    project_dict = project_analysis.model_dump() if hasattr(project_analysis, "dict") else project_analysis
    prompt = prompt_template.format(
        project=json.dumps(project_dict, indent=2),
        team=json.dumps(final_team, indent=2)
    )
    report = llm.invoke(prompt)
    print("\n🤖 Coordinator Agent Report:\n")
    print(report)
    return report