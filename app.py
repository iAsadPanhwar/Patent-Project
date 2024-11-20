from fastapi import FastAPI
from pydantic import BaseModel
from src.flow import run_flow
import asyncio

app = FastAPI()

class InputData(BaseModel):
    company_name: str
    sector: str
    target_clients: str
    resources: str
    strategic_priorities: str
    project_name: str
    challenge_description: str
    purpose: str
    focus_constraints: str

@app.post("/generate-insights")
async def generate_insights(input_data: InputData):
    insights = await run_flow(input_data.dict())
    return {"insights": insights}