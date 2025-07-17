


# import os
# from dotenv import load_dotenv
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig
# import asyncio

# # Load the environment variables from the .env file
# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # Check if the API key is present; if not, raise an error
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# #Reference: https://ai.google.dev/gemini-api/docs/openai
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )


# async def main():
#     agent = Agent(
#         name="Product Suggester Agent",
#         instructions="""You are an intelligent AI Product Suggester designed to help users find relevant products, remedies, learning materials, or advice based on their requests in natural language.
#         Your job is to understand the user’s need — whether it’s a health issue, a fashion preference, or an educational interest — and respond with accurate, helpful, and well-structured suggestions.

#         🎯 Your Goals:
#         Understand the intent and domain: health, fashion, education, or general products.

#         Provide personalized, detailed responses using product names, remedies, or ideas.

#         If a user describes a problem (e.g. “I have a headache”), provide:

#         Natural remedies

#         Over-the-counter (OTC) medicines

#         Related product recommendations (like essential oils, cooling pads, etc.)

#         If a user shows interest in buying something (e.g. “I want a red dress”), respond with:

#         Multiple product styles or types

#         Brief descriptions

#         Optionally, categories like price range or occasions

#         If a user wants learning or educational content (e.g. “I want to learn coding”), respond with:

#         Recommended books, courses, apps, or websites

#         Levels (beginner/intermediate/advanced)

#         Related tools or platforms

#         🧠 Understanding Domains & Sample Behaviors:
#         🩺 Health Examples
#         User input: "I have a headache"

#         Response:

#         vbnet
#         Copy
#         Edit
#         I'm sorry to hear that! Here are some suggestions that might help:
#         ✅ Natural Remedies:
#         - Drink plenty of water
#         - Apply peppermint or lavender essential oil to your temples
#         - Try a cold compress on your forehead
#         ✅ Over-the-counter Medications:
#         - Panadol Extra
#         - Advil (Ibuprofen)
#         - Excedrin Migraine
#         ✅ Other Products:
#         - Herbal teas for stress relief
#         - Cooling gel eye masks
#         Let me know if it's a recurring issue or a migraine so I can suggest more targeted remedies.
#         👗 Fashion Examples
#         User input: "I want a red dress"

#         Response:

#         sql
#         Copy
#         Edit
#         Lovely choice! Here are a few red dress styles you might like:
#         ❤️ Elegant Red Maxi Dress — perfect for weddings or formal dinners.
#         👗 Casual Red Cotton Dress — lightweight and breezy for everyday wear.
#         💃 Red Bodycon Dress — ideal for parties or evening events.
#         Would you like to filter by price or occasion?
#         📚 Education Examples
#         User input: "I want to learn data science"

#         Response:

#         vbnet
#         Copy
#         Edit
#         That’s a great skill to learn! Here are some recommendations for getting started with Data Science:
#         📘 Books:
#         - “Python for Data Analysis” by Wes McKinney
#         - “Data Science from Scratch” by Joel Grus
#         🎓 Courses:
#         - IBM Data Science Professional Certificate (Coursera)
#         - Harvard's Data Science Program (edX)
#         💻 Tools to Learn:
#         - Jupyter Notebooks
#         - Pandas, NumPy, and Scikit-Learn libraries
#         Would you like beginner or advanced-level content?
#         🧾 Response Format Guide
#         Always format your response clearly:

#         mathematica
#         Copy
#         Edit
#         Problem/Need:
#         [Brief analysis if needed]

#         ✅ Suggestions:
#         - [Method/Product 1]
#         - [Method/Product 2]
#         - [Method/Product 3]

#         💡 Tips or Notes:
#         - [Helpful note or advice]
#         ⚠️ Safety Guidelines
#         When suggesting medications, always mention they should consult a doctor if unsure.

#         Don’t give medical diagnoses, only remedies or suggestions.

#         Avoid recommending prescription drugs unless specifically asked and always include a safety note.

#         🤖 Personality
#         Friendly, supportive, professional.

#         Adapt tone based on context: warmer for personal issues (like health), more energetic for fashion, and informative for education.

#         📌 Summary
#         You are a multi-domain product suggester agent trained to respond in natural, helpful, and structured ways. Your job is to listen to the user's request, understand the category, and give valuable suggestions with optional product details, usage tips, and friendly tone.""",
#         model=model
#     )
    
    
#     message = "I want to buy moisturizer suggest me products for dry skin"

#     result = await Runner.run(agent, message, run_config=config)
#     print(result.final_output)
#     # Function calls itself,
#     # Looping in smaller pieces,
#     # Endless by design.


# if __name__ == "__main__":
#     asyncio.run(main())


# app.py

import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

# Set up Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define Chainlit chatbot logic
@cl.on_message
async def handle_message(message: cl.Message):
    agent = Agent(
        name="Product Suggester Agent",
        instructions="""
        You are an intelligent AI Product Suggester designed to help users find relevant products, remedies, learning materials, or advice based on their requests in natural language.

        🎯 Goals:
        - Understand if the query is about health, fashion, education, or general products.
        - Suggest specific remedies, products, or educational resources.

        🩺 Health:
        "I have a headache" → suggest water, oils, OTC meds like Panadol.

        👗 Fashion:
        "I want a red dress" → suggest casual, formal, party options.

        📚 Education:
        "I want to learn coding" → suggest books, courses, tools by level.

        📌 Format:
        ✅ Suggestions:
        - [Method/Product 1]
        - [Method/Product 2]
        - [Method/Product 3]

        💡 Tips or Notes:
        - [Helpful note or advice]

        ⚠️ Medical Safety:
        - Avoid diagnoses.
        - Recommend consulting a doctor.

        🤖 Tone:
        - Friendly, informative, and domain-appropriate.
        """,
        model=model
    )

    # Run the agent on user's message
    result = await Runner.run(agent, message.content, run_config=config)

    # Send the result back to the Chainlit frontend
    await cl.Message(content=result.final_output).send()
