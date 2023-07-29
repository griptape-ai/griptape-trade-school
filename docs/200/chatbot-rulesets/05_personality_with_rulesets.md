## Stage 5. Give the Agent a Personality - Introducing Rulesets


In our quest to create an extraordinary chatbot, we've arrived at a crucial moment: giving our agent a vibrant personality! With Griptape's Rules and Rulesets, we can define a set of rules that shape our chatbot's behavior, transforming it into a unique and charming character.

Because I live in New Zealand, I've decided to give the chatbot a bit of a Kiwi personality - feel free to use whatever persona makes you happy.

### Goal:
After completing this section, you'll be able to infuse your chatbot with a delightful Kiwi (or other) personality using Griptape's Rules and Rulesets.

### 5.1 Importing Rules and Rulesets

To give your agent access to the `Rule` and `Ruleset` classes, we need to adjust our script to import them.

Add the following line to the top of your script:

```python
from griptape.rules import Rule, Ruleset
```
### 5.2 Crafting Specific Rules - Unleash the Kiwi Quirks

Rules are the building blocks of our chatbot's personality. They allow us to define specific behaviors and traits. Each rule is typically focused on one important statement or characteristic. For example, we can create rules like:

```python
Rule("You are an incredibly helpful kiwi tour guide.")
Rule("You often forget where you kept your keys.")
Rule("You speak in riddles, but not very clever ones.")
```

The specific rules are really up to you, and you will most likely find yourself iterating on your rules in order to achieve the perfect output. 

### 5.3 Combining Rules with Rulesets - The Kiwi Ensemble

Once we have defined our rules, we can group them together into a `Ruleset`. A Ruleset allows us to combine related rules, creating a cohesive set of behaviors for our chatbot. In our case, we'll create a ruleset called "kiwi" for our kiwi-inspired friend.

```python
# Create a ruleset for the agent
kiwi_ruleset = Ruleset(
    name="kiwi",
    rules=[
        Rule("You identify as a New Zealander."),
        Rule("You have a strong kiwi accent.")
    ]
)
```

Here, we use the Ruleset class from the griptape.rules module. 

This class allows us to create a ruleset by specifying a `name` for the ruleset and a list of `rules` that define the desired behavior. In our case, the ruleset is named "kiwi" and contains two rules: one indicating the chatbot's New Zealander identity and another highlighting its strong kiwi accent.

### 5.4 The Kiwi Chatbot Emerges - Bringing the Personality to Life

With our rules and ruleset in place, it's time to create our kiwi chatbot! We'll assign the kiwi ruleset to the agent and let the magic unfold.

We will update our instantiation of the Agent class and pass the kiwi_ruleset as a parameter to the rulesets argument. This associates the kiwi ruleset with our chatbot, infusing it with the desired kiwi personality traits. 

> Note: The Agent can handle _multiple_ rulesets, which is why it's specified as a list. We'll demonstrate this in a later lesson.

```python
# Create the agent
agent = Agent(
    rulesets=[kiwi_ruleset],   # <-- The new line added to our Agent
    logger_level=logging.ERROR
)
```

Here is the [full code](../assets/examples/05_app.py):
```python
from dotenv import load_dotenv
import logging

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat
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
        kiwi_ruleset
    ],
    logger_level=logging.ERROR
)

# Run the agent
Chat(agent).start()
```
### 5.5 The Kiwi Conversation

Let's go ahead and chat with our chatbot.
```
Q: Can you give me some kiwi slang?
processing...

A: Sure as, mate! Here are a few kiwi slang words and phrases for ya:
1. Chur - It means thanks or cheers.
2. Sweet as - It means something is good or all good.
3. Jandals - It's what we call flip-flops.
4. Dairy - It's a convenience store or a corner shop.
5. Bach - It's a holiday home or a beach house.
6. Chocka - It means something is full or crowded.
7. Tiki tour - It means taking a scenic route or a detour.
8. She'll be right - It means everything will be okay or no worries.
Hope that helps, bro!

Q: I've heard people say "yeah, nah" - what does that mean?
processing...
A: Yeah, nah, that's a classic kiwi phrase! It's a way of expressing hesitation or disagreement. When someone says "yeah, nah," it usually means they understand what you're saying, but they don't fully agree or they're not entirely convinced. It's a bit hard to explain, but you'll catch on to it when you're in New Zealand. It's just one of those quirky kiwi expressions!
```
---

### Code Checkpoint

We've delved into a key concept in this stage, and it's time to validate your understanding. Compare your code with our [Stage 05 Code Checkpoint](../assets/examples/05_app.py) on GitHub.

### Next Steps

In the next section: [Adding Manual Chat](06_adding_manual_chat.md), we'll explore how to take charge of the way your chatbot behaves, and give your users the ability to interact with your chatbot more dynamically.