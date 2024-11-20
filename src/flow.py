import asyncio
from crewai import Flow
from crewai.flow.flow import Flow, start, listen
from src.crews import PatentCrew, ScholarCrew, InsightsCrew


patent_crew = PatentCrew().patent_crew()
scholer_crew = ScholarCrew().scholar_crew()
insights_crew = InsightsCrew().insights_crew()


input_3 = {
    # Company inputs
    "company_name": "Fastrock Coffee",
    "sector": "Food & Beverage / Coffee",
    "target_clients": "Retailers, foodservice providers, convenience stores, and hospitality industries",
    "resources": "Vertically integrated supply chain; advanced roasting and manufacturing facilities; expertise in sustainable sourcing",
    "strategic_priorities": "Expand global sourcing and supply chain capabilities; invest in sustainable and traceable supply chain practices; enhance product innovation",

    # Project inputs
    "project_name": "Utilization of Coffee By-Products for New Revenue Streams",
    "challenge_description": "Explore alternative uses for coffee by-products to create new revenue streams and reduce waste",
    "purpose": "Develop processes that are cost-effective and environmentally sustainable",
    "focus_constraints": "Ensure new processes are economically viable and align with the company's sustainability goals",
}

class InsightGen(Flow):
    @start()
    async def start_parallel_execution(self):
        patents_future = patent_crew.kickoff_async(inputs=input_3)
        scholar_future = scholer_crew.kickoff_async(inputs=input_3)

        patents_output, scholar_output = await asyncio.gather(patents_future, scholar_future)

        # Extract raw output from CrewOutput objects
        patents_data = patents_output.raw_output if hasattr(patents_output, 'raw_output') else str(patents_output)
        scholar_data = scholar_output.raw_output if hasattr(scholar_output, 'raw_output') else str(scholar_output)

        self.state["patents_crew_results"] = patents_data
        self.state["scholar_crew_results"] = scholar_data
        return {"patents": patents_data, "scholar": scholar_data}

    @listen(start_parallel_execution)
    def generate_insights(self, parallel_results):
        combined_output = {
            **parallel_results,
            "sector": input_3["sector"],
            "target_clients": input_3["target_clients"],
            "resources": input_3["resources"],
            "strategic_priorities": input_3["strategic_priorities"],
            "project_name": input_3["project_name"],
            "challenge_description": input_3["challenge_description"],
            "purpose": input_3["purpose"],
            "focus_constraints": input_3["focus_constraints"]
        }

        insights = insights_crew.kickoff(combined_output)

        # Extract raw output from CrewOutput
        insights_data = insights.raw_output if hasattr(insights, 'raw_output') else str(insights)

        self.state["insights_crews_results"] = insights_data
        return insights_data
    
# Run the flow
async def run_flow():
    flow = InsightGen()
    my_insights = await flow.kickoff_async()
    return my_insights

if __name__ == "__main__":
    # Use asyncio.run to execute the asynchronous function
    insights = asyncio.run(run_flow())
    print(insights)  # Optional: print the results