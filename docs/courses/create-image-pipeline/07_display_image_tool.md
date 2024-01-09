# Display Image Tool

![gallery](assets/img/gallery.png)

## Overview
In this section, we'll create the Display Image Tool. It will take the file path for the image generated, and use whatever the default image viewer is for the operating system to display it.

### Copy `reverse_string_tool`

1. In Visual Studio Code, select the folder `reverse_string_tool` and choose ++cmd+c++, ++cmd+v++ on Mac, or ++ctrl+c++, ++ctrl+v++ on Windows.

2. Rename the new folder as `display_image_tool` by selecting it and choosing **Right Mouse Button** -> **Rename...** (or just select it and hit the ++return++ key)

### Delete `__pycache__`

The `__pycache__` folder is a directory used by Python to store compiled compiled files. When you run a Python program it saves a 'shortcut' version of the program in this folder. The next time you run the same program, Python uses these shortcuts to start the program more quickly.

In this case, you don't want it because it holds the compiled code for the `reverse_string_tool`.

3. Delete the `__pycache__` folder that is inside `display_image_tool` by choosing **Right Mouse Button** -> **Delete** (or select it and hit ++cmd+delete++ on Mac, ++ctrl+delete++ on Windows.)

### Modify `__init__.py`

Remember from earlier, that the `__init__.py` file in Python is used to mark a directory as a Python package. In our current `__init__.py` file, it's being used to import the `ReverseStringTool` class. We're going to be replacing that class with our own: `DisplayImageTool`. So we'll need to update this file.

Replace all instances of `ReverseStringTool` with `DisplayImageTool` in the file. _Note: we haven't created that class yet, we'll do that in a couple of steps._

```python title="display_image_tool/__init__.py"
from .tool import DisplayImageTool

__all__ = ["DisplayImageTool"]

```

### Modify `manifest.yml`

The `manifest.yml` file provides information for people and other downstream systems to understand what this Tool is about. At the moment it contains information about the `Reverse String Tool`. Modify it to look like the following (don't forget to include your own contact email and legal details).

```yaml title="display_image_tool/manifest.yaml"
version: "v1"
name: Display Image Tool
description: Tool for displaying an image
contact_email: contact@example.com
legal_info_url: https://www.example.com/legal

```

### Create `requirements.txt`

Some Tools you create for Griptape will require various Python dependencies - other libraries that they need to operate correctly.  Griptape allows you to easily include these requirements by adding them to a `requirements.txt` file, located inside your tool folder. You will then import the required dependency _inside the method where it's used_. 

This particular tool doesn't need any external libraries to be imported, so we can just leave the `requirements.txt` file blank. You could simply ignore it and not create the file, but if you decide to change this later and use a library within your code it's good to know how to use this.

1. Select the `display_image_tool` folder and choose **Right Mouse Button** -> **New File..**
2. Name the new file `requirements.txt`

## Update `tool.py`

### Description

Now we're at the part where we update the Display Image Tool itself. We'll be modifying `tool.py` with the following steps:

* Rename the class
* Define parameters
* Update the activity
* Update the method
* Import requirements
* Create a function to display the image
* Use it

### Rename the Class

Rename the class definition from `ReverseStringTool` to `DisplayImageTool`.

```python title="display_image_tool/tool.py" hl_lines="4"
# ...

@define
class DisplayImageTool(BaseTool):
        @activity(
            # ...
        )
        #...
# ...
```

### Update the Activity

The method we're going to create will allow us to display an image. We need to describe that method in the `@activity` section. The description itself should be pretty straightforward.. something like "Can be used to display an image". We will require the path of the image to be sent, and we'll use the `schema` for that.

* Change the `description`
* Update the `schema` section of the activity. 

```python title="display_image_tool/tool.py" hl_lines="7-14"
# ...
@define
class DisplayImageTool(BaseTool):
    # ...
    @activity(
        config={
            "description": "Can be used to display an image",
            "schema": Schema(
                {
                    Literal(
                        "filename", description="The filename of the image to view."
                    ): str,
                }
            ),
        }
    )
    # ...

#...
```

### Rename the method

The method is still named `reverse_string`. Let's rename it to what we're actually doing - displaying the image.

```python title="display_image_tool/tool.py" hl_lines="7"
# ...
@define
class DisplayImageTool(BaseTool):
    @activity(
            #..
    )
    def display_image(self, params: dict) -> TextArtifact | ErrorArtifact:
        # ...
#...

```

### Get the Parameter

We're passing the `filename` as a parameter, so let's make sure we grab that value right away. Update `input_value = params["values"].get("input")` so we're getting the filename, and for now just return the `filename` from the method. Here's what the whole method should look like:

```python hl_lines="5-11"
# ...

class DisplayImageTool(BaseTool):
    # ...
    def display_image(self, params: dict) -> TextArtifact | ErrorArtifact:
        filename = params["values"].get("filename")
        try:
            return TextArtifact(filename)

        except Exception as e:
            return ErrorArtifact(str(e))
# ...
```

### Import Libraries

In order to display the image, we need a bit of code that will work on Mac, Windows, and Linux. Our goal is to simply open the image in whatever image viewer the user likes to use.

The `sys` module has a variable called `platform` that can get the operating system. Then, depending on the operating system we'll need one of two different methods to call. Windows uses `os.startfile`, and both Mac and Linux use the `subprocess` library.

Let's start by importing the three libraries required, then we'll create the function.

In the `imports` section of `tool.py`, add the following:

```python hl_lines="2"
# ...
import os, subprocess, sys

# ...
```

### Create open_image

Now we can create the function to open the image. It will take a filepath, and then depending on the operating system use the correct command to open the image.

Add the following function _after_ you import the libraries, but _before_ `@define`.

```python title="display_image_tool/tool.py" hl_lines="3-10"
# ...

# Open an image
def open_image(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    elif sys.platform == "darwin":  # macOS
        subprocess.run(["open", filename])
    else:  # linux variants
        subprocess.run(["xdg-open", filename])

@define
class DisplayImageTool(BaseTool):
    # ...
# ...
```
### Open Image
Now we can use the function to attempt to open an image.

Inside the `try:` statement for the `display_image` method, use the `open_image` function and pass it `filename`.

```python title="display_image_tool/tool.py" hl_lines="10"
# ...

class DisplayImageTool(BaseTool):
    @activity(
        # ...    
    )
    def display_image(self, params: dict) -> TextArtifact | ErrorArtifact:
        filename = params["values"].get("filename")
        try:
            open_image(filename)
            return TextArtifact(filename)
        
        except Exception as e:
            return ErrorArtifact(str(e))
```

### Final `tool.py`

Let's look at the resulting `tool.py` and make sure all the changes are present.

```python title="display_image_tool/tool.py" linenums="1"
from __future__ import annotations
from griptape.artifacts import TextArtifact, ErrorArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import define

import os, subprocess, sys


# Open an image
def open_image(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    elif sys.platform == "darwin":  # macOS
        subprocess.run(["open", filename])
    else:  # linux variants
        subprocess.run(["xdg-open", filename])


@define
class DisplayImageTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to display an image",
            "schema": Schema(
                {
                    Literal(
                        "filename", description="The filename of the image to view."
                    ): str,
                }
            ),
        }
    )
    def display_image(self, params: dict) -> TextArtifact | ErrorArtifact:
        filename = params["values"].get("filename")
        try:
            open_image(filename)
            return TextArtifact(filename)

        except Exception as e:
            return ErrorArtifact(str(e))
```

## Update app.py

Now that we have the tool, let's update our application to use it.

### Import DisplayImageTool

Just like we imported the `ReverseStringTool` in the previous lesson, we need to import the `DisplayImageTool` into our application in order to use it.

Add the following import statement in the imports section of your `app.py` (_note: we're back working on `app.py`, not `test_tool.py`_):

```python title="app.py" hl_lines="2"
# ...
from display_image_tool import DisplayImageTool

# ...
```

### Update display_image_task

Change the `display_image_task` from a `PromptTask` to a `ToolkitTask`. Then we can pass it the `DisplayImageTool`, and modify the prompt to not say "Pretend" to display an image, but just go ahead and display it.

```python title="app.py" hl_lines="3 5 9"
# ...

display_image_task = ToolkitTask(
    """
    Display the image to the user.
    {{output_dir}}/{{ parent.output.name }}
    """,
    context={"output_dir": output_dir},
    tools=[DisplayImageTool(off_prompt=False)],
    id="Display Image Task",
)

# ...

```

### Test it out

Go ahead and run the code. If everything works as expected, after the Pipeline finishes you an image viewer will open up with a beautiful image!

![Cow](assets/img/image_artifact_231218061609_wkcd.png)
---

## Code Review

You can now generate an image and display it using a Pipeline. Excellent work! Let's review the current state of our application and tools:

### app.py
```python linenums="1" title="app.py" hl_lines="9 45 47 51"
from dotenv import load_dotenv

# Griptape
from griptape.structures import Pipeline
from griptape.tasks import PromptTask, PromptImageGenerationTask, ToolkitTask
from griptape.drivers import OpenAiDalleImageGenerationDriver
from griptape.engines import PromptImageGenerationEngine

from display_image_tool import DisplayImageTool

load_dotenv()  # Load your environment

# Variables
output_dir = "./images"

# Create the driver
image_driver = OpenAiDalleImageGenerationDriver(
    model="dall-e-3", api_type="open_ai", image_size="1024x1024"
)

# Create the engine
image_engine = PromptImageGenerationEngine(image_generation_driver=image_driver)

# Create the pipeline object
pipeline = Pipeline()

# Create tasks
create_prompt_task = PromptTask(
    """
    Create a prompt for an Image Generation pipeline for the following topic: 
    {{ args[0] }}
    in the style of {{ style }}.
    """,
    context={"style": "a 1970s polaroid"},
    id="Create Prompt Task",
)

generate_image_task = PromptImageGenerationTask(
    "{{ parent_output }}",
    image_generation_engine=image_engine,
    output_dir=output_dir,
    id="Generate Image Task",
)

display_image_task = ToolkitTask(
    """
    Display the image to the user.
    {{output_dir}}/{{ parent.output.name }}
    """,
    context={"output_dir": output_dir},
    tools=[DisplayImageTool(off_prompt=False)],
    id="Display Image Task",
)

# Add tasks to pipeline
pipeline.add_tasks(create_prompt_task, generate_image_task, display_image_task)

# Run the pipeline
pipeline.run("a cow")

```

### display_image_tool/tool.py

```python title="display_image_tool/tool.py"
from __future__ import annotations
from griptape.artifacts import TextArtifact, ErrorArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import define

import os, subprocess, sys


# Open an image
def open_image(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    elif sys.platform == "darwin":  # macOS
        subprocess.run(["open", filename])
    else:  # linux variants
        subprocess.run(["xdg-open", filename])


@define
class DisplayImageTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to display an image",
            "schema": Schema(
                {
                    Literal(
                        "filename", description="The filename of the image to view."
                    ): str,
                }
            ),
        }
    )
    def display_image(self, params: dict) -> TextArtifact | ErrorArtifact:
        filename = params["values"].get("filename")
        try:
            open_image(filename)
            return TextArtifact(filename)

        except Exception as e:
            return ErrorArtifact(str(e))

```

### display_image_tool/__init__.py
```python title="display_image_tool/__init__.py"
from .tool import DisplayImageTool

__all__ = ["DisplayImageTool"]

```

### display_image_tool/manifest.yml
```yaml title="display_image_tool/manifest.yml"
version: "v1"
name: Display Image Tool
description: Tool for displaying an image
contact_email: contact@example.com
legal_info_url: https://www.example.com/legal
```

---
## Are we there yet?


Congratulations! At this point, you have completed the main requirements for this course! You've built a pipeline that can execute multiple tasks to generate and display an image! You could high-five yourself, call your friends and brag about your accomplishments, and go eat a nice pizza to celebrate.

![pizza](assets/img/pizza.png)

Or... continue with the next steps and learn more about various parameters for DALL·E 3, Leonardo.Ai, and Amazon Bedrock image generation.

## Next Step
Let's take a look at some of the attributes available to us with each of the Image Generation Drivers available in Griptape. Let's start with [OpenAI DALL·E 3](08_dalle-3.md).