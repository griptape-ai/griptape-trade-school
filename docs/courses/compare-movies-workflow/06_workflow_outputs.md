# Workflow Outputs

## Overview
In the previous section we added a `ToolkitTask` that used the `WebScraper` and `TaskMemoryClient` tools to get detailed information about the movies presented.

In this section, we'll add the ability to get the `output` from the `workflow` in order to integrate it with whatever application we may be building.

``` mermaid
graph TB 
    subgraph " "
        direction TB
        A("PromptTask: Start"):::main 
        B("PromptTask: Movie Task 1")
        G("PromptTask: Movie Task <i>n</i>" ):::dash
        C("ToolkitTask: Summary Task 1"):::tool
        H("ToolkitTask: Summary Task <i>n</i>" ):::tool-dash
        I("PromptTask: End"):::main
        J(["\n  Incredible movie insights. \n\n"]):::output
        A --> B --> C --> I --> J
        A --> G --> H --> I
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
    classDef dash stroke-dasharray: 5 5
    classDef tool stroke:#f06090
    classDef tool-dash stroke:#f06090,stroke-dasharray: 5 5
    classDef output fill:#333,stroke:#555

```


## Workflow Output_Task

Looking at our current workflow, you can see that there's one last task - the `End` task. Ideally we can run the workflow and get the output of this last task.

**Every** task in Griptape has an attribute on it called `output_task`. If you took the Converational Chatbot course, you would have seen it when customizing the output of the agent.

We can use this `output_task` of the `workflow` to get the final output value.

```python
#...
# Run the workflow
workflow.run()     

print(workflow.output_task.output.value)

```


### Test

Execute the code and let's review the output.

```
While these movies - "E.T. the Extra-Terrestrial", "Jaws", 
and "The Princess Bride" - have different plots and settings, 
they share some common elements. All three films involve 
characters facing significant challenges and overcoming them. 
They also all involve elements of adventure and suspense. 
Additionally, they were all released in the 20th century and 
have become iconic films in American cinema.
```

---

## Code Review

In this final section we learned out to get the `output` from the `workflow` in order to be able to integrate this workflow into our application.

Review your code.

```python linenums="1" title="app.py" hl_lines="54-55"
from dotenv import load_dotenv

# Griptape
from griptape.structures import Workflow
from griptape.tasks import PromptTask, ToolkitTask
from griptape.tools import WebScraper, TaskMemoryClient

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
        tools=[WebScraper(), TaskMemoryClient(off_prompt=False)],
    )

    workflow.insert_tasks(start_task, [movie_task], end_task)
    workflow.insert_tasks(movie_task, [summary_task], end_task)

# Run the workflow
workflow.run()

# View the output
print(workflow.output_task.output.value)

```

---
## Next Step
But wait.. don't stop yet!

There's new bonus material we've recently added that helps you understand the structure of your workflow!

Head over to the next section: [Workflow Display Graphs](07_workflow_display_graph.md) to learn how to understand the structure of your graph while you create it.
