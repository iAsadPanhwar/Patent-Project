import json
import os
import requests
from crewai_tools import BaseTool

class PatentSearchTool(BaseTool):
    name: str = "Patent Search tool"
    description: str = "Search the internet for Patents."

    # @record_tool(tool_name="Patent search tool")
    def _run(self, query: str) -> str:
        """
        Search the internet for Patents.
        """

        url = "https://google.serper.dev/patents"

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

            # Log the entire response structure for debugging
            print("Response data structure:", json.dumps(response_data, indent=2))

            # Ensure 'figures' exists and is a list, and limit to 1 figure
            if 'figures' in response_data and isinstance(response_data['figures'], list):
                if response_data['figures']:  # Check if the list is not empty
                    response_data['figures'] = [response_data['figures'][0]]  # Keep only the first figure
                else:
                    response_data['figures'] = []  # If no figures, set to an empty list
            else:
                response_data['figures'] = []  # If 'figures' key does not exist, set to an empty list

            # Ensure only one URL and thumbnail, assuming they are nested under 'results' (adjust based on actual API response)
            if 'results' in response_data and isinstance(response_data['results'], list) and response_data['results']:
                first_result = response_data['results'][0]  # Get the first result only
                response_data['results'] = [first_result]  # Replace results with only the first result

                # Optionally, if URLs and thumbnails are within each result
                if 'url' in first_result:
                    first_result['url'] = first_result['url']
                if 'thumbnail' in first_result:
                    first_result['thumbnail'] = first_result['thumbnail']

            # Convert the response data to a JSON string and return
            return json.dumps(response_data, indent=2)

        # Handle non-200 status code
        return f"Error: Received status code {response.status_code}"