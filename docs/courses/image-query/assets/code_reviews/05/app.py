from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import ImageQueryTool, FileManagerTool
from griptape.engines import ImageQueryEngine
from griptape.drivers import OpenAiImageQueryDriver

from rich import print as print  # Modifies print to use the Rich library

load_dotenv()  # Load your environment

# Create an Image Query Driver
driver = OpenAiImageQueryDriver(model="gpt-4o")

# Create an Image Query Engine
engine = ImageQueryEngine(
    image_query_driver=driver,
)

# Configure the ImageQueryTool
image_query_tool = ImageQueryTool(image_query_engine=engine, off_prompt=False)

# Create the Agent
agent = Agent(
    tools=[image_query_tool, FileManagerTool(off_prompt=False)],
    stream=True,
)


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
