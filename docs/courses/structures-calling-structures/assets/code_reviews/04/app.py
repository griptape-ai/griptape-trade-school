from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.drivers import LocalStructureRunDriver
from griptape.tools import StructureRunClient

from image_pipeline import create_image_pipeline

from rich import print as print  # Modifies print to use the Rich library

load_dotenv()  # Load your environment

# Create the driver
image_pipeline_driver = LocalStructureRunDriver(
    structure_factory_fn=create_image_pipeline
)

# Create the Client
image_pipeline_client = StructureRunClient(
    name="Image Creator",
    description="Create an image based on a prompt.",
    driver=image_pipeline_driver,
    off_prompt=False,
)

# Create the Agent
agent = Agent(logger_level=0, tools=[image_pipeline_client])

# Configure the agent to stream it's responses.
agent.config.prompt_driver.stream = True


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

