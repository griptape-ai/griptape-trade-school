# Creating Images

## Overview
Image Generation via Griptape is handled via a few components.

* **Image Generation Driver** - Determines the model to be used. For example, [OpenAI DALL·E 3](https://openai.com/dall-e-3){target="_blank"} or [Leonardo.AI](https://leonardo.ai/){target="_blank"}.
* **Image Generation Engines** - The engine that facilitates the use of the Driver.
* **Image Generation Task** or **Image Generation Tool**. The Task or Tool is what will be provided to the Griptape Structure. Pipelines and Workflows can use `ImageGenerationTask` directly. You can provide an `ImageGenerationTool` to an Agent, to a ToolTask, or to a ToolkitTask.

For example, to create an image with OpenAI DALL·E 3 as a **task** you could do something like:

```python

# Create an Image Generation Driver
driver = OpenAiDalleImageGenerationDriver(
    model="dall-e-3", api_type="open_ai", image_size="1024x1024"
)

# Create an Image Generation Engine
engine = ImageGenerationEngine( image_generation_driver=driver )

# Create an Image Generation Task
task = ImageGenerationTask(
    "Create a drawing of a pineapple",
    image_generation_engine=engine,
    output_dir="./images"
)
```

Once you generate the task, you would add it to the pipeline or workflow.

You can also use the `ImageGenerator` tool and assign it to an Agent. It takes many of the same arguments. If you had previously created the `driver` and `engine` as specified above, you would do something like:

```python
agent = Agent(
    tools=[ImageGenerator(
        image_generation_engine=engine,
        output_dir="./images",
        off_prompt=False,
    )]
)
```

The main thing to be aware of is that these components always exist. You choose the model with the **Driver**, use the **Engine** to facilitate the use of the model, and then access the engine with either a **Task** or a **Tool**.

In this course, because we're focusing on image generation as part of a pipeline, we'll use generate images using a task.

## The Image Task

In order to get started, we'll begin by replacing the Fake Image Generation task with a real one, using OpenAI DALL·E 3. We'll start with the basics, and adjust settings in a future step. For now, we just want to get things working.

### Imports

To use the Driver, Engine, and Task we'll need to add them to our `imports` section in `app.py`. You'll modify `griptape.tasks` to inlude `ImageGenerationTask`, and add imports for the Driver and Engine.

```python hl_lines="5-7"
# ...

# Griptape
from griptape.structures import Pipeline
from griptape.tasks import PromptTask, ImageGenerationTask
from griptape.drivers import OpenAiDalleImageGenerationDriver
from griptape.engines import ImageGenerationEngine

# ...
```

### Create the Driver

Now we'll create our image generation driver. We'll dive into detail about some of the settings on the driver later, but first we'll get everything hooked up and working. Remember, the Driver controls what Image Generation Model we'll be using.

In `app.py`, create the driver before you create the pipeline.

```python hl_lines="5-8"
# ...

load_dotenv()  # Load your environment

# Create the driver
image_driver = OpenAiDalleImageGenerationDriver(
    model="dall-e-3", api_type="open_ai", image_size="1024x1024"
)

# Create the pipeline object
# ...
```

### Create the Engine

The engine facilitates the use of the particular model. It will be what we pass to the task or tool. After the creation of the driver, create the engine:

```python hl_lines="8-9"
# ...

# Create the driver
image_driver = OpenAiDalleImageGenerationDriver(
    model="dall-e-3", api_type="open_ai", image_size="1024x1024"
)

# Create the engine
image_engine = ImageGenerationEngine(image_generation_driver=image_driver)

# Create the pipeline object
# ...
```

### Replace the ImageTask

Next, we'll replace our fake image generation task with a _real_ image generation task. We'll want to


HERE !!!!

## OpenAI DALL·E 3

## Leonardo.AI

## Stable Diffusion on Amazon Bedrock
---

## Code Review

We created the scaffolding for our application. Let's review the code and make sure it's working as expected.

```python linenums="1" title="app.py"
from dotenv import load_dotenv

# Griptape
from griptape.structures import Pipeline
from griptape.tasks import PromptTask

load_dotenv()  # Load your environment

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

generate_image_task = PromptTask(
    """
    Pretend to create an image using this prompt, 
    and return the filename of the generated image: 
    {{ parent_output }}
    """,
    id="Generate Image Task",
)

display_image_task = PromptTask(
    """
    Pretend to display the image to the user. 
    {{ parent_output }}.
    """,
    id="Display Image Task",
)

# Add tasks to pipeline
pipeline.add_tasks(create_prompt_task, generate_image_task, display_image_task)

# Run the pipeline
pipeline.run("a cow")


```

## Next Step
In the next section, we are going to replace our fake Image Generation task with a real one. Check out [Creating Images](04_creating_images.md) when you're ready to continue.
