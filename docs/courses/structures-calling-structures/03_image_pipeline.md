# Image Pipeline

![Capybara Packaged ](assets/capybara_packaged.webp)

In this part of the course we’ll take the image pipeline from this course: [Image Generation - Pipelines](../create-image-pipeline/index.md), turn it into a function, and save it as a separate file we can bring into our existing `app.py`. It is good practice to keep these useful structures in separate files, this way your code can be more modular. Also, if you get paid by the number of files you create, it’ll really impress your employer.

## Create `image_pipeline.py`

1. In your application folder, create a new file called `image_pipeline.py`. 

2. Navigate to the Image Generation Pipelines course, go to the Displaying Images section, and scroll down to [Code Review](../create-image-pipeline/07_display_image_task.md#code-review). 

3. Copy the code from this section and paste it into the `image_pipeline.py`.

## Wrap the code in a function

You can keep your code the same, but wrap it into a function. After your import statements are finished, create the image_pipeline function like this:

```python title="image_pipeline.py"
# ...

def image_pipeline() -> Pipeline:
    # Variables
    output_dir = "images"

    # ... rest of your code
```

This says you’re creating the function, and returning a Pipeline structure.

## Remove the Run statement

In your existing code you’re still running the pipeline, but we no longer need to do that - the Agent will run it when it gets called. 

Delete the following lines from the bottom :

```py
    # Run the pipeline
    pipeline.run("a cow")
```

## Add a return

Finally, we need to return the pipeline structure. In the place where you had the Run the Pipeline code, replace it with a return statement.

```python title="image_pipeline.py"
	# ...

    # Return the pipeline
    return pipeline
```

## Code Review

That’s it for setting up your image pipeline script! Let’s review the code

```python title="image_pipeline.py" linenums="1"
--8<-- "docs/courses/structures-calling-structures/assets/code_reviews/03/image_pipeline.py"
```

---
## Next Steps

In the [next section](04_drawing_agent.md), we’ll update our app to have an agent, bring in the image_generation pipeline, create the appropriate driver and client, and give that to the agent.
