from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from schemas.project_analysis import ProjectAnalysis
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=ProjectAnalysis)

prompt = PromptTemplate(
    template="""
You are a senior software architect.

Analyze the following project idea and return ONLY valid JSON.
Do not include explanations or extra text.

{format_instructions}

Project idea:
{idea}
""",
    input_variables=["idea"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)


def run_project_analysis(project_idea: str) -> ProjectAnalysis:
    llm = OllamaLLM(model="llama3", temperature=0.2)
    chain = prompt | llm | parser

    for attempt in range(5):
        print(f"\n🔁 Attempt {attempt + 1}")
        try:
            result = chain.invoke({"idea": project_idea})
            print("\n--- PARSED RESULT ---\n")
            print(result)
            return result  
            # ✅ كائن Pydantic
        except Exception as e:
            print("⚠️ Invalid JSON, retrying...\n")

    raise RuntimeError("Failed to get valid JSON from LLM after retries")