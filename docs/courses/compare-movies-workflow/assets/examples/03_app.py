from dotenv import load_dotenv

# Griptape
from griptape.structures import Workflow
from griptape.tasks import PromptTask


# Load environment variables
load_dotenv()

# Create a Workflow
workflow = Workflow()

# Create tasks
movie_1_task = PromptTask(
    "What movie is this? Return only the movie name: A boy discovers an alien in his back yard",
    id="movie_1",
)
movie_2_task = PromptTask(
    "What movie is this? Return only the movie name: a shark attacks a beach.",
    id="movie_2",
)

compare_task = PromptTask(
    """
    How are these movies the same:
    {{parent_outputs['movie_1']}}
    {{parent_outputs['movie_2']}}
    """,
    id="compare",
)

# Add tasks to the workflow
workflow.add_task(movie_1_task)
workflow.add_task(movie_2_task)

# Add compare as a child
movie_1_task.add_child(compare_task)
movie_2_task.add_child(compare_task)

# Run the workflow
workflow.run()
