from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat  #   <-- Added Chat

# Load environment variables
load_dotenv()

# Create the agent
agent = Agent()

# Run the agent
# agent.run("Hi, how are you?")     <-- We no longer need this line

# Begin Chatting
Chat(agent).start()
