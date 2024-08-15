from dotenv import load_dotenv

# Griptape
from griptape.tasks import PromptTask
from griptape.structures import Workflow

# Load Env Variables
load_dotenv()

# Start Task, Generates two movies from the 90's
start_task = PromptTask("Generate two movies from the 90's", id="START")

# Summary Task, Summarizes the previously generated movies
summary_task = PromptTask("Summarize these movies: {{parent_outputs}}", id="SUMMARIZE")

# Compare Tasks, Compare the two movies.
compare_task = PromptTask("Compare these movies: {{parent_outputs}}", id="COMPARE")

# Takes in the summary and compare Tasks to rank the movies
rank_end_task = PromptTask("Rank the movies 1 or 2: {{parent_outputs}}", id="RANK_END")

# Specify parent-child relationships imperatively
summary_task.add_parent(start_task)
compare_task.add_parent(start_task)
rank_end_task.add_parents([summary_task, compare_task])

# Create the Workflow
workflow = Workflow(
    tasks=[start_task, summary_task, compare_task, rank_end_task],
)

# Run the Workflow
workflow.run()
