import asyncio
from crewai import Flow
from typing import Dict, Any
from crewai.flow.flow import Flow, start, listen
from src.crews import PatentCrew, ScholarCrew, InsightsCrew, DocAnalystCrew, OpportunitiesImagesCrew, OpportunitiesCrew, TrendsCrew, NewsCrew, CostumersCrew, CompetitorsCrew
from src.config import DEFAULT_INPUT
import json
from datetime import datetime

my_input = DEFAULT_INPUT

class InsightGen(Flow):
    CREW_MAPPING = {
        "patents": PatentCrew().patent_crew(),
        "scholar": ScholarCrew().scholar_crew(),
        "trends": TrendsCrew().trends_crew(),
        "news": NewsCrew().news_crew(),
        "customers": CostumersCrew().costumers_crew(),
        "competitors": CompetitorsCrew().competitors_crew(),
    }
    
    def __init__(self, selected_crews=None):
        super().__init__()
        self.selected_crews = selected_crews if selected_crews else list(self.CREW_MAPPING.keys())

    @start()
    async def start_parallel_execution(self):
        # Dynamically kick off only selected crews
        futures = {
            crew_name: self.CREW_MAPPING[crew_name].kickoff_async(inputs=my_input)
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

#####################################################################################

    @listen(start_parallel_execution)
    def check_and_trigger_doc_analyst(self, parallel_results):
        # Check if document is provided and trigger doc_analyst_crew
        if "document" in my_input and my_input["document"]:
            doc_analyst_input = {
                "documents": my_input["document"],
                "sector": my_input["sector"],
                "target_clients": my_input["target_clients"],
                "resources": my_input["resources"],
                "strategic_priorities": my_input["strategic_priorities"],
                "project_name": my_input["project_name"],
                "challenge_description": my_input["challenge_description"],
                "purpose": my_input["purpose"],
                "focus_constraints": my_input["focus_constraints"],
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

#####################################################################################

    @listen(check_and_trigger_doc_analyst)
    def generate_insights(self, previous_results):
        combined_output = {
            **{f"{crew_name}": self.state.get(f"{crew_name}_crew_results", "") for crew_name in self.selected_crews},
            "doc_summary": self.state.get("doc_analyst_results", ""),
            "sector": my_input["sector"],
            "target_clients": my_input["target_clients"],
            "resources": my_input["resources"],
            "strategic_priorities": my_input["strategic_priorities"],
            "project_name": my_input["project_name"],
            "challenge_description": my_input["challenge_description"],
            "purpose": my_input["purpose"],
            "focus_constraints": my_input["focus_constraints"],
        }

        insights_output = InsightsCrew().insights_crew().kickoff(combined_output)
        insights_data = (
            insights_output.raw_output
            if hasattr(insights_output, "raw_output")
            else str(insights_output)
        )

        self.state["insights_crews_results"] = insights_data
        return insights_data

#####################################################################################

    @listen(generate_insights)
    def generate_opportunity_spaces(self, insights_data):
        opp_spaces_input = {
            "insights": insights_data,
            "sector": my_input["sector"],
            "target_clients": my_input["target_clients"],
            "resources": my_input["resources"],
            "strategic_priorities": my_input["strategic_priorities"],
            "project_name": my_input["project_name"],
            "challenge_description": my_input["challenge_description"],
            "purpose": my_input["purpose"],
            "focus_constraints": my_input["focus_constraints"],
        }

        opp_spaces_output = OpportunitiesCrew().opp_spaces_crew().kickoff(opp_spaces_input)
        opp_spaces_data = (
            opp_spaces_output.raw_output
            if hasattr(opp_spaces_output, "raw_output")
            else str(opp_spaces_output)
        )

        self.state["opp_spaces_results"] = opp_spaces_data
        return opp_spaces_data

#####################################################################################

    @listen(generate_opportunity_spaces)
    def generate_opportunity_images(self, opp_spaces_data):
        opp_images_input = {
            "opportunity_spaces": opp_spaces_data,
            "sector": my_input["sector"],
            "target_clients": my_input["target_clients"],
            "resources": my_input["resources"],
            "strategic_priorities": my_input["strategic_priorities"],
            "project_name": my_input["project_name"],
            "challenge_description": my_input["challenge_description"],
            "purpose": my_input["purpose"],
            "focus_constraints": my_input["focus_constraints"],
        }

        opp_images_output = OpportunitiesImagesCrew().opp_images_crew().kickoff(opp_images_input)
        opp_images_data = (
            opp_images_output.raw_output
            if hasattr(opp_images_output, "raw_output")
            else str(opp_images_output)
        )

        self.state["opp_images_results"] = opp_images_data
        return opp_images_data

#####################################################################################

    async def kickoff_async(self):
        result = await super().kickoff_async()
        return {
            **{f"{crew_name}_data": self.state.get(f"{crew_name}_crew_results") for crew_name in self.selected_crews},
            "insights_data": self.state.get("insights_crews_results"),
            "opp_spaces_data": self.state.get("opp_spaces_results"),
            "opp_images_data": self.state.get("opp_images_results"),
        }

def write_results_to_markdown(insights: Dict[str, Any], filename: str = "insights_results.md"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Insights Results\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for key, value in insights.items():
            f.write(f"## {key.replace('_', ' ').title()}\n\n")
            if isinstance(value, dict):
                f.write("```json\n")
                f.write(json.dumps(value, indent=2))
                f.write("\n```\n\n")
            else:
                f.write(f"{value}\n\n")

async def run_flow(selected_crews: list = None):
    selected_crews = selected_crews or ["patents", "scholar", "trends", "news"]
    flow = InsightGen(selected_crews)
    try:
        my_insights = await flow.kickoff_async()
        print("[INFO] Final Insights generated. Writing to file...")
        write_results_to_markdown(my_insights)
        print("[INFO] Results saved to insights_results.md")
        return my_insights
    except Exception as e:
        error_message = f"[ERROR] Error in run_flow: {str(e)}"
        print(error_message)
        write_results_to_markdown({"error": error_message})
        return {"error": error_message}

if __name__ == "__main__":
    insights = asyncio.run(run_flow())
    print("Results have been saved to insights_results.md")