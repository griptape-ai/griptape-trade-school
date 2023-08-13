# First Workflow

## Overview
In this section we're going to create the first workflow in our Movie Comparison application. By the end of this section you will have a workflow that lets you create a cursury comparision between two movies.

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
    A[Workflow] --> B(Movie 1) --> D(Compare Task)
    A --> C(Movie 2) --> D

```

As you can see, there are three tasks that will be created. Two will be siblings (Movie 1 and Movie 2), and one will be dependent on them to complete before it can execute (Compare Task).

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

## First Workflow Tasks
### Initialize the Workflow

Now, let's create the foundation for our Workflow. After the line `load_dotenv()`, create an instance of the Workflow class:

```python hl_lines="4-5"
# ... truncated for brevity
load_dotenv() # Load your environment

# Create the workflow object
workflow = Workflow()
```

### Create a Task

Next, let's create our first `PromptTask`. This task will be used to simply ask to the LLM to tell us what movie we're talking about.

After the `workflow` line, add:

```python
# Create tasks
movie_1_task = PromptTask("What movie is this: boy finds alien in backyard.", id="movie_1")
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
workflow.add_task(movie_1_task)
```

At this point, your workflow flow graph looks like:

``` mermaid
graph TB
    A[workflow] --> B(PromptTask: movie_1_task)
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
[08/12/23 19:53:08] INFO     Task movie_1                                                                          
                             Input: What movie is this?: A boy discovers an alien in his back yard                 
[08/12/23 19:53:10] INFO     Task movie_1                                                                          
                             Output: That sounds like the movie "E.T. the Extra-Terrestrial".                      
```

As you can see, the LLM was able to determine what movie it was.

## Another Task

This is still a very linear pipeline. In fact, there's only one task in the workflow. Let's go ahead and add our second task.

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
Just like before, we need to add `movie_2_task` to `workflow` with the `add_task` method.

```python hl_lines="5"
# ...

# Add tasks to workflow
workflow.add_task(movie_1_task)
workflow.add_task(movie_2_task)

# ...
```
This adds the task as a **sibling** of the first task, because we added it to the `workflow` object.

You can see this in the resulting graph:
``` mermaid
graph TB
    A[workflow] --> B(PromptTask: movie_1_task)
    A --> C(PromptTask: movie_2_task)
```

And if we run the script, you'll see both tasks being executed *in parallel*, and both outputs.

```shell
[08/12/23 20:03:14] INFO     Task movie_1                                                                          
                             Input: What movie is this?: A boy discovers an alien in his back yard                 
                    INFO     Task movie_2                                                                          
                             Input: What movie is this?: a shark attacks a beach.                                  
[08/12/23 20:03:16] INFO     Task movie_1                                                                          
                             Output: That sounds like the movie "E.T. the Extra-Terrestrial".                      
                    INFO     Task movie_2                                                                          
                             Output: That could be several movies, but the most famous one is probably "Jaws".  
```
## Comparison

You'll remember that our goal in this section is to get a simple comparison of the two movies. In order to do this we'll need to create another task where we ask the LLM to compare the results of the previous tasks.

### Comparison Task

After the previous movie PromptTasks, create a compare task.

``` python hl_lines="6"
# ...

movie_1_task = PromptTask("What movie is this?: A boy discovers an alien in his back yard", id="movie_1")
movie_2_task = PromptTask("What movie is this?: a shark attacks a beach.", id="movie_2")

compare_task = PromptTask("How are these movies the same?", id="compare")

# ...
```
### Make the Compare Task a Child

Now we get to create our first child task. We want the Compare task to only evaluate *after* the two movie tasks have completed.

This can be done by using the `add_child` method with the task you want to be the `parent`.

After the `workflow.add_task` lines, add the following:

```python
movie_1_task.add_child(compare_task)
```
This adds the `compare` task as a child to *only* the `movie_1` task. This is what the graph looks like:

``` mermaid
graph TB
    A[workflow] --> B(PromptTask: movie_1_task)
    A --> C(PromptTask: movie_2_task)
    B --> D(PromptTask: compare_task)
```

This obviously isn't what we want, we want *both* movie tasks to be the parent of the compare task. Luckily, that's easily accomplished by by just adding another `add_child` line. Here's what that section of code should look like:

```python hl_lines="9"
# ...

# Add tasks to the workflow
workflow.add_task(movie_1_task)
workflow.add_task(movie_2_task)

# Add compare as a child
movie_1_task.add_child(compare_task)
movie_2_task.add_child(compare_task)

# ...
```

And the resulting graph:

``` mermaid
graph TB
    A[workflow] --> B(PromptTask: movie_1_task)
    A --> C(PromptTask: movie_2_task)
    B --> D(PromptTask: compare_task)
    C --> D
```

### Test

Go ahead and run the code and notice the result:

```shell
# ... truncated for brevity

[08/12/23 20:54:56] INFO     Task compare                                                 
                             Output: To provide an accurate response, could you please specify which movies you are
                             referring to?            
```

Hmm. It doesn't look like the `compare` task knows what we're talking about. The workflow evaluated both we sent it, we can see that in the logs above, but the compare task has no knowledge of them. 

That's because we need to *pass* the results of the previous task to the current task. This is a very important feature, as it allows us to be *very specific* about what data is sent to the LLM.

## Pass the Data

In order to send the data to the PromptTask, we need to somehow feed the result of the previous task's execution to the prompt.

### Jinja2
Griptape uses the [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) template engine, which allows you to insert data into the prompt. There's a lot of power available with Jinja templates, but in this course we'll keep our focus rather small.

Jinja templates access variables using the `{{ }}` syntax. **Tasks** have a property `inputs` that tell us what objects are coming into the node.

!!! note
    The `inputs` property may be changing shortly to `parent_output`. This document will be updated when that happens.

### Update the Prompt
In order to update the prompt, we want to tell it what tasks to be looking at. If you check your code, you can see that we used the `id` property earlier when we were creating the tasks:

```python
movie_1_task = PromptTask("What movie is this?: A boy discovers an alien in his back yard", id="movie_1")
movie_2_task = PromptTask("What movie is this?: a shark attacks a beach.", id="movie_2")
```

So `movie_1` and `movie_2` are the two ids we can use in our Jinja template. They can be specified like this: `{{ inputs['movie_1'] }}` and `{{ inputs['movie_2'] }}`

Update the `compare` task to specify the particular ids of the inputs. Note - I'm using `"""` in order to allow us to use multiple lines for the PromptTask string.

```python
compare_task = PromptTask("""
    How are these movies the same:
    {{ inputs['movie_1'] }}
    {{ inputs['movie_2'] }}
    """,
    id="compare")

```

### Test

When you run the script now, you should see a much better Input:

```shell
[08/12/23 21:34:59] INFO     Task compare                                                                          
                             Input:                                                                                
                                 How are these movies the same:                                                    
                                 That sounds like the movie "E.T. the Extra-Terrestrial".                          
                                 That could be several movies, but the most famous one is probably "Jaws".         
                                                                                                                   
[08/12/23 21:35:02] INFO     Task compare                                                                          
                             Output: Both "E.T. the Extra-Terrestrial" and "Jaws" are iconic films directed by     
                             Steven Spielberg. They are known for their memorable storylines, groundbreaking       
                             special effects for their time, and their significant impact on popular culture.  
```

The code works but it's if you look closely at the `compare` task input, you'll see that it's using the full string of the response from the prompts:

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
    id="movie_1")
movie_2_task = PromptTask(
    "What movie is this? Return only the movie name: a shark attacks a beach.", 
    id="movie_2")

compare_task = PromptTask("""
    How are these movies the same:
    {{inputs['movie_1']}}
    {{inputs['movie_2']}}
    """,
    id="compare")

# Add tasks to the workflow
workflow.add_task(movie_1_task)
workflow.add_task(movie_2_task)

# Add compare as a child
movie_1_task.add_child(compare_task)
movie_2_task.add_child(compare_task)

# Run the workflow
workflow.run()

```

## Next Step
In the next section we are going to make our script a bit more flexible by making it possible to compare as many movie descriptions as we want. Check out [Adding Flexibility](04_adding_flexibility.md) when you're ready to continue.