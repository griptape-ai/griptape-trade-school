from dotenv import load_dotenv
import os

from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTimeTool

# from reverse_string_tool import ReverseStringTool
from shotgrid_tool import ShotGridTool

load_dotenv()

SHOTGRID_URL = os.environ["SHOTGRID_URL"]
SHOTGRID_API_KEY = os.environ["SHOTGRID_API_KEY"]
SHOTGRID_SCRIPT = "Griptape API"

# Instantiate the tool
shotgrid_tool = ShotGridTool(
    base_url=SHOTGRID_URL,
    api_key=SHOTGRID_API_KEY,
    script_name=SHOTGRID_SCRIPT,
    off_prompt=False,
)

# Instantiate the agent
agent = Agent(
    tools=[
        DateTimeTool(off_prompt=False),
        shotgrid_tool,
        # ReverseStringTool(off_prompt=False),
    ],
    stream=True
)

# Start chatting
Chat(agent).start()
