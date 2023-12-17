# Your First Tool

## Overview
We'll use a Griptape Tool Template that's available on GitHub to create our first Tool, and then modify it slightly to demonstrate multiple activities.

## Getting the template

The Tool template provided creates a `reverse_string` Tool. It will take any text and reverse it. It's a nice simple example of how to use a Tool with your LLM.

The template contains examples of how to use the Tool, testing, and more. The idea is that you can take this template and publish your own Tool on GitHub to share with the world. 

For the purposes of *this course*, we'll keep things simple and just focus on the Tool itself, using the code to create our own as part of our current project.

1. Navigate to the [Gritptape tool-template repository](https://github.com/griptape-ai/tool-template){target="_blank"} on GitHub.
2. Find the **Code** button and click on it.
3. Choose **Download zip** to download a zip file of the project.

    !!!info
        If you have a GitHub account and have experience with GitHub repos, you are more than welcome to choose **Use this template** and work the way you are comfortable. 

4. Extract the contents of the .zip file by double-clicking on it.

    ![Extracted contents of the zip file](assets/img/tool-template-main.png)

    The **reverse_string_tool** folder is the one we are interested in, it contains the required files for the Tool. You can read more about them in the [Griptape Custom Tool documentation](https://docs.griptape.ai/en/latest/griptape-tools/custom-tools/){target="_blank"}.

5. Copy the **reverse_string_tool** folder into the folder where your `app.py` file sits. 

    !!!tip
        You can just drag the folder from your Finder or Windows Explorer and drop it directly into Visual Studio Code to copy it.

    You should now see the folder in Visual Studio Code next to `app.py` and `.env`.

    ![Reverse String Tool in Visual Studio Code](assets/img/reverse-string-tool.png)

## Use Reverse String

Here's the code for the Reverse String Tool (as of December 2023). I've highlighted some important lines from the code.

```python linenums="1" hl_lines="10 11 13 14 17"
from __future__ import annotations
from griptape.artifacts import TextArtifact, ErrorArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import define


@define
class ReverseStringTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to reverse a string",
            "schema": Schema({Literal("input", description="The string to be reversed"): str}),
        }
    )
    def reverse_string(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        try:
            return TextArtifact(input_value[::-1])

        except Exception as e:
            return ErrorArtifact(str(e))

```

The highlighted lines illustrate that the Tool (Class) is called `ReverseString`. It has one module, `reverse_string`. It has an `activity` that says it "Can be used to reverse a string", and it appears to take one parameter named `input` which is described as "The string to be reversed".

### Add it to test_tool.py

Just like any other Griptape Tool, you need to `import` it. However, because this Tool isn't part of the default Griptape repository, the import line will look slightly different. Add the following line to `test_tool.py`:

```python 
# ...
from reverse_string_tool import ReverseStringTool
# ...
```

!!! tip
    How do you know to choose `reverse_string_tool` and `ReverseStringTool` in the `import` statement?

    The `__init__.py` file is a hint. You can think of that file as a sort of index or table of contents for the items in the folder. Its presence tells Python that the directory is a special kind of directory - a package from which you can import `modules`.

    Because I saw that `__init__.py` file, I knew I could import modules *from* that folder. 

### Give it to the agent

Remember, the agent takes a list of Tools. We can add this Tool to the agent by simply adding it to the list.

Find the line where you instantiate the agent and add the `ReverseStringTool`:

```python 

# ...

# Instantiate the agent
agent = Agent(tools=[DateTime(off_prompt=False), ReverseStringTool(off_prompt=False)])

# ...
```

Notice the agent now has access to *two* Tools, `DateTime` and `ReverseStringTool`. 

### Test it out

Now test the Tool by running the application and asking it to say something in reverse.

```text hl_lines="5-17"
Q: can you say this in revese "I'm a lumberjack and I'm okay"
processing...
[12/03/23 05:56:54] INFO    ToolkitTask 656bcf9d58654d53a60ae24a7dad6af2
                    Input: can you say this in revese "I'm a lumberjack and I'm okay"
[12/03/23 05:57:01] INFO    Subtask 6eeda1fd106a480ebaa8fe112fffdfe6
                    Thought: I need to use the ReverseStringTool action to reverse the given string.
                    Action:
                        {
                            "name": "ReverseStringTool",
                            "path": "reverse_string",
                            "input":
                            {
                                "values":
                                {
                                    "input": "I'm a lumberjack and I'm okay"
                                }
                            }
                        }                                                                                                                
                    INFO    Subtask 6eeda1fd106a480ebaa8fe112fffdfe6
                    Response: yako m'I dna kcajrebmul a m'I
                                             
[12/03/23 05:57:03] INFO    ToolkitTask 656bcf9d58654d53a60ae24a7dad6af2
                    Output: The reversed string is "yako m'I dna kcajrebmul a m'I". 
                        A: The reversed string is "yako m'I dna kcajrebmul a m'I".

```

As you can see in the highlighted section above, the `Subtask` shows that the agent has decided to use the ReverseStringTool action.

### Combine requests

You can absolutely use multiple Tools at the same time. Try a few examples where you might use both the `DateTime` Tool and the `ReverseStringTool`.

```text
Q: Can you reverse the month?
A: The reversed month is "rebmeceD".

Q: Tell me how many days there are until December 25th, and then reverse the entire response
A: The reversed response is "syad 32 era ereht".
```

## Adding a method

Let's add another method to the `ReverseStringTool`. This will take a sentence and reverse the words instead of the letters.

It will:

* Split the sentence into words
* Reverse the list of words
* Join the reverse words back into a sentence

### Open tool.py

1. In Visual Studio Code, open the `reverse_string_tool` folder and select `tool.py`.

### Add `reverse_sentence`

1. Duplicate the code from the first `@activity` line through the end of the `def reverse_string` method.

1. Rename the *second* method to `reverse_sentence`.

1. Change the *description* of the second activity to `Can be used to reverse a sentence` and the *schema description* to `The sentence to be reversed`.

Here's the resulting code, with much of it commented out for brevity. I've highlighted the specific sections where we replaced `string` with `sentence`. This new method won't reverse sentences yet, we will add that later.

```python hl_lines="18-20 23"
# ...

@define
class ReverseStringTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to reverse a string",
            "schema": Schema({Literal("input", description="The string to be reversed"): str}),
        }
    )
    def reverse_string(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        # ...
                
    @activity(
        config={
            "description": "Can be used to reverse a sentence",
            "schema": Schema(
                {Literal("input", description="The sentence to be reversed"): str}),
        }
    )
    def reverse_sentence(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        # ...

```

### Update the logic

Within the `reverse_sentence` method, find the section of code after `try:` and before the `except`, and replace it with the following code:

```python hl_lines="7-16"
# ...

    def reverse_sentence(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        try:
            # Splitting the sentence into words
            words = input_value.split()

            # Reversing the list of words
            reversed_words = words[::-1]

            # Joining the reversed words back into a sentence
            reversed_sentence = " ".join(reversed_words)

            return TextArtifact(reversed_sentence)

        except Exception as e:
            return ErrorArtifact(str(e))

```

### Try it out

Now that you've added this new method, let's give it a try!

```text
Q: Can you reverse the words in this sentence? "I must eat, therefore, I am hungry".
A: The reversed sentence is "hungry am I therefore, eat, must I".
```

Well done! Now go grab a snack and we'll continue.

## Code Review

You have added a Griptape Tool *and* modified it to add a new activity! Well done! Let's take a look at all the code to review it before moving on.


### `test_tool.py`
```python title="test_tool.py" linenums="1" hl_lines="6 11"
from dotenv import load_dotenv
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTime

from reverse_string_tool import ReverseStringTool

load_dotenv()

# Instantiate the agent
agent = Agent(tools=[DateTime(off_prompt=False), ReverseStringTool(off_prompt=False)], stream=True)

# Start chatting
Chat(agent).start()

```

### `reverse_string_tool/tool.py`
``` python title="reverse_string_tool/tool.py" linenums="1" hl_lines="28-52"
from __future__ import annotations
from griptape.artifacts import TextArtifact, ErrorArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import define


@define
class ReverseStringTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to reverse a string",
            "schema": Schema(
                {Literal("input", description="The string to be reversed"): str}
            ),
        }
    )
    def reverse_string(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        try:
            return TextArtifact(input_value[::-1])

        except Exception as e:
            return ErrorArtifact(str(e))

    @activity(
        config={
            "description": "Can be used to reverse a sentence",
            "schema": Schema(
                {Literal("input", description="The sentence to be reversed"): str}
            ),
        }
    )
    def reverse_sentence(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        try:
            # Splitting the sentence into words
            words = input_value.split()

            # Reversing the list of words
            reversed_words = words[::-1]

            # Joining the reversed words back into a sentence
            reversed_sentence = " ".join(reversed_words)

            return TextArtifact(reversed_sentence)

        except Exception as e:
            return ErrorArtifact(str(e))


```


---
## Next Steps
In the [next section](07_display_image_tool.md), we'll take what we learned from these exercises, and create a tool that will display an image when passed the file path.