from dotenv import load_dotenv
import logging

# Griptape Items
from griptape.structures import Agent
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

# Create a subclass for the Agent
class MyAgent(Agent):

    def respond (self, user_input):
        agent_response = agent.run(user_input)
        print("")
        print(f"Kiwi: {agent_response.output_task.output.value}")
        print("")

# Create the agent
agent = MyAgent(
    rulesets=[
        kiwi_ruleset,
    ],
    logger_level=logging.ERROR
)

# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = input("Chat with Kiwi: ")
        if user_input == "exit":
            is_chatting = False
        else:
            agent.respond(user_input)
      
# Run the agent
chat(agent)