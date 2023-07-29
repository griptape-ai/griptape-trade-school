## Stage 10: Markdown Madness for Supercharged Code Display

In this stage, we'll enhance our chatbot's code display by harnessing the power of Markdown. With Markdown, we can beautifully format and highlight code snippets to make them more readable and visually appealing. 

### 10.1 See why it's broken
First let's see why our current output doesn't work. Ask the chatbot to do something useful - like create a bash script that will create an alias to launch VS Code.

```
Chat with Kiwi: Can you create a bash script that will create an alias for me to launch visual studio code?

╭──────────────────────────────────────────────────────────────────────────────╮
│ Kiwi: Kia ora! G'day mate! I can definitely help you with that. Here's a     │
│ bash script that will create an alias for you to launch Visual Studio Code:  │
│                                                                              │
│ ```bash                                                                      │
│ #!/bin/bash                                                                  │
│                                                                              │
│ echo "alias code='open -a Visual\ Studio\ Code'" >> ~/.bash_profile          │
│ source ~/.bash_profile                                                       │
│                                                                              │
│ echo "Alias created! You can now launch Visual Studio Code by typing 'code'  │
│ in your terminal. Let me know if you need any further assistance!"           │
│ ```                                                                          │
│                                                                              │
│ Just copy and paste this script into a new file, save it with a `.sh`        │
│ extension (e.g., `create_alias.sh`), and then run it in your terminal using  │
│ `bash create_alias.sh`. Let me know if you have any questions or need        │
│ further help!                                                                │
╰──────────────────────────────────────────────────────────────────────────────╯

```

As you can see, the script is fine, but it doesn't _look_ like a script. It looks like something you'd enter in a Markdown file that you'd expect to eventually be rendered as a script. We're going to make this look much nicer.

### 10.2 Importing the Required Libraries

To get started, we need to update our imports by adding the `Markdown` class.

```python
from rich.markdown import Markdown
```

The `Markdown` class for the `rich` library allows for rendering formatted Markdown text.

### 10.3 Enhancing the Chatbot Output

Next, we'll modify the `respond` method to use the `Markdown` class. There are a few things we'll need to do. First, we'll take the output of the chatbot's response and convert it into a formeted Markdown text using the following line:
```python
        # ...
        response = data["response"]
        continue_chatting = data["continue_chatting"]

        formatted_response = Markdown(response)
        # ...
```

Then, we'll replace our `rprint` statement in the panel to use the `formatted_reponse` instead of the string we were sending earlier.

```python
        # ...
        rprint(Panel.fit(formatted_response, width=80))
        # ...
```

> Note: Make sure you don't do something like `rprint(Panel.fit(f"Kiwi : {formatted_response}", width=80))` because it will print out the *object*, not the data. 

Here's the new `respond` method in it's entirety:

```python
# Create a subclass for the Agent
class MyAgent(Agent):
        
    def respond (self, user_input):
        agent_response = self.run(user_input)
        data = json.loads(agent_response.output.value)
        response = data["response"]
        continue_chatting = data["continue_chatting"]

        formatted_response = Markdown(response)

        print("")
        rprint(Panel.fit(formatted_response, width=80))
        print("")
        
        return continue_chatting
```

Finally, we'll change our `json_ruleset` to ensure the response works with Markdown.

Modify the **second** rule in the `json_ruleset` so it specifies the response should be able to be safely converted into markdown format.

```python
        # ... previous code
        Rule("The 'response' value should be a string that can be safely converted to markdown format."),
        # ...
```
And the result. I've added a screenshot so you can see how much better it looks.

![Alt text](assets/img/10_markdown_bash.png)

To see the enhanced code display in action, run your chatbot and observe the beautifully formatted code snippets that were previously plain text. Try creating tables, csv files, python, tasks lists, etc. Enjoy the new level of elegance and readability brought by Markdown magic!

---
### Code Checkpoint

Before moving forward, make sure your code works as expected by checking the [Stage 10 Code Checkpoint](../assets/examples/10_app.py) on GitHub.

### Next Steps

In the next section, [Stage 11: Improving the Prompt](11_gleaming_the_chat.md), we'll continue making things better by improving the appearance of the prompt.

