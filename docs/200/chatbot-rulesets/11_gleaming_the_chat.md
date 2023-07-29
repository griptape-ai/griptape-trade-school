## Stage 11: Gleaming the Chat

In this stage, we'll improve the chatbot experience by using colors with the `rich` library. This will allow us to distinguish the chatbot's response from our prompt.

### 11.1 Using the `Style` class

To add colors, we'll take advantage of the `Style` class from the `rich` library. This [class](https://rich.readthedocs.io/en/stable/style.html) allows you to use one of the 256 [Standard Colors](https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors) that are accepted in terminals, Hex values, or RGB values. It's pretty nice.

To add it, update the `import` section of your code to include the `Style` class:

```python
from rich.style import Style
```

### 11.2 Give it some color

Let's demonstrate how this works by updating our `respond` method to add some color.

Change the `rprint` line to include the `style` attribute:

```python
class MyAgent(Agent):
    def chatbot(agent, user_input):
        # ...
        rprint(Panel.fit(formatted_response, 
            width=80, 
            style=Style(color="light_sea_green")
            ))
        # ...
```
Let's see how it looks:

![Alt text](assets/img/11_gday_in_green.png)

### 11.3 Enhancing the Prompt

We can also take advantage of a `Prompt` class in the `rich` library to make our prompt a bit nicer to look at by separating the color of the prompt from the text the user enters.

First, import the Prompt class:

```python
from rich.prompt import Prompt
```

Then, change the `input` line in the `chat` function to use the `Prompt.ask()` function:

```python
def chat(agent):
        # ...
        user_input = Prompt.ask("[grey50]Chat with Kiwi:")
        # ...
```

In this updated code, we replace the standard `input` function with `Prompt.ask()` and pass it a color to create an improved prompt. Of course, you can choose whatever color you want to make it stand out even more. 

![Alt text](assets/img/11_prompt_color.png)

There are a few interesting options with the Prompt class that are worth exploring, including default values, a list of choices, and more. Check out the [documentation](https://rich.readthedocs.io/en/stable/prompt.html) for more goodness.


Engage in a conversation with Kiwi and enjoy the interactive and intuitive nature of the prompt. Respond to the prompt using natural language, and observe the chatbot's responses displayed in the familiar chat-like format.

---

### Code Checkpoint
We covered a bit of new material here, please compare your code with the [Stage 11 Code Checkpoint](../assets/examples/11_app.py) on GitHub.


### Next Steps

In the next section, [Stage 12: Multiple Personas](12_multiple_personas.md), we'll dive into an explosion of personality by using Rulesets to create multiple personas to chat with.
