from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask


# Load environment variables
load_dotenv()

# Create a Workflow
workflow = Workflow()


movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "a shark attacks a beach."
]

compare_task = PromptTask("How are these movies the same: \n{{inputs.items()}}")

for description in movie_descriptions:
    movie_task = PromptTask(f"What movie title is this?:{description}")
    workflow.add_task(movie_task)

    movie_task.add_child(compare_task)

# Run the workflow
workflow.run()
