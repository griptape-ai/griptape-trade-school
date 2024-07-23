# Colorful Personalities

<iframe  src="https://www.youtube.com/embed/pNqvebn2hbY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

In this step, we're going to add some flair to our chatbot by assigning different colors to each persona. This will visually distinguish the different personalities, making the conversation more engaging and fun! 

We'll do this by giving each persona a favorite color, then add another key to our `json_output` ruleset, and use that key in our `respond` method.

## Updating Rulesets

### Favorite Colors

To assign colors to each persona, we'll add new rules to each of our identity ruleset to give them all favorite colors. You're welcome to use [Standard Colors](https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors){target="_blank"}, Hex, or RGB values. Whatever makes you happy.

```python

kiwi_ruleset = Ruleset(
    name = "kiwi",
    rules = [
        # ... truncated for brevity
        Rule("Favorite color: light_sea_green")
    ]
)
zelda_ruleset = Ruleset(
    name="Zelda",
    rules=[
        # ...
        Rule("Favorite color: light_pink3")

    ]
)
dad_ruleset = Ruleset(
    name="Dad",
    rules=[
        # ... 
        Rule("Favorite color: light_steel_blue")
    ]
)

```
### Add Key

We also need to make changes to the `json_ruleset` to include the Favorite Color key. Modify the first rule to include that key:

```python hl_lines="4"
json_ruleset = Ruleset(
    name="json_ruleset",
    rules=[
        Rule("Respond in plain text only with valid JSON objects that have the following keys: response, favorite_color, continue_chatting."),
        # ... 
    ]
)
```
## Respond Method

Next, we'll adjust the `respond` method get the favorite color, and use it properly.

### Get the color

After the `continue_chatting = data["continue_chatting"]` line, add one to get the color:

```python hl_lines="5"
class MyAgent(Agent):
    def respond(self, user_input):
        # ...
        continue_chatting = data["continue_chatting"]
        color = data["favorite_color"]
        # ...
```

### Use it

Then, update the `style` line in the `rprint` statement to use `color` instead of specifying it directly as we were before:

```python hl_lines="7"
class MyAgent(Agent):
    def respond(self, user_input):
        # ...
        rprint(Panel.fit(
            formatted_response, 
            width=80, 
            style=Style(color=color)
        ))
        # ...
```

### Try it

Run the code and notice how much nicer it is to be able to discern who is talking based on their color.

![Alt text](assets/img/13_color_output.png)

## Adding a Name

We're not quite finished yet. We also can make things a bit easier to follow if we clarify the name of the persona we're chatting with.

### Update Ruleset

This will be a relatively quick fix. We just need to add another key to the `json_ruleset`, and then modify the `rprint` statement again.

First, add the `name` key:

```python hl_lines="5"
json_ruleset = Ruleset(
    name="json_ruleset",
    rules=[
        # ...
        Rule("Respond in plain text only with valid JSON objects that have the following keys: name, response, favorite_color, continue_chatting."),
        # ...
    ]
)

```

### Get the Name

Now get the `name` from the json data in the `respond` method of the `MyAgent` class:


```python hl_lines="5"
class MyAgent(Agent):
    def respond(self, user_input):
        # ...
        color = data["favorite_color"]
        name = data["name"]
        # ...
```

### Use it

Then, add a `title` and `title_align` in the `rprint` function:

```python hl_lines="8-9"
class MyAgent(Agent):
    def respond(self, user_input):
        # ...
        rprint(Panel.fit(
            formatted_response, 
            width=80, 
            style=Style(color=color),
            title=name,
            title_align="left"
        ))
        # ...
```

### Try it 

Give it a try and see how much nicer it is!

![Alt text](assets/img/13_with_names.png)

---

## Code Review

Lots of changes in this section, with some great usability enhancements! 

```python linenums="1" title="app.py"
--8<-- "docs/courses/chatbot-rulesets/assets/code_reviews/13/app.py"
```

## Next Steps

In the next section: [Quick Feedback](14_making_it_quick.md), we'll make the chatbot feel a bit more responsive to user input by giving it a spinner so it doesn't feel like it's lagging while the LLM is fetching it's response.