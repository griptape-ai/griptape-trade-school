# Drawing Agent

![alt text](assets/capybara_cam.webp)

Now it’s time to take our agent and give it the ability to create beautiful images worthy of sharing with friends and family.

## Import Driver and Tool

First, let’s add the required structure imports. In `app.py` add the following to your imports section:

```python title="app.py" hl_lines="6-7"
# ...

# Griptape Items
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.drivers import LocalStructureRunDriver
from griptape.tools import StructureRunTool

# ...
```

## Add create_image_pipeline function

Now we need to bring in the `create_image_pipeline` function we created in the last step. Because this is in another file, we’ll import it directly.

After the Griptape imports, add this line:

```python title="app.py" hl_lines="3"
# ...

from image_pipeline import create_image_pipeline

# ...
```

## Create the Driver

Next, we’ll create the `image_pipeline_driver` using the `LocalStructureRunDriver`.

After `load_dotenv()`, and before the section of the code where you create the Agent, create your driver:

```python title="app.py" hl_lines="3-6"
# ...

# Create the driver
image_pipeline_driver = LocalStructureRunDriver(
    structure_factory_fn=create_image_pipeline
)

# ...
```

!!! question "What is a "Factory"?"
    You may have noticed that the parameter we’re using to tell the `LocalStructureRunDriver` what function to use has the word “factory” in it.

    ```python
    structure_factory_fn=create_image_pipeline
    ```

    In Python, a "factory" is a concept rather than a specific feature or part of the language. It's a way of organizing your code so that you can create objects—think of objects as individual instances of things—without needing to know the exact details of how they are made. This is especially useful when you have different kinds of objects that share some common traits but might be created differently.

    Imagine you run a toy shop, and you want to make different types of toys, like cars, planes, or dolls. Instead of building each toy from scratch every time, you set up a "factory" that knows how to make each type of toy based on what you ask for. You just tell the factory, "I need a car," and the factory gives you a car. You don’t need to know how the factory puts the wheels on or paints it; you just get the finished car ready to play with.

    In Python, a factory function is a function you call to create these objects for you. You tell the function what kind of object you want, and it handles all the details, returning the new object.

## Create the Tool

Time to create the Tool. This will take the driver, and we’ll pass it to the Agent.

Two very important properties to call out are the `name` and the `description`. You _must_ define these, as they will help the Agent figure out when it’s appropriate to use this tool. If you named it “clam shucker” and gave it a description of “loves to eat clams on a Wednesday”, the agent would have no idea that this pipeline could create images.

```python title="app.py" hl_lines="3-9"
# ...

# Create the Tool
image_pipeline_tool = StructureRunTool(
    name="Image Creator",
    description="Create an image based on a prompt.",
    driver=image_pipeline_driver,
    off_prompt=False,
)

# ...
```

## Give the client to the Agent

Now the exciting part, let’s give the client to the agent as a tool. Modify your Agent creation code to accept this new tool.

```python title="app.py" hl_lines="4"
# ...

# Create the Agent
agent = Agent(tools=[image_pipeline_tool])

# ...
```

## Try it out

Let’s go ahead and run the script and see what kind of magic happens! Ask it to create an image based on the topic of your choosing.

![prompt agent for beach chair](assets/prompt_for_beach_chair.webp)

And the resulting image:

![beach chair](assets/beach_chair.webp)

If you've set it up correctly, you should now see an image in the style of a 1970s polaroid! You can ask it to create a bunch of images, and it will do so, keeping the same style in that pipeline.

![binoculars](assets/binoculars.webp){align=left, width=200}
![computer](assets/computer.webp){align=left, width=200}
![kiwi](assets/kiwi.webp){align=left, width=200}
![sofa](assets/sofa.webp){align=left, width=200}
![coffee](assets/coffee.webp){align=left, width=200}
![airplane](assets/airplane.webp){align=left, width=200}


## Code Review

```python title="app.py" linenums="1"
--8<-- "docs/courses/structures-calling-structures/assets/code_reviews/04/app.py"
```

---
## Next Steps

Congratulations! You’ve adapted an existing pipeline to one that can now be given to an Agent, or used as a step in another pipeline!

To continue your exploration, try creating multiple pipelines with very different tasks and give those to an agent. Try creating a series of agents with different skill sets. Let us know what you explore in our [Discord Channel](https://discord.gg/pqTxMFFK)!

Happy coding!
