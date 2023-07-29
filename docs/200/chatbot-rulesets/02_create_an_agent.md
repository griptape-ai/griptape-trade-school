## Stage 2: Demonstrate Agent and Basic Interaction

In this section, we'll introduce you to Griptape's `Agent` and demonstrate the simplest example of creating and running an agent.

### Goal:
After completing this section, you will have a Griptape Agent running that can complete a simple task based on a text prompt.

### 2.1 Creating and Running the Agent

First, we'll demonstrate the core functionality of Griptape by creating an agent and running it. The agent is the key component that interacts with the OpenAI language model. Add the code to`app.py`:

```python
from griptape.structures import Agent

# Create the agent
agent = Agent()

# Run the agent
agent.run("Hi, how are you?")
```

In this code, we import the `Agent` class from `griptape.structures`. Then, we create an instance of the agent by calling `Agent()`. Finally, we run the agent using `agent.run("Hi, how are you?")`, passing in a prompt `"Hi, how are you?"` as the input.

The `agent.run()` method sends the prompt to the language model, which will generate a response based on the provided input. The agent will handle the communication with the model and retrieve the generated response.

Go ahead and save the code and run it by hitting the little `play` icon in the toolbar above the coding area.

![Alt text](assets/img/02_run_icon.png)

When you look in the terminal, you'll see something that looks like:
```text
[07/19/23 20:10:37] INFO     Task a18579b8591b4a119978411a5714de59                                            
                             Input: Hi, how are you?                                                          
[07/19/23 20:10:40] INFO     Task a18579b8591b4a119978411a5714de59                                            
                             Output: Hi, I'm an AI conversational bot, so I don't have feelings. But I'm here 
                             to help you with any questions or tasks you have. How can I assist you today?    
```

While this might be overwhelming at first and not really what you're interested in ("I just wanted the answer!") - _don't panic_. This is just displaying the _log_ of what is happening under the hood. 

In the log you can see the **DateTime**, the fact that this event is a **Task**, the **Task ID**, the **Input** and the resulting **Output**.

For the moment we'll leave the log showing, but a few modules from now we'll show you how to use logging to turn off the display of the log because honestly.. you don't want to see this every time you use the chatbot. Or maybe you do? We won't judge here.

> Coming Soon: In future courses we will be demonstrating adding [Tools](https://docs.griptape.ai/en/latest/griptape-tools/) (calculators, web scrapers, etc) agents. In those cases the logs will be quite a bit more interesting, displaying subtasks, [chain-of-thought reasoning](https://ai.googleblog.com/2022/05/language-models-perform-reasoning-via.html) and more.


Hey.. how about an awesome haiku about logs!

> Log files tell all, \
Python's mischief takes its toll, \
Errors bring the LOLs.

---

### Code Checkpoint 
We've only gotten started, but to make sure everything is flowing smoothly, take a minute to check your code against the [Stage 02 Code Checkpoint](../assets/examples/02_app.py) on GitHub.

### Next Steps

That's it for this section! In the next part [Step 3 - The Chat Utility](03_the_chat_utility.md), we'll explore further functionality and make our agent interactive.