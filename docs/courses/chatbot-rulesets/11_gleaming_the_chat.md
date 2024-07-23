# Improving the Prompt

<iframe src="https://www.youtube.com/embed/mtwKto1vGzE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

In this stage, we'll improve the chatbot experience by using colors with the `rich` library. This will allow us to distinguish the chatbot's response from our prompt.

## Style Class

To add colors, we'll take advantage of the `Style` class from the `rich` library. This [class](https://rich.readthedocs.io/en/stable/style.html){target="_blank"} allows you to use one of the 256 [Standard Colors](https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors){target="_blank"} that are accepted in terminals, Hex values, or RGB values. It's pretty nice.

### Import


To add it, update the `import` section of your code to include the `Style` class:

```python
from rich.style import Style
```

### Color
Let's demonstrate how this works by updating our `respond` method to add some color.

Change the `rprint` line to include the `style` attribute:

```python hl_lines="7"
class MyAgent(Agent):
    def chatbot(agent, user_input):
        # ...
        rprint(Panel.fit(
            formatted_response, 
            width=80, 
            style=Style(color="light_sea_green"),
        ))
        # ...
```
Let's see how it looks:

![Alt text](assets/img/11_gday_in_green.png)

## Prompt Class

We can also take advantage of the `Prompt` class in the `rich` library to make our prompt more readable by separating the color of the prompt from the text the user enters.

### Import


First, import the `Prompt` class:

```python
from rich.prompt import Prompt
```

### Prompt

Then, change the `input` line in the `chat` function to use the `Prompt.ask()` method:

```python hl_lines="3"
def chat(agent):
        # ...
        user_input = Prompt.ask("[grey50]Chat with Kiwi:")
        # ...
```

In the updated code, we replaced the standard `input` function with `Prompt.ask()` and passed it a color to create a more readable prompt. Of course, you can choose whatever color you want to make it stand out even more. 

![Alt text](assets/img/11_prompt_color.png)

There are a few interesting options with the Prompt class that are worth exploring, including default values, a list of choices, and more. Check out the [documentation](https://rich.readthedocs.io/en/stable/prompt.html){target="_blank"} for more goodness.

### Try it

Engage in a conversation with Kiwi and enjoy the interactive and intuitive nature of the prompt. Respond to the prompt using natural language, and observe the chatbot's responses displayed in the familiar chat-like format.

---

## Code Review

```python linenums="1" title="app.py"
--8<-- "docs/courses/chatbot-rulesets/assets/code_reviews/11/app.py"
```

## Next Steps

In the next section: [Multiple Personas](12_multiple_personas.md), we'll dive into an explosion of personality by using Rulesets to create multiple personas to chat with.
