from dotenv import load_dotenv
import logging

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.rules import Rule, Ruleset

# Load environment variables
load_dotenv()

# Create a ruleset for the agent
kiwi_ruleset = Ruleset(
    name = "kiwi",
    rules = [
        Rule("You identify as a New Zealander."),
        Rule("You have a strong kiwi accent.")
    ]
)

# Create the agent
agent = Agent(
    rulesets=[
        kiwi_ruleset
    ],
    logger_level=logging.ERROR
)

# Run the agent
Chat(agent).start()