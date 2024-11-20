import json
import os
import requests
from crewai_tools import BaseTool

class NewsSearchTool(BaseTool):
    name: str = "Custom Serper Dev Tool"
    description: str = "Search the internet for news."

    # @record_tool(tool_name="Custom Serper Dev Tool")
    def _run(self, query: str) -> str:
        """
        Search the internet for news.
        """

        url = "https://google.serper.dev/news"

        payload = json.dumps({
            "q": query,
            "num": 10,
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

            # Log the entire response structure for debugging
            print("Response data structure:", json.dumps(response_data, indent=2))

            # Ensure 'news' exists and is a list
            if 'news' in response_data and isinstance(response_data['news'], list):
                if response_data['news']:  # Check if the list is not empty
                    response_data['news'] = [response_data['news'][0]]  # Keep only the first news item
                else:
                    response_data['news'] = []  # If no news items, set to an empty list
            else:
                response_data['news'] = []  # If 'news' key does not exist, set to an empty list

            # Convert the response data to a JSON string
            return json.dumps(response_data, indent=2)

        # Handle non-200 status code
        return f"Error: Received status code {response.status_code}"