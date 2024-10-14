# Showing the Logs

<iframe src="https://www.youtube.com/embed/GTG1YfKudRA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

In the previous section, we had a blast engaging with our chatbot, but some of the chatbot's output was hidden from us. Fear not! In this section, we'll show you how to turn on the logs and let your chatbot's brilliance shine.


### Goal
After completing this section, you'll be able to enjoy clean and clutter-free conversations with your chatbot by disabling the logs.

### Import

First, we need to import Python's `logging` module. This will give us access to some handy constants.

```python hl_lines="1"
import logging
```

### Add to Agent

It's time to modify our Chat utility to show those logs and allow our chatbot's brilliance to shine through. Adjust the code where the Chat is started, like so:

```python hl_lines="2"
# Run the agent
Chat(agent,logger_level=logging.INFO).start()
```

Here is the code with the new lines highlighted:

``` py linenums="1" hl_lines="2 15" 
from dotenv import load_dotenv
import logging                     

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat

# Load environment variables
load_dotenv()

# Create the agent
agent = Agent()

# Run the agent
Chat(agent,logger_level=logging.INFO).start()
```

### Give it a try
Go ahead and execute the script and have a chat.

```
User: Hello!
processing...
[07/20/23 06:37:45] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Input: Hello!                                                                                                                                           
[07/20/23 06:37:46] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Output: Hello! How can I assist you today?                                                                                                              
Assistant: Hello! How can I assist you today?
User: Tell me a joke about python
processing...
[07/20/23 06:37:58] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Input: Tell me a joke about python                                                                                                                      
[07/20/23 06:38:00] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Output: Why did the python programmer get bitten by a snake? Because they forgot to use a python exception handler!                                     
Assistant: Why did the python programmer get bitten by a snake? Because they forgot to use a python exception handler!
```

!!! Success
    While this is great for understanding what's happening behind the scenes, let's remove it so that our conversations will flow seamlessly, without any distracting logs cluttering our chatbot's responses.

---

## Code Review

We've made valuable progress in this stage. Before proceeding, let's verify your code.

```python linenums="1" title="app.py"
--8<-- "docs/courses/chatbot-rulesets/assets/code_reviews/04/app.py"
```

## Next Steps

In the next section: [Personality With Rulesets](05_personality_with_rulesets.md), we'll unlock the true potential of your chatbot by giving it a vibrant personality with the help of **Rulesets**. Prepare to witness your chatbot's transformation as it takes on unique traits, behaviors, and even multiple personas. 
