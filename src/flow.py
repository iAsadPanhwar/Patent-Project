import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Flow
from crewai.flow.flow import Flow, start, listen
from src.crews import PatentCrew, ScholarCrew, InsightsCrew

# Define the crews
patent_crew = PatentCrew().patent_crew()
scholar_crew = ScholarCrew().scholar_crew()
insights_crew = InsightsCrew().insights_crew()

# Define FastAPI app
app = FastAPI()

# Define the input schema for the API
class UserInput(BaseModel):
    company_name: str
    sector: str
    target_clients: str
    resources: str
    strategic_priorities: str
    project_name: str
    challenge_description: str
    purpose: str
    focus_constraints: str


class InsightGen(Flow):
    @start()
    async def start_parallel_execution(self, user_input: dict):
        try:
            # Kick off the Patent and Scholar crews asynchronously
            patents_future = patent_crew.kickoff_async(inputs=user_input)
            scholar_future = scholar_crew.kickoff_async(inputs=user_input)

            # Wait for both results
            patents_output, scholar_output = await asyncio.gather(patents_future, scholar_future)

            # Extract raw output from CrewOutput
            patents_data = patents_output.raw_output if hasattr(patents_output, 'raw_output') else str(patents_output)
            scholar_data = scholar_output.raw_output if hasattr(scholar_output, 'raw_output') else str(scholar_output)

            # Save to state for later use
            self.state["patents_crew_results"] = patents_data
            self.state["scholar_crew_results"] = scholar_data

            # Debugging logs
            print("[DEBUG] Patents Crew Output (raw):", patents_data)
            print("[DEBUG] Scholar Crew Output (raw):", scholar_data)

            return {"patents": patents_data, "scholar": scholar_data}

        except Exception as e:
            print("[ERROR] Error in start_parallel_execution:", str(e))
            raise

    @listen(start_parallel_execution)
    def generate_insights(self, parallel_results):
        try:
            # Extract `user_input` from state if available
            user_input = self.state.get("user_input", {})

            # Combine inputs for the Insights Crew
            combined_output = {
                **parallel_results,
                "sector": user_input.get("sector", ""),
                "target_clients": user_input.get("target_clients", ""),
                "resources": user_input.get("resources", ""),
                "strategic_priorities": user_input.get("strategic_priorities", ""),
                "project_name": user_input.get("project_name", ""),
                "challenge_description": user_input.get("challenge_description", ""),
                "purpose": user_input.get("purpose", ""),
                "focus_constraints": user_input.get("focus_constraints", ""),
            }

            # Debugging log
            print("[DEBUG] Combined Input for Insights Crew:", combined_output)

            # Kickoff Insights Crew
            insights = insights_crew.kickoff(combined_output)

            # Extract raw output
            insights_data = insights.raw_output if hasattr(insights, 'raw_output') else str(insights)

            # Debugging logs
            print("[DEBUG] Insights Crew Output (raw):", insights_data)

            # Save results in state
            self.state["insights_crews_results"] = insights_data
            return insights_data

        except Exception as e:
            print("[ERROR] Error in generate_insights:", str(e))
            return {"error": str(e)}


# Create an API endpoint to receive user input and process it
@app.post("/generate-insights/")
async def generate_insights_endpoint(user_input: UserInput):
    try:
        # Convert the user input to a dictionary
        user_input_dict = user_input.dict()

        # Instantiate the InsightGen flow
        flow = InsightGen()

        # Save the user input to flow state for use in `generate_insights`
        flow.state["user_input"] = user_input_dict

        # Run the flow and get results
        insights = await flow.start_parallel_execution(user_input_dict)

        # Generate insights based on the parallel execution results
        final_insights = flow.generate_insights(insights)

        return {"status": "success", "data": final_insights}
    except Exception as e:
        print("[ERROR] Error in generate_insights_endpoint:", str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

