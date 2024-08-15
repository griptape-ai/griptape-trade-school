from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTimeTool

load_dotenv()

# Instantiate the agent
agent = Agent(tools=[DateTimeTool(off_prompt=False)])
agent.config.prompt_driver.stream=True

# Start chatting
Chat(agent).start()
