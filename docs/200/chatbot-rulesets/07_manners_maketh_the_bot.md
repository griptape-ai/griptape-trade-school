# Manners Maketh the Bot

<iframe src="https://www.youtube.com/embed/AXLWIIS8yTw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

This course covers two topics:

- Adding manners
- Making agent interaction more consistent by creating a `respond` method

We'll start with manners, as that will clearly demonstrate our need to find a way to make our interaction with our agent more consistent.

## Manners

### Chatbot can you hear me?

It's always awkward to walk into the middle of a conversation and not have someone acknowledge your presence. Let's modify the code to have the chatbot introduce itself before you begin talking.

Add a call to the agent to introduce itself before the `# Run the agent` line:

```python hl_lines="1-3"
# Introduce the agent
agent_response = agent.run("Introduce yourself to the user.")
print(f"Kiwi: {agent_response.value.output}")

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
```

### Repeating ourselves

Just like it's not polite to ignore someone when they walk into a conversation, it's not great to repeat yourself over and over.

Notice we're doing exactly that at the moment. 

```python hl_lines="12-13 16-17"
# ...

# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = input("Chat with Kiwi: ")
        if user_input == "exit":
            is_chatting = False
        else:
            # Keep on chatting
            agent_result = agent.run(user_input)
            print (f"Kiwi: {agent_result.output.value}")

# Introduce the agent
agent_response = agent.run("Introduce yourself to the user.")
print(f"Kiwi: {agent_response.value.output}")
 
# Run the agent
chat(agent)
```

This is not a great programming practice because it means any changes we want to make to the output of our chat will have to be done in multiple places. It make maintaining the code way more difficult, and it doens't adhere to the DRY principle (Don't Repeat Yourself).

There are a numbmer of ways we could approach this, including:

- Create a `respond` function
- Subclass the Agent and create a `respond` method.

Both are valid solutions and it's worth looking at what it would feel like to work with each of them to see what feels best.

=== "Function"

    ``` python
    
    # Send a command to the agent
    agent.run("Can I have a haiku?")

    # Run a command and print the result to the user
    respond(agent, "Can I have a haiku?")
    ```

=== "Method"

    ``` python
    
    # Send a command to the agent
    agent.run("Can I have a haiku?")

    # Run a command and print the result to the user
    agent.respond("Can I have a haiku?")
    ```

Taking a look at both options, I think in the end it feels more consistent to use a **method** instead of a function due to the consistent feel of working with the agent: `agent.run()` and `agent.respond()`.

## Adding the Method
### Subclass the Agent

First we'll need to create a **subclass** for the Agent. This will allow us to create additional methods for the agent, and still inherit all the wonderful things Agent gives us.

Add the following lines before `agent = Agent()` in your code:

``` python 
# Create a subclass for the Agent
class MyAgent(Agent):
    

# Create the agent
```

### The `Respond` Method

Now, add the respond method to the MyAgent class and use the same agent_response = agent.run and print commands you used earlier. 

```python
# Create a subclass for the Agent
class MyAgent(Agent):
    def respond (self, user_input):
        agent_response = agent.run(user_input)
        print(f"Kiwi: {agent_response.output.value}") 
```

### Update Agent

Next, replace the line where you create the agent:

```python
agent = Agent()
```

with

```python
agent = MyAgent()
```

to make sure we're now calling the new agent.

### Update calls to agent response
Finally, replace the lines where we were previously getting the result of the `agent.run()` function with `agent.respond()`. At the moment this will be in two locations:

- Inside the `chat` function
- When the agent introduces itself

Replace:
```python
agent_result = agent.run(user_input)
print(f"Kiwi: {agent_result.output.value}")
```

with:

```python
agent.respond(user_input)
```

!!! warning
    Don't replace those lines _inside_ the `respond` method. Only replace them outside the method.

### Review
Since we just made some big changes, here are those alterations brought together, with new lines highlighted.

```python hl_lines="3-7 19 22"
# ...

# Create a subclass for the Agent
class MyAgent(Agent):
    def respond (self, user_input):
        agent_response = agent.run(user_input)
        print(f"Kiwi: {agent_response.output.value}")

# ... truncated for brevity

# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = input("Chat with Kiwi: ")
        if user_input == "exit":
            is_chatting = False
        else:
            agent.respond(user_input)

# Introduce the agent
agent.respond("Introduce yourself to the user.")

# ...
```
## More Manners
### Don't leave without saying Goodbye

Let's give the chatbot a bit _more_ social grace and have it say goodbye when the person stops the chat. Before setting `is_chatting = False`, add the following line:

```python
agent.respond("The user is finished chatting. Say goodbye.")

```
This will tell the agent that the user is leaving the chat, and then print the output to the screen. Here's that section of the code in context:

Here's an example of how that would play out:
```
Chat with kiwi: exit
Kiwi: Good on ya, mate! Take care and have a ripper day!
```

### Clean up the output

Finally, let's enhance the readability of the chat by adding a bit more space around the output of the chat.

This can be done by modifying the `resopnd` method to add two print statements.

``` python hl_lines="4 6"
class MyAgent(Agent):
    def respond (self, user_input):
        agent_response = agent.run(user_input)
        print("")
        print(f"Kiwi: {agent_response.output.value}")
        print("")

```

---

## Code Checkpoint

We made some major updates to the code in this section. Take a look:

``` python linenums="1" title="app.py"
from dotenv import load_dotenv
import logging

# Griptape Items
from griptape.structures import Agent
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

# Create a subclass for the Agent
class MyAgent(Agent):

    def respond (self, user_input):
        agent_response = agent.run(user_input)
        print("")
        print(f"Kiwi: {agent_response.output.value}")
        print("")

# Create the agent
agent = MyAgent(
    rulesets=[
        kiwi_ruleset,
    ],
    logger_level=logging.ERROR
)

# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = input("Chat with Kiwi: ")
        if user_input == "exit":
            agent.respond("The user is finished chatting. Say goodbye.")
            is_chatting = False
        else:
            agent.respond(user_input)

# Introduce the agent
agent.respond("Introduce yourself to the user.")

# Run the agent
chat(agent)
```

### Next Steps

Congratulations on implementing manual chat functionality and taking control of the conversation! In the next section [Adding Another Ruleset](08_adding_another_ruleset_for_output.md), we'll explore the world of output rulesets, unlocking the ability to control the chatbot's responses in different formats such as JSON, YAML, or even haiku.