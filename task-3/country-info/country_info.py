# # # # # # import os
# # # # # # import asyncio
# # # # # # import requests
# # # # # # from typing import Optional, Dict
# # # # # # from dotenv import load_dotenv
# # # # # # from agents import (
# # # # # #     Agent,
# # # # # #     Runner,
# # # # # #     AsyncOpenAI,
# # # # # #     OpenAIChatCompletionsModel,
# # # # # #     function_tool,
# # # # # # )
# # # # # # from agents.run import RunConfig

# # # # # # # Load environment variables
# # # # # # load_dotenv()
# # # # # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # # # # if not GEMINI_API_KEY:
# # # # # #     raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# # # # # # # Set up OpenAI-compatible Gemini client (via proxy or compatibility layer)
# # # # # # external_client = AsyncOpenAI(
# # # # # #     api_key=GEMINI_API_KEY,
# # # # # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# # # # # # )

# # # # # # # Configure the model
# # # # # # model = OpenAIChatCompletionsModel(
# # # # # #     model="gemini-2.0-flash",
# # # # # #     openai_client=external_client
# # # # # # )

# # # # # # # Run configuration
# # # # # # config = RunConfig(
# # # # # #     model=model,
# # # # # #     model_provider=external_client,
# # # # # #     tracing_disabled=True,
# # # # # # )

# # # # # # # Tool: Get Country Info
# # # # # # @function_tool
# # # # # # def get_country_info(country_name: str) -> Dict[str, Optional[str]]:
# # # # # #     """
# # # # # #     Returns detailed information about a given country using the REST Countries API.
# # # # # #     """
# # # # # #     try:
# # # # # #         response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
# # # # # #         if response.status_code != 200:
# # # # # #             return {"error": "Country not found or API error."}

# # # # # #         data = response.json()[0]

# # # # # #         return {
# # # # # #             "country": data.get("name", {}).get("common", "Unknown"),
# # # # # #             "capital": data.get("capital", ["Unknown"])[0],
# # # # # #             "population": f"{data.get('population', 'Unknown'):,}",
# # # # # #             "languages": ", ".join(data.get("languages", {}).values()) or "Unknown",
# # # # # #             "flag_url": data.get("flags", {}).get("png"),
# # # # # #             "map_link": data.get("maps", {}).get("googleMaps", ""),
# # # # # #         }

# # # # # #     except Exception as e:
# # # # # #         return {"error": f"An error occurred: {str(e)}"}

# # # # # # # Main function
# # # # # # async def main():
# # # # # #     print("🌍 Welcome to Country Info CLI!")
    
# # # # # #     agent = Agent(
# # # # # #         name="country_info_agent",
# # # # # #         instructions="""
# # # # # # You are a helpful assistant that takes a country name and uses a tool to provide:
# # # # # # - Capital
# # # # # # - Population
# # # # # # - Official languages


# # # # # # You must always use the `get_country_info` tool when a country is mentioned.
# # # # # # Return results clearly in a readable format.
# # # # # # """,
# # # # # #         model=model,
# # # # # #         tools=[get_country_info],
# # # # # #     )

# # # # # #     while True:
# # # # # #         country = input("\nEnter country name (or type 'exit' to quit): ").strip()
# # # # # #         if country.lower() == "exit":
# # # # # #             print("👋 Exiting...")
# # # # # #             break

# # # # # #         query = f"Give me all details about {country}"
# # # # # #         result = await Runner.run(agent, query, run_config=config)
# # # # # #         print(result.final_output)

# # # # # # #         # info = result.final_output if isinstance(result.final_output, dict) else {}
# # # # # # #         info = result.tool_outputs[0].output if result.tool_outputs else {"error": "Tool did not return any output."
# # # # # # # }


# # # # # # #         if info.get("error"):
# # # # # # #             print(f"❌ {info['error']}")
# # # # # # #         else:
# # # # # # #             print(f"""\n📍 {info.get("country", "N/A")}
# # # # # # # 🏛 Capital: {info.get("capital", "N/A")}
# # # # # # # 🗣 Languages: {info.get("languages", "N/A")}
# # # # # # # 👥 Population: {info.get("population", "N/A")}
# # # # # # # 🌍 View on Map: {info.get("map_link", "N/A")}
# # # # # # # 🚩 Flag URL: {info.get("flag_url", "N/A")}\n""")

# # # # # # # Run the app
# # # # # # if __name__ == "__main__":
# # # # # #     asyncio.run(main())
        
        



# # # # # # import os
# # # # # # import requests
# # # # # # from dotenv import load_dotenv
# # # # # # import chainlit as cl

# # # # # # from agents import (
# # # # # #     Agent,
# # # # # #     Runner,
# # # # # #     AsyncOpenAI,
# # # # # #     OpenAIChatCompletionsModel,
# # # # # #     function_tool,
# # # # # # )
# # # # # # from agents.run import RunConfig

# # # # # # # Load environment variables
# # # # # # load_dotenv()
# # # # # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # # # # if not GEMINI_API_KEY:
# # # # # #     raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# # # # # # # Gemini (OpenAI-compatible) client
# # # # # # external_client = AsyncOpenAI(
# # # # # #     api_key=GEMINI_API_KEY,
# # # # # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai",
# # # # # # )
# # # # # #  # Configure the model
# # # # # # model = OpenAIChatCompletionsModel(
# # # # # #     model="gemini-2.0-flash",
# # # # # #     openai_client=external_client
# # # # # # )
# # # # # # config = RunConfig(
# # # # # #     model=model,
# # # # # #     model_provider=external_client,
# # # # # #     tracing_disabled=True,
# # # # # # )


# # # # # # # Tool to get country info
# # # # # # @function_tool
# # # # # # def get_country_info(name: str) -> dict:
# # # # # #     """Get capital, population, languages, and map link for a country."""
# # # # # #     try:
# # # # # #         response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
# # # # # #         data = response.json()[0]

# # # # # #         return {
# # # # # #             "Capital": data.get("capital", ["N/A"])[0],
# # # # # #             "Population": f"{data.get('population', 'N/A'):,}",
# # # # # #             "Languages": ", ".join(data.get("languages", {}).values()) or "N/A",
# # # # # #             "Map": data.get("maps", {}).get("googleMaps", "N/A"),
# # # # # #         }
# # # # # #     except Exception as e:
# # # # # #         return {"Error": f"Country not found or API error: {e}"}

# # # # # # # Define the agent
# # # # # # async def main():
    
    
# # # # # #     agent = Agent(
# # # # # #         name="country_info_agent",
# # # # # #         instructions="""
# # # # # # You are a helpful assistant that takes a country name and uses a tool to provide:
# # # # # # - Capital
# # # # # # - Population
# # # # # # - Official languages


# # # # # # You must always use the `get_country_info` tool when a country is mentioned.
# # # # # # Return results clearly in a readable format.
# # # # # # """,
# # # # # #         model=model,
# # # # # #         tools=[get_country_info],
# # # # # #     )

# # # # # # # runner = Runner(agent=agent)

# # # # # # # Chainlit message handler
# # # # # # @cl.on_message
# # # # # # async def handle_user_input(message: cl.Message):
# # # # # #     user_input = message.content

# # # # # #     # Call the agent
# # # # # #     result = Runner.run(user_input, run_config=config)

# # # # # #     # Extract the assistant reply (string expected)
# # # # # #     if isinstance(result.output, str):
# # # # # #         await cl.Message(content=result.output).send()
# # # # # #     else:
# # # # # #         # Fallback: Format the tool's dictionary response if it's not a string
# # # # # #         try:
# # # # # #             output_dict = result.output
# # # # # #             response_str = "\n".join(f"**{k}**: {v}" for k, v in output_dict.items())
# # # # # #             await cl.Message(content=response_str).send()
# # # # # #         except Exception:
# # # # # #             await cl.Message(content="❌ Unexpected response format.").send()




# # # # # # import os
# # # # # # import requests
# # # # # # from dotenv import load_dotenv
# # # # # # import chainlit as cl

# # # # # # from agents import (
# # # # # #     Agent,
# # # # # #     Runner,
# # # # # #     AsyncOpenAI,
# # # # # #     OpenAIChatCompletionsModel,
# # # # # #     function_tool,
# # # # # # )
# # # # # # from agents.run import RunConfig

# # # # # # # Load environment variables from .env file
# # # # # # load_dotenv()
# # # # # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # # # # if not GEMINI_API_KEY:
# # # # # #     raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# # # # # # # Gemini (OpenAI-compatible) client setup
# # # # # # external_client = AsyncOpenAI(
# # # # # #     api_key=GEMINI_API_KEY,
# # # # # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai",
# # # # # # )

# # # # # # # Define the model
# # # # # # model = OpenAIChatCompletionsModel(
# # # # # #     model="gemini-2.0-flash",
# # # # # #     openai_client=external_client
# # # # # # )

# # # # # # # Run configuration
# # # # # # config = RunConfig(
# # # # # #     model=model,
# # # # # #     model_provider=external_client,
# # # # # #     tracing_disabled=True,
# # # # # # )

# # # # # # # Tool to get country info
# # # # # # @function_tool
# # # # # # def get_country_info(name: str) -> dict:
# # # # # #     """Get capital, population, languages, and map link for a country."""
# # # # # #     try:
# # # # # #         response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
# # # # # #         data = response.json()[0]

# # # # # #         return {
# # # # # #             "Capital": data.get("capital", ["N/A"])[0],
# # # # # #             "Population": f"{data.get('population', 'N/A'):,}",
# # # # # #             "Languages": ", ".join(data.get("languages", {}).values()) or "N/A",
# # # # # #             "Map": data.get("maps", {}).get("googleMaps", "N/A"),
# # # # # #         }
# # # # # #     except Exception as e:
# # # # # #         return {"Error": f"Country not found or API error: {e}"}

# # # # # # # Define the agent globally so it can be reused
# # # # # # agent = Agent(
# # # # # #     name="country_info_agent",
# # # # # #     instructions="""
# # # # # # You are a helpful assistant that takes a country name and uses a tool to provide:
# # # # # # - Capital
# # # # # # - Population
# # # # # # - Official languages

# # # # # # You must always use the `get_country_info` tool when a country is mentioned.
# # # # # # Return results clearly in a readable format.
# # # # # # """,
# # # # # #     model=model,
# # # # # #     tools=[get_country_info],
# # # # # # )

# # # # # # # Instantiate the runner
# # # # # # runner = Runner(agent=agent)

# # # # # # # Chainlit message handler
# # # # # # @cl.on_message
# # # # # # async def handle_user_input(message: cl.Message):
# # # # # #     user_input = message.content

# # # # # #     try:
# # # # # #         # Run the agent with user input
# # # # # #         result = await runner.run(user_input, run_config=config)

# # # # # #         # Handle string or dictionary output
# # # # # #         if isinstance(result.output, str):
# # # # # #             await cl.Message(content=result.output).send()
# # # # # #         else:
# # # # # #             output_dict = result.output
# # # # # #             response_str = "\n".join(f"**{k}**: {v}" for k, v in output_dict.items())
# # # # # #             await cl.Message(content=response_str).send()

# # # # # #     except Exception as e:
# # # # # #         await cl.Message(content=f"❌ Error during execution: {e}").send()




# # # # # import os
# # # # # import requests
# # # # # from dotenv import load_dotenv
# # # # # import chainlit as cl

# # # # # from agents import (
# # # # #     Agent,
# # # # #     Runner,
# # # # #     AsyncOpenAI,
# # # # #     OpenAIChatCompletionsModel,
# # # # #     function_tool,
# # # # # )
# # # # # from agents.run import RunConfig

# # # # # # Load environment variables
# # # # # load_dotenv()
# # # # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # # # if not GEMINI_API_KEY:
# # # # #     raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# # # # # # Gemini (OpenAI-compatible) client
# # # # # external_client = AsyncOpenAI(
# # # # #     api_key=GEMINI_API_KEY,
# # # # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai",
# # # # # )

# # # # # # Configure the model
# # # # # model = OpenAIChatCompletionsModel(
# # # # #     model="gemini-2.0-flash",
# # # # #     openai_client=external_client
# # # # # )
# # # # # config = RunConfig(
# # # # #     model=model,
# # # # #     model_provider=external_client,
# # # # #     tracing_disabled=True,
# # # # # )

# # # # # # Tool to get country info
# # # # # @function_tool
# # # # # def get_country_info(name: str) -> dict:
# # # # #     """Get capital, population, languages, and map link for a country."""
# # # # #     try:
# # # # #         response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
# # # # #         data = response.json()[0]

# # # # #         return {
# # # # #             "Capital": data.get("capital", ["N/A"])[0],
# # # # #             "Population": f"{data.get('population', 'N/A'):,}",
# # # # #             "Languages": ", ".join(data.get("languages", {}).values()) or "N/A",
# # # # #             "Map": data.get("maps", {}).get("googleMaps", "N/A"),
# # # # #         }
# # # # #     except Exception as e:
# # # # #         return {"Error": f"Country not found or API error: {e}"}

# # # # # # Define the agent globally
# # # # # agent = Agent(
# # # # #     name="country_info_agent",
# # # # #     instructions="""
# # # # # You are a helpful assistant that takes a country name and uses a tool to provide:
# # # # # - Capital
# # # # # - Population
# # # # # - Official languages

# # # # # You must always use the get_country_info tool when a country is mentioned.
# # # # # Return results clearly in a readable format.
# # # # # """,
# # # # #     model=model,
# # # # #     tools=[get_country_info],
# # # # # )

# # # # # # Chainlit message handler
# # # # # @cl.on_message
# # # # # async def handle_user_input(message: cl.Message):
# # # # #     user_input = message.content

# # # # #     # Call Runner.run with agent, input, and config
# # # # #     result = await Runner.run(agent, user_input, config)

# # # # #     # Extract the assistant reply
# # # # #     if isinstance(result.output, str):
# # # # #         await cl.Message(content=result.output).send()
# # # # #     else:
# # # # #         # Fallback: Format the tool's dictionary response if it’s not a string
# # # # #         try:
# # # # #             output_dict = result.output
# # # # #             response_str = "\n".join(f"**{k}**: {v}" for k, v in output_dict.items())
# # # # #             await cl.Message(content=response_str).send()
# # # # #         except Exception:
# # # # #             await cl.Message(content="❌ Unexpected response format.").send()

# # # # import os
# # # # import requests
# # # # from dotenv import load_dotenv
# # # # import chainlit as cl

# # # # from agents import (
# # # #     Agent,
# # # #     Runner,
# # # #     AsyncOpenAI,
# # # #     OpenAIChatCompletionsModel,
# # # #     function_tool,
# # # # )
# # # # from agents.run import RunConfig

# # # # # Load environment variables from .env file
# # # # load_dotenv()
# # # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # # if not GEMINI_API_KEY:
# # # #     raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# # # # # Set up Gemini (OpenAI-compatible) client
# # # # external_client = AsyncOpenAI(
# # # #     api_key=GEMINI_API_KEY,
# # # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai"
# # # # )

# # # # # Define model
# # # # model = OpenAIChatCompletionsModel(
# # # #     model="gemini-2.0-flash",
# # # #     openai_client=external_client
# # # # )

# # # # # Tool function
# # # # @function_tool
# # # # def get_country_info(name: str) -> dict:
# # # #     """Get capital, population, languages, and map link for a country."""
# # # #     try:
# # # #         response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
# # # #         data = response.json()[0]
# # # #         return {
# # # #             "Capital": data.get("capital", ["N/A"])[0],
# # # #             "Population": f"{data.get('population', 'N/A'):,}",
# # # #             "Languages": ", ".join(data.get("languages", {}).values()) or "N/A",
# # # #             "Map": data.get("maps", {}).get("googleMaps", "N/A"),
# # # #         }
# # # #     except Exception as e:
# # # #         return {"Error": f"Country not found or API error: {e}"}

# # # # # Define Agent
# # # # agent = Agent(
# # # #     name="country_info_agent",
# # # #     instructions="""
# # # # You are a helpful assistant that takes a country name and uses a tool to provide:
# # # # - Capital
# # # # - Population
# # # # - Official languages

# # # # You must always use the `get_country_info` tool when a country is mentioned.
# # # # Return results clearly in a readable format.
# # # # """,
# # # #     model=model,
# # # #     tools=[get_country_info],
# # # # )

# # # # # Define RunConfig
# # # # config = RunConfig(
# # # #     model=model,
# # # #     model_provider=external_client,
# # # #     tracing_disabled=True,
# # # # )

# # # # # Instantiate runner
# # # # runner = Runner(agent=agent)

# # # # # Chainlit handler
# # # # @cl.on_message
# # # # async def handle_user_input(message: cl.Message):
# # # #     user_input = message.content

# # # #     try:
# # # #         # FIXED: Use the instance method and pass input + config
# # # #         result = await runner.run(input=user_input, run_config=config)

# # # #         # Handle string or dict
# # # #         if isinstance(result.output, str):
# # # #             await cl.Message(content=result.output).send()
# # # #         else:
# # # #             response_str = "\n".join(f"**{k}**: {v}" for k, v in result.output.items())
# # # #             await cl.Message(content=response_str).send()

# # # #     except Exception as e:
# # # #         await cl.Message(content=f"❌ Error: {str(e)}").send()




# # # import os
# # # import requests
# # # from dotenv import load_dotenv
# # # import chainlit as cl

# # # from agents import (
# # #     Agent,
# # #     Runner,
# # #     AsyncOpenAI,
# # #     OpenAIChatCompletionsModel,
# # #     function_tool,
# # # )
# # # from agents.run import RunConfig

# # # # Load .env variables
# # # load_dotenv()
# # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # if not GEMINI_API_KEY:
# # #     raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# # # # Configure OpenAI-compatible Gemini client
# # # external_client = AsyncOpenAI(
# # #     api_key=GEMINI_API_KEY,
# # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai"
# # # )

# # # # Define the model
# # # model = OpenAIChatCompletionsModel(
# # #     model="gemini-2.0-flash",
# # #     openai_client=external_client
# # # )

# # # # Run configuration
# # # config = RunConfig(
# # #     model=model,
# # #     model_provider=external_client,
# # #     tracing_disabled=True,
# # # )

# # # # Tool to fetch country info
# # # @function_tool
# # # def get_country_info(name: str) -> dict:
# # #     """Get capital, population, languages, and map link for a country."""
# # #     try:
# # #         response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
# # #         data = response.json()[0]

# # #         return {
# # #             "Capital": data.get("capital", ["N/A"])[0],
# # #             "Population": f"{data.get('population', 'N/A'):,}",
# # #             "Languages": ", ".join(data.get("languages", {}).values()) or "N/A",
# # #             "Map": data.get("maps", {}).get("googleMaps", "N/A"),
# # #         }
# # #     except Exception as e:
# # #         return {"Error": f"Country not found or API error: {e}"}

# # # # Define the agent
# # # agent = Agent(
# # #     name="country_info_agent",
# # #     instructions="""
# # # You are a helpful assistant that takes a country name and uses a tool to provide:
# # # - Capital
# # # - Population
# # # - Official languages

# # # You must always use the `get_country_info` tool when a country is mentioned.
# # # Return results clearly in a readable format.
# # # """,
# # #     model=model,
# # #     tools=[get_country_info],
# # # )

# # # # Chainlit message handler
# # # @cl.on_message
# # # async def handle_user_input(message: cl.Message):
# # #     user_input = message.content

# # #     try:
# # #         # FIXED: Call Runner.run as a class method, pass agent + input + config
# # #         result = await Runner.run(input=user_input, agent=agent, run_config=config)

# # #         if isinstance(result.output, str):
# # #             await cl.Message(content=result.output).send()
# # #         else:
# # #             # Format dict response
# # #             output = result.output
# # #             response_str = "\n".join(f"**{k}**: {v}" for k, v in output.items())
# # #             await cl.Message(content=response_str).send()

# # #     except Exception as e:
# # #         await cl.Message(content=f"❌ Error: {str(e)}").send()





import os
import requests
from dotenv import load_dotenv
import chainlit as cl

from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
)
from agents.run import RunConfig

# Load .env variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# Configure OpenAI-compatible Gemini client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# Define the model
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

# Tool to fetch country info
@function_tool
def get_country_info(name: str) -> dict:
    """Get capital, population, languages, and map link for a country."""
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
        data = response.json()[0]

        return {
            "Capital": data.get("capital", ["N/A"])[0],
            "Population": f"{data.get('population', 'N/A'):,}",
            "Languages": ", ".join(data.get("languages", {}).values()) or "N/A",
            "Map": data.get("maps", {}).get("googleMaps", "N/A"),
        }
    except Exception as e:
        return {"Error": f"Country not found or API error: {e}"}

# Define the agent
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

# Chainlit message handler
@cl.on_message
async def handle_user_input(message: cl.Message):
    user_input = message.content

    try:
        # FIXED: Call Runner.run as a class method, pass agent + input + config
        result = await Runner.run(input=user_input, agent=agent, run_config=config)

        if isinstance(result.output, str):
            await cl.Message(content=result.output).send()
        else:
            # Format dict response
            output = result.output
            response_str = "\n".join(f"**{k}**: {v}" for k, v in output.items())
            await cl.Message(content=response_str).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
