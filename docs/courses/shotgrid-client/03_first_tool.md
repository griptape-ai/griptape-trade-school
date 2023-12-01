# Your First Tool - DateTime

## Overview
In this module, we will explore the DateTime tool within Griptape, demonstrating its integration into an `Agent` and breaking down how activities function. We'll then show how you can use the tool in a `Pipeline` by employing `ToolTask` and `ToolkitTask`. But first, we must update our current app to give it access to an Agent.

## Setting up the Agent

### Updating the app
First, let's set up a basic Agent in our application. If you've taken the other courses, this should feel very familiar. Your current `app.py` file looks something like:

```python linenums="1" title="app.py"
from dotenv import load_dotenv

load_dotenv()
```

Let's add the lines to import the Agent and the Chat utility.

```python
# ... shortened for brevity
from griptape.structures import Agent
from griptape.utils import Chat

# ...
```

Then we'll instantiate the Agent, and call it with the chat utility. Add the following lines as the end of the code.

```python
# ...

# Instantiate the agent
agent = Agent()

# Start chatting
Chat(agent).start()
```

Here's the code in it's entirety:

```python linenums="1" title="app.py"
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.utils import Chat

load_dotenv()

# Instantiate the agent
agent = Agent()

# Start chatting
Chat(agent).start()

```

### Test it out

Now that you have an agent, let's give it a try by running the application. Remember, you can execute the app by using the `Run Python` button in the top right of your Visual Studio Code editor.

When the application launches, you should see a prompt that looks like the following:

```text
Q:
```

This is the prompt for the Chat, indicating you can now chat with the agent.

Ask the agent: `"What day is it?"`

You will receive a response similar to this:

```text
Q: What day is it?
processing...
[12/02/23 05:23:35] INFO     PromptTask 8774d4cf5d2e4630bce4937864a6dd81                                      
                             Input: What day is it?                                                           
[12/02/23 05:23:39] INFO     PromptTask 8774d4cf5d2e4630bce4937864a6dd81                                      
                             Output: As an AI, I don't have real-time capabilities to provide the current     
                             date. Please check your device for the current date.                             
A: As an AI, I don't have real-time capabilities to provide the current date. Please check your device for the current date.

```

As you can see, the LLM does not have access to any tools that tell it what day it is. Luckily - Griptape provides a tool that does! The DateTime tool!

## Adding Tools

Griptape Tools allow you to add functionality that Griptape structures (Agents, Pipelines, Workflows) can use. We'll use the DateTime tool to give the agent the ability to figure out the current time. For more information on the DateTime tool, you can visit the [DateTime Tool Documentation](https://docs.griptape.ai/en/latest/griptape-tools/official-tools/date-time/). 

Adding a tool is a relatively straightforward process. You simply `import` it, configure it if necessary, and then give it to the Agent (or task). Some tools are more complicated than others, which is why we're getting started with a nice simple one.

### Include DateTime

* Modify the import statements to include the DateTime tool:

    ```python
    # ...
    from griptape.tools import DateTime
    # ...
    ```

* Next, provide the tool to the agent. Agents can work with multiple tools, so you will be adding it as a list. Modify the code where we instantiate the agent so it looks like:

    ```python
    # ...

    # Instantiate the agent
    agent = Agent(tools=[DateTime(off_prompt=False)])
    # ...
    ```

    !!!tip "What is "off_prompt"?"
        **Important Note**: Griptape directs outputs from tool activities into short-term [TaskMemory](https://docs.griptape.ai/en/latest/griptape-framework/tools/task-memory/), keeping them 'off_prompt' and secure from the LLM. To change this default for more direct interaction with the LLM, set the `off_prompt` parameter to `False`. This allows the LLM to access and respond to tool outputs directly.

### Try it again

* Run the application, and at the `Q:` prompt again ask what day it is.

    You'll see a very different response this time, something similar to the following:

    ```text hl_lines="5-16"
    Q: What day is it?
    processing...
    [12/02/23 06:07:08] INFO     ToolkitTask 0024a33acd8946deac94355ca92ccfde                                     
                                Input: What day is it?                                                           
    [12/02/23 06:07:12] INFO     Subtask c9606eb9fbb243998e821fb0ebeb961a                                         
                                Thought: To answer this question, I need to get the current date and time. I can 
                                use the "get_current_datetime" action for this.                                  
                                                                                                                
                                Action:                                                                          
                                {                                                                                
                                "name": "DateTime",                                                            
                                "path": "get_current_datetime",                                                
                                "input": {}                                                                    
                                }                                                                                
                        INFO     Subtask c9606eb9fbb243998e821fb0ebeb961a                                         
                                Response: 2023-12-02 06:07:12.902983                                             
    [12/02/23 06:07:15] INFO     ToolkitTask 0024a33acd8946deac94355ca92ccfde                                     
                                Output: Today is December 2, 2023.                                               
    A: Today is December 2, 2023.
    ```

Notice the highlighted section above. This is the `subtask`, where the Agent is using Chain-of-thought to figure out what to do. It recognizes the need to use one of activities - in this case `get_current_datetime` to get the result.

Take a look at the `Action`:

```json
Action:
{           
    "name": "DateTime", 
    "path": "get_current_datetime",
    "input": {}   
}                   
```

It's using the `DateTime` tool, with a method `get_current_datetime`, and no `inputs` (parameters).

## Tool Classes

### The DateTime Class
Let's take a look at the `DateTime` class itself and see if we can determine what's happening.

* Find the line in your code where you `import` `DateTime`:

    ```python
    from griptape.tools import DateTime
    ```

* Hover over `DateTime` and choose `Ctrl+Click` (`Cmd+Click` on Mac). This will open the DateTime class for Griptape in your editor.

    !!!tip
        In Visual Studio Code, you can navigate to the Definition of a class by using `Ctrl+Click` (`Cmd+Click` on Mac). Learn more in the [documentation](https://code.visualstudio.com/docs/editor/editingevolved#_go-to-definition).

    ![DateTime](assets/img/DateTime.png)

    As you can see in the editor, this is the DateTime class, ready for you to inspect. Jumping around between definitions of classes and functions you use is a very handy way to learn more about how tools are implement. 10 stars - would highly recommend.

### Tool Structure

In Griptape, a "tool" is a `Class`. It is a blueprint that defines the properties and behaviors the tool will have.

Each tool has `activities` and `methods`.

#### Methods
Methods are functions that are associated with a class. In the case of the `DateTime` tool, it has a few methods - like `get_current_datetime`. They define specific actions the tool can perform.

#### Activities
Activities are Python decorators that add information and certain features to methods - kind of like attaching a label or instruction. For example the `@activity` decorator in `DateTime` describes what the method does, and how it should behave.

### DateTime Structure

Let's look specifically at the DateTime structure. I'll comment out details so we can keep it simple.

``` python
# ...

class DateTime(BaseTool):
    @activity(config={"description": "Can be used to return current date and time."})
    def get_current_datetime(self, _: dict) -> BaseArtifact:
        try:
            # ...
        except Exception as e:
            # ...

    @activity(
        config={
            "description": "Can be used to return a relative date and time.",
            "schema": Schema(
                {
                    Literal(
                        "relative_date_string",
                        description='Relative date in English...
                    ): str
                }
            ),
        }
    )
    def get_relative_datetime(self, params: dict) -> BaseArtifact:
        # ...
        try:
            # ...
        except Exception as e:
            # ...

```

If you look carefully, you can see there are **two** `methods`: `get_current_datetime` and `get_relative_datetime`.

```python hl_lines="5 14"
# ...

class DateTime(BaseTool):
    @activity(config={"description": "Can be used to return current date and time."})
    def get_current_datetime(self, _: dict) -> BaseArtifact:
            # ...

    @activity(
        config={
            "description": "Can be used to return a relative date and time.",
            # ...
        }
    )
    def get_relative_datetime(self, params: dict) -> BaseArtifact:
        # ...

```

And each `method` has it's associated `activity`.

```python hl_lines="4 8-13"
# ...

class DateTime(BaseTool):
    @activity(config={"description": "Can be used to return current date and time."})
    def get_current_datetime(self, _: dict) -> BaseArtifact:
            # ...

    @activity(
        config={
            "description": "Can be used to return a relative date and time.",
            # ...
        }
    )
    def get_relative_datetime(self, params: dict) -> BaseArtifact:
        # ...

```

The LLM uses the description of the activities to figure out what it can do, and what the appropriate method is to call.

In our earlier example, the Action taken was `get_current_datetime`:

```json
Action:
{           
    "name": "DateTime", 
    "path": "get_current_datetime",
    "input": {}   
}
```

As you see in the DateTime Class, that method exists! 

## Methods

### Basic Structure

Diving into the basic structure of a method, let's use the `get_current_datetime` as an example.

```python hl_lines="1"
    def get_current_datetime(self, _: dict) -> BaseArtifact:
        try:
            current_datetime = datetime.now()

            return TextArtifact(str(current_datetime))
        except Exception as e:
            return ErrorArtifact(f"error getting current datetime: {e}")

```

* `get_current_datetime`: This is the name of the method we are defining. 
* `(self, _: dict)`: These are the parameters the method takes. `self` refers to the object itself (common in class methods), and `_` is a placeholder for a parameter that is a dictionary (`dict`), but this dictionary is not actively used in the method.
* `-> BaseArtifact`: This indicates that the method will return an object of type `BaseArtifact`. Griptape provides various artifacts, including Text, List, Blob, etc. You can learn more about them in the [documentation](https://docs.griptape.ai/en/latest/griptape-framework/data/artifacts/). 

Since we're not using `self`, or `_` in this method, and Python is a dynamically typed language so we don't need to specify what a function will return, this could probably be re-written more simply as:

```python
def get_current_datetime():
```

However, including type hints in method definitions is good practice as it enhances the overall quality and maintainability of our code.

### Try / Except

Moving further into the method, you'll see the `try` and `except` block. 

```python hl_lines="2 6"
    def get_current_datetime(self, _: dict) -> BaseArtifact:
        try:
            current_datetime = datetime.now()

            return TextArtifact(str(current_datetime))
        except Exception as e:
            return ErrorArtifact(f"error getting current datetime: {e}")

```

* `try` Block:
    * The `try` keyword starts a block of code Python will attempt to execute. In this case, it's trying to get the current date and return it as a `TextArtifact` (more on text artifacts in the [documentation](https://docs.griptape.ai/en/latest/griptape-framework/data/artifacts/#textartifact)). 
    * Think of it as saying "Hey - give this a shot and see if it works?"
* `except` Block:
    * Code doesn't always work as expected, and the `except` block is what happens if `try` encounters an error.
    * `Exception as e` part catches any error and stores it in a variable `e`.
    * Simply put, the `excpet` block says "If there was a problem in `try`, let's do this instead.
    
Using `try/except` is always good practice, *especially* with tools in Griptape. One of the benefits of using this is that `ErrorArtifacts` *get passed back to Griptape*. This means Griptape can evaluate the error, and try again - often fixing it's own mistake!

### Return

```python hl_lines="5 7"
    def get_current_datetime(self, _: dict) -> BaseArtifact:
        try:
            current_datetime = datetime.now()

            return TextArtifact(str(current_datetime))
        except Exception as e:
            return ErrorArtifact(f"error getting current datetime: {e}")

```

Finally, the `return` statements. Whatever is in these will be returned to the subtask in order to continue. As mentioned in the `try/except` section above, `ErrorArtifacts` are really important to return because it allows Griptape to try again.

### More Testing

Let's experiment with different ways of requesting the current time. Try requesting for day, time, date, day of the month, time of year, etc. Notice how the LLM is able to handle all these different results, with *only one method*.

```
Q: What's the date?
A: Today's date is December 2, 2023.

Q: What day of the week is it?
A: Today is Saturday.

Q: What's the time in New Zealand?
A: The current time in New Zealand is 07:58 on December 2, 2023.

Q: What's the time if Yoda said it?
A: The current time in Yoda's speech would be, "58 past 7 it is."

Q: What's the current time as Beaker from the Muppets?
A: As Beaker from the Muppets, the current time would be expressed as, "Meep meep, meep meep meep!"
```

---
## Next Steps
Now that you have your environment set up and access to ShotGrid, you're ready to get started with Griptape Tools. In the [next section](03_first_tool.md), we'll get started by using one of Griptape's built in tools (DateTime) and understand how it works.