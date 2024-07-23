# Using Tools

## Overview
We added flexibility in the last section to allow our application to handle an undefined number of movies. The workflow hierarchy looks like:


``` mermaid
graph TB 
    subgraph " "
        direction TB
        A("PromptTask: Start"):::main 
        B("PromptTask: Movie Task 1")
        G("PromptTask: Movie Task <i>n</i>" ):::dash
        I("PromptTask: End"):::main
        A --> B --> I
        A --> G --> I
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
    classDef dash stroke-dasharray: 5 5
    classDef tool stroke:#f06090

```

However, the comparisons coming back don't feel very deep and meaningful. We'd like to get a more detailed analysis of the film comparisons by getting a better summary of each film from the web. 

To do that we'll use add a `ToolkitTask` to our workflow for each movie. This will result in the following chart.

``` mermaid
graph TB 
    subgraph " "
        direction TB
        A("PromptTask: Start"):::main 
        B("PromptTask: Movie Task 1")
        C("ToolkitTask: Summary Task 1"):::tool
        G("PromptTask: Movie Task <i>n</i>" ):::dash
        H("ToolkitTask: Summary Task <i>n</i>" ):::tool-dash
        I("PromptTask: End"):::main
        A --> B --> C --> I
        A --> G --> H --> I
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
    classDef dash stroke-dasharray: 5 5
    classDef tool stroke:#f06090
    classDef tool-dash stroke:#f06090,stroke-dasharray: 5 5
```


## Import

The three new classes we'll need to import are `ToolkitTask`, `TaskMemoryClient`, and `WebScraper`.


**[ToolkitTask](https://docs.griptape.ai/stable/griptape-framework/structures/tasks/#toolkit-task){target="_blank"}** is a task just like **PromptTask**, except it allows you to specify the use of Tools. 

**[TaskMemoryClient](https://docs.griptape.ai/stable/griptape-framework/structures/task-memory/){target="_blank"}** is a way to handle data used in a task. It allows you to control where information is sent, keeping it off-prompt and away from the LLM when required. Note: in this course we'll be setting `off-prompt` to `False`, allowing the LLM to see the task results. In future courses we'll discuss ways to keep the data private.

**[WebScraper](https://docs.griptape.ai/stable/griptape-tools/official-tools/web-scraper/){target="_blank"}** is a specific tool that allows the LLM to scrape the web for information. We'll use this to get a better summary of each movie.

In the top of your application, modify the import statements to include ToolkitTask, TaskMemoryClient, and WebScraper.

```python hl_lines="5-6"
from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask, ToolkitTask
from griptape.tools import WebScraper, TaskMemoryClient

```

## Summary ToolkitTask 

Now we'll add the `ToolkitTask` to the section of our code where we iterate through each movie description.

We will call it the same way we do PromptTask, except the ToolkitTask takes a **list** of **tools**. In this example, you can see that it's using two tools - **WebScraper** and **TaskMemoryClient**

```python
summary_task = ToolkitTask(
    "Use metacritic to get a summary of this movie: {{ }}", 
    tools = [WebScraper(), TaskMemoryClient(off_prompt=False)],
    )
```

When we call the `ToolkitTask` we'll need to pass the output of the previous task (the movie_task) to it. There are a few options we can use to do this, depending on the needs of our application.

### Option 1: All Incoming Items
If you recall from the [previous section](04_adding_flexibility.md), using the Jinja Template `{{ parent_outputs }}` will give you a list of dicts from *all incoming tasks*. 
    
Example: 
``` python
    "Use metacritic to get a summary of this movie: {{ parent_outputs }}"
```

In this case, the return would look something like:
```
Input: Get a summary of the movie: {'4aca083cdc5a4b76bb7ee7b91f0ec358': 'The Princess Bride'}                                                                       
```

While this works, it does provide some extraneous information. We know that there is only one item coming in - so it's not necessary to use this list of dicts. Jinja2 provides filters to reduce this.

### Option 2: Filter for One Item

Jinja2 allows you to use filters to return specific information. The format with Jinja2 is to use a `|` notation to add a filter.

For example, we can use `{{ parent_outputs.values() | list }}`to return a `list` of values, and then also get just the `last` item in the list. That would look like: `{{ parent_outputs.values()|list|last }}`:

```python
    "Use metacritic to get a summary of this movie: {{ parent_outputs.values()|list|last }}"
```

And the result would be:

```shell
Input: Get a summary of the movie: The Princess Bride                      
```

### Compare all options

As you can see, there are multiple ways to get the result we're looking for. Review the options below to see how they are unique. 

=== "All Items"
    ```python
    # code
    summary_task = ToolkitTask(
        "Use metacritic to get a summary of this movie: {{ parent_outputs }}",
        tools=[WebScraper(), TaskMemoryClient(off_prompt=False)],
        )

    # result
    {'4aca083cdc5a4b76bb7ee7b91f0ec358': 'The Princess Bride'} 
    ```
=== "Filter For One"
    ```python
    # code
    summary_task = ToolkitTask(
        "Use metacritic to get a summary of this movie: {{ parent_outputs.values()|list|last }}",
        tools=[WebScraper(), TaskMemoryClient(off_prompt=False)],
        )

    # result
    The Princess Bride
    ```

As you can see, Jinja filters are extremely powerful. Let's use the second option as it gives us exactly the result we are looking for: just the name of the movie.

### Add ToolkitTask

Inside the `for description in movie_descriptions:` loop, add the `summary_task` *after* the `movie_task` but *before* the call to the `insert_tasks` method of `workflow.`

```python linenums="1" hl_lines="9-12"
# ...

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }} ",
        context={"description": description})
    
    summary_task = ToolkitTask(
        "Use metacritic to get a summary of this movie: {{ parent_outputs.values()|list|last  }}",
        tools=[WebScraper(), TaskMemoryClient(off_prompt=False)],
        )
    
    workflow.insert_tasks(start_task, [movie_task], end_task)

# ...
```

## Insert Summary Task

At the moment we've created the Summary Task for each movie, but we haven't inserted them into the workflow.

``` mermaid
graph TB 
    subgraph " "
        direction TB
        C("ToolkitTask: Summary Task 1"):::tool
        H("ToolkitTask: Summary Task <i>n</i>" ):::tool-dash
        A("PromptTask: Start"):::main 
        B("PromptTask: Movie Task 1")
        G("PromptTask: Movie Task <i>n</i>" ):::dash
        I("PromptTask: End"):::main
        A --> B --> I
        A --> G --> I
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
    classDef dash stroke-dasharray: 5 5
    classDef tool stroke:#f06090
    classDef tool-dash stroke:#f06090,stroke-dasharray: 5 5
```

To insert them, we'll need to use another `insert_tasks` method call, this time telling it to insert between the `movie_task` and the `end_task`.

Inside the `movie_description` for loop, after `workflow.insert_tasks(start_task, [movie_task], end_task)`
modify the code to look like:

```python hl_lines="7"
# ...

# Iterate through the movie descriptions
for description in movie_descriptions:
    # ...
    workflow.insert_tasks(start_task, [movie_task], end_task)
    workflow.insert_tasks(movie_task, [summary_task], end_task)

# ...
```

Now the workflow graph looks like we expect:

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
        A --> B --> C --> I
        A --> G --> H --> I
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
    classDef dash stroke-dasharray: 5 5
    classDef tool stroke:#f06090
    classDef tool-dash stroke:#f06090,stroke-dasharray: 5 5
```



## Test

Execute the code and let's review the output logs.

!!! note
    I've removed the timestamps from the logs to make it easier to read. Yours will most likely still have them.

```bash
INFO Task END                                  
    Input:                                                                                                  
        How are these movies the same:                                                                      
        The movie "E.T. the Extra-Terrestrial" is about a troubled child who summons the courage to help a  
    friendly alien escape from Earth and return to his home planet.                                         
        "Jaws" is a movie about a killer shark that unleashes chaos on a beach community off Cape Cod. It's 
    up to a local sheriff, a marine biologist, and an old seafarer to hunt the beast down. The shark        
    terrorizes the community, affecting the number of tourists that usually flock to the island. After many 
    attempts, the shark won't go away, leading the sheriff, the marine biologist, and the seafarer to decide
    to go after the shark and kill it.                                                                      
        The movie "The Princess Bride" is about a bedridden boy's grandfather who reads him the story of a  
    farmboy-turned-pirate. This farmboy encounters numerous obstacles, enemies, and allies in his quest to  
    be reunited with his true love. The movie is known for its satirical humor, great dialogue, and fun     
    adventure scenes. It is whimsical and romantic while also poking fun at the conventions of the fairy    
    tale genre. 

INFO Task END                                  
    Output: While these three movies, "E.T. the Extra-Terrestrial", "Jaws", and "The Princess Bride", seem  
    very different in terms of plot and genre, they do share some similarities. All three films involve a   
    central conflict that requires the main characters to overcome significant challenges. In "E.T.", the   
    child must help the alien return home, in "Jaws", the characters must hunt down a dangerous shark, and  
    in "The Princess Bride", the farmboy-turned-pirate must overcome obstacles to reunite with his love.    
    Each movie also explores themes of courage, friendship, and determination. Furthermore, they are all    
    iconic films that have left a significant impact on popular culture.                                    

```

As you can see, the `END` task has a lot more detail in it now. We're getting great summaries of the films, and therefore the output is even more detailed and valuable.

!!! info "Experiment"
    You could enhance this output by providing more detail to the prompt compare prompt. For example, instead of just asking how they're the same, some options:

    * "Act as a movie critic. Why are these movies relevant to society?"
    * "Act as a film studies professor. What are common themes in these movies?"

!!! tip "Hot Tip"
    Instead of modifying the prompt, try using **Rules** and **Rulesets** to give your workflow more specific behavior.

    You can learn about Rulesets in the [Multi Persona Chatbot](../chatbot-rulesets/index.md) course. 

---

## Code Review

We added some of helpful functionality in this section, mainly getting wonderful descriptions of these films from the web by using the `WebScraper` tool and `ToolkitTasks`.

Review your code.

```python linenums="1" title="app.py"
--8<-- "docs/courses/compare-movies-workflow/assets/code_reviews/05/app.py"
```

## Next Step
Congratulations, we've got a working movie comparison application! We can add a list of movies to compare, and the result is a detailed comparison that provides valuable insight as to how these movies can impact society.

However, we're currently only viewing the results in the **logs**. If we want to use this data inside an application, we need to get the **output** of the workflow.

In the next section, we'll learn how Workflows handle the output of their tasks and grab just the value of the summary task. Saunter over to [Workflow Outputs](06_workflow_outputs.md) when you're ready.
