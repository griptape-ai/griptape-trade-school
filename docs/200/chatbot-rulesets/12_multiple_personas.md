## Stage 12. Multiple Personas

In this exciting stage, we're going to give our chatbot multiple personalities to make conversations even more dynamic and engaging. Imagine your chatbot being able to switch between different identities, each with its own unique characteristics. Let's get started!

### 12.1 Defining the Personalities

To give our chatbot multiple personas, we'll create separate rulesets for each identity. These rulesets will define the behavior and characteristics of each persona. Here, I've added two new rulesets: "Zelda" (my grandmother), and "Dad" (my dad). 

```python
# Create rulesets for each persona
kiwi_ruleset = Ruleset(
        name='Kiwi',
        rules=[
            Rule('You identify only as a New Zealander.'),
            Rule('You have a very strong Kiwi accent.')
        ]
    )
zelda_ruleset = Ruleset(
        name='Zelda',
        rules=[
            Rule('You identify only as a grandmother.'),
            Rule('You like to use Yiddish.')
        ]
    )
dad_ruleset = Ruleset(
        name='Dad',
        rules=[
            Rule('You identify only as a dad.'),
            Rule('You like to use dad jokes.')
        ]
    )
```
### 12.2 Rules for Switching Personas

We can't just give the chatbot all these personas and expect it to know what to do. We need to provide some structure around it. So we're going to create another ruleset called the **Switcher**. This ruleset will understand how and when to switch personalities. There are some key rules for us to think of:

  - We want the chatbot to be able to switch personalities when it makes sense to (either it thinks it needs to, or the user asks for it)
  - We don't want it to identify as the "Switcher" or "json_output" rulesets. That wouldn't make any sense.
  - When it _does_ switch rulesets, it should only take on the new persona
  - When it switches personas, it should remember the facts from the previous conversation, but not act like the previous identity.

```python

switcher_ruleset = Ruleset(
    name='Switcher',
    rules=[
        Rule("IMPORTANT: you have the ability to switch identities when you find it appropriate."),
        Rule("IMPORTANT: You can not identify as 'Switcher' or 'json_output'."),
        Rule("IMPORTANT: When you switch identities, you only take on the persona of the new identity."),
        Rule("IMPORTANT: When you switch identities, you remember the facts from your conversation, but you do not act like your old identity."),
    ]
)

```
### 12.3 Add the Rulesets

Let's now give the agent all these rulesets to work with. We'll simply add them to the list of `rulesets` in the `agent` instantiation.

```python
# Create the agent
agent = MyAgent(
    rulesets=[kiwi_ruleset, zelda_ruleset, dad_ruleset, switcher_ruleset, json_ruleset],
    logger_level=logging.ERROR
)

```

### 12.4 Remove the name of the chatbot from the Prompt

It doesn't make sense for us to keep prompting the user to "Chat with Kiwi:" if we might have multiple personalities, so let's modify the `Prompt` in the `chat` function:

```python
def chat(agent):
        # ...
        user_input = Prompt.ask("[grey50]Chat")
        # ...
```

### 12.5 Chat away

Now your chatbot is ready to switch between different personalities and engage in exciting conversations with users! Go ahead and run the chatbot. Ask it how many personalities it has, ask it to switch them up, etc. See how it performs. 

![Alt text](assets/img/12_two_personalities.png)

Notice in the above image we've got two personas talking, but it's difficult to tell them apart. We'll fix that in the next section.

---

### Code Checkpoint
We're making great progress. Review the [Stage 12 Code Checkpoint](../assets/examples/12_app.py) on GitHub.

### Next Steps

In the next stage: [Stage 13 - Differentiating Personalities](13_adding_personality_colors.md), we'll make it easier to differentiate between which chatbot you're speaking with.