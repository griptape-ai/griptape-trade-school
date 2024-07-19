# First Workflow

## Overview
In this section we're going to create the first workflow in our Movie Comparison application. By the end of this section you will have a workflow that lets you create a cursory comparison between two movies.

For example, if you pass it these two descriptions:

* "A boy discovers an alien in his back yard"
* "A shark attacks a beach"

It will come back with:

!!! Example "Result"
    Both E.T. the Extra-Terrestrial and Jaws are directed by Steven Spielberg.    
    They are also both iconic films that have had a significant impact on popular culture.

The hierarchy we will create looks like the following:

``` mermaid
graph TB 
    subgraph " "
        direction TB
        B(Describe Workflow):::main --> C(Movie 1) --> E(Compare Task):::main
        B --> D(Movie 2) --> E
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
```



As you can see, there is a `Workflow` Structure, and four tasks that will be created. The **Start** and **End** tasks (Describe Workflow and Compare Task), and two siblings (Movie 1 and Movie 2). Compare Task will be dependent on them to complete before it can execute.

!!! tip
    Workflows must always have a **Start** and **End** task.

To generate this structure, we will first create our Start and End tasks, and then **insert** the movie tasks. This will guarantee that our tasks exist in the workflow exactly where we want them.
``` mermaid
flowchart TB 
    subgraph Step 2 ["Insert"]
        direction TB
        C(Describe Workflow):::main --> D(Movie 1) --> F(Compare Task):::main
        C --> E(Movie 2) --> F
    end

    subgraph Step 1 ["Start & End"]
        direction TB
        A(Describe Workflow):::main --> B(Compare Task):::main
    end

    classDef main fill:#4274ff1a, stroke:#426eff
```

Let's get started.

## Importing Required Modules

Before starting, we need to import the necessary modules. Open the `app.py` file you created in the [setup](01_setup.md) section and import the two Griptape classes you'll need: `Workflow` and `PromptTask`:

```python linenums="1" hl_lines="3-5"
from dotenv import load_dotenv

# Griptape
from griptape.structures import Workflow
from griptape.tasks import PromptTask

load_dotenv() # Load your environment

```

!!! Note
    You might recall that `Agent` was also imported through `griptape.structures`. That's because `Agent`, `Workflow`, and `Pipeline` are all Griptape's ways of working with LLMs. 

## Create Workflow Structure
### Initialize the Workflow

Now, let's create the foundation for our Workflow. After the line `load_dotenv()`, create an instance of the Workflow class:

```python hl_lines="4-5"
# ... truncated for brevity
load_dotenv() # Load your environment

# Create the workflow object
workflow = Workflow()
```

### Create a Start task

First, we'll create our "start" task. This will be a simple `PromptTask` that lets the LLM know what we're going to do. 

After the `workflow` line, add:
```python
# Create tasks
start_task = PromptTask("I will provide you a list of movies to compare.", id="START")
```

There are two things that are important to point out in this task creation.

1. Notice that we're using a `PromptTask`. That's because we don't need to use any tools for this particular task, we only want to use the LLM.
2. We have given the task an `id`. This is so we can reference it later in the script. If you don't pass this value, the task will be given a random string as the id.

!!! important
    Every task in a workflow must have a unique id. If two tasks have the same id, the workflow will fail.

### Add Task to the Workflow

You have created the task, but it's not yet part of the workflow. In order to do that, we'll need to use the `add_task` method.

After the PromptTask line, add:

```python
# Add tasks to workflow
workflow.add_task(start_task)
```

At this point, your workflow flow graph looks like:

``` mermaid
graph TB 
    subgraph " "
        direction TB
        B(PromptTask: START):::main
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
```


However if you execute your script, nothing will happen. That's because you need to tell the workflow graph to run.

### Run the Workflow

To run a workflow, you simply need to call the method `run`:

```python
# Run the workflow
workflow.run()
```

Here's the result. Notice in the logs you can see the Task inputs and outputs:
``` shell
[11/15/23 13:05:49] INFO     PromptTask START                                                                                   
                             Input: I will provide you a list of movies to compare.                                             
[11/15/23 13:05:52] INFO     PromptTask START                                                                                   
                             Output: Sure, please provide the list of movies you want me to compare.                            
```

As you can see, the LLM is ready to take a list of movies.

### Add the end task

The next task we'll add will be the last task. This is a good place to create a task that summarizes what has been done, and then add it to the end of the workflow using the same `add_task` method.

```python hl_lines="3 7"
# Create tasks
start_task = PromptTask("I will provide you a list of movies to compare.", id="START")
end_task = PromptTask("How are the movies the same?", id="END")

# Add tasks to workflow
workflow.add_task(start_task)
workflow.add_task(end_task)
```

``` mermaid
graph TB 
    subgraph " "
        direction TB
        B(PromptTask: START):::main --> C(PromptTask: END):::main
    end
    
    classDef main fill:#4274ff1a, stroke:#426eff
```

!!! tip
    This process has changed from versions of Griptape prior to v0.20.

    In previous versions, the `add_task` method would add tasks as **siblings** of the parent task. With versions greater than 0.20, they add them one after another. To add tasks as **siblings** you will be **inserting** tasks.

    ```python
    # Add tasks to workflow
    workflow.add_task(start_task)
    workflow.add_task(end_task)
    ```

    === "After Griptape 0.2.0"
        ``` mermaid
        graph TB 
            subgraph " "
                direction TB
                B(PromptTask: START):::main --> C(PromptTask: END):::main
            end
            
            classDef main fill:#4274ff1a, stroke:#426eff
        ```

    === "Before Griptape 0.2.0"
        ``` mermaid
        graph TB 
            subgraph " "
                direction TB
                B(PromptTask: START):::main
                C(PromptTask: END):::main
            end
            
            classDef main fill:#4274ff1a, stroke:#426eff
        ```

## Add Tasks into Workflow
### Create the first Movie Prompt task

Now it's time to create the first task asking the LLM to identify a movie. This will be a `PromptTask`.

In your code, after the `end_task`, add:

```python hl_lines="5-6"
# Create tasks
start_task = PromptTask("I will provide you a list of movies to compare.", id="START")
end_task = PromptTask("How are the movies the same?", id="END")

# Create movie tasks
movie_1_task = PromptTask("What movie is this: boy finds alien in backyard.", id="movie_1")
```

### Insert the Task into the Workflow

You have created the task, but it's not yet part of the workflow. In order to do that, we'll need to use the `insert_tasks` method.

The `insert_tasks` method takes a couple of arguments. It looks like this:
```python
workflow.insert_tasks(task_a, [task_c, task_d], task_b)
workflow.insert_tasks(task_c, [task_e, task_f], task_b)
```

Notice the second argument is a `list` of tasks. This method will take two tasks that already have a parent/child relationship, and *insert* whatever tasks are listed in that second argument between them. 

The graph above would look something like:

``` mermaid
graph TB 
    subgraph " "
        direction TB
        A(task_a)
        B(task_b)
        C(task_c)
        D(task_d)
        E(task_e)
        F(task_f)
        A --> B --> D
        A --> C --> E --> D
        C --> F --> D
    end
    
```

We'll see this in more detail shortly, but for now let's just add the single task.

In your script, after the `add_task` lines, add:

```python
# Add tasks to workflow
workflow.insert_tasks(start_task, [movie_1_task], end_task)
```

At this point, your workflow flow graph looks like:
    ``` mermaid
    graph TB 
        subgraph " "
            direction TB
            A(PromptTask: START):::main
            B(PromptTask: movie_1_task)
            C(PromptTask: END):::main
            A --> B --> C
        end
        
        classDef main fill:#4274ff1a, stroke:#426eff
    ```

### Run the Workflow

Run the script to see the output.

Here's the result. Notice the tasks being executed, and the summary where it tries to compare the results:

``` shell
[11/15/23 14:10:59] INFO     PromptTask START                                                                                   
                             Input: I will provide you a list of movies to compare.                                             
[11/15/23 14:11:00] INFO     PromptTask START                                                                                   
                             Output: Sure, please provide the list of movies you want me to compare.                            
                    INFO     PromptTask movie_1                                                                                 
                             Input: What movie is this: boy finds alien in backyard.                                            
[11/15/23 14:11:02] INFO     PromptTask movie_1                                                                                 
                             Output: The movie you are referring to is likely "E.T. the Extra-Terrestrial" directed by Steven    
                             Spielberg.                                                                                         
                    INFO     PromptTask END                                                                                     
                             Input: How are the movies the same?                                                                
[11/15/23 14:11:06] INFO     PromptTask END                                                                                     
                             Output: As an AI, I need specific movies to compare in order to provide similarities. Please       
                             provide the names of the movies you want to compare.                                               
```

The LLM is unable to compare the results for two reasons - first, we only passed a single movie. Second, we didn't pass the information about the movie back to the LLM so it doesn't know what we were talking about. We'll take care of these one at a time.

First, we'll add a second movie.

### Second Movie Task

Just below the first movie PromptTask, add a second one with another description.

```python hl_lines="5"
# ...

# Create tasks
movie_1_task = PromptTask("What movie is this: boy finds alien in backyard.", id="movie_1")
movie_2_task = PromptTask("What movie is this?: a shark attacks a beach.", id="movie_2")

# ...
```

!!! important
    Don't forget to add the id to the second task and make sure it's unique from the first task.

### Add Second Task to Workflow
Just like before, we need to *insert* `movie_2_task` to `workflow` with the `insert_tasks` method. Modify the previous insert_tasks line to include both movie tasks.

```python hl_lines="4"
# ...

# Add tasks to workflow
workflow.insert_tasks(start_task, [movie_1_task, movie_2_task], end_task)

# ...
```


### Test

Go ahead and run the code and notice that the two movie tasks executed in *parallel*:

```shell
# ... truncated for brevity

[11/15/23 14:14:32] INFO     PromptTask START                                                                                   
                             Input: I will provide you a list of movies to compare.                                             
[11/15/23 14:14:34] INFO     PromptTask START                                                                                   
                             Output: Sure, I am ready to help you compare the movies. Please provide the list.                   
                    INFO     PromptTask movie_2                                                                                 
                             Input: What movie is this?: a shark attacks a beach.                                               
                    INFO     PromptTask movie_1                                                                                 
                             Input: What movie is this: boy finds alien in backyard.                                            
[11/15/23 14:14:38] INFO     PromptTask movie_2                                                                                 
                             Output: This could refer to several movies as shark attacks are a common theme in many films.      
                             However, the most iconic one is "Jaws" directed by Steven Spielberg.                               
                    INFO     PromptTask movie_1                                                                                 
                             Output: This could refer to several movies, but the most famous one is probably "E.T. the          
                             Extra-Terrestrial" directed by Steven Spielberg.                                                   
                    INFO     PromptTask END                                                                                     
                             Input: How are the movies the same?                                                                
[11/15/23 14:14:41] INFO     PromptTask END                                                                                     
                             Output: As an AI, I need more specific details to provide a comparison. Please provide the names of
                             the movies you want to compare.                                                        
```

Hmm. It doesn't look like the `compare` task knows what we're talking about. The workflow evaluated both we sent it, we can see that in the logs above, but the compare task has no knowledge of them. 

That's because we need to *pass* the results of the previous task to the current task. This is a very important feature, as it allows us to be *very specific* about what data is sent to the LLM.

## Pass the Data

In order to send the data to the PromptTask, we need to somehow feed the result of the previous task's execution to the prompt.

### Jinja2
Griptape uses the [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/){target="_blank"} template engine, which allows you to insert data into the prompt. There's a lot of power available with Jinja templates, but in this course we'll keep our focus rather small.

Jinja templates access variables using the `{{ }}` syntax. **Tasks** have a property `parent_outputs` that tell us what objects are coming into the node.


### Update the Prompt
In order to update the prompt, we want to tell it what tasks to be looking at. If you check your code, you can see that we used the `id` property earlier when we were creating the tasks:

```python
movie_1_task = PromptTask("What movie is this?: A boy discovers an alien in his back yard", id="movie_1")
movie_2_task = PromptTask("What movie is this?: a shark attacks a beach.", id="movie_2")
```

So `movie_1` and `movie_2` are the two ids we can use in our Jinja template. They can be specified like this: `{{ parent_outputs['movie_1'] }}` and `{{ parent_outputs['movie_2'] }}`

Update the `END` task to specify the particular ids of the parent_outputs. Note - I'm using `"""` in order to allow us to use multiple lines for the PromptTask string.

```python
end_task = PromptTask("""
    How are these movies the same:
    {{ parent_outputs['movie_1'] }}
    {{ parent_outputs['movie_2'] }}
    """,
    id="END")

```

### Test

When you run the script now, you should see a much better Input:

```shell
[11/15/23 14:19:24] INFO     PromptTask END        
                             Input:                                                                                             
                                 How are these movies the same:                                                                 
                                 This could be referring to "E.T. the Extra-Terrestrial" directed by Steven Spielberg.          
                                 This could be referring to several movies as shark attacks are a common theme in films.        
                             However, the most iconic movie featuring a shark attack on a beach is "Jaws" directed by Steven    
                             Spielberg.                                                                                         
[11/15/23 14:19:26] INFO     PromptTask END
                             Output: These movies are the same in that they are both directed by Steven Spielberg.
```

The code works but it's if you look closely at the `END` task input, you'll see that it's using the full string of the response from the prompts:

``` shell
How are these movies the same:                                                    
That sounds like the movie "E.T. the Extra-Terrestrial".                          
That could be several movies, but the most famous one is probably "Jaws". 
```        

What we really want is just the name of the movie, not any commentary. We can fix that by adjusting the prompt in the initial query.

### Fix the Prompt
Change the movie PromptTasks so we ask for just the name:
``` python 
movie_1_task = PromptTask(
    "What movie is this? Return only the movie name: A boy discovers an alien in his back yard", 
    id="movie_1")
movie_2_task = PromptTask(
    "What movie is this? Return only the movie name: a shark attacks a beach.", 
    id="movie_2")
```

After running the response input task should be much cleaner:

```shell                              
How are these movies the same: 
E.T. the Extra-Terrestrial                  
Jaws   
```

---

## Code Review

We covered quite a lot of ground creating your first workflow. Double-check your script and make sure you've got it working as expected:

```python linenums="1" title="app.py"
--8<-- "docs/courses/compare-movies-workflow/assets/code_reviews/03/app.py"
```

## Next Step
In the next section we are going to make our script a bit more flexible by making it possible to compare as many movie descriptions as we want. Check out [Adding Flexibility](04_adding_flexibility.md) when you're ready to continue.
