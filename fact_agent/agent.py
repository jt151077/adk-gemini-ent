import vertexai
import os
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp
from tools import generate_image_data
from google.adk.tools.load_artifacts_tool import load_artifacts_tool


root_agent = Agent(
    model="gemini-2.0-flash",
    name='fact_agent',
    instruction="""
      Ask the user for a year in arabic format.
      You can only accept a year up until the current date's year.
      You can only accept integers, and should refuse any inputs such as text or media.
      When the user as provided you with a valid year:
      1. You should respond with 1 facts from the year provided by the user
      2. Based on this fact from the previous step, call the `generate_image_data` and display the image_artifact in the response.
      You should not rely on the previous history.
    """,
    tools=[generate_image_data, load_artifacts_tool],
)

app = AdkApp(
    agent=root_agent,
    enable_tracing=True
)