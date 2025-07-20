import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from tools import get_country_info
import asyncio

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

# Set up OpenAI-compatible Gemini client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Configure the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Set up run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

# Define the agent
agent = Agent(
    name="country_info_agent",
    instructions="""
You are a helpful assistant that takes a country name and uses a tool to provide:
- Capital
- Population
- Official languages
- Flag image
- Google Maps location link

You must always use the `get_country_info` tool when a country is mentioned.
Return results clearly in a readable format.
""",
    model=model,
    tools=[get_country_info],
)

async def main():
    print("🌍 Welcome to the Country Info CLI App!")
    while True:
        country = input("Enter country name (or type 'exit' to quit): ").strip()
        if country.lower() == "exit":
            break

        query = f"Give me all details about {country}"
        result = await Runner.run(agent, query, run_config=config)
        info = result.output if isinstance(result.output, dict) else {}

        if info.get("error"):
            print(f"❌ {info['error']}")
        else:
            print(f"""\n📍 {info.get("country", "N/A")}
🏛 Capital: {info.get("capital", "N/A")}
🗣 Languages: {info.get("languages", "N/A")}
👥 Population: {info.get("population", "N/A")}
🌍 View on Map: {info.get("map_link", "N/A")}
🚩 Flag URL: {info.get("flag_url", "N/A")}\n""")

# Run the app
if __name__ == "__main__":
    asyncio.run(main())
