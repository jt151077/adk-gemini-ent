import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv

load_dotenv()

from agent import app


vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket="gs://" + os.getenv("GOOGLE_CLOUD_PROJECT")+"-factagent",
)

remote_app = agent_engines.create(
    display_name="fact_agent",
    description="Agent to provide facts about the year given by the user",
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]"
    ],
    extra_packages = ["agent.py", "tools.py"]
)
