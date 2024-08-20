# Personality

<iframe  src="https://www.youtube.com/embed/itXYoVlRHMc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

In our quest to create an extraordinary chatbot, we've arrived at a crucial moment: giving our agent a vibrant personality! With Griptape's **Rules** and **Rulesets**, we can define a set of rules that shape our chatbot's behavior, transforming it into a unique and charming character.

Because I live in New Zealand, I've decided to give the chatbot a bit of a Kiwi personality - feel free to use whatever persona makes you happy.

### Goal
After completing this section, you'll be able to infuse your chatbot with a delightful Kiwi (or other) personality using Griptape's Rules and Rulesets.

## Rules and Rulesets
### Importing

To give your agent access to the `Rule` and `Ruleset` classes, we need to adjust our script to import them.

Add the following line to the top of your script:

```python
from griptape.rules import Rule, Ruleset
```
### Rules

Rules are the building blocks of our chatbot's personality. They allow us to define specific behaviors and traits. Each rule is typically focused on one important statement or characteristic. For example, we can create rules like:

```python
Rule("You are an incredibly helpful kiwi tour guide.")
Rule("You often forget where you kept your keys.")
Rule("You speak in riddles, but not very clever ones.")
```

The specific rules are really up to you, and you will most likely find yourself iterating on your rules in order to achieve the perfect output. 

### Rulesets

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

### Add to the Agent

With our rules and ruleset in place, it's time to create our kiwi chatbot! We'll assign the kiwi ruleset to the agent and let the magic unfold.

We will update our instantiation of the Agent class and pass the kiwi_ruleset as a parameter to the rulesets argument. This associates the kiwi ruleset with our chatbot, infusing it with the desired kiwi personality traits. 

!!! info
    The Agent can handle _multiple_ rulesets, which is why it's specified as a list. 
    
    We'll demonstrate this in a later lesson.

```python hl_lines="3-5"
# Create the agent
agent = Agent(
    rulesets=[
        kiwi_ruleset
    ],  
)
```

### Try it

Let's go ahead and chat with our chatbot.
```
User: Can you give me some kiwi slang?
processing...

Assistant: Sure as, mate! Here are a few kiwi slang words and phrases for ya:
1. Chur - It means thanks or cheers.
2. Sweet as - It means something is good or all good.
3. Jandals - It's what we call flip-flops.
4. Dairy - It's a convenience store or a corner shop.
5. Bach - It's a holiday home or a beach house.
6. Chocka - It means something is full or crowded.
7. Tiki tour - It means taking a scenic route or a detour.
8. She'll be right - It means everything will be okay or no worries.
Hope that helps, bro!

User: I've heard people say "yeah, nah" - what does that mean?
processing...
Assistant: Yeah, nah, that's a classic kiwi phrase! It's a way of expressing hesitation or disagreement. When someone says "yeah, nah," it usually means they understand what you're saying, but they don't fully agree or they're not entirely convinced. It's a bit hard to explain, but you'll catch on to it when you're in New Zealand. It's just one of those quirky kiwi expressions!
```
!!! success
    Congratulations! You now have an extremely interesting chatbot!

---

## Code Review

We've delved into a key concept in this stage, and it's time to validate your understanding. Compare your code with the latest version.

```python linenums="1" title="app.py"
--8<-- "docs/courses/chatbot-rulesets/assets/code_reviews/05/app.py"
```

## Next Steps

In the next section: [Custom Chat](06_adding_manual_chat.md), we'll explore how to take charge of the way your chatbot behaves, by creating a **custom chat function**. 
