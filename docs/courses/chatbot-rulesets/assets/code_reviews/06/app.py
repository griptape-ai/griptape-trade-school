from dotenv import load_dotenv

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

# Create the agent
agent = Agent(
    rulesets=[
        kiwi_ruleset,
    ],
)


# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = input("Chat with Kiwi: ")
        if user_input == "exit":
            is_chatting = False
        else:
            # Keep on chatting
            agent_result = agent.run(user_input)
            print(f"Kiwi: {agent_result.output_task.output.value}")


# Run the agent
chat(agent)
