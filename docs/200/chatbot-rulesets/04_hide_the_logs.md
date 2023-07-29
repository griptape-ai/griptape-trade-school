## Stage 4. Demonstrate Logging to Improve Output

In the previous section, we had a blast engaging with our chatbot, but there was one tiny detail that interrupted the flow of our conversations - those verbose logs cluttering our output. Fear not!  In this section, we'll show you how to turn off the logs and let your chatbot's brilliance shine without unnecessary distractions.

### Goal:
After completing this section, you'll be able to enjoy clean and clutter-free conversations with your chatbot by disabling the logs.


### 4.1 Silencing the Logs - Embrace the Zen of Silence

   We'll begin by importing the logging library, which will give us the power to control the verbosity of our chatbot's output. Add the following import statement to your code:
   
   ```python
   import logging
   ```

   Now we're ready to silence those logs and enjoy the tranquility of clean output.

### 4.2 Revamping the Agent - Silent but Brilliant

   It's time to modify our agent to quiet those logs and allow our chatbot's brilliance to shine through. Adjust the code where the agent is created, like so:
   
   ```python
   # Create the agent
   agent = Agent(logger_level=logging.ERROR)
   ```

   By specifying `logger_level=logging.ERROR`, we indicate that we only want to receive logs of the highest priority, suppressing the informational logs and leaving us with a cleaner output.

Here is the [full code](../assets/examples/04_app.py):

```python
from dotenv import load_dotenv
import logging                      # <-- Here's the new line

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat

# Load environment variables
load_dotenv()

# Create the agent
agent = Agent(
    logger_level=logging.ERROR      # <-- Add the logger_level parameter
    
)

# Run the agent
Chat(agent).start()
```

### 4.3 Give it a try
Go ahead and execute the script and have a chat.

```shell
Q: Give me a haiku about python skateboarders
processing...
A: Python skateboarders
Glide on wheels, swift and free
Thrilling tricks they show
Q: 
```

   Ahh, isn't it refreshing? Now our conversations will flow seamlessly, without any distracting logs cluttering our chatbot's responses.

---

### Code Checkpoint
We've made valuable progress in this stage. Before proceeding, let's verify your code with the [Stage 04 Code Checkpoint](../assets/examples/04_app.py) on GitHub.


### Next Steps

In the next section: [Personality With Rulesets](05_personality_with_rulesets.md), we'll unlock the true potential of your chatbot by giving it a vibrant personality with the help of rulesets. Prepare to witness your chatbot's transformation as it takes on unique traits, behaviors, and even multiple personas. 
