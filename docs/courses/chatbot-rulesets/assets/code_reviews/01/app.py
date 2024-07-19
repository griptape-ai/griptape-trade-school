from dotenv import load_dotenv

from griptape.structures import Agent

load_dotenv() # Load your environment

# Create an agent
agent = Agent()

# Run the agent
agent.run("I'm ready to chat.")