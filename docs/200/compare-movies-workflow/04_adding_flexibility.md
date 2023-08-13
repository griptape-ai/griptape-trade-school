# Adding Flexibility

## Overview
In the previous section you created your first workflow. It works well for two movie descriptions, however if you want to expand to more movies it could be a bit difficult for a few reasons.

1. We're creating the tasks and adding them to the workflow one at a time.
2. In the comparison task we target the specific ids of the movie tasks.
3. We're repeating our prompt "What movie is this? Return only the name" over and over again.

So in this section, we'll make our application more flexible by defining a **list** of movie descriptions, and then **iterate** through that list to create PromptTasks and add them to the workflow.

## Movie Description List

Locate the section of your code where you create the list of movie tasks:
``` python
# ...

# Create tasks
movie_1_task = PromptTask(
    "What movie is this? Return only the movie name: A boy discovers an alien in his back yard", 
    id="movie_1")
movie_2_task = PromptTask(
    "What movie is this? Return only the movie name: a shark attacks a beach.", 
    id="movie_2")

# ...
```

We're going to replace this entire section with a `descriptions` list instead. This will be a list of python dictionaries with an "id" and a "descriptoin".

It should look something like:
``` python 
# Create a list of movie descriptions
movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "A shark attacks a beach"
]
```

## Iterate through list

Now to create our PromptTasks, we'll iterate through the list of movie_descriptions.

Locate the code after the `compare_task` where we add tasks to the workflow:

```python
# Add tasks to the workflow
workflow.add_task(movie_1_task)
workflow.add_task(movie_2_task)

# Add compare as a child
movie_1_task.add_child(compare_task)
movie_2_task.add_child(compare_task)

```

We will replace this with a for loop where we create the PromptTask and add it to the workflow.

```python
# ...

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }}",
        context = {
            "description": description
        })

    workflow.add_task(movie_task)

    # Add compare as a child
    movie_task.add_child(compare_task)

# ...
```

As you can see, we:

1. Iterate through each `description` in the list of `movie_descriptions`. 
2. Create a `PromptTask` and pass that `description` to the `context` into a variable also called `description`.
3. Use that variable via **Jinja2 templates** in the prompt itself: `{{ description }}`.
4. Once the `PromptTask` is created, we add it to the workflow using the `add_task` method.
5. Add `compare_task` as a child to the task using the `add_child` method.

## Update Compare Task

There's one final step we need to take before we can run this. In our `compare_task`, we're specifically identifying `movie_1` and `movie_2` in the prompt:

```python hl_lines="3-4"
compare_task = PromptTask("""
    How are these movies the same:
    {{inputs['movie_1']}}
    {{inputs['movie_2']}}
    """,
    id="compare")
```

This will no longer work because we are not defining the ids when we create the PromptTask - we just let it come up with it's own unique identifiers. Also, we don't know exactly how many movies we might be comparing, so it doesn't make much sense to define and add each one individually.

Luckily, intead of specifically specifying the items via id, we can just say "hey - give me all the input items" using `{{ inputs.items() }}`. This will return the entire `dict` of items that are input to the task.

Replace the two lines:

```python
    {{inputs['movie_1']}}
    {{inputs['movie_2']}}   
```

with:

```python
    {{ inputs.items() }}
```

The `compare_task` section should now look like:

```python hl_lines="3"
compare_task = PromptTask("""
    How are these movies the same:
    {{ inputs.items() }}
    """,
    id="compare")
```

### Test
Let's run the code and see what we get.

```shell
[08/13/23 10:08:28] INFO     Task compare                                                                                                                     
                             Input:                                                                                                                           
                                 How are these movies the same:                                                                                               
                                 dict_items([('60b7763430c24ca1bb0bffacb016f37f', 'E.T. the Extra-Terrestrial'), ('f6810857060e4b029ff66ff8a2f35be9',         
                             'Jaws')])                                                                                                                        
                                                                                                                                                              
[08/13/23 10:08:31] INFO     Task compare                                                                                                                     
                             Output: Both 'E.T. the Extra-Terrestrial' and 'Jaws' are iconic movies directed by Steven Spielberg. They are known for their    
                             memorable storylines and have had a significant impact on popular culture.                                                       

```

We get the proper output for our task - it compares ET and Jaws as we expect. But notice the input.

```shell
Input:                                                                                                                           
    How are these movies the same:                                                                                               
    dict_items([('60b7763430c24ca1bb0bffacb016f37f', 'E.T. the Extra-Terrestrial'), ('f6810857060e4b029ff66ff8a2f35be9',         
'Jaws')])                               
```

Instead of passing just the names of the movies, it's passing the entire dictionary of items. It *works* but it's messy. Don't worry, there's a way to clean this up using Jinja2 for loops.

## Iterate Through Items

Jinja2 has a for loop structure that looks like:
```
{% for item in list %}
{{ item }}
{% endfor %}
```

We can use this inside our PromptTask to iterate through the items and just output the names.

Replace the `{{ inputs.items }}` section of the `PromptTask` with a for loop that will get the key/value pairs (id, movie name) and output just the value.

```python hl_lines="5-7"
# ... 

compare_task = PromptTask("""
    How are these movies the same:
    {% for key, value in inputs.items() %}
    {{ value }}
    {% endfor %}
    """,
    id="compare")

# ...
```

### Test

Run the script again and let's see how it looks.

```shell
INFO     Task compare
            Input:
                How are these movies the same:
                E.T. the Extra-Terrestrial
                Jaws
```

Much better. Go ahead and add a third movie to the structure and run it again. Everything should work as expected. I added "A princess and a man named Wesley" (from the movie **The Princess Bride**) and got the following result:

!!! example "Result"
    All three movies, E.T. the Extra-Terrestrial, Jaws, and The Princess Bride, are iconic films    
    from the late 20th century. They all fall under the genre of adventure and have elements of fantasy.    
    Additionally, they have been highly influential in popular culture and have received critical acclaim.  

---

## Code Review

There was not as much work in this section, but we did conver some important concepts. 

* We made our code more flexible by using a list of descirptions to create PromptTasks instead of creating them one at a time.
* We used a Jinja2 template **for loop** to iterate through each incoming item.

Review your code with the current state to make sure everything is working as expected.

```python linenums="1" title="app.py" hl_lines="13-18 22-24 28-35"
from dotenv import load_dotenv

# Griptape 
from griptape.structures import Workflow
from griptape.tasks import PromptTask

# Load environment variables
load_dotenv()

# Create a Workflow
workflow = Workflow()

# Create a list of movie descriptions
movie_descriptions = [
    "A boy discovers an alien in his back yard",
    "A shark attacks a beach",
    "A princess and a man named Wesley"
]

compare_task = PromptTask("""
    How are these movies the same:
    {% for key, value in inputs.items()%}
    {{ value }}
    {% endfor %}
    """,
    id="compare")

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }} ",
        context={"description": description})
    workflow.add_task(movie_task)

    movie_task.add_child(compare_task)

# Run the workflow
workflow.run()

```

## Next Step
Our code works, but the descriptions of the movies aren't as detailed as they could be. It would be better if we could search the web for detailed information about the movies, and use those results for a more comprehensive comparison.

In the next section we will add to our workflow by adding a ToolkitTask that uses the `WebScraper` tool to get more detailed information. Jump to [Using Tools](05_using_tools.md) when you're ready to continue.