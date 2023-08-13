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


# Define the OpenAiPromptDriver with Max Tokens
driver = OpenAiPromptDriver(
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
    {% for key, value in inputs.items() %}
    {{ value }}
    {% endfor %}
    """,
    driver=driver,
    id="compare")

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }} ",
        context={"description": description},
        driver=driver
        )
    
    summary_task = ToolkitTask(
        """
        Give me a very short summary of the movie from imdb:
        {% for key, value in inputs.items() %}
        {{ value }}
        {% endfor %}
        """,
        tools=[WebScraper()],
        driver=driver
        )
    
    workflow.add_task(movie_task)
    movie_task.add_child(summary_task)
    summary_task.add_child(compare_task)

# Run the workflow
workflow.run()

# View the output
for task in workflow.output_tasks():
    print(task.output.value)    

