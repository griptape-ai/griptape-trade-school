# Quick Feedback

<iframe src="https://www.youtube.com/embed/Qi09TRhCh4k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## UX Enhancement

The UX of our application can be enhanced by letting the user know that the application is working after they execute a command. At the moment, it _is_ processing, but it just doesn't let the user know. We'll use the Spinner functionality from the Rich library to make the application a little more user-friendly and  visually appealing.

## Spinner

The `Console` class has a `status` method which will allow us to display a `Spinner` to the user while Griptape is waiting for the LLM response.

!!! abstract
    There are lots of spinners available. You can check them out by running the following in your terminal:
    
    ```shell
    python -m rich.spinner
    ```
    
    ![Alt text](assets/img/14_spinners.png)

### Importing the Console

```python
from rich.console import Console
```

Importing the Console class from the `rich` library is simple and straightforward, and should be familliar to you by this point in the lesson.

### Modify Respond

We will add a spinner to our `respond` method in the `MyAgent` subclass. This will show an animated spinner in the console while our agent is processing the user's input. This makes the app feel more responsive.

Update the `respond` method as follows:

```python hl_lines="4-6"
class MyAgent(Agent):
    def respond(self, user_input):

        console = Console()
        with console.status(spinner="simpleDotsScrolling", status=""):
            agent_response = self.run(user_input)
        
        # ...
```

In the code above, `console.status(spinner="simpleDotsScrolling", status="")` starts an animated spinner in the console that will run until the block of code it is wrapping (the agent's processing of user input) completes. 

!!! note
    We've left `status` blank - because we don't really need to send any text. However, feel free to add some text here if you desire.

Now when you run the chat, you'll notice the animated spinner right after you ask the chatbot a question!

![Alt Text](assets/img/14_spinner_response.gif)

---
## Code Review

Double-check your code to make sure the spinner is working as expected.

```python linenums="1" title="app.py" hl_lines="11 69-71"
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
            agent_response = self.run(user_input)

        data = json.loads(agent_response.output.value)
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
    rulesets=[
        kiwi_ruleset, zelda_ruleset, dad_ruleset,
        switcher_ruleset, json_ruleset  
    ],
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
```

## All Done!

!!! success
    You did it!

That's it! We've come a long way in this tutorial series and now you have a multi-persona chat application written with Griptape. Hopefully you've been able to see how using Rulesets can be used for both creative and structural control of your applications.

Congratulations on making it through! We're thrilled you decided to join us for this course and we hope you've enjoyed it as much as we have. We'd love to hear your feedback, so please don't hesitate to let us know what you thought.

More importantly, we wish you all the best as you continue your journey with Griptape and Python. Remember to have fun, experiment, and keep on learning. Happy coding! 🚀