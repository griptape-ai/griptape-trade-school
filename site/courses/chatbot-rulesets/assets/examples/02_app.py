from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent

# Load environment variables
load_dotenv()

# Create the agent
agent = Agent()

# Run the agent
agent.run("Hi, how are you?")