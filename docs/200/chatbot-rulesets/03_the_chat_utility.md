## Stage 3: Make Agent Interactive Using Chat Utility

Now that we have our agent up and running, it's time to make it truly interactive and engaging. We'll introduce the **Chat utility** from Griptape, which is a quick way to have dynamic conversations with our chatbot. Get ready to dive into the world of witty banter and Python-powered humor!

### Goal:
After completing this section, you'll be able to have lively and interactive conversations with your chatbot using the Chat utility.

### 3.1 Importing the Chat Utility - Let the Fun Begin!

   To get started, we need to import the magical `Chat` utility from Griptape. This utility will be our ticket to engaging conversations with our chatbot. In your code, add the following import statement:
   
   ```python
   from griptape.utils import Chat
   ```

   With the Chat utility at our disposal, we're armed with the power to unleash our chatbot's conversational prowess.

### 3.2 Let the Conversations Flow - The Chat Has Begun!

   It's time to unleash our chatbot's conversational skills and start the interactive chat session. Replace the previous `agent.run()` line with the following code:
   
   ```python
   Chat(agent).start()
   ```

   This simple line of code will open up a world of possibilities, allowing you to converse with your chatbot as if it were your witty Python companion.

Here is the full code: 

```python
from dotenv import load_dotenv

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat #   <-- Added Chat

# Load environment variables
load_dotenv()

# Create the agent
agent = Agent()

# Run the agent
# agent.run("Hi, how are you?")     <-- We no longer need this line

# Begin Chatting
Chat(agent).start()
```

### 3.3 An example of a chat

It's time to play around with your chatbot. Ask it some questions, have a laugh, etc.
Here's a quick example of a not-very-funny joke with the chatbot:

```shell
Q: Hello!
processing...
[07/20/23 06:37:45] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Input: Hello!                                                                                                                                           
[07/20/23 06:37:46] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Output: Hello! How can I assist you today?                                                                                                              
A: Hello! How can I assist you today?
Q: Tell me a joke about python
processing...
[07/20/23 06:37:58] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Input: Tell me a joke about python                                                                                                                      
[07/20/23 06:38:00] INFO     Task 167f55dda2be46a7bc9002a48214dbf4                                                                                                                   
                             Output: Why did the python programmer get bitten by a snake? Because they forgot to use a python exception handler!                                     
A: Why did the python programmer get bitten by a snake? Because they forgot to use a python exception handler!
```

### 3.4 Exit with Style - Knowing When to Say Goodbye

   Conversations must come to an end, even with the most entertaining chatbot. We want to gracefully exit the chat session when we're ready to bid our virtual friend farewell. To exit the chat, simply type `exit` as your input. The Chat utility will catch this magic word and gracefully end the conversation.

   So go ahead, chat away, exchange jokes, discuss Python's quirks, and when it's time to say goodbye, just type `exit` and gracefully conclude your interaction.

```
Q: exit
exiting...
```
---

### Code Checkpoint 
Take a minute to check your code against the [Stage 03 Code Checkpoint](../assets/examples/03_app.py) on GitHub.

### Next Steps

In the next section: [Hide The Logs](04_hide_the_logs.md), we'll hide those pesky but oh-so-helpful logs by using the `logging` library. This will make our chatbot much easier to understand and work with.