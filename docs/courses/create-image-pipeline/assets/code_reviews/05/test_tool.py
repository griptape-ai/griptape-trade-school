from dotenv import load_dotenv
from griptape.structures import Pipeline
from griptape.tasks import ToolkitTask
from griptape.tools import DateTimeTool

load_dotenv()

# Create the pipeline
pipeline = Pipeline()

# Create task
task = ToolkitTask("{{ args[0] }}", tools=[DateTimeTool(off_prompt=False)], id="Task")

# Add task to the pipeline
pipeline.add_task(task)

# Run the pipeline
pipeline.run("How much time is there before April 3?")
