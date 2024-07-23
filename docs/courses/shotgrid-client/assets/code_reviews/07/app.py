from dotenv import load_dotenv
import os

from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTime

# from reverse_string_tool import ReverseStringTool
from shotgrid_tool import ShotGridTool

load_dotenv()

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

# Instantiate the agent
agent = Agent(
    tools=[
        DateTime(off_prompt=False),
        shotgrid_tool,
        # ReverseStringTool(off_prompt=False),
    ],
)
agent.config.prompt_driver.stream=True

# Start chatting
Chat(agent).start()
