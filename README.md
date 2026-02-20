# Selecting Software Development Teams Using AI

This repository contains the implementation of a **Master’s Degree project** focused on applying Artificial Intelligence techniques to the problem of **software development team selection**.

The project proposes an intelligent system that analyzes project requirements, retrieves suitable developer profiles, and selects an optimal team using Large Language Models (LLMs) combined with Retrieval-Augmented Generation (RAG).

---

## Project Motivation

Team formation in software engineering is a complex decision-making process that depends on multiple factors such as skills, experience, availability, and role balance.  
This research explores how **AI-driven semantic retrieval and reasoning** can support and improve this process compared to traditional manual approaches.

---

## System Design

The proposed system adopts a **pipeline-based architecture** composed of four sequential stages, where each stage incrementally contributes to the final team selection decision.

### 1. Project Analysis  
A Large Language Model (LLM) analyzes the project description and extracts structured requirements, including required roles, seniority levels, and technical skills.

### 2. Candidate Retrieval (RAG)  
Relevant developer profiles are retrieved from a vector database using **semantic similarity search**.  
This stage implements a **Retrieval-Augmented Generation (RAG)** approach, grounding the system’s reasoning in real developer data stored as vector embeddings.

### 3. Team Selection  
An LLM reasons over the retrieved candidates while considering experience balance, role diversity, availability constraints, and seniority distribution. The output is a structured team composition.

### 4. Result Interpretation and Explanation  
A final LLM-based reasoning stage generates **explicit natural language explanations** for each selected team member, justifying the selection decisions and improving system transparency and interpretability.

Although multiple LLM-based components are employed, the overall architecture is best described as a **single agent with multiple sequential reasoning stages**, rather than a fully autonomous multi-agent system.

---

## Data Representation

Developer profiles are stored in a structured JSON dataset.  
Semantic fields (e.g., skills, experience, domains, and summaries) are embedded into vector representations, while structured attributes (e.g., role, seniority, availability) are stored as metadata to support filtering and constraints.

---

## Vector Databases and Embeddings

Two independent ChromaDB vector databases are implemented for experimental comparison:

- **BGE-based ChromaDB** using `bge-m3`
- **Nomic-based ChromaDB** using `nomic-embed-text`

Both databases are built from the same dataset to evaluate embedding behavior under identical conditions.

---

## Retrieval-Augmented Generation (RAG)

The system implements RAG by grounding LLM reasoning in retrieved developer profiles rather than relying solely on model-generated knowledge.  
This approach improves relevance, transparency, and controllability of the final team selection.

---

## Technologies Used

- Python
- FastAPI
- LangChain
- ChromaDB
- Ollama (local LLM execution)
- Embedding Models: BGE, Nomic
- LLMs: LLaMA 3, Mistral
- Frontend: HTML, CSS
- Environment: Miniconda / Anaconda

---

## Output

The system produces a final software development team in structured JSON format.  
Each selected team member includes an explicit justification, supporting explainability and academic analysis.

---

## Conclusion

This project demonstrates the feasibility of using AI-driven semantic retrieval and LLM-based reasoning as a decision-support tool for software team selection.  
The results highlight the potential of RAG-based systems in human-centric decision-making tasks within software engineering.

---
