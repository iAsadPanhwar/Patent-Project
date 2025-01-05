from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
from crewai import Flow
from crewai.flow.flow import Flow, start, listen
from src.crews import PatentCrew, ScholarCrew, InsightsCrew, DocAnalystCrew, OpportunitiesImagesCrew, OpportunitiesCrew, TrendsCrew, NewsCrew, CostumersCrew, CompetitorsCrew

app = FastAPI()

class InsightRequest(BaseModel):
    selected_crews: List[str]
    input_data: Dict[str, Any]

class InsightGen(Flow):
    CREW_MAPPING = {
        "patents": PatentCrew().patent_crew(),
        "scholar": ScholarCrew().scholar_crew(),
        "trends": TrendsCrew().trends_crew(),
        "news": NewsCrew().news_crew(),
        "customers": CostumersCrew().costumers_crew(),
        "competitors": CompetitorsCrew().competitors_crew(),
    }

    def __init__(self, selected_crews=None, input_data=None):
        super().__init__()
        self.selected_crews = selected_crews if selected_crews else list(self.CREW_MAPPING.keys())
        self.input_data = input_data

    @start()
    async def start_parallel_execution(self):
        # Dynamically kick off only selected crews
        futures = {
            crew_name: self.CREW_MAPPING[crew_name].kickoff_async(inputs=self.input_data)
            for crew_name in self.selected_crews if crew_name in self.CREW_MAPPING
        }

        # Wait for all selected crews to finish
        results = await asyncio.gather(*futures.values(), return_exceptions=True)

        # Process and store results dynamically in the state
        for crew_name, result in zip(futures.keys(), results):
            self.state[f"{crew_name}_crew_results"] = (
                result.raw_output if hasattr(result, "raw_output") else str(result)
            )

        # Return combined results for use in subsequent tasks
        return {
            crew_name: self.state[f"{crew_name}_crew_results"] for crew_name in futures.keys()
        }

    @listen(start_parallel_execution)
    def check_and_trigger_doc_analyst(self, parallel_results):
        # Check if document is provided and trigger doc_analyst_crew
        if "document" in self.input_data and self.input_data["document"]:
            doc_analyst_input = {
                "documents": self.input_data["document"],
                "sector": self.input_data["sector"],
                "target_clients": self.input_data["target_clients"],
                "resources": self.input_data["resources"],
                "strategic_priorities": self.input_data["strategic_priorities"],
                "project_name": self.input_data["project_name"],
                "challenge_description": self.input_data["challenge_description"],
                "purpose": self.input_data["purpose"],
                "focus_constraints": self.input_data["focus_constraints"],
            }

            doc_analyst_output = DocAnalystCrew().doc_analyst_crew().kickoff(doc_analyst_input)
            doc_analyst_data = (
                doc_analyst_output.raw_output
                if hasattr(doc_analyst_output, "raw_output")
                else str(doc_analyst_output)
            )

            self.state["doc_analyst_results"] = doc_analyst_data

            return {**parallel_results, "doc_analyst": doc_analyst_data}
        else:
            return parallel_results

    @listen(check_and_trigger_doc_analyst)
    def generate_insights(self, previous_results):
        combined_output = {
            **{f"{crew_name}": self.state.get(f"{crew_name}_crew_results", "") for crew_name in self.selected_crews},
            "doc_summary": self.state.get("doc_analyst_results", ""),
            **self.input_data,
        }

        insights_output = InsightsCrew().insights_crew().kickoff(combined_output)
        insights_data = (
            insights_output.raw_output
            if hasattr(insights_output, "raw_output")
            else str(insights_output)
        )

        self.state["insights_crews_results"] = insights_data
        return insights_data

    @listen(generate_insights)
    def generate_opportunity_spaces(self, insights_data):
        opp_spaces_input = {
            "insights": insights_data,
            **self.input_data,
        }

        opp_spaces_output = OpportunitiesCrew().opp_spaces_crew().kickoff(opp_spaces_input)
        opp_spaces_data = (
            opp_spaces_output.raw_output
            if hasattr(opp_spaces_output, "raw_output")
            else str(opp_spaces_output)
        )

        self.state["opp_spaces_results"] = opp_spaces_data
        return opp_spaces_data

    @listen(generate_opportunity_spaces)
    def generate_opportunity_images(self, opp_spaces_data):
        opp_images_input = {
            "opportunity_spaces": opp_spaces_data,
            **self.input_data,
        }

        opp_images_output = OpportunitiesImagesCrew().opp_images_crew().kickoff(opp_images_input)
        opp_images_data = (
            opp_images_output.raw_output
            if hasattr(opp_images_output, "raw_output")
            else str(opp_images_output)
        )

        self.state["opp_images_results"] = opp_images_data
        return opp_images_data

    async def kickoff_async(self):
        result = await super().kickoff_async()
        return {
            **{f"{crew_name}_data": self.state.get(f"{crew_name}_crew_results") for crew_name in self.selected_crews},
            "insights_data": self.state.get("insights_crews_results"),
            "opp_spaces_data": self.state.get("opp_spaces_results"),
            "opp_images_data": self.state.get("opp_images_results"),
        }

@app.post("/generate-insights")
async def generate_insights(request: InsightRequest):
    flow = InsightGen(request.selected_crews, request.input_data)
    try:
        insights = await flow.kickoff_async()
        return {"status": "success", "data": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
