As with any project, the first step is setting up your environment. Let's get started by ensuring you have a project structure ready to work with.

!!! Tip "Important"
    Since this is an intermediate-level course, please ensure you've gone through the [Griptape Setup - Visual Studio Code](../../setup/index.md) course to set up your environment. We will be starting from the code at that point.

### Create a Project

Following the instructions in [Griptape Setup - Visual Studio Code ](../../setup/01_setting_up_environment.md) please:

1. Create your project folder. Example: `griptape-structure-client`
2. Set up your virtual environment
3. Ensure you `pip install griptape python-dotenv`
4. Create a `.env` file with your `OPENAI_API_KEY`
5. Create your `app.py` file with the following code:

```py title="app.py" linenums="1"
from dotenv import load_dotenv

load_dotenv() # Load your environment
```

### Create a Chatbot

In a typical setup for a TradeSchool course we’d leave the setup at this step - however in this case we’ll take it a step further and create a Chatbot. We’re going to use code from another course and just copy that over. 

The [Image Query SEO Bonanza](../image-query/01_setup.md) course has a great agent we can use. Simply copy the code from the Chatbot section in the [Code Review](../image-query/02_chatbot.md#code-review) area and save that as your app.py.

```py title="app.py" linenums="1"
from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat

from rich import print as print  # Modifies print to use the Rich library

load_dotenv()  # Load your environment

# Create the Agent
agent = Agent(logger_level=0)

# Configure the agent to stream it's responses.
agent.config.global_drivers.prompt_driver.stream = True

# Modify the Agent's response to have some color.
def formatted_response(response: str) -> str:
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
```

---
## Next Steps
And there you go, your environment is all set up! In the [next section](02_concepts.md), learn more about how StructureRunDrivers work.