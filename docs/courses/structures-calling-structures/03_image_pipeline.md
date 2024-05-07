# Image Pipeline

In this section we’ll take the image pipeline from this course: [Image Generation - Pipelines](../create-image-pipeline/), turn it into a function, and save it as a separate file we can bring into our existing `app.py`. This is a good practice to keep these useful structures in separate files, so your code can be more modular. Also, if you get paid by the number of files you create, it’ll really impress your employer.

## Create `image_pipeline.py`

1. In your application folder, create a new file called `image_pipeline.py`. 

2. Navigate to the Image Generation Pipelines course, go to the Displaying Images section, and scroll down to [Code Review](../create-image-pipeline/07_display_image_task.md#code-review). 

3. Copy the code from this section and paste it into the `image_pipeline.py`.

## Wrap the code in a function

You can keep all the same code you have, but wrap it into a function. After your import statements are finished, create the image_pipeline function like this:

```py title="image_pipeline.py`
# ...

def image_pipeline() -> Pipeline:
    # Variables
    output_dir = "./images"

    # ... rest of your code
```

This says you’re creating the function, and returning a Pipeline structure.

## Remove the Run statement

In your existing code, you’re still running the pipeline. We no longer need to do that - the Agent will run it when it gets called. 

Delete the following lines from the bottom :

```py
    # Run the pipeline
    pipeline.run("a cow")
```

## Add a return

Finally, we need to return the pipeline structure. So in the place where you had the Run the Pipeline code, replace it with a return statement.

```py title="image_pipeline.py"
	# ...

    # Return the pipeline
    return pipeline
```

## Code Review

That’s it for setting up your image pipeline script! Let’s review the code

```py title="image_pipeline.py" linenums="1"
from dotenv import load_dotenv

# Griptape
from griptape.structures import Pipeline
from griptape.tasks import (
    PromptTask,
    PromptImageGenerationTask,
    CodeExecutionTask,
)
from griptape.artifacts import TextArtifact
from griptape.drivers import OpenAiImageGenerationDriver
from griptape.engines import PromptImageGenerationEngine


def create_image_pipeline() -> Pipeline:
    # Variables
    output_dir = "./images"

    # Create the driver
    image_driver = OpenAiImageGenerationDriver(
        model="dall-e-3", api_type="open_ai", image_size="1024x1024"
    )

    # Create the engine
    image_engine = PromptImageGenerationEngine(image_generation_driver=image_driver)

    # Create a function to display an image
    def display_image(task: CodeExecutionTask) -> TextArtifact:
        import os, subprocess, sys

        # Get the filename
        filename = task.input.value

        # Get the output_dir
        output_dir = task.context["output_dir"]

        # Get the path of the image
        image_path = f"{output_dir}/{filename}"

        # Open the image
        if sys.platform == "win32":
            os.startfile(image_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", image_path])
        else:  # linux variants
            subprocess.run(["xdg-open", image_path])

        return TextArtifact(image_path)

    # Create the pipeline object
    pipeline = Pipeline()

    # Create tasks
    create_prompt_task = PromptTask(
        """
        Create a prompt for an Image Generation pipeline for the following topic: 
        {{ args[0] }}
        in the style of {{ style }}.
        """,
        context={"style": "a polaroid photograph from the 1970s"},
        id="Create Prompt Task",
    )

    generate_image_task = PromptImageGenerationTask(
        "{{ parent_output }}",
        image_generation_engine=image_engine,
        output_dir=output_dir,
        id="Generate Image Task",
    )

    display_image_task = CodeExecutionTask(
        "{{ parent.output.name }}",
        context={"output_dir": output_dir},
        run_fn=display_image,
        id="Display Image Task",
    )

    # Add tasks to pipeline
    pipeline.add_tasks(create_prompt_task, generate_image_task, display_image_task)

    # Return the pipeline
    return pipeline
```

---
## Next Steps

In the [next section](04_drawing_agent.md), we’ll update our app to have an agent, bring in the image_generation pipeline, create the appropriate driver and client, and give that to the agent.
