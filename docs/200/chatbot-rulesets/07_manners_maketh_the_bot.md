## Stage 7. Manners Maketh the Bot

To create a great experience for the user, in this stage we'll get the chatbot to introduce itself when you start talking, and say goodbye when you're done.

### 7.1 Hey, it isn't polite to just leave without saying goodbye

Let's give the chatbot a bit social grace and have it say goodbye when the person stops the chat. Before setting `is_chatting = False`, add the following line:

```python
agent.respond("The user is finished chatting. Say goodbye.")

```
This will tell the agent that the user is leaving the chat, and then print the output to the screen. Here's that section of the code in context:

```python
    # ... truncated for brevity ... 
    while is_chatting:

        # ... 
        if user_result == "exit":
            agent.respond("The user is finished chatting. Say goodbye.")
            chatting = False
        # ... 

```

Here's an example of how that would play out:
```
Chat with kiwi: exit

Kiwi: Good on ya, mate! Take care and have a ripper day!
```

### 7.2 You say goodbye, but what about hello?

It's always awkward to walk into the middle of a conversation and not have someone acknowledge your presence. Let's modify the code to have the chatbot introduce itself before you begin talking.

Add a call to the agent to introduce itself before the `# Run the agent` line:
```python
# Introduce the agent
agent.respond("Introduce yourself to the user.")

# Run the agent
chat(agent)
```

Now feel free to run the chat a few times. 

```
Kiwi: Kia ora! G'day mate! I'm a conversational bot from Aotearoa, also known as New Zealand. How can I help you today?

Chat with the kiwi: Can I have a funny haiku about gumboots?

Kiwi:  Sure as, bro! Here's a funny haiku about gumboots:
Gumboots on my feet,
Squishy mud, they can't be beat,
Kiwi fashion feat!

Chat with the kiwi: nice, thanks!

Kiwi:  No worries, mate! Anytime you need a laugh, just give me a holler. Cheers!

Chat with the kiwi: exit

Kiwi: Sweet as, bro! Thanks for chattin' with me. Take care and catch you later! Ka kite!
```

---

### Code Checkpoint

Politeness isn't necessary to the execution of the code, but it's a key element to giving it personality. Check your code against the [Stage 7 Code Checkpoint](../assets/examples/07_app.py) on Github.

### Next Steps

Congratulations on implementing manual chat functionality and taking control of the conversation! In the next section [Adding Another Ruleset](08_adding_another_ruleset_for_output.md), we'll explore the world of output rulesets, unlocking the ability to control the chatbot's responses in different formats such as JSON, YAML, or even haiku.