# Workflow Outputs

## Overview
In the previous section we added a `ToolkitTask` that used the `WebScraper` tool to get detailed information about the movies presented.

In this section, we'll add the ability to get the `output` from the `workflow` in order to integrate it with whatever application we may be building.

``` mermaid
graph TB
    A(Movie Descriptions) --> B("PromptTask: Movie Task 1") --> C("ToolkitTask: Summary Task 1"):::tool --> I("PromptTask: Compare")
    A --> G("PromptTask: Movie Task <i>n</i>" ):::dash  --> H("ToolkitTask: Summary Task <i>n</i>"):::tool-dash
    H --> I
    I --> J(["\n  Incredible movie insights. \n\n"]):::output
    classDef dash stroke-dasharray: 5 5
    classDef tool stroke:#f06090
    classDef tool-dash stroke:#f06090,stroke-dasharray: 5 5
    classDef output fill:#5552,stroke:#555

```

## Workflow Output_Tasks

If you look at our current workflow in detail, you will notice that it has a *single* node that has no children - the `Compare` node.

Whenever our workflow runs, that final node is the last one that will evaluate. However, this isn't always necessarily the case. Imagine a situation where you have  *multiple* final tasks. For example - Saving multiple versions of these summaries to disk, or saving the state of an evaluation. You may have *multiple* tasks with no children.

``` mermaid
graph TB
    A(Movie Descriptions) 
    B("PromptTask: Movie Task 1")
    C("ToolkitTask: Summary Task 1"):::tool
    I("PromptTask: Compare")
    G("PromptTask: Movie Task <i>n</i>" ):::dash
    H("ToolkitTask: Summary Task <i>n</i>"):::tool-dash
    J(["\n  Incredible movie insights. \n\n"]):::output
    K("ToolkitTask: Save Summary"):::tool
    L("ToolkitTask: Save Summary <i>n</i>"):::tool-dash

    A --> B --> C 
    C --> K
    C --> I
    A --> G --> H --> I
    H --> L
    I --> J

    classDef dash stroke-dasharray: 5 5
    classDef tool stroke:#f06090
    classDef tool-dash stroke:#f06090,stroke-dasharray: 5 5
    classDef output fill:#5552,stroke:#555

```

In this case you would have at least 3 nodes that "finish" the workflow.

Luckily, the `workflow` class has an `output_tasks` method that will return all the output tasks of your workflow.

### List Output Task
To get a list of output tasks that are available on a workflow, you can simply do:

```python
tasks = workflow.output_tasks()
```

For example, if we want to print the `id` and see the `prompt_template` of the output tasks of our workflow, you can comment out the `workflow.run()` call so it doesn't execute, and then iterate through the output_tasks printing the `id` and `prompt_template`.

```python
# ...

# Run the workflow
# workflow.run()            <-- Commented out

for task in workflow.output_tasks():
    print(f"id: {task.id}")
    print(f"prompt_template: {task.prompt_template}")

```

Execute this and you should see the id and template of the final task.

!!! note
    When you execute this code you are not running the workflow, you're just getting information about each node.

```text
id: compare
prompt_template: 
    How are these movies the same: 
    {% for key, value in inputs.items() %}
    {{ value }}
    {% endfor %}
```

### Workflow Attributes

To see what other attributes are available on the workflow, go ahead and use the `dir` function.

```python
# use dir() to get all the attributes of the task.
# note: we're using workflow.output_tasks()[0] to just reference the 
# first output_task.
print (dir(workflow.output_tasks()[0]))

```

The result:
```text
['DEFAULT_PROMPT_TEMPLATE', 'State', '__abstractmethods__', '__annotations__', '__attrs_attrs__', '__attrs_own_setattr__', 
'__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
'__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lshift__', '__lt__',
'__match_args__', '__module__', '__ne__', '__new__','__reduce__', '__reduce_ex__', '__repr__',
'__rshift__', '__setattr__', '__setstate__', '__sizeof__', '__slots__', '__str__',
'__subclasshook__', '__weakref__', '_abc_impl', 'active_driver', 'add_child', 'add_parent', 'after_run',
'before_run', 'can_execute', 'child_ids', 'children', 'context', 'driver', 'execute', 'full_context', 'id', 
'input', 'is_executing', 'is_finished', 'is_pending', 'output', 'parent_ids', 'parents', 'prompt_stack', 
'prompt_template', 'render', 'reset', 'run', 'state', 'structure']
```

Notice that this includes all the "special" attributes (also known as `dunder`) and methods. We can filter those out by using list comprehension.

```python
filtered_attributes = [attr for attr in dir(workflow.output_tasks()[0]) if not (attr.startswith('__') and attr.endswith('__'))]

print(filtered_attributes)
```

This will give us a much nicer group of attributes to work with:

```text
['DEFAULT_PROMPT_TEMPLATE', 'State', '_abc_impl', 'active_driver', 'add_child', 'add_parent', 'after_run', 
'before_run', 'can_execute', 'child_ids', 'children', 'context', 'driver', 'execute', 'full_context', 'id', 
'input', 'is_executing', 'is_finished', 'is_pending', 'output', 'parent_ids', 'parents', 'prompt_stack', 
'prompt_template', 'render', 'reset', 'run', 'state', 'structure']
```

There are a number of interesting attributes in there for you to check out, but the one we care about in this case is going to be `output`.

### Output Value

To print the `output.value` we can do the following:

```python

# Run the workflow
workflow.run()          # <-- re-enabled so the workflow will run

for task in workflow.output_tasks():
    print(task.output.value)    

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

I this final section we learned out to get the `output` from the `workflow` in order to be able to integrate this workflow into our application.

Review your code.

```python linenums="1" title="app.py" hl_lines="64-66"
from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask, ToolkitTask
from griptape.tools import WebScraper
from griptape.drivers import OpenAiPromptDriver


# Load environment variables
load_dotenv()

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

```

## Finished

!!! success
    Congratulations! You have created a successful Griptape Workflow!

Well done, you've successfully created a Griptape Workflow that allows you to execute complex and interesting dependency graphs.

You have learned how to:

* Create tasks that can handle prompts and tools
* Learned a bit about Jinja2 templates
* Create parent/child relationships
* Create tasks that are depending on multiple incoming tasks
* Get the output from a workflow for integration with other applications.

We hope you enjoyed this course, and look forward to seeing what you're able to create with these new skills.
