from dotenv import load_dotenv

# Griptape
from griptape.structures import Workflow
from griptape.tasks import PromptTask


# Load environment variables
load_dotenv()

# Create a Workflow
workflow = Workflow()

# Create a list of movie descriptions
movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "A shark attacks a beach",
    "A princess and a man named Wesley",
]

compare_task = PromptTask(
    """
    How are these movies the same:
    {% for key, value in parent_outputs.items() %}
    {{ value }}
    {% endfor %}
    """,
    id="compare",
)

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }} ",
        context={"description": description},
    )
    workflow.add_task(movie_task)

    movie_task.add_child(compare_task)

# Run the workflow
workflow.run()
