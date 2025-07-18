import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel , function_tools
from agents.run import RunConfig
import asyncio

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tools
def get_capital(country_name: str) -> str:
    """
    get the name of capital of the country name given by the user in input.
    """
@function_tools
def get_language(language: str) -> str:
    """
    get the name of language of the country name given by the user in input.
    """
@function_tools
def get_population(population: int) -> str:
    """
    get the total number of population of the country name given by the user in input.
    """    

async def main():
    agent = Agent(
        name="country info agent",
        instructions="""You are country info bot.
        You will be given a country name and you will use the tools to get the capital, language and population of the country.
        Use the tools to get the information and return it in a single response.
        return the response in the following format:
        "The capital of {country_name} is {capital}, the language is {language} and the population is {population}.",
        """,
        model=model
        tools=[get_capital, get_language, get_population]
    )
    
    message = "What is the capital, language and population of India?"

    result = await Runner.run(agent, message, run_config=config)
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    #
    #⿣ Country Info Bot (Using Tools)
#⿣ Country Info Bot (Using Tools)
# File name: country_info_toolkit.py

# Create 3 tool agents:

# One tells the capital of a country

# One tells the language

# One tells the population
# An orchestrator agent takes the country name and uses all 3 tools to give complete info.

