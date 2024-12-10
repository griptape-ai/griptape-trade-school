from dotenv import load_dotenv
import os

# Griptape Items
from griptape.drivers import OpenAiChatPromptDriver
from griptape.structures import Agent, Workflow
from griptape.tasks import TextSummaryTask, ToolTask, ToolkitTask
from griptape.utils import Chat
from griptape.tools import ImageQueryTool, FileManagerTool


from rich import print as print  # Modifies print to use the Rich library

load_dotenv()  # Load your environment

# Create an Image Query Driver
driver = OpenAiChatPromptDriver(model="gpt-4o")


# Configure the ImageQueryTool
image_query_tool = ImageQueryTool(prompt_driver=driver, off_prompt=False)

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
            + "SEO description, Caption, Alt-text, 5 keywords, an HTML snippet to "
            + "display the image. Save this to image_descriptions/{{ filename }}.yml\n"
            + "in YAML format.\n\n{{ parent_outputs }}",
            tools=[FileManagerTool(off_prompt=False)],
            context={"image": image},
            id=f"seo_{image}",
        )

        # Insert it to the workflow
        workflow.insert_tasks(startTask, [image_summary_task], endTask)
        workflow.insert_tasks(image_summary_task, [image_seo_task], endTask)

    # Run the workflow
    workflow.run()
else:
    # Create the Agent
    agent = Agent(tools=[image_query_tool, FileManagerTool(off_prompt=False)], stream=True)

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
        handle_output=formatted_response,  # Uses the formatted_response function
    ).start()
