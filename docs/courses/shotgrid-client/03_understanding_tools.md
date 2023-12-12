# Understanding Tools - DateTime

## Overview
In this module, we will explore the DateTime Tool within Griptape, demonstrating its integration into an `Agent` and breaking down how activities function. We'll then show how you can use the tool in a `Pipeline` by employing `ToolTask` and `ToolkitTask`. 

## What is a Griptape Tool?

Griptape Tools are like additional helpers when dealing with tasks that a Language Learning Model (LLM) can't handle by itself. They expand the capabilities of a system, allowing it to connect with external applications and use specific Python functionalities that aren't part of the LLM's standard toolkit. Whether it's for an automated workflow, a data processing pipeline, or an interactive agent, Griptape Tools provides the extra abilities needed to tackle a wider range of problems and tasks, enhancing the overall functionality and efficiency of the system.

## Setting up the Agent

Let's update our current app to give it access to an Agent so we can interact with the LLM.

### Updating the app
First, let's set up a basic Agent in our application. If you've taken the other courses, this should feel very familiar. Your current `app.py` file looks something like this:

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

Then we'll instantiate the Agent, and call it with the chat utility. Add the following lines at the end of the code.

```python
# ...

# Instantiate the agent
agent = Agent(stream=True)

# Start chatting
Chat(agent).start()
```

Here's the code in its entirety:

```python linenums="1" title="app.py"
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.utils import Chat

load_dotenv()

# Instantiate the agent
agent = Agent(stream=True)

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

!!! tip
    You may see a different prompt than `Q:`. We are currently experimenting with different prompt suggestions to find something more intuitive. If you want to specify the prompt explicitly, you can pass the `prompt_prefix` parameter to the `Chat` utility.

    ```python
    Chat(agent, prompt_prefix="Q: ").start()
    ``` 

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

As you can see, the LLM does not have access to any tools that tell it what day it is. Luckily - Griptape provides one that does! The DateTime Tool!

## Adding Tools

Griptape Tools allow you to add functionality that Griptape Structures (Agents, Pipelines, Workflows) can use. We'll use the DateTime Tool to give the agent the ability to figure out the current time. 

Adding a Tool is a straightforward process. You `import` it, configure it if necessary, and then give it to the Agent (or task). Some Tools are more complicated than others, which is why we're getting started with a nice simple one.

### Include DateTime

* Modify the import statements to include the DateTime Tool:

    ```python
    # ...
    from griptape.tools import DateTime
    # ...
    ```

* Next, provide the Tool to the agent. Agents can work with multiple Tools, so you will be adding it as a list. Modify the code where we instantiate the agent so it looks like:

    ```python
    # ...

    # Instantiate the agent
    agent = Agent(tools=[DateTime(off_prompt=False)], stream=True)
    # ...
    ```

    !!!tip "What is "off_prompt"?"
        **Important Note**: Griptape directs outputs from Tool activities into short-term [TaskMemory](https://docs.griptape.ai/en/latest/griptape-framework/tools/task-memory/){target="_blank"}, keeping them 'off_prompt' and separate from the LLM. This makes it easy to work with big data securely and with low latency. To change this default for more direct interaction with the LLM, set the `off_prompt` parameter to `False`. This allows the LLM to access and respond to Tool outputs directly.

    !!!abstract "DateTime"
        For more information on the DateTime Tool, you can visit the [DateTime Tool Documentation](https://docs.griptape.ai/en/latest/griptape-tools/official-tools/date-time/){target="_blank"}. 

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

Notice the highlighted section above. This is the `subtask`, where the Agent is using [Chain-of-Thought](https://www.promptingguide.ai/techniques/cot){target="_blank"} to figure out what to do. It recognizes the need to use one of its activities - in this case, `get_current_datetime` to get the result.

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

* Hover over `DateTime` and `Ctrl+Click` (`Cmd+Click` on Mac). This will open the DateTime class for Griptape in your editor.

    !!!tip
        In Visual Studio Code, you can navigate to the Definition of a class by using `Ctrl+Click` (`Cmd+Click` on Mac). See the [documentation](https://code.visualstudio.com/docs/editor/editingevolved#_go-to-definition){target="_blank"} to learn more about Visual Studio Code tips for code navigation.

    ![DateTime](assets/img/DateTime.png)

    As you can see in the editor, this is the DateTime class, ready for you to inspect. Jumping around between definitions of classes and functions you use is a very handy way to learn more about how Tools are implemented. 10 stars - would highly recommend.

### Tool Structure

In Griptape, a "Tool" is a `Class`. It is a blueprint that defines the properties and behaviors the Tool will have.

Each Tool has `activities` and `methods`.

```python
# Example of a very simple class with an activity and method

class SayHello():
    @activity(config={
        "description": "Can be used to say Hello!"
        }
    )
    def say_hello():
        return TextArtifact("Hello!")
```

#### Methods
Methods define the actions that the Tool can perform. They are implemented as Python functions in the class. In the case of the `DateTime` Tool, it has a few methods - `get_current_datetime` and `get_relative_datetime`. They define specific actions it can perform.

#### Activities
Activities tell the LLM what the action does and when it might want to use it - kind of like attaching a label or instruction. They are implemented as a decorator above the Python method. For example, the `@activity` decorator in `DateTime` describes what the `get_current_datetime` method does ("Can be used to return current date and time"), and how it should behave.

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

Notice there are **two** `methods`: `get_current_datetime` and `get_relative_datetime`.

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

And each `method` has its associated `activity`.

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

### Methods

#### Basic Structure

Let's use the `get_current_datetime` to understand the structure of a method.

```python hl_lines="1"
def get_current_datetime(self, _: dict) -> BaseArtifact:
    try:
        current_datetime = datetime.now()

        return TextArtifact(str(current_datetime))
    except Exception as e:
        return ErrorArtifact(f"error getting current datetime: {e}")

```

* `get_current_datetime`: This is the *name* of the method we are defining. 
* `(self, _: dict)`: These are the *parameters* the method can take. `self` refers to the object itself (common in class methods), and `_` is a placeholder for a parameter that is a dictionary (`dict`), but this dictionary is not actively used in the method.

    !!! tip
        Neither of these are used in this particular method, but they're there because it's good practice to include them.

* `-> BaseArtifact`: This indicates that the method will *return* an object of type `BaseArtifact`. Griptape provides various artifacts, including Text, List, Blob, etc. You can learn more about them in the [documentation](https://docs.griptape.ai/en/latest/griptape-framework/data/artifacts/){target="_blank"}. 

Since we're not using `self`, or `_` in this method, and Python is a dynamically typed language, we don't need to specify what a function will return. We could probably write this method as:

```python
def get_current_datetime():
```

However, including type hints in method definitions is good practice as it enhances the overall quality and maintainability of our code.

In summary, he's a great way to understand the `def` line:

| Item | What it's used for |
|------|---------------|
| `def`  | Let's define a method! |
| `get_current_datetime` | That's the name of my method! |
| `(self, _: dict)` | Some stuff we're passing *to* the method! |
| `--> BaseArtifact:` | The stuff I want to get back *from* the method! |

#### Try / Except

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
    * The `try` keyword starts a block of code Python will attempt to execute. In this case, it's trying to get the current date and return it as a `TextArtifact` (more on text artifacts in the [documentation](https://docs.griptape.ai/en/latest/griptape-framework/data/artifacts/#textartifact){target="_blank"}). 
    * Think of it as saying "Hey - give this a shot and see if it works?"
* `except` Block:
    * Code doesn't always work as expected, and the `except` block is what happens if `try` encounters an error.
    * `Exception as e` part catches any error and stores it in a variable `e`.
    * Simply put, the `except` block says "If there was a problem in `try`, let's do this instead.
    
Using `try/except` is always a good practice, *especially* with Tools in Griptape. One of the benefits of using this is that `ErrorArtifacts` *get passed back to Griptape*. This means Griptape can evaluate the error, and try again - often fixing mistakes the LLM made in its query!

#### Return

```python hl_lines="5 7"
def get_current_datetime(self, _: dict) -> BaseArtifact:
    try:
        current_datetime = datetime.now()

        return TextArtifact(str(current_datetime))
    except Exception as e:
        return ErrorArtifact(f"error getting current datetime: {e}")

```

Finally, the `return` statements. Whatever is in these will be returned to the subtask in order to continue. As mentioned in the `try/except` section above, `ErrorArtifacts` are important to return because they will allow Griptape to try again.

### Activities

As mentioned previously, `activities` add information and certain features to methods. With Griptape Tools, they can provide simple information (like a description), or even schemas defining what kind of parameters should be passed.

For the `get_current_datetime` method, there are no parameters, so the activity itself is quite simple - it's just a description that tells the LLM when to use it.

```python
@activity(config={"description": "Can be used to return current date and time."})
```

As you can see, any time the LLM determines the task is to return the current date and/or time, it will use this method.

Notice with the `get_relative_datetime` method (the other method in the DateTime class) the activity is different - it says to return a _relative_ date and time and also has a `schema` involved. We'll dive into this detail shortly - for now, let's just understand that any time the LLM thinks that its task is to return something about the *current* date and time, it will use the `get_current_datetime` method.

### More Testing

Let's experiment with different ways of requesting the current time. Try requesting for day, time, date, day of the month, time of year, etc. Notice how the LLM can handle all these different results, with *only one method*.

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

### Parameters

Sometimes you want an activity to take a specific parameter. In the case of the `DateTime` Tool, the `get_relative_datetime` needs to take a parameter to understand what the day _should be relative to_.

Let's try it out. Run the app and ask how far away April 3rd is from today.
Notice a few actions are happening now - the first is `get_current_datetime` to find out what "today" is, then the second is `get_relative_datetime` where it passes an input.

```
Action: {"name": "DateTime", "path": "get_current_datetime", "input": {}}

Action: {"name": "DateTime", "path": "get_relative_datetime", "input": {"values": {"relative_date_string": "April 3, 2024"}}}
```

Before we dive into the parameters, there are two things worth pointing out:

1. We didn't specify the number of steps it should take to get to the answer. We just asked one somewhat ambiguous question and the LLM figured out that it would take two tasks - getting the current date and then getting the relative date.
2. We also didn't specify the `relative_date_string` key/value pair. We didn't need to. The LLM saw what key/value pairs the `get_relative_datetime` method required, and figured out how to pass them. 

This is why working with Griptape Tools starts to get exciting - once you define the parameters, the LLM can figure out the right way to pass the data.

### Schema

Schemas are how we define what parameters are going to be passed to the method. They are like a checklist for data. They're a set of rules that describe what kind of data you expect, and how it should be structured.

For example, if you are creating a schema for a person you might say:

* There must be a name, and it should be text.
* There must be an age, and it should be a number.
* There *might* be an email address. If there is, it should be in the format of an email address. If not, well that's just okay with us.

Then the method can use the schema as a checklist to make sure everything matches. If age is written as text instead of a number (for example), you know there's a mistake.

You can learn more about Python schemas in the [schema documentation](https://pypi.org/project/schema/){target="_blank"}.

For Griptape Tool Activities, schemas are defined as part of the `config` dictionary using the `Schema` class.

Let's look at the schema for `get_relative_datetime`:

```python
config={
    "description": "Can be used to return a relative date and time.",
    "schema": Schema(
        {
            Literal(
                "relative_date_string",
                description='Relative date in English. For example, "now EST", "20 minutes ago", '
                '"in 2 days", "3 months, 1 week and 1 day ago", or "yesterday at 2pm"',
            ): str
        }
    ),
}

```

Right now the Schema has *one* parameter it's looking for: `relative_date_string`. The `description` tells us what kind of data it should be. It says:

    Relative date in English. For example or example, "now EST", 
    "20 minutes ago", "in 2 days", "3 months, 1 week and 1 day ago", 
    or "yesterday at 2 pm"

Finally, the `: str` part means the information should be provided as a string, which basically is just a line of text. This could also be `: int`, `: dict`, `: list`, etc depending on your needs.

#### Optional Parameters

It's possible to also provide *optional* parameters with Schemas. For example, if we were making our own version of DateTime we could include something like:

```python
"schema": Schema(
    {
        Literal(
            "relative_date_string",
            description='Relative date in English.',
        ): str,
        Optional("timezone"): str  # This is an optional parameter
    }
),

```

## Code Review
Throughout this section, we've explored quite a bit about Griptape Tools. We learned how to import and use them, how they're structured, and what `methods` and `activities` are. You understand `schemas` and how they allow you to pass parameters to various `methods`.

Before continuing, let's look at our app in its current state where you can chat with the agent and ask important questions, like how much time you have before my birthday (April 3rd).


```python title="app.py" linenums="1"
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTime

load_dotenv()

# Instantiate the agent
agent = Agent(tools=[DateTime(off_prompt=False)], stream=True)

# Start chatting
Chat(agent).start()

```


---
## Next Steps
You have access to DateTime (not quite as cool as SpaceTime, but still..). In the [next section](04_first_tool.md), you will build your first Griptape Tool.