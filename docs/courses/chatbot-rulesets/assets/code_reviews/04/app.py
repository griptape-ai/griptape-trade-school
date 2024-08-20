from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat

# Load environment variables
load_dotenv()


# Create the agent
agent = Agent()

# Run the agent
Chat(agent).start()
