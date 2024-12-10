from dotenv import load_dotenv

# Griptape
from griptape.structures import Workflow
from griptape.tasks import PromptTask, ToolkitTask
from griptape.tools import WebScraperTool, PromptSummaryTool

load_dotenv()

# Create the workflow object
workflow = Workflow()


# Create tasks
start_task = PromptTask("I will provide you a list of movies to compare.", id="START")
end_task = PromptTask(
    """
    How are these movies the same:
     {% for value in parent_outputs.values() %} 
     {{ value }}
     {% endfor %}
    """,
    id="END",
)

# Create a list of movie descriptions
movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "A shark attacks a beach",
    "A princess and a man named Wesley",
]

# Add tasks to workflow
workflow.add_task(start_task)
workflow.add_task(end_task)

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }}",
        context={"description": description},
    )
    summary_task = ToolkitTask(
        "Use metacritic to get a summary of this movie: {{ parent_outputs.values() | list |last }}",
        tools=[WebScraperTool(), PromptSummaryTool(off_prompt=False)],
    )

    workflow.insert_tasks(start_task, [movie_task], end_task)
    workflow.insert_tasks(movie_task, [summary_task], end_task)

# Run the workflow
workflow.run()

# View the output
print(workflow.output_task.output.value)
