from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from chains.orchestrator_chain import run_orchestrator
import json

app = FastAPI(title="Team Builder using AI")

# -----------------------------
# الصفحة الرئيسية
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Team Builder using AI</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg,#11c2cb,#1C110A);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                width: 90%;
                max-width: 800px;
                text-align: center;
            }
            textarea {
                background: #F2F0EF;
                width: 100%;
                height: 120px;
                padding: 0.5rem;
                margin-bottom: 1rem;
                border-radius: 0.5rem;
                border: none;
            }
            button {
                background: linear-gradient(135deg,#11c2cb,#1C110A);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                font-size: 1rem;
                border-radius: 0.5rem;
                cursor: pointer;
                transition: 0.3s;
                width: 100%;
            }
            button:hover {
                opacity: 0.9;
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Team Builder using AI</h1>
            <form action="/build_team" method="post">
                <textarea name="project_idea" placeholder="Enter Project Idea"></textarea>
                <button type="submit">Build Team</button>
            </form>
        </div>
    </body>
    </html>
    """

# -----------------------------
# صفحة النتائج
# -----------------------------
@app.post("/build_team", response_class=HTMLResponse)
async def build_team(project_idea: str = Form(...)):
    try:
        result = run_orchestrator(project_idea)
    except Exception as e:
        return f"<h2>Error: {e}</h2>"

    # Project Analysis HTML
    project_analysis_html = f'<div class="project-analysis"><pre>{json.dumps(result["project_analysis"], indent=2)}</pre></div>'

    # Team Members Cards
    team_html = ""
    for member in result['final_team']['team']:
        team_html += f"""
        <div class="card">
            <h3>{member['name']} ({member['role']})</h3>
            <p><b>Seniority:</b> {member['seniority']}</p>
            <p><b>Reason:</b> {member['reason']}</p>
        </div>
        """

    # Coordinator Report
    coordinator_html = f"<div class='card'><pre>{result['report']}</pre></div>"

    # Final HTML
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Team Builder using AI - Results</title>
        <style>
            body {{
                margin:0;
                font-family:'Segoe UI',sans-serif;
                background: linear-gradient(135deg,#11c2cb,#1C110A);
                display:flex;
                justify-content:center;
            }}
            .container {{
                background:white;
                padding:2rem;
                border-radius:1rem;
                box-shadow:0 10px 25px rgba(0,0,0,0.2);
                width:90%;
                max-width:800px;
                text-align:center;
            }}
            .card {{
                background:#f9f9f9;
                border-radius:1rem;
                padding:1rem;
                margin-bottom:1rem;
                box-shadow:0 5px 15px rgba(0,0,0,0.1);
                text-align:left;
            }}
            .card pre {{    
                width: 100%;
                white-space: pre-wrap;
                word-wrap: break-word;
                word-break: break-word;
                overflow-x: hidden;
            }}
            .card p {{
                margin-bottom: 0.75rem;
            }}
            .card small {{
                color: #6b7280;
                font-size: 0.8rem;
            }}
            .card hr {{
                border: none;
                border-top: 1px solid #e5e7eb;
                margin: 0.75rem 0;
            }}
            .project-analysis pre {{
                text-align: left;
                background: #f4f4f4;
                padding: 1rem;
                border-radius: 0.5rem;
                overflow-x: auto;
                white-space: pre-wrap;
                word-break: break-word;
            }}
            h2 {{
                color:#1C110A;
                margin-top:1rem;
            }}
            button {{
                background: linear-gradient(135deg,#11c2cb,#1C110A);
                color:white;
                border:none;
                padding:0.75rem 1.5rem;
                font-size:1rem;
                border-radius:0.5rem;
                cursor:pointer;
                transition:0.3s;
                width:100%;
            }}
            button:hover {{
                opacity:0.9;
                transform:scale(1.05);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Team Builder using AI</h1>

            <h2>📝 Project Analysis</h2>
            {project_analysis_html}

            <h2>🤖 Team Members</h2>
            {team_html}

            <h2>📌 Coordinator Report</h2>
            {coordinator_html}

            <form action="/" method="get">
                <button>⬅ Back</button>
            </form>
        </div>
    </body>
    </html>
    """