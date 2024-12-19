import asyncio
from crewai import Flow
from typing import Dict, Any
from crewai.flow.flow import Flow, start, listen
from src.crews import PatentCrew, ScholarCrew, InsightsCrew, DocAnalystCrew, OpportunitiesImagesCrew, OpportunitiesCrew
# Define the crews
patent_crew = PatentCrew().patent_crew()
scholar_crew = ScholarCrew().scholar_crew()
insights_crew = InsightsCrew().insights_crew()
doc_analyst_crew = DocAnalystCrew().doc_analyst_crew()
opps_images_crew = OpportunitiesImagesCrew().opp_images_crew()
opps_space_crew = OpportunitiesCrew().opp_spaces_crew()

# Define inputs
input_3 = {
    "document":"",
    "company_name": "Fastrock Coffee",
    "sector": "Food & Beverage / Coffee",
    "target_clients": "Retailers, foodservice providers, convenience stores, and hospitality industries",
    "resources": "Vertically integrated supply chain; advanced roasting and manufacturing facilities; expertise in sustainable sourcing",
    "strategic_priorities": "Expand global sourcing and supply chain capabilities; invest in sustainable and traceable supply chain practices; enhance product innovation",
    "project_name": "Utilization of Coffee By-Products for New Revenue Streams",
    "challenge_description": "Explore alternative uses for coffee by-products to create new revenue streams and reduce waste",
    "purpose": "Develop processes that are cost-effective and environmentally sustainable",
    "focus_constraints": "Ensure new processes are economically viable and align with the company's sustainability goals",
}


class InsightGen(Flow):
    @start()
    async def start_parallel_execution(self):
        try:
            patents_future = patent_crew.kickoff_async(inputs=self.input_data)
            scholar_future = scholar_crew.kickoff_async(inputs=self.input_data)
            
            patents_output, scholar_output = await asyncio.gather(patents_future, scholar_future)
            
            patents_data = patents_output.raw_output if hasattr(patents_output, 'raw_output') else str(patents_output)
            scholar_data = scholar_output.raw_output if hasattr(scholar_output, 'raw_output') else str(scholar_output)
            
            self.state["patents_crew_results"] = patents_data
            self.state["scholar_crew_results"] = scholar_data
            
            print("[DEBUG] Patents Crew Output:", patents_data)
            print("[DEBUG] Scholar Crew Output:", scholar_data)
            
            return {"patents": patents_data, "scholar": scholar_data}
        except Exception as e:
            print("[ERROR] Error in start_parallel_execution:", str(e))
            return {"error": str(e)}

    @listen(start_parallel_execution)
    async def check_and_trigger_doc_analyst(self, parallel_results: Dict[str, Any]) -> Dict[str, Any]:
        if "document" in self.input_data and self.input_data["document"]:
            doc_analyst_input = {
                "documents": self.input_data["document"],
                **{k: self.input_data[k] for k in [
                    "sector", "target_clients", "resources", "strategic_priorities",
                    "project_name", "challenge_description", "purpose", "focus_constraints"
                ]}
            }
            
            doc_analyst_output = await doc_analyst_crew.kickoff_async(doc_analyst_input)
            doc_analyst_data = doc_analyst_output.raw_output if hasattr(doc_analyst_output, "raw_output") else str(doc_analyst_output)
            
            self.state["doc_analyst_results"] = doc_analyst_data
            return {**parallel_results, "doc_analyst": doc_analyst_data}
        else:
            return parallel_results

    @listen(check_and_trigger_doc_analyst)
    async def generate_insights(self, previous_results: Dict[str, Any]) -> str:
        combined_output = {
            "patents": self.state.get("patents_crew_results", ""),
            "scholar": self.state.get("scholar_crew_results", ""),
            "doc_summary": self.state.get("doc_analyst_results", ""),
            **{k: self.input_data[k] for k in [
                "sector", "target_clients", "resources", "strategic_priorities",
                "project_name", "challenge_description", "purpose", "focus_constraints"
            ]}
        }
        
        insights_output = await insights_crew.kickoff_async(combined_output)
        insights_data = insights_output.raw_output if hasattr(insights_output, "raw_output") else str(insights_output)
        
        self.state["insights_crews_results"] = insights_data
        return insights_data

    @listen(generate_insights)
    async def generate_opportunity_spaces(self, insights_data: str) -> str:
        opp_spaces_input = {
            "insights": insights_data,
            **{k: self.input_data[k] for k in [
                "sector", "target_clients", "resources", "strategic_priorities",
                "project_name", "challenge_description", "purpose", "focus_constraints"
            ]}
        }
        
        opp_spaces_output = await opps_space_crew.kickoff_async(opp_spaces_input)
        opp_spaces_data = opp_spaces_output.raw_output if hasattr(opp_spaces_output, 'raw_output') else str(opp_spaces_output)
        
        self.state["opp_spaces_results"] = opp_spaces_data
        return opp_spaces_data

    @listen(generate_opportunity_spaces)
    async def generate_opportunity_images(self, opp_spaces_data: str) -> str:
        opp_images_input = {
            "opportunity_spaces": opp_spaces_data,
            **{k: self.input_data[k] for k in [
                "sector", "target_clients", "resources", "strategic_priorities",
                "project_name", "challenge_description", "purpose", "focus_constraints"
            ]}
        }
        
        opp_images_output = await opps_images_crew.kickoff_async(opp_images_input)
        opp_images_data = opp_images_output.raw_output if hasattr(opp_images_output, 'raw_output') else str(opp_images_output)
        
        self.state["opp_images_results"] = opp_images_data
        return opp_images_data

    async def kickoff_async(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.input_data = input_data
        result = await super().kickoff_async()
        return {
            "insights_data": self.state.get("insights_crews_results"),
            "opp_spaces_data": self.state.get("opp_spaces_results"),
            "opp_images_data": self.state.get("opp_images_results")
        }

# Run the flow
async def run_flow():
    flow = InsightGen()
    try:
        my_insights = await flow.kickoff_async(input_3)
        print("[INFO] Final Insights:", my_insights)
        return my_insights
    except Exception as e:
        print("[ERROR] Error in run_flow:", str(e))
        return {"error": str(e)}

if __name__ == "__main__":
    insights = asyncio.run(run_flow())
    print(insights)  # Optional: print the results