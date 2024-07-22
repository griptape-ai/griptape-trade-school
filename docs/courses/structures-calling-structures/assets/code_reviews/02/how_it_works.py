from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.rules import Rule, Ruleset
from griptape.drivers import LocalStructureRunDriver
from griptape.tools import StructureRunClient, TaskMemoryClient
from griptape.utils import Chat

load_dotenv()  # Load your environment


# Create a grammar analyzer Agent as a function to be used
# with LocalStructureRunDriver
def grammar_agent():
    # Create the agent with appropriate rules
    agent = Agent(
     logger_level=0, # Keep this agent's logs hidden.
        rulesets=[
            Ruleset(
                name="Grammar Checker",
                rules=[
                    Rule(
                        "Follow standard grammar rules from recognized sources to evaluate and correct sentences."
                    ),
                    Rule(
                        "Ensure sentences are clear and readable, suggesting simpler alternatives for complex structures or jargon."
                    ),
                    Rule("Check for spelling and punctuation errors."),
                    Rule(
                        "Offer suggestions for improving the overall quality of the text, including word choice and sentence structure."
                    ),
                ],
            )
        ]
    )

    # Return the agent from the function
    return agent


# Create a LocalStructureRunDriver
# We pass the grammar_agent function to the structure_factory_fn
grammar_agent_driver = LocalStructureRunDriver(
    structure_factory_fn=grammar_agent
)

# Create a client using the driver
# It's important to define the name and the description, this is how
# the agent we're chatting with will know to use the grammar agent.
#
# In this example we're setting off_prompt to True. This demonstrates
# how the agent's response could be kept private from the original LLM.
grammar_agent_client = StructureRunClient(
    name="Grammar Agent",
    description="An agent to evaluate and correct sentences based on standard grammar rules.",
    driver=grammar_agent_driver,
    off_prompt=True,
)

# Create an agent to chat with
# Pass it the grammar_agent_client and TaskMemoryClient to access
# the agent's responses.
chat_agent = Agent(
    tools=[
        grammar_agent_client,  # Add the Grammar Agent
        TaskMemoryClient( off_prompt=False ),  
    ],
)

Chat(chat_agent).start()  # start the chat
