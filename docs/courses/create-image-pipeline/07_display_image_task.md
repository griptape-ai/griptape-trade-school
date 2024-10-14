# Display Image Task

![gallery](assets/img/gallery.png)

## Overview
In this section, we'll create a function to display an image, and then call it using the `CodeExecutionTask`. It will take the file path for the image generated, and use the [Python Image Library](https://pillow.readthedocs.io/en/stable/) to display it.

## What is the CodeExecutionTask

There are many types of Tasks available as part of Griptape, and most of them utilize an LLM. There are times, however, when it's not necessary to use an LLM to accomplish a goal - in fact, many times you may find that you want to simply operate on the output of a task without needing to call an LLM. 

For example, you might want to search and replace some text from the output of a run, re-format a date, analyze some text using an external library, split a string into a list, or many many other things. 

The `CodeExecutionTask` allows you to execute a generic Python function on the output of a previous task, and return data in a way that's useful for a downstream task.

Here's a very simple example of a function that can count for the number of occurrences of a particular string output from a previous task.

```python
# Create a function that takes the current task as an input and returns a TextArtifact
def count_mentions(task: CodeExecutionTask) --> TextArtifact:
    # Get the input text from the task. 
    input_text = task.input.value

    # Convert the string to lower case to make the search case-insensitive
    lowercase_text = input_text.lower()

    # Count the occurrences
    num_mentions = lowercase_text.count("skateboard")

    return TextArtifact(num_mentions)
```

And here's how you would use that function when defining the `CodeExecutionTask`:
```python
# Create the CodeExecutionTask that takes the output from the previous task
# and runs the function count_mentions.
get_mentions_task = CodeExecutionTask(
    "{{parent_output}}",
    run_fn = count_mentions
)
```

!!! tip
    You'll notice that the function has **Type Hinting** where we inform Python that the `task` parameter is of type `CodeExecutionTask` and the function will return a `TextArtifact`.

    You don't absolutely _need_ to do this - it's just a best practice to help with code clarity.

    You could just as easily define the function this way:
    ```python
    def count_mentions(task):
        # ...
    ```

    But as mentioned above, it's a best practice to use type hinting wherever you can, so we included it in the example.

### Task Context

You'll notice in the function `count_mentions` we passed `task` as a parameter, and we got the task's `input.value`. But what _other_ data is available in this function?

If you remember from the [Creating Images](04_creating_images.md#pipeline-context) section of the course, Pipelines contain `Context`. Tasks also have context, and we can access that data in our function.

When creating a `PromptTask`, you can use `context` to send more data to the prompt. For example:

```python
my_task = PromptTask(
    "Create an image in this style: {{style}}",
    context = {
        "style": "8-bit 80s video game"
    }
)
```

You can do something similar with the `CodeExecutionTask`, but instead of injecting the context into the prompt, you can grab it _in the function_. Let's take the example used above, but instead of hard-coding "skateboard" as the term to search for, we'll add it using `context`.

```python hl_lines="6 7"
# Create a function that takes the current task as an input and returns a TextArtifact
def count_mentions(task: CodeExecutionTask) --> TextArtifact:
    # Get the input text from the task. 
    input_text = task.input.value

    # get the search term
    search_term = task.context["search_term"]

    # Convert the string to lower case to make the search case-insensitive
    lowercase_text = input_text.lower()

    # Count the occurrences
    num_mentions = lowercase_text.count(search_term)

    return TextArtifact(num_mentions)
```

Here is what the `CodeExecutionTask` would look like:

```python hl_lines="6-8"
# Create the CodeExecutionTask that takes the output from the previous task
# and runs the function count_mentions.
get_mentions_task = CodeExecutionTask(
    "{{parent_output}}",
    run_fn = count_mentions,
    context = {
        "search_term": "skateboard"
    }
)
```

We'll use this combination of techniques to send the `output_dir` and the name of the image to a function that will display the image.

## Add Display Image Task

First, let's change the `display_image_task` from a `PromptTask` to a `CodeExecutionTask`. 

### Import `CodeExecutionTask`

First we need to import the `CodeExecutionTask`. In the imports section of `app.py`, add it to the appropriate line:

```python title="app.py" hl_lines="5"
# ...
from griptape.tasks import (
    PromptTask, 
    PromptImageGenerationTask, 
    CodeExecutionTask
)
# ...
```


### Modify display_image_task

Change the `display_image_task` from a `PromptTask` to a `CodeExecutionTask`. We'll then modify the prompt to just take the image name, and also provide the `run_fn`. Note, we haven't _created_ the function yet, we'll do that in the next step.

```python title="app.py" hl_lines="3 4 6"
# ...

display_image_task = CodeExecutionTask(
    "{{ parent.output.name }}",
    context={"output_dir": output_dir},
    run_fn=display_image,
    id="Display Image Task",
)

# ...
```

## Create Display Image Function

Now we get to create the `display_image` function that the `CodeExecutionTask` will run. You can create this anywhere in your code _before_ you create the `display_image_task`, however, to ensure your code is easy to read I recommend you do it before you instantiate the Pipeline. Before creating it, we'll need to import one more item.

### Import TextArtifact

The function requires an Artifact to be returned. Since this will be our last step in the Pipeline, it's not important _what_ we return, but since we're displaying an image we might as well return the path of the image displayed.

Add a section to your imports where you import a `TextArtifact` from `griptape.artifacts`.

```python title="app.py" hl_lines="2"
# ...
from griptape.artifacts import TextArtifact
# ...
```

Your full imports section for Griptape should look something like this:

```python
from griptape.structures import Pipeline
from griptape.tasks import (
    PromptTask,
    PromptImageGenerationTask,
    CodeExecutionTask
)
from griptape.drivers import OpenAiImageGenerationDriver
from griptape.engines import PromptImageGenerationEngine
from griptape.artifacts import TextArtifact

```

### Add the function

We won't display the image yet, we'll just create the function and make sure we have the proper path for the file.

```python title="app.py" hl_lines="6-17"
# ...

# Create the engine
image_engine = PromptImageGenerationEngine(image_generation_driver=image_driver)

# Create a function to display an image
def display_image(task: CodeExecutionTask) --> TextArtifact:
    # Get the filename
    filename = task.input.value

    # Get the output_dir
    output_dir = task.context["output_dir"]

    # Get the path of the image
    image_path = os.path.join(output_dir, filename)

    return TextArtifact(image_path)

# Create the pipeline object
pipeline = Pipeline()

# ...
```

### Test

Before displaying the image, let's execute the code and make sure our function is working correctly.

If you run the code, you should see something in the logs similar to this:
```bash hl_lines="4"
[01/11/24 11:10:58] INFO    CodeExecutionTask Display Image Task
                            Input: image_artifact_240111111058_1hzy.png 
                    INFO    CodeExecutionTask Display Image Task
                            Output: ./images/image_artifact_240111111058_1hzy.png
```

Notice how the `Output` has the full path to the image. Success! We have the path to the image that was generated - the next step is to show it to the user.

## Display Image

Now we'll update the function to display the image. To do this, we'll need to use the [Python Image Library (Pillow)](https://pillow.readthedocs.io/en/stable/) so that our images will display properly on all operating systems.

### Import Libraries

The `PIL` module allows us to do basic image processing in python. We will use the `os` module for getting our image path.

Let's start by importing the two libraries required, then we'll create the function.

Instead of adding the imports to the main `imports` section of your application, we can import them directly into the function that's using them.

In the `display_image` function, add the following:

```python hl_lines="5-6"
# ...

# Create a function to display an image
def display_image(task: CodeExecutionTask) -> TextArtifact:
    import os
    from PIL import Image

    # ...
```

### Open the Image

Now we'll add the code to open the image. Inside the `display_image` function, before the `return` statement, add the code for loading and displaying the image:

```python title="app.py" hl_lines="17-19"
# ...

# Create a function to display an image
def display_image(task: CodeExecutionTask) -> TextArtifact:
    import os
    from PIL import Image

    # Get the filename
    filename = task.input.value

    # Get the output_dir
    output_dir = task.context["output_dir"]

    # Get the path of the image
    image_path = os.path.join(output_dir, filename)

    # Open the image
    image = Image.open(image_path)
    image.show()

    return TextArtifact(image_path)

# ...
```


### Test it out

Go ahead and run the code. If everything works as expected, after the Pipeline finishes, an image viewer will open up with a beautiful image!

![Cow](assets/img/image_artifact_231218061609_wkcd.png)
---

## Code Review

You can now generate an image and display it using a Pipeline. Excellent work! Let's review the current state of our application.

```python title="app.py" linenums="1"
--8<-- "docs/courses/create-image-pipeline/assets/code_reviews/07/app.py"
```

---
## Are we there yet?


Congratulations! At this point, you have completed the main requirements for this course! You've built a pipeline that can execute multiple tasks to generate and display an image! You could high-five yourself, call your friends and brag about your accomplishments, and go eat a nice pizza to celebrate.

![pizza](assets/img/pizza.png)

Or... continue with the next steps and learn more about various parameters for DALL·E 3, Leonardo.Ai, and Amazon Bedrock image generation.

## Next Step
Let's take a look at some of the attributes available to us with each of the Image Generation Drivers available in Griptape. Let's start with [OpenAI DALL·E 3](08_dalle-3.md).
