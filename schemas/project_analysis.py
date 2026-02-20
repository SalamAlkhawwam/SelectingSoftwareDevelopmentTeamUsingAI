from pydantic import BaseModel
from typing import List


class RequiredRole(BaseModel):
    role: str
    seniority: str
    skills: List[str]


class ProjectAnalysis(BaseModel):
    project_type: str
    domains: List[str]
    required_roles: List[RequiredRole]
    tech_stack: List[str]
    team_size: int