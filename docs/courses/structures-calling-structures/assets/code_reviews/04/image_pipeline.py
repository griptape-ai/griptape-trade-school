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
    output_dir = "images"

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
        image_path = os.path.join(output_dir, filename)

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