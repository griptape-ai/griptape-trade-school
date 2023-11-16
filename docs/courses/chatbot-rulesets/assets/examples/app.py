"""
Chatbot Agent

This script creates a command line chatbot with various 'identities' it can assume.
The chatbot uses the Griptape library for managing identities and interactions.

An identity is determined by a ruleset, and the chatbot can switch identities based 
on user choice. The identities in this example are: 'Kiwi', 'Zelda', and 'Dad'
each with their specific characteristics and conversation styles.

Key Features:
1. Uses Griptape Rulesets and LLMs for a natural chat experience
2. Random identity selection
3. Switch identities simply by asking
4. Exit chat using natural language

Usage:
Run the script and just start chatting

Requirements:
- OpenAI API Key stored in a .env file. 
  You can get it here: https://beta.openai.com/account/api-keys

Dependencies:
- griptape
- rich
- python-dotenv
- json
- logging
"""

from dotenv import load_dotenv
import logging
import json

# Rich
from rich import print as rprint
from rich.panel import Panel
from rich.markdown import Markdown
from rich.style import Style
from rich.prompt import Prompt
from rich.console import Console

# Griptape 
from griptape.structures import Agent
from griptape.rules import Rule, Ruleset

# Load environment variables
load_dotenv()

# Create rulesets for each persona
kiwi_ruleset = Ruleset(
        name='Kiwi',
        rules=[
            Rule('You identify only as a New Zealander.'),
            Rule('You have a very strong Kiwi accent.'),
            Rule("Favorite color: light_sea_green")

        ]
    )
zelda_ruleset = Ruleset(
        name='Zelda',
        rules=[
            Rule('You identify only as a grandmother.'),
            Rule('You like to use Yiddish.'),
            Rule("Favorite color: light_pink3")

        ]
    )
dad_ruleset = Ruleset(
        name='Dad',
        rules=[
            Rule('You identify only as a dad.'),
            Rule('You like to use dad jokes.'),
            Rule("Favorite color: light_steel_blue")

        ]
    )

switcher_ruleset = Ruleset(
    name='Switcher',
    rules=[
        Rule("IMPORTANT: you have the ability to switch identities when you find it appropriate."),
        Rule("IMPORTANT: You can not identify as 'Switcher' or 'json_output'."),
        Rule("IMPORTANT: When you switch identities, you only take on the persona of the new identity."),
        Rule("IMPORTANT: When you switch identities, you remember the facts from your conversation, but you do not act like your old identity."),
    ]
)

json_ruleset = Ruleset(
    name="json_ruleset",
    rules=[
        Rule("Respond in plain text only with JSON objects that have the following keys: name, response, favorite_color, continue_chatting."),
        Rule("The 'response' value should be a string that can be safely converted to markdown format."),
        Rule("If it sounds like the person is done chatting, set 'continue_chatting' to False, otherwise it is True"),
    ]
)

# Create a subclass for the Agent
class MyAgent(Agent):

    def respond (self, user_input):
        console = Console()
        with console.status(spinner="simpleDotsScrolling", status=""):
            agent_response = agent.run(user_input)  
        data = json.loads(agent_response.output_task.output.value)
        response = data["response"]
        continue_chatting = data["continue_chatting"]
        color = data["favorite_color"]
        name = data["name"]

        formatted_response = Markdown(response)

        print("")
        rprint(Panel.fit(formatted_response, 
            width=80, 
            style=Style(color=color),
            title=name,
            title_align="left"
            ))
        print("")

        return continue_chatting

# Create the agent
agent = MyAgent(
    rulesets=[switcher_ruleset, json_ruleset, kiwi_ruleset, zelda_ruleset, dad_ruleset, ],
    logger_level=logging.ERROR
)

# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = Prompt.ask("[grey50]Chat")
        is_chatting = agent.respond(user_input)

# Introduce the agent
agent.respond("Introduce yourself.")

# Run the agent#
chat(agent)