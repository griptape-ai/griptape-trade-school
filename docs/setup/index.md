
# Setting Up Your Python Environment for Griptape

## Kickoff and Foundations

<iframe src="https://www.youtube.com/embed/FoMx8mXKW5E" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Welcome to the getting started course for Griptape. We'll be using Visual Studio Code and the Griptape library, which make a great combo for coding with Large Language Models (LLMs). 

### What will I learn?

By the end of the course you will have the ability to use Griptape to work with Large Language Models. You will be setting up your Python environment, install a code editor, install Griptape, and be ready to go.

``` py title="griptape_developer.py"

from dotenv import load_dotenv
from griptape.structures import Agent

load_dotenv()

# Create an agent
agent = Agent()

# Run the agent
agent.run("Hello! I'm a new Griptape Developer!")
```

###  Who is this course for?
This course is aimed at **beginners** to **intermediate** level Python developers who are interested in setting up a Python environment to develop tools and applications with Griptape.

## Why Visual Studio Code?

Using the right coding software (or Integrated Development Environment - IDE) can make your coding sessions a breeze... or not (if you choose the wrong one).

Visual Studio Code (VS Code for short) is our IDE of choice for a few reasons. It's lightweight, highly customizable, and has a vast range of extensions. 

## Griptape and Python

Griptape provides a simple, Pythonic interface to interact with these models, taking care of the complexities so we can focus on coding our applications. 

In the next stages, we will be going through:

- **[Setting Up](01_setting_up_environment.md)**: Here, we will install and set up the basic tools we need: Visual Studio Code, Python, and create our directory structure. We'll also ensure that you have the right Python environment in place.

- **[OpenAI API Key](02_openai.md)**: Before jumping into Griptape, we need to get our OpenAI API Key and set up our environment so it's ready.

- **[Griptape](03_griptape.md)**: We'll install the Griptape library and send our first message to the LLM!

Are you ready to get started? Let's move on to [Setting up your environment](01_setting_up_environment.md)!