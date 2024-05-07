# An ImageQuery SEO Bonanza!

## Course Description
The goal of this course is to teach people how to use Griptape’s ability to give Structures (Agents, Pipelines, and Workflows) to other Structures so they can be run as tools or tasks via a StructureRunDriver. This means you can build a really cool pipeline to do something like generate an image based off a prompt  and upload it to s3, provide that pipeline to the StructureRunDriver, and then give that to an Agent. Then, anytime you tell the agent to generate an image, it’ll always execute the proper series of tasks.

![soda](assets/soda.png){ align=right, width=200 }
![rainbow](assets/rainbow.png){ align=right, width=200 }
![icecream](assets/icecream.png){ align=right, width=200 }

You could also create specific Agents with abilities and rules, like one that’s great at technical documentation, another with the ability to research topics from the web, and a third that can generate marketing copy & SEO. Then give all three of those agents to another agent that could orchestrate a conversation between those three. The cool thing is that each of these agents could use different models, have different rulesets, and tools, and more. The possibilities are endless... and stupifying. But mostly endless.


## What we're going to build
For this course, we’ll take an existing TradeSchool course ([Image Generation - Pipelines](../create-image-pipeline/index.md)) and turn that into a structure we can give to an Agent to use as a tool. This will demonstrate how we can enhance the capabilities of Agents quickly.

As a reminder, the Image Generation Pipeline course walks you through how to create a `Pipeline` in Griptape. The user enters a topic for an image (example: “a cow”) and the pipeline will:

* Use a `PromptTask` to create an image generation prompt based on the topic in the style of “a polaroid photograph from the 1970s”.
* Use an `PromptImageGenerationTask` to generate the image.
* Use a `CodeExecutionTask` to display the image.

Here is an example of an image generated using this pipeline:
![boat](assets/boat.png)

By the end of this course, you’ll be able to chat with an agent and say “Can you create 3 images for me: A truck, an ice cream cone, and a wild hedgehog” and it will use the pipeline to generate the images and display them, exactly as you want.

## Who is this course for
This course is aimed at intermediate level Python developers who are interested in learning about how to give Griptape Structures (Agents, Pipelines and Workflows) more complex and interesting functionality.

## Prerequisites
Before beginning this course, you will need:

* An OpenAI API Key (available here: [OpenAI](https://beta.openai.com/account/api-keys){target="_blank"})
* Python 3.11+ installed on your machine
* An IDE (such as Visual Studio Code or PyCharm) to write and manage your code

If you don't have those items available, it's highly recommended you go through the [Griptape Setup - Visual Studio Code](../../setup/index.md) course to set up your environment.

It's also recommended to go through the  [Image Generation - Pipelines](../create-image-pipeline/index.md) course if you haven't viewed it before, as we will be using the code created in that course to complete this one.


## Useful Resources and Links

- [Griptape Documentation](https://github.com/griptape-ai/griptape){target="_blank"}
- [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}


---
## Next Steps

Get yourself all set up and ready by moving on to [Setup](01_setup.md).

