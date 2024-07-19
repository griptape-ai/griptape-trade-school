from dotenv import load_dotenv

# Griptape
from griptape.structures import Workflow
from griptape.tasks import PromptTask

load_dotenv() 

# Create the workflow object
workflow = Workflow()

# Create tasks
start_task = PromptTask("I will provide you a list of movies to compare.", id="START")
end_task = PromptTask(
    """
    How are these movies the same: 
    {{ parent_outputs['movie_1'] }}
    {{ parent_outputs['movie_2'] }}
    """,
    id="END",
)
# Create movie tasks
movie_1_task = PromptTask(
    "What movie is this? Return only the movie name: A boy discovers an alien in his back yard",
    id="movie_1",
)
movie_2_task = PromptTask(
    "What movie is this? Return only the movie name: a shark attacks a beach.",
    id="movie_2",
)

# Add tasks to workflow
workflow.add_task(start_task)
workflow.add_task(end_task)

# Add tasks to workflow
workflow.insert_tasks(start_task, [movie_1_task, movie_2_task], end_task)

# Run the workflow
workflow.run()