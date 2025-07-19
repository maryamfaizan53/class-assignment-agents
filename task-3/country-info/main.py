
import os
import requests
from difflib import get_close_matches
from dotenv import load_dotenv
import chainlit as cl
from chainlit.input_widget import Select
from chainlit.playground.providers import ChatOpenAI
from openai import AsyncOpenAI

from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel

# Load .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Tool (Was in tools.py, now merged)
from chainlit.server.utils import function_tool

@function_tool
def get_country_info(country: str) -> dict:
    """
    Get information about a country using REST API.
    """
    url = "https://restcountries.com/v3.1/all"
    try:
        res = requests.get(url, timeout=10)
        countries = res.json()
        country_names = [c.get("name", {}).get("common", "") for c in countries]
        match = get_close_matches(country, country_names, n=1, cutoff=0.5)
        if not match:
            return {"error": "No close match found for the country name."}

        country_data = next((c for c in countries if c["name"]["common"] == match[0]), None)
        if not country_data:
            return {"error": "Country not found."}

        return {
            "country": country_data.get("name", {}).get("common", "N/A"),
            "capital": country_data.get("capital", ["N/A"])[0],
            "population": country_data.get("population", "N/A"),
            "area": country_data.get("area", "N/A"),
            "region": country_data.get("region", "N/A"),
            "flag": country_data.get("flags", {}).get("png", ""),
        }
    except Exception as e:
        return {"error": str(e)}

# Chainlit config
external_client = AsyncOpenAI(api_key=GEMINI_API_KEY)

config = RunConfig(
    max_iterations=1,
    stream=True,
    metadata={"model": "gpt-3.5-turbo"},
)

agent = Agent(
    tools=[get_country_info],
    llm=OpenAIChatCompletionsModel(client=external_client, model="gpt-3.5-turbo"),
)

runner = Runner(agent=agent, config=config)

# Chainlit UI handler
@cl.on_message
async def on_message(message: cl.Message):
    result = await runner.run(input=message.content)
    
    output = result.output_data
    if not isinstance(output, dict):
        await cl.Message(content="❌ No country info returned.").send()
        return

    if "error" in output:
        await cl.Message(content=f"❌ Error: {output['error']}").send()
        return

    response = f"""📍 **{output.get('country', 'N/A')}**
🌍 Region: {output.get('region', 'N/A')}
🏙️ Capital: {output.get('capital', 'N/A')}
👥 Population: {output.get('population', 'N/A'):,}
📐 Area: {output.get('area', 'N/A'):,} km²"""

    img = output.get("flag")

    await cl.Message(content=response).send()
    if img:
        await cl.Message(content="🏳️ Flag:", elements=[cl.Image(name="flag", display="inline", url=img)]).send()




# # main.py

# import os
# from dotenv import load_dotenv
# import chainlit as cl
# import requests
# from difflib import get_close_matches

# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
# from agents.run import RunConfig

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("Missing GEMINI_API_KEY in .env file")

# # Setup OpenAI-compatible Gemini client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # Configure model
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# # Setup run configuration
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True,
# )

# # ✅ Tool function defined here
# @function_tool
# def get_country_info(country_name: str) -> dict:
#     """Get capital, population, languages, flag and map location of a country using RESTCountries API"""
#     url = "https://restcountries.com/v3.1/all"
#     try:
#         res = requests.get(url, timeout=10)
#         data = res.json()

#         # Spelling correction (case-insensitive)
#         country_names = [c["name"]["common"] for c in data]
#         country_lookup = {name.lower(): name for name in country_names}
#         closest = get_close_matches(country_name.lower(), country_lookup.keys(), n=1)
#         if not closest:
#             return {"error": "Country not found. Try again."}

#         matched = country_lookup[closest[0]]
#         country_data = next(item for item in data if item["name"]["common"] == matched)

#         capital = country_data.get("capital")
#         capital = capital[0] if capital else "N/A"

#         population = f'{country_data.get("population", 0):,}'

#         languages_dict = country_data.get("languages", {})
#         languages = ", ".join(languages_dict.values()) if languages_dict else "N/A"

#         flag_url = country_data.get("flags", {}).get("png") or "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/World_map_blank_without_borders.svg/640px-World_map_blank_without_borders.svg.png"

#         latlng = country_data.get("latlng", [0, 0])
#         map_link = f"https://www.google.com/maps/search/?api=1&query={latlng[0]},{latlng[1]}"

#         return {
#             "country": matched,
#             "capital": capital,
#             "population": population,
#             "languages": languages,
#             "flag_url": flag_url,
#             "map_link": map_link
#         }

#     except Exception as e:
#         return {"error": f"❌ API Error: {str(e)}"}

# # Define the agent
# agent = Agent(
#     name="country_info_agent",
#     instructions="""
# You are a helpful assistant that takes a country name and uses a tool to provide:
# - Capital
# - Population
# - Official languages
# - Flag image
# - Google Maps location link

# You must always use the `get_country_info` tool when a country is mentioned.
# Return results clearly in a readable format.
# """,
#     model=model,
#     tools=[get_country_info],
# )

# # Welcome message
# @cl.on_chat_start
# async def on_start():
#     await cl.Message(content="🌍 Welcome! Type a country name to get detailed information.").send()

# # Message handler
# @cl.on_message
# async def on_message(message: cl.Message):
#     country = message.content.strip()
#     query = f"Give me all details about {country}"

#     result = await Runner.run(agent, query, run_config=config)
#     info = result.final_output if isinstance(result.final_output, dict) else {}

#     if info.get("error"):
#         await cl.Message(content=f"❌ {info['error']}").send()
#     else:
#         response = f"""📍 **{info['country']}**
# **🏛 Capital:** {info['capital']}
# **🗣 Languages:** {info['languages']}
# **👥 Population:** {info['population']}
# 🌍 [View on Map]({info['map_link']})
# """
#         msg = cl.Message(content=response)
#         if info.get("flag_url"):
#             msg.elements = [
#                 cl.Image(name="Flag", display="inline", url=info["flag_url"])
#             ]
#         await msg.send()



# import os
# from dotenv import load_dotenv
# import chainlit as cl
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig
# from tools import get_country_info

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("Missing GEMINI_API_KEY in .env file")

# # Set up OpenAI-compatible Gemini client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # Configure the model
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# # Set up run configuration
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True,
# )

# # Define the agent
# agent = Agent(
#     name="country_info_agent",
#     instructions="""
# You are a helpful assistant that takes a country name and uses a tool to provide:
# - Capital
# - Population
# - Official languages
# - Flag image
# - Google Maps location link

# You must always use the `get_country_info` tool when a country is mentioned.
# Return results clearly in a readable format.
# """,
#     model=model,
#     tools=[get_country_info],
# )

# # Optional: Send welcome message when chat starts
# @cl.on_chat_start
# async def on_start():
#     await cl.Message(content="🌍 Welcome! Type a country name to get detailed information.").send()

# # Handle user message
# @cl.on_message
# async def on_message(message: cl.Message):
#     country = message.content.strip()
#     query = f"Give me all details about {country}"

#     result = await Runner.run(agent, query, run_config=config)
#     info = result.output if isinstance(result.output, dict) else {}

#     if info.get("error"):
#         await cl.Message(content=f"❌ {info['error']}").send()
#     else:
#         response = f"""📍 **{info['country']}**
# **🏛 Capital:** {info['capital']}
# **🗣 Languages:** {info['languages']}
# **👥 Population:** {info['population']}
# 🌍 [View on Map]({info['map_link']})
# """
#         msg = cl.Message(content=response)
#         if info.get("flag_url"):
#             msg.elements = [
#                 cl.Image(name="Flag", display="inline", url=info["flag_url"])
#             ]
#         await msg.send()

# # # main.py

# # import os
# # from dotenv import load_dotenv
# # import chainlit as cl
# # from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# # from agents.run import RunConfig
# # from tools import get_country_info

# # # Load environment variables
# # load_dotenv()
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # if not GEMINI_API_KEY:
# #     raise ValueError("Missing GEMINI_API_KEY in .env file")

# # # Set up OpenAI-compatible Gemini client
# # external_client = AsyncOpenAI(
# #     api_key=GEMINI_API_KEY,
# #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# # )

# # # Configure the model
# # model = OpenAIChatCompletionsModel(
# #     model="gemini-2.0-flash",
# #     openai_client=external_client
# # )

# # # Set up run configuration
# # config = RunConfig(
# #     model=model,
# #     model_provider=external_client,
# #     tracing_disabled=True,
# # )

# # # Define the agent
# # agent = Agent(
# #     name="country_info_agent",
# #     instructions="""
# # You are a helpful assistant that takes a country name and uses a tool to provide:
# # - Capital
# # - Population
# # - Official languages
# # - Flag image
# # - Google Maps location link

# # You must always use the `get_country_info` tool when a country is mentioned.
# # Return results clearly in a readable format.
# # """,
# #     model=model,
# #     tools=[get_country_info],
# # )

# # # Optional: Greet the user when chat starts
# # @cl.on_chat_start
# # async def on_start():
# #     await cl.Message(content="🌍 Welcome! Type a country name to get detailed information.").send()

# # # Handle user message
# # @cl.on_message
# # async def on_message(message: cl.Message):
# #     country = message.content.strip()
# #     query = f"Give me all details about {country}"

# #     result = await Runner.run(agent, query, run_config=config)
# #     info = result.tool_outputs[0] if result.tool_outputs else {}

# #     if info.get("error"):
# #         await cl.Message(content=f"❌ {info['error']}").send()
# #     else:
# #         response = f"""📍 **{info['country']}**
# # **🏛 Capital:** {info['capital']}
# # **🗣 Languages:** {info['languages']}
# # **👥 Population:** {info['population']}
# # 🌍 [View on Map]({info['map_link']})
# # """
# #         msg = cl.Message(content=response)
# #         if info.get("flag_url"):
# #             msg.elements = [
# #                 cl.Image(name="Flag", display="inline", url=info["flag_url"])
# #             ]
# #         await msg.send()








# # # # main.py
# # # import os
# # # from dotenv import load_dotenv
# # # import chainlit as cl
# # # from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# # # from agents.run import RunConfig
# # # from tools import get_country_info

# # # # Load environment variables
# # # load_dotenv()
# # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # if not GEMINI_API_KEY:
# # #     raise ValueError("Missing GEMINI_API_KEY in .env file")

# # # # Set up OpenAI-compatible Gemini client
# # # external_client = AsyncOpenAI(
# # #     api_key=GEMINI_API_KEY,
# # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# # # )

# # # # Configure the model
# # # model = OpenAIChatCompletionsModel(
# # #     model="gemini-2.0-flash",
# # #     openai_client=external_client
# # # )

# # # # Set up run configuration
# # # config = RunConfig(
# # #     model=model,
# # #     model_provider=external_client,
# # #     tracing_disabled=True,
# # # )

# # # # Define the agent
# # # agent = Agent(
# # #     name="country_info_agent",
# # #     instructions="""
# # # You are a helpful assistant that takes a country name and uses a tool to provide:
# # # - Capital
# # # - Population
# # # - Official languages
# # # - Flag image
# # # - Google Maps location link

# # # You must always use the `get_country_info` tool when a country is mentioned.
# # # Return results clearly in a readable format.
# # # """,
# # #     model=model,
# # #     tools=[get_country_info],
# # # )

# # # # Define what happens when a user sends a message
# # # # @cl.on_message
# # # # async def on_message(message: cl.Message):
# # # #     country = message.content.strip()
# # # #     query = f"Give me all details of {country}"

# # # #     result = await Runner.run(agent, query, run_config=config)

# # # #     # Extract tool response
# # # #     info = result.tool_outputs[0] if result.tool_outputs else {}

# # # #     # Handle response
# # # #     if info.get("error"):
# # # #         await cl.Message(content=f"❌ {info['error']}").send()
# # # #     else:
# # # #         response = f"""📍 **{info['country']}**
# # # # **🏛 Capital:** {info['capital']}
# # # # **🗣 Languages:** {info['languages']}
# # # # **👥 Population:** {info['population']}
# # # # 🌍 [View on Map]({info['map_link']})
# # # # """
# # # #         msg = cl.Message(content=response)

# # # #         if info.get("flag_url"):
# # # #             msg.elements = [
# # # #                 cl.Image(name="Flag", display="inline", url=info["flag_url"])
# # # #             ]

# # # #         await msg.send()
# # # @cl.on_message
# # # async def on_message(message: cl.Message):
# # #     country = message.content.strip()
# # #     query = f'get_country_info("{country}")'

# # #     result = await Runner.run_agent(agent, query, run_config=config)
# # #     info = result.tool_outputs[0] if result.tool_outputs else {}

# # #     if info.get("error"):
# # #         await cl.Message(content=f"❌ {info['error']}").send()
# # #     else:
# # #         response = f"""📍 **{info['country']}**
# # # **🏛 Capital:** {info['capital']}
# # # **🗣 Languages:** {info['languages']}
# # # **👥 Population:** {info['population']}
# # # 🌍 [View on Map]({info['map_link']})
# # # """
# # #         msg = cl.Message(content=response)
# # #         if info.get("flag_url"):
# # #             msg.elements = [
# # #                 cl.Image(name="Flag", display="inline", url=info["flag_url"])
# # #             ]
# # #         await msg.send()
