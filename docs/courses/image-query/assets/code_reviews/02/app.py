from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat

from rich import print as print  # Modifies print to use the Rich library

load_dotenv()  # Load your environment

# Create the Agent
agent = Agent(logger_level=0, stream=True)



# Modify the Agent's response to have some color.
def formatted_response(response: str) -> None:
    print(f"[dark_cyan]{response}", end="", flush=True)


# Begin Chatting
Chat(
    agent,
    intro_text="\nWelcome to Griptape Chat!\n",
    prompt_prefix="\nYou: ",
    processing_text="\nThinking...",
    response_prefix="\nAgent: ",
    output_fn=formatted_response,  # Uses the formatted_response function
).start()
