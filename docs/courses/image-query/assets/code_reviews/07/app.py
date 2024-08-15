from dotenv import load_dotenv
import os

# Griptape Items
from griptape.structures import Workflow, Agent
from griptape.tasks import TextSummaryTask, ToolTask, ToolkitTask
from griptape.tools import ImageQueryTool, FileManagerTool
from griptape.engines import ImageQueryEngine
from griptape.drivers import OpenAiImageQueryDriver
from griptape.utils import Chat

from rich import print as print  # Modifies print to use the Rich library

load_dotenv()  # Load your environment

# Create an Image Query Driver
driver = OpenAiImageQueryDriver(model="gpt-4o")

# Create an Image Query Engine
engine = ImageQueryEngine(
    image_query_driver=driver,
)

# Configure the ImageQueryTool
image_query_tool = ImageQueryTool(image_query_engine=engine, off_prompt=False)
flow = "WORKFLOW"
if flow == "WORKFLOW":
    # Create a Workflow
    workflow = Workflow()

    # Create the Start and End tasks.
    startTask = TextSummaryTask("We are going to start a new workflow.", id="START")
    endTask = TextSummaryTask(
        "We have completed the workflow. Summarize what we did {{ parent_outputs }}",
        id="END",
    )

    # Add the tasks to the workflow
    workflow.add_tasks(startTask, endTask)

    # For each image in the directory
    image_dir = "./images"
    for image in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image)
        filename = os.path.splitext(image)[0]

        # Create an Image Summary Task
        image_summary_task = ToolTask(
            "Describe this image in detail: {{ image_path }}",
            context={"image_path": image_path},
            tool=image_query_tool,
            id=f"{image}",
        )

        # Create an Image SEO Task
        image_seo_task = ToolkitTask(
            "Based on this image description, create the following:\n"
            + "A nice title based on the image name, \n"
            + "The path to the image: {{ image_path }}, \n"
            + "Brief SEO description, "
            + "alt-text, 3 keywords, caption, "
            + "and an HTML snippet to display the image.\n"
            + "To format the data, use the example in the "
            + "template file: 'template.yml',\n"
            + "and save the result to image_descriptions/{{ filename }}.yml\n"
            + "in YAML format.\n\n{{ parent_outputs }}",
            tools=[FileManagerTool(off_prompt=False)],
            context={"image": image, "image_path": image_path},
            id=f"seo_{image}",
        )

        # Insert it to the workflow
        workflow.insert_tasks(startTask, [image_summary_task], endTask)
        workflow.insert_tasks(image_summary_task, [image_seo_task], endTask)

    # Run the workflow
    workflow.run()

else:
    # Create the Agent
    agent = Agent(
        logger_level=0, tools=[image_query_tool, FileManagerTool(off_prompt=False)]
    )

    # Configure the agent to stream it's responses.
    agent.config.prompt_driver.stream = True

    # Modify the Agent's response to have some color.
    def formatted_response(response: str) -> None:
        print(f"[dark_cyan]{response}", end="", flush=True)

    # Begin Chatting
    Chat(
        agent,
        intro_text="\nWelcome to Griptape Chat!\n",
        prompt_prefix="\nYou: ",
        processing_text="\nThinking...",
        response_prefix="\nAgent: ",
        output_fn=formatted_response,  # Uses the formatted_response function
    ).start()
