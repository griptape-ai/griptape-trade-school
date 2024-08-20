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

# Create movie tasks
movie_1_task = PromptTask(
    "What movie is this? Return only the movie name: A boy discovers an alien in his back yard", 
    id="movie_1")
movie_2_task = PromptTask(
    "What movie is this? Return only the movie name: a shark attacks a beach.", 
    id="movie_2")

# ...
```

We're going to replace this entire section with a `descriptions` list instead. This will be a list of python dictionaries with an "id" and a "description".

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

Locate the `insert_task` code where we inserted the tasks into the workflow:

```python
# Add tasks to workflow
workflow.insert_tasks(start_task, [movie_1_task, movie_2_task], end_task)

```

We will replace this with a for loop where we create the PromptTask then insert it.

```python
# ...

# Iterate through the movie descriptions
for description in movie_descriptions:
    movie_task = PromptTask(
        "What movie title is this? Return only the movie name: {{ description }}",
        context = {
            "description": description
        })

    workflow.insert_tasks(start_task, [movie_task], end_task)

# ...
```

As you can see, we:

1. Iterate through each `description` in the list of `movie_descriptions`. 
2. Create a `PromptTask` and pass that `description` to the `context` into a variable also called `description`.
3. Use that variable via **Jinja2 templates** in the prompt itself: `{{ description }}`.
4. Once the `PromptTask` is created, we insert it to the workflow using the `insert_tasks` method.

## Update End Task

There's one final step we need to take before we can run this. In our `end_task`, we're specifically identifying `movie_1` and `movie_2` in the prompt:

```python hl_lines="3-4"
end_task = PromptTask("""
    How are these movies the same:
    {{parent_outputs['movie_1']}}
    {{parent_outputs['movie_2']}}
    """,
    id="compare")
```

This will no longer work because we are not defining the ids when we create the PromptTask - we just let it come up with it's own unique identifiers. Also, we don't know exactly how many movies we might be comparing, so it doesn't make much sense to define and add each one individually.

Luckily, instead of specifically specifying the items via id, we can just say "hey - give me all the input items" using `{{ parent_outputs }}`. This will return the entire `python dictionary` of items that are input to the task.

Replace the two lines:

```python
    {{parent_outputs['movie_1']}}
    {{parent_outputs['movie_2']}}   
```

with:

```python
    {{ parent_outputs }}
```

The `end_task` section should now look like:

```python hl_lines="3"
end_task = PromptTask("""
    How are these movies the same:
    {{ parent_outputs }}
    """,
    id="END")
```

### Test
Let's run the code and see what we get.

```shell
[08/13/23 10:08:28] INFO     Task END                                                                                                                     
                             Input:                                                               
                                 How are these movies the same:{'74bd46cfd17a4ccaa92308029b508751': 'E.T. the                  
                             Extra-Terrestrial', '90ed4594b9af4ad9ac2fe45cd53c7889': 'Jaws'}                                                             

[08/13/23 10:08:31] INFO     Task END                                                                                                                     
                             Output: Both 'E.T. the Extra-Terrestrial' and 'Jaws' are iconic movies directed by Steven Spielberg. They are known for their    
                             memorable storylines and have had a significant impact on popular culture.                                                       

```

We get the proper output for our task - it compares ET and Jaws as we expect. But notice the input.

```shell
Input:                                                                                                                           
    How are these movies the same:                                                                                               
    {'74bd46cfd17a4ccaa92308029b508751': 'E.T. the Extra-Terrestrial', '90ed4594b9af4ad9ac2fe45cd53c7889': 'Jaws'}                                                             
                              
```

Instead of passing just the names of the movies, it's passing the entire dictionary of items. It *works* but it's extra data. Don't worry, there's a way to clean this up using Jinja2 for loops.

## Iterate through item values

Jinja2 has a for loop structure that looks like:
```
{% for value in list.values() %}
{{ value }}
{% endfor %}
```

We can use this inside our PromptTask to iterate through the items and just output the names.

Replace the `{{ parent_outputs }}` section of the `PromptTask` with a for loop that will get the key/value pairs (id, movie name) and output just the value.

!!! tip
    For Jinja2 to iterate through the values of dict, you need to use `parent_outputs.values()`.

```python hl_lines="5-7"
# ... 

end_task = PromptTask("""
    How are these movies the same:
    {% for value in parent_outputs.values() %}
    {{ value }}
    {% endfor %}
    """,
    id="END")

# ...
```

### Test

Run the script again and let's see how it looks.

```shell
INFO     Task END
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

There was not as much work in this section, but we did cover some important concepts. 

* We made our code more flexible by using a list of descriptions to create PromptTasks instead of creating them one at a time.
* We used a Jinja2 template **for loop** to iterate through each incoming item.

Review your code with the current state to make sure everything is working as expected.

```python linenums="1" title="app.py"
--8<-- "docs/courses/compare-movies-workflow/assets/code_reviews/04/app.py"
```

## Next Step
Our code works, but the descriptions of the movies aren't as detailed as they could be. It would be better if we could search the web for detailed information about the movies, and use those results for a more comprehensive comparison.

In the next section, we will add to our workflow by adding a ToolkitTask that uses the `WebScraperTool` tool to get more detailed information. Jump to [Using Tools](05_using_tools.md) when you're ready to continue.
