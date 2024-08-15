from dotenv import load_dotenv
import logging

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat

# Load environment variables
load_dotenv()

# Create the agent
agent = Agent(
    logger_level=logging.ERROR,
)

# Run the agent
Chat(agent).start()
