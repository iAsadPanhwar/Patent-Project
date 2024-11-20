import json
import os
import requests
from crewai_tools import BaseTool

class ScholarSearchTool(BaseTool):
    name: str = "Scholar search tool"
    description: str = "Search the internet for academic articles."

    # @record_tool(tool_name="Scholar Search Tool")
    def _run(self, query: str) -> str:
        """
        Search the internet for academic articles.
        """

        url = "https://google.serper.dev/scholar"

        payload = json.dumps({
            "q": query,
            "num": 5,
            "autocorrect": False,
            "tbs": "qdr:d"
        })

        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()

        # Convert the news data back to a JSON string
        return json.dumps(response_data, indent=2)