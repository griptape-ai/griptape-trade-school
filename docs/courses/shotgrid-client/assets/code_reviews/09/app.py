from dotenv import load_dotenv
from textwrap import dedent
import os

from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTime, VectorStoreClient
from griptape.drivers import (
    LocalVectorStoreDriver,
    OpenAiChatPromptDriver,
    OpenAiEmbeddingDriver,
)
from griptape.engines import VectorQueryEngine
from griptape.loaders import WebLoader
from griptape.rules import Rule, Ruleset

from shotgrid_tool import ShotGridTool

load_dotenv()

# Create the vector database
vector_store_driver = LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver())

# Create the query engine
query_engine = VectorQueryEngine(
    prompt_driver=OpenAiChatPromptDriver(model="gpt-3.5-turbo"),
    vector_store_driver=vector_store_driver,
)

# API Documentation
shotgrid_api_urls = [
    "https://developers.shotgridsoftware.com/python-api/reference.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/usage_tips.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/attachments.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/updating_tasks.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/task_dependencies.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/split_tasks.html",
]

# Load the API documentation
artifacts = []
for url in shotgrid_api_urls:
    artifacts.append(WebLoader().load(url))

# Upsert documentation  into the vector database
namespace = "shotgrid_api"

for artifact in artifacts:
    query_engine.vector_store_driver.upsert_text_artifacts({namespace: artifact})

# Instantiate the Vector Store Client
vector_store_tool = VectorStoreClient(
    description="Contains information about ShotGrid api. Use it to help with ShotGrid client requests.",
    query_engine=query_engine,
    namespace=namespace,
    off_prompt=False,
)

SHOTGRID_URL = os.environ["SHOTGRID_URL"]
SHOTGRID_API_KEY = os.environ["SHOTGRID_API_KEY"]
SHOTGRID_SCRIPT = "Griptape API"
SHOTGRID_USER = os.environ["SHOTGRID_USER"]
SHOTGRID_PASSWORD = os.environ["SHOTGRID_PASSWORD"]


# Instantiate the tool
shotgrid_tool = ShotGridTool(
    base_url=SHOTGRID_URL,
    api_key=SHOTGRID_API_KEY,
    script_name=SHOTGRID_SCRIPT,
    user_login=SHOTGRID_USER,
    user_password=SHOTGRID_PASSWORD,
    login_method="user",
    off_prompt=False,
)

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        Rule("Act as a studio coordinator who is an expert with Autodesk ShotGrid"),
        Rule(
            "Your main objective is to find and update information in ShotGrid using the ShotGridTool"
        ),
        Rule(
            dedent(
                """
            For specific information about how to use ShotGrid API activities, the 
            VectorStoreClient should be used. Take the necessary time to consult the 
            VectorStoreClient to ensure the most accurate and context-aware decisions 
            when interacting with the ShotGridTool and API.
            """
            )
        ),
        Rule(
            dedent(
                """
            Always use the ShotGrid batch() method when performing multiple create, update, or delete operations in ShotGrid.
            This should be done in a single request to improve efficiency and speed. Batch method uses "request_type", "entity_type", and "entity_id".
            Failure to use the batch() method in these instances will be considered a violation of the rules."""
            )
        ),
        Rule(
            dedent(
                """
            When asked to find, list, create, update, delete, retrieve details of entities, 
            update task status, update task data, list task assignments, retrieve the history of changes to 
            entities, manage versions of assets, manage project timelines, track project 
            progress, manage notes and reviews, manage user roles and permissions, or 
            integrate with other tools and workflows, the ShotGrid Client API is always used."""
            )
        ),
    ],
)

# Instantiate the agent
agent = Agent(
    tools=[DateTime(off_prompt=False), shotgrid_tool, vector_store_tool],
    rulesets=[shotgrid_agent_ruleset],
)
agent.config.prompt_driver.stream=True

# Start chatting
Chat(agent).start()
