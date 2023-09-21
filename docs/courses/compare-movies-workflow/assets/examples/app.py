"""
Compare Movies Workflow 

This script demonstrates how to use Griptape Workflows to create non-sequential 
dependency tasks.

The script takes a list of rough movie description and for each description figures out:
    - The *actual* name of the movie
    - Searches the web for the description
    - Summarizes the description

After all the summaries for all the descriptions are finished, it then compares the
movies and displays their similarities.

Key Features:
1. Uses Griptape PromptTasks and ToolkitTasks to communicate with LLMs
2. Uses the OpenAiPromptDriver to control the number of tokens being used at any given time.
3. Uses Griptape Workflows to control the flow of tasks
4. Uses the WebScraper tool to get information from the web
5. Uses Rules and Rulesets to help determine how the Workflow behaves

Usage:
Create a list of movie descriptions, then run the script.

Requirements:
- OpenAI API Key stored in a .env file. 
  You can get it here: https://beta.openai.com/account/api-keys

Dependencies:
- griptape
- python-dotenv
"""
from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask, ToolkitTask
from griptape.tools import WebScraper
from griptape.drivers import OpenAiChatPromptDriver


# Load environment variables
load_dotenv()

# Define the OpenAiChatPromptDriver with Max Tokens
driver = OpenAiChatPromptDriver(
    model="gpt-4",
    max_tokens=500
)

# Create a Workflow
workflow = Workflow()

# Create a list of movie descriptions
movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "a shark attacks a beach.",
    "A princess and a man named Wesley"
]

compare_task = PromptTask("""
    How are these movies the same: 
    {% for key, value in parent_outputs.items() %}
    {{ value }}
    {% endfor %}
    """,
    prompt_driver=driver,
    id="compare")

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }} ",
        context={"description": description},
        prompt_driver=driver
        )
    
    summary_task = ToolkitTask(
        """
        Give me a very short summary of the movie from imdb:
        {% for key, value in parent_outputs.items() %}
        {{ value }}
        {% endfor %}
        """,
        tools=[WebScraper()],
        prompt_driver=driver
        )
    
    workflow.add_task(movie_task)
    movie_task.add_child(summary_task)
    summary_task.add_child(compare_task)

# Run the workflow
workflow.run()

# View the output
for task in workflow.output_tasks():
    print(task.output.value)    

