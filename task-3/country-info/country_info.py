import os
import asyncio
import requests
from typing import Optional, Dict
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
)
from agents.run import RunConfig

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# Set up OpenAI-compatible Gemini client (via proxy or compatibility layer)
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Configure the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

# Tool: Get Country Info
@function_tool
def get_country_info(country_name: str) -> Dict[str, Optional[str]]:
    """
    Returns detailed information about a given country using the REST Countries API.
    """
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        if response.status_code != 200:
            return {"error": "Country not found or API error."}

        data = response.json()[0]

        return {
            "country": data.get("name", {}).get("common", "Unknown"),
            "capital": data.get("capital", ["Unknown"])[0],
            "population": f"{data.get('population', 'Unknown'):,}",
            "languages": ", ".join(data.get("languages", {}).values()) or "Unknown",
            "flag_url": data.get("flags", {}).get("png"),
            "map_link": data.get("maps", {}).get("googleMaps", ""),
        }

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# Main function
async def main():
    print("🌍 Welcome to Country Info CLI!")
    
    agent = Agent(
        name="country_info_agent",
        instructions="""
You are a helpful assistant that takes a country name and uses a tool to provide:
- Capital
- Population
- Official languages


You must always use the `get_country_info` tool when a country is mentioned.
Return results clearly in a readable format.
""",
        model=model,
        tools=[get_country_info],
    )

    while True:
        country = input("\nEnter country name (or type 'exit' to quit): ").strip()
        if country.lower() == "exit":
            print("👋 Exiting...")
            break

        query = f"Give me all details about {country}"
        result = await Runner.run(agent, query, run_config=config)
        print(result.final_output)


# Run the app
if __name__ == "__main__":
    asyncio.run(main())
        
        



