from dotenv import load_dotenv
from griptape.artifacts import TextArtifact
from griptape.drivers import OpenAiImageGenerationDriver

# Griptape
from griptape.structures import Pipeline
from griptape.tasks import (
    CodeExecutionTask,
    PromptImageGenerationTask,
    PromptTask,
)

load_dotenv()  # Load your environment

# Variables
output_dir = "images"

# Create the driver
image_driver = OpenAiImageGenerationDriver(model="dall-e-3", api_type="open_ai", image_size="1024x1024")


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
    image_generation_driver=image_driver,
    output_dir=output_dir,
    id="Generate Image Task",
)

display_image_task = CodeExecutionTask(
    "{{ parent.output.name }}",
    context={"output_dir": output_dir},
    on_run=display_image,
    id="Display Image Task",
)

# Add tasks to pipeline
pipeline.add_tasks(create_prompt_task, generate_image_task, display_image_task)

# Run the pipeline
pipeline.run("a cow")
