## Overview

Now that you've got your environment all set up, it's time to actually start moving. In this stage, we'll put together a basic Griptape application and see it in action. 

<iframe  src="https://www.youtube.com/embed/_rg5rbzNc4c" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### Our Application

We are going to build a very simple application. It's going to simply take in a prompt, and return the result of that prompt. For example, we will be able to ask: "What's a good place to visit in New Zealand?" and it will give us an answer like "Abel Tasman" or "All of it".

## Griptape
### Agents

There are multiple ways communicate with LLMs via Griptape, but the one we'll use in this example is an **Agent**. You can learn more about Agents in [documentation](https://docs.griptape.ai/en/latest/griptape-framework/structures/agents/), but here's a simple way to understand them:

!!! Abstract
    Agents can do **one task**.

You give the Agent a prompt, it thinks for a bit, figures things out, and then returns a result. While that sounds relatively simple, it's actually quite cool. You can give the agent tools (WebScraper, Calculator, EmailClient, to name a few), you can give it rules about how to behave, and more. Agents can actually do quite a lot - but they're still one of the more simple ways of interacting with Griptape, which is why we'll use them to start with in this course.

Speaking of interacting with Griptape... we need to install it!

### Installing Griptape

Just like we installed the `python_dotenv` library, we need to do the same with Griptape. 

Open your Terminal and use `pip` to install `griptape`:

```sh
pip install griptape

```

!!! info
    This will take a minute to install. Another chance to enjoy a :coffee:!

### Import Griptape

Now comes the moment you've all been waiting for! Actually, it's the moment _before_ the moment. In this moment, we're going to import the Agent from the Griptape library. The moment _after_ that is probably the one you're really waiting for. But we have to do this moment first. Live in the now.

Modify your `app.py` to import the agent

```py title="app.py" hl_lines="3" linenums="1"
from dotenv import load_dotenv

from griptape.structures import Agent

load_dotenv() # Load the environment variables
```

As you can see, we're importing the Agent from `griptape.structures`. There are other structures we can work with, but again.. this is just setting up your environment. We'll talk about those in another course.

## The fun part
### Create the Agent

To create the Agent, we'll instantiate the class. 

```py title="app.py" hl_lines="7 8" linenums="1"
from dotenv import load_dotenv

from griptape.structures import Agent

load_dotenv() # Load the environment variables

# Create the Agent
agent = Agent()
```

### Run the Agent
_Now_ you get to tell the Agent what to do. Use the Agent's `run` method to execute a prompt.

```py title="app.py" hl_lines="10 11" linenums="1"
from dotenv import load_dotenv

from griptape.structures import Agent

load_dotenv() # Load the environment variables

# Create the Agent
agent = Agent()

# Run the agent
agent.run("Give me a haiku about skateboarding")
```

### Test the Agent

Let's see if our application works.

1. Save your file.
2. Use the **Run** icon in the upper right corner of VS Code, or open your terminal and type `python app.py`.

If everything has been set up correctly, you should see the result of the `agent.run()` command printed in the terminal. The exact output will depend on the current configuration and performance of the OpenAI API, but it should be a haiku about skateboarding.

```shell
[07/21/23 05:39:22] INFO     Task 801254fc5df64cda8930917a8afbc5bc                                              
                             Input: Create me a haiku about skateboarding                                       
[07/21/23 05:39:24] INFO     Task 801254fc5df64cda8930917a8afbc5bc                                              
                             Output: Skateboard glides swiftly,                                                 
                             Tricks and flips in the air, high,                                                 
                             Thrilling ride, pure bliss.      
```

!!! Success
    Congrats! You've taken the first push and created your first python script that works with a large language model!

---

## Next Steps

You've successfully set up your development environment, installed the necessary packages, obtained your OpenAI API key, and written and run a simple Griptape application. You've done a great job, so don't forget to celebrate your progress. 

Now that you've successfully completed the course, please check out these [Helpful Resources](04_helpful_resources.md) to learn more about Griptape!


