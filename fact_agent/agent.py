import vertexai
import os
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp


root_agent = Agent(
    model="gemini-2.0-flash",
    name='fact_agent',
    instruction="""
      Ask the user for a year in arabic format.
      You can only accept a year up until the current date's year.
      You can only accept integers, and should refuse any inputs such as text or media.
      When the user as provided you with a valid year:
      1. You should respond with 1 facts from the year provided by the user
      You should not rely on the previous history.
    """,
    tools=[],
)

app = AdkApp(
    agent=root_agent,
    enable_tracing=True
)