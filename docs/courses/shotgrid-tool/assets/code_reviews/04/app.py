from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTimeTool

from reverse_string_tool import ReverseStringTool

load_dotenv()

# Instantiate the agent
agent = Agent(
    tools=[DateTimeTool(off_prompt=False), ReverseStringTool(off_prompt=False)],
    stream=True,
)

# Start chatting
Chat(agent).start()
