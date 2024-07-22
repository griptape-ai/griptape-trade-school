from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask

# Load environment variables
load_dotenv()

# Create a Workflow
workflow = Workflow()

# Create tasks
start_task = PromptTask("I will provide you a list of movies to compare.", id="START")

# Create a list of movie descriptions
movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "A shark attacks a beach",
    "A princess and a man named Wesley"
]

end_task = PromptTask("""
    How are these movies the same:
    {% for value in parent_outputs.values()%}
    {{ value }}
    {% endfor %}
    """,
    id="END")

# Add tasks to workflow
workflow.add_task(start_task)
workflow.add_task(end_task)

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }} ",
        context={"description": description})
    workflow.insert_tasks(start_task, [movie_task], end_task)

# Run the workflow
workflow.run()
