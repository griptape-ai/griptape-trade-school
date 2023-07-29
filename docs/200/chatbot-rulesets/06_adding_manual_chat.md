## Stage 6. Implementing Manual Chat - Taking Control

While the chatbot is working, it's not very user-friendly yet. The `Q:` and `A:` prompts don't make for the most engaging for a user experience.

In this step, we'll implement a manual chat experience, giving us more control over the conversation with our chatbot. We'll remove the Chat utility and create our own custom functions to facilitate interactive and dynamic conversations.

Let's get started!

### 6.1 Removing the Chat Utility

   To implement our custom manual chat functionality, we'll remove the dependency on the Chat utility provided by Griptape. We'll no longer need the line `from griptape.utils import Chat` in our code.

   Update the code by commenting out or removing the following line:

   ```python
   # from griptape.utils import Chat
   ```

   Don't forget to remove or comment out the line where we use the Chat utility with the agent at the bottom of the script:
   ```python
   # Run the agent
   # Chat(agent).start()
   ```
   With the Chat utility out of the picture, we're ready to take charge and create our own chat function.

### 6.2 Say it over and over and over and..
Now that the Chat function has been removed, we'll need to replace it with our own code. Let's start by with a simple loop that takes the user input until they type `exit`.


```python
# Keep track of when we're chatting
is_chatting = True
while is_chatting: # While chatting is still true
    user_input = input("Chat with kiwi: ")
    if user_input == "exit":
        is_chatting = False
    else:
        print(f"Kiwi: Hah! you said: {user_input}!")

```

If you just run this code on it's own, you'll see that it allows the user to keep entering information over and over again until they type exit.

It's not very amazing, and certainly doesn't interact with the agent yet, so let's modify the code to handle that.

After the `else:` statement, change the code to call `agent.run()`:

```python
while is_chatting:
    # ... truncated for brevity ... #
else:
    agent_result = agent.run(user_input)
    print (f"Kiwi: {agent_result.output.value}")
```

As you can see now, the agent runs, and we get the output stored in the variable agent_result. We can then print that output by using the `output.value` attribute.


### 6.3 Creating a `respond` method

At the moment, our mode of chatting with the agent is to call `agent.run()`, get the response, then print `agent_response.output.value`. While these two lines of code aren't difficult to create, it will be more consistent if we had two options for working with the agent:
 - `agent.run()` to run a task with the agent
 - `agent.respond()` to run the agent and show the response to the user.

 We can do that by creating a **subclass** of the `Agent` class that has a `respond` method where we get the output from `agent.run()` and `print` it..

 First, let's create the subclass by adding it before `agent = Agent()`, and also fix the output of the response so there is some spacing around it.:

 ```python

# Create a subclass for the Agent
class MyAgent(Agent):
    def respond (self, user_input):
        agent_response = agent.run(user_input)
        print("")
        print(f"Kiwi: {agent_response.output.value}") 
        print("")
 ```

Next, replace the line:
```python
agent = Agent()
```
with
```python
agent = MyAgent()
```
to make sure we're now calling the new agent.

Finally, replace the lines where we call the agent in the `while is_chatting` loop from:

```python
else:
    # Keep on chatting
    agent_result = agent.run(user_input)
    print(f"Kiwi: {agent_result.output.value}")
```
to:
```python
else:
    # Keep on chatting
    agent.respond(user_input)
```

### 6.7 Keep on tidying - Creating a `chat` function

   Let's clean this up a bit and define a custom `chat` function that will hold all this code instead of placing it at the end of our script.

   Here's the code for the `chat` function and the way we can call it:

   ```python
   # Chat function
   def chat(agent):
       is_chatting = True
       while is_chatting:
            user_result = input("Chat with Kiwi: ")
            if user_result == "exit":
                is_chatting = False
            else:           
                # Keep on chatting
                agent.respond(user_result)

   # Run the agent
   chat(agent)
   ```

   The `chat` function takes the `agent` as an argument.

   You shouldn't notice any difference to how you ran this before, it's just a bit cleaner.

Engage in stimulating conversations, explore various topics, and enjoy the interactive experience as you communicate with your chatbot.

---

### Code Checkpoint

We made a lot of important changes in this stage. Before we move forward, let's ensure your code is aligned with the [Stage 06 Code Checkpoint](../assets/examples/06_app.py) on GitHub.

### Next Steps

Congratulations on implementing manual chat functionality and taking control of the conversation! In the next section [Adding Another Ruleset](07_manners_maketh_the_bot.md), we'll give the bot some manners.