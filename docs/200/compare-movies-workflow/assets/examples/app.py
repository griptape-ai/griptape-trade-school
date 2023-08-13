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
- logging
"""

from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask, ToolkitTask
from griptape.tools import WebScraper
from griptape.drivers import OpenAiPromptDriver

# CREATE THE LIST OF MOVIES
# 
# Add to the list of movie descriptions you want to comapre.
#
# Examples:
#   "a kid discovers an alien in his backyard in the 80s"
#   "A movie about a kid who suddenly gets big.",
#   "It was a movie about the start of sound in cinema, there was dancing."
#

movies = [
    "a kid discovers an alien in his backyard in the 80s",
    "Black and white movie turns color",
    "Kid suddenly becomes big."
]


# Load environment variables
load_dotenv()

# Create a Workflow
# Give it the movie_researcher rulset because we want this workflow to research and compare a number of movies.
workflow = Workflow(
    rulesets=[movie_researcher]
)

# Define the OpenAiPromptDriver with Max Tokens
driver_4 = OpenAiPromptDriver(
    model="gpt-4",
    max_tokens=500
)

# Create a Compare Task
#
# This task will run at the end of the workflow - and will compare all of the movies that are described as parents.
#
# Note: It's using Jinja2 templates to iterate through the descriptions.
#       {% for key, value in inputs.items() %} is the start. It will look at each of the parents
#       and print out the {{ value }} that is the description.
#       {% endfor %} is the end.

compare_task = PromptTask(
    """Tell me what's similar about the movies:
{% for key, value in inputs.items() %}
{{ value }}
{% endfor %}
""")

# For every movie in the list of movies:
#   * Create a PromptTask to get the name of the movie that's described
#   * Create a ToolkitTask to search the web for a description of the movie
#   * Create another PromptTask to summarize what was found on the web (sometimes there is a lot of extra stuff)
#
#   * Then, add the name_task PromptTask to the Workflow.
#   * Add the description_task ToolkitTask as a child to the name_task.
#   * Add the summarize_task PromptTask as a child to the description_task.
#   * Finally, add the compare_task as a child to the summarize_task.
#
# This will result in the compare_task being a child of _each_ of the summarize_tasks.

for movie in movies:

    # Use a PromptTask to get the name of the movie.
    name_task = PromptTask(
                    f"What is the name of the movie described: { movie }", 
                    driver=driver_4)
    
    # Use a ToolkitTask to search the web with the WebScraper tool for a description of the movie.
    # Note: We're passing a Jinja2 template to get the value of the incoming parent.
    # In this case, we know we only have 1 parent - so we can use the dict.values() method
    # and then the `list` filter. Adding `first` to the end gives us the first value, which
    # is all we need.
    #  
    description_task = ToolkitTask(
                    "Return a very short description of the movie: {{  inputs.values()|list|first }}", 
                    driver=driver_4, 
                    tools=[WebScraper()],
                    )
    
    # The website will often return extra data. So now we can create a short summary of that data
    # using another PromptTask.
    summarize_task = PromptTask(
                "Shortly summarize the movie description: {{ inputs.values()|list|first }}", 
                driver=driver_4, 
                )


    # Finally, we want to add these tasks to the workfow.
    workflow.add_task(name_task)
    name_task.add_child(description_task)
    description_task.add_child(summarize_task)

    # At the end of the chain, we'll add the summarize task.
    summarize_task.add_child(compare_task)

# Run the workflow
workflow.run()
