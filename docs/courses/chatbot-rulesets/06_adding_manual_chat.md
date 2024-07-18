# Custom Chat
<iframe src="https://www.youtube.com/embed/jCCWwxmgkwc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

!!! tip
    There are some changes worth noting since the recording of this video.
    
    1. The `Chat` utility has added a few new options. You can now provide `prompt_prefix`, `response_prefix`, `exit_keywords` and more.

        Review the `Chat Utility` [reference guide](https://docs.griptape.ai/latest/reference/griptape/utils/chat/){target="_blank"} for a full breakdown.

    2. Agent Output has changed from: 

        `agent_result.output_task.output.value` to `agent_result.output_task.output.value`.

        This change is reflected in the code in the course, but not in the video at this time.
    
While the chatbot is working, it's not very user-friendly yet. The `User:` and `Assistant:` prompts don't make for the most engaging for a user experience.

In this step, we'll implement a manual chat experience, giving us more control over the conversation with our chatbot. We'll remove the Chat utility and create our own custom functions to facilitate interactive and dynamic conversations.

Let's get started!

## Remove the Chat Utility

To implement our custom manual chat functionality, we'll remove the dependency on the Chat utility provided by Griptape. We'll no longer need the line `from griptape.utils import Chat` in our code.

Update the code by commenting out or removing the following line:

```python
# from griptape.utils import Chat
```

Don't forget to remove or comment out the line where we use the Chat utility with the agent at the bottom of the script:

```python
# Run the agent
# Chat(agent).start()
```

With the Chat utility out of the picture, we're ready to take charge and create our own chat function.

## Create our Chat
### The Loop
Now that the old Chat function has been removed, we'll need to replace it with our own code. Let's start by with a simple loop that takes the user input until they type `exit`.


```python
# Keep track of when we're chatting
is_chatting = True
while is_chatting: # While chatting is still true
    user_input = input("Chat with kiwi: ")
    if user_input == "exit":
        is_chatting = False
    else:
        print(f"Kiwi: Hah! you said: {user_input}!")

```

If you just run this code on it's own, you'll see that it allows the user to keep entering information over and over again until they type exit.

It's not very amazing, and certainly doesn't interact with the agent yet, so let's modify the code to handle that.

## Add the Agent

After the `else:` statement, change the code to call `agent.run()`:

```python hl_lines="4 5"
while is_chatting:
    # ... truncated for brevity ... #
else:
    agent_result = agent.run(user_input)
    print (f"Kiwi: {agent_result.output_task.output.value}")
```

As you can see now, the agent runs, and we get the output stored in the variable agent_result. We can then print that output by using the `output.value` attribute.

## Chat Function
### Create

Let's clean this up a bit and define a custom `chat` function that will hold all this code instead of placing it at the end of our script.

Here's the code for the `chat` function and the way we can call it:

```python
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
            print (f"Kiwi: {agent_result.output_task.output.value}")
```

### Call

Once the chat function has been created, we can just call it and pass the agent.
``` python
# Run the agent
chat(agent)
```

The `chat` function takes the `agent` as an argument.

You shouldn't notice any difference to how you ran this before, it's just a bit cleaner.

Engage in stimulating conversations, explore various topics, and enjoy the interactive experience as you communicate with your chatbot.

---

## Code Checkpoint

We made a lot of important changes in this stage. Before we move forward, let's compare code. Changed lines are highlighted.

```python PYTEST_CHECK linenums="1" hl_lines="28-38 41" title="app.py"
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

# Create the agent
agent = Agent(
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
            # Keep on chatting
            agent_result = agent.run(user_input)
            print (f"Kiwi: {agent_result.output_task.output.value}")
      
# Run the agent
chat(agent)
```
## Next Steps

Congratulations on implementing manual chat functionality and taking control of the conversation! In the next section: [Manners Maketh the Bot](07_manners_maketh_the_bot.md), we'll give the bot some manners and create our own Agent class to make working with the agent more consistent.