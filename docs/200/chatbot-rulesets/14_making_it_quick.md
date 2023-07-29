# Stage 14: Making it Quick

This is it, you're ready to ride! Let's add a final touch to our chat application to make it a little more user-friendly and visually appealing. We'll be utilizing the `Console` class from the `rich` library and its `spinner` functionality. This will provide a visual cue to the user that the agent is processing their input.

**Note:** There are lots of spinners available. You can check them out by running `python -m rich.spinner` in your terminal.

![Alt text](assets/img/14_spinners.png)

## Step 14.1: Importing the Console

```python
from rich.console import Console
```

Importing the Console class from the `rich` library is simple and straightforward, and should be familliar to you by this point in the lesson.

## Step 14.2: Modifying the Respond Method

We will add a spinner to our `respond` method in the `MyAgent` subclass. This will show an animated spinner in the console while our agent is processing the user's input. This makes the app feel more responsive.

Update the `respond` method as follows:

```python
class MyAgent(Agent):
    def respond(self, user_input):
        console = Console()
        with console.status(spinner="simpleDotsScrolling", status=""):
            agent_response = self.run(user_input)
        
```

In the code above, `console.status(spinner="simpleDotsScrolling", status="")` starts an animated spinner in the console that will run until the block of code it is wrapping (the agent's processing of user input) completes. Note, we've left `status` blank - because we don't really need to send any text. However, feel free to add some text here if you desire.

Now when you run the chat, you'll notice the animated spinner right after you ask the chatbot a question!

![Alt Text](assets/img/14_spinner_response.gif)

---

### All Done!

Check your work with the Stage 14 Code Checkpoint: [Stage 14 Checkpoint](../assets/examples/14_app.py)

That's it! We've come a long way in this tutorial and now you have a multi-persona chat application written with Griptape. Hopefully you've been able to see how using Rulesets can be used for both creative and structural control of your applications.

Congratulations on making it through! We're thrilled you decided to join us for this course and we hope you've enjoyed it as much as we have. We'd love to hear your feedback, so please don't hesitate to let us know what you thought.

More importantly, we wish you all the best as you continue your journey with Griptape and Python. Remember to have fun, experiment, and keep on learning. Happy coding! 🚀