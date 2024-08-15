from dotenv import load_dotenv
import logging
import json

# Griptape Items
from griptape.structures import Agent
from griptape.rules import Rule, Ruleset

# Load environment variables
load_dotenv()

# Create a ruleset for the agent
kiwi_ruleset = Ruleset(
    name="kiwi",
    rules=[
        Rule("You identify as a New Zealander."),
        Rule("You have a strong kiwi accent."),
    ],
)

json_ruleset = Ruleset(
    name="json_ruleset",
    rules=[
        Rule(
            "Respond in plain text only with JSON objects that have the following keys: response, continue_chatting."
        ),
        Rule(
            "The 'response' value should be a string that is your response to the user."
        ),
        Rule(
            "If it sounds like the person is done chatting, set 'continue_chatting' to false, otherwise it is true"
        ),
    ],
)


# Create a subclass for the Agent
class MyAgent(Agent):
    def respond(self, user_input):
        agent_response = agent.run(user_input)
        data = json.loads(agent_response.output_task.output.value)
        response = data["response"]
        continue_chatting = data["continue_chatting"]

        print("")
        print(f"Kiwi: {response}")
        print("")

        return continue_chatting


# Create the agent
agent = MyAgent(rulesets=[kiwi_ruleset, json_ruleset], logger_level=logging.ERROR)


# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = input("Chat with Kiwi: ")
        is_chatting = agent.respond(user_input)


# Introduce the agent
agent.respond("Introduce yourself to the user.")

# Run the agent
chat(agent)
