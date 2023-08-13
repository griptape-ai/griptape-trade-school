# Main Concepts

## Understanding Workflows and Pipelines

Frequently when creating applications you will want to execute a series of steps in a very specific order. Workflows and Pipelines are both structures that allow us to do that. They have many of the same features as Agents, but are more directable. Whereas Agents can be given behaviors and tools and will use them when prompted appropriately, Pipelines and Workflows utilize hieararchies of tasks in very specific ways.

### Pipelines
[Pipelines](https://docs.griptape.ai/en/latest/griptape-framework/structures/pipelines/) are always a sequential series of steps - one task after another until it is finished. They have a **single output**, and just like [Agents](https://docs.griptape.ai/en/latest/griptape-framework/structures/agents/), they can use [Memory](https://docs.griptape.ai/en/latest/griptape-framework/structures/conversation-memory/).

In this course we're going to be taking some rough descriptions of movies and getting their actual names, then getting the summaries from the web and comparing them. Doing this as a **Pipeline** might look something like:

1. Get movie descriptions
3. Get the actual name of the movie
4. Look up the summary 

The flow of tasks would be:
``` mermaid
graph LR
    A(Movie Description) --> C(Get Name ) --> D(Get Summary)
```

This works great for our simple task, but the point of this course is to compare *multiple* movies. If we use a standard linear pipeline, it would mean:

``` mermaid
graph LR
    A(Movie Descriptions) --> B(Get Name 1) --> D(Get Summary 1) --> E(Get Name 2) 
    E --> F(Get Summary 2) --> G("Get Name <i>n</i>" ):::dash --> H("Get Summary <i>n</i>"):::dash 
    H --> I(Compare)
    
    classDef dash stroke-dasharray: 5 5

```

As you can tell, this could get quite unweildy. In addition, it doesn't make much sense for getting the name of the 4th movie to have to wait until the summary of the 3rd movie is figured out, as they're not really dependent on each other.

Workflows are perfect for this sort of situation. They allow you to parallelize tasks that aren't dependent. Let's see how something like this might look.

### Workflows
[Workflows](https://docs.griptape.ai/en/latest/griptape-framework/structures/workflows/) allow for complex interactions, resembling tree branches.

Workflows are **non-sequential** and can contain **multiple outputs**. Because their flows can be quite complicated, they don't contain ConversationalMemory.

This is what a Workflow might look like for doing what we mentiond above. 
!!! Note
    The graph is drawn top to bottom for this example because it's easier to understand the flow of data, but it can be drawn in either direction.

``` mermaid
graph TB
    A(Movie Descriptions) --> B(Get Name 1) --> D(Get Summary 1) --> I(Compare)
    A --> E(Get Name 2) --> F(Get Summary 2) --> I
    A --> G("Get Name <i>n</i>" ):::dash
    G --> H("Get Summary <i>n</i>"):::dash 
    H --> I
    classDef dash stroke-dasharray: 5 5

```

Notice how the movies can be evaluated in parallel, but the **Compare** task will wait until all it's **parent** tasks are completed. 

## Tasks

Before we dive in and start setting up our own workflow, it's important to review the concepts of Tasks. With Griptape, there are two types of tasks you'll be working with:

* **PromptTask**
* **ToolkitTask**

Both of these task types are used to work with the LLM. They both take an input as a prompt, can take arguments, use specific drivers, and have parent/child relationships.
The main difference between them is that **ToolkitTasks** can also use **tools** like Calculator(), FileBrowser(), and more. View all the tools available with Griptape [here](https://docs.griptape.ai/en/latest/griptape-tools/).

```python
# Example PromptTask to get a movie name
#
movie_task = PromptTask(
    "What is this movie: {{ descr }}",
    context = {                        
        "descr": "princess and farmhand named Wesley" 
    },
    id="movie_id"                      # task id can be referenced by other tasks
)

# This ToolkitTask works with the output of the previous task, and can use tools.
#
describe_task = ToolkitTask(
    "Get the description of this movie: {{ inputs['movie_id'] }}",       
    tools = [                          
        WebScraper()
    ],
    id='describe_id')
```

I have found that the best way to really understand how PromptTasks and ToolkitTasks work is to use them in context. So let's move on to the next section where we'll create our [First Workflow](03_first_workflow.md), and get an understanding of the basics of how parent/child relationships can work.
