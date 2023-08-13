from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask
from griptape.drivers import OpenAiPromptDriver


# Load environment variables
load_dotenv()

# Create a Workflow
# Give it the movie_researcher rulset because we want this workflow to research and compare a number of movies.
workflow = Workflow()

# Define the OpenAiPromptDriver with Max Tokens
driver_4 = OpenAiPromptDriver(
    model="gpt-4",
    max_tokens=500
)

movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "a shark attacks a beach."
]

compare_task = PromptTask("""
            How are these movies the same: 
            {% for key, value in inputs.items() %}
            {{ value }}
            {% endfor %}
            """)

for description in movie_descriptions:
    movie_task = PromptTask(f"What movie title is this? Output just the title.:{description}")
    workflow.add_task(movie_task)

    movie_task.add_child(compare_task)

# Run the workflow
workflow.run()
