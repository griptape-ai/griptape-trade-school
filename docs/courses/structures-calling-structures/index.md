# Structures Calling Structures

## Course Description
The goal of this course is to teach people how to use Griptape’s ability to give Structures (Agents, Pipelines, and Workflows) to other Structures so they can run as tools or tasks via a StructureRunDriver. This means you can build a really cool pipeline to do something such as generate an image based off a prompt, upload it to s3, provide that pipeline to the StructureRunDriver, and then give that to an Agent. Then, anytime you tell the agent to generate an image, it’ll always execute the proper series of tasks.

![soda](assets/soda.webp){ align=right, width=200 }
![rainbow](assets/rainbow.webp){ align=right, width=200 }
![icecream](assets/icecream.webp){ align=right, width=200 }

You could also create specific Agents with abilities and rules. For example, you could have one that’s great at technical documentation, another with the ability to research topics from the web, and a third that can generate marketing copy & SEO. Then you could give all three of those agents to another agent who will then orchestrate a conversation between the three. What's even more exciting is that each of these agents could use different models, have different rulesets, different tools, and so on. The possibilities are endless... and stupefying. But, mostly endless.


## What we're going to build
For this course, we’ll take an existing TradeSchool course ([Image Generation - Pipelines](../create-image-pipeline/index.md)) and turn it into a structure we can give to an Agent to use as a tool. This will demonstrate how we can enhance the capabilities of Agents quickly.

As a reminder, the Image Generation Pipeline course walks you through how to create a `Pipeline` in Griptape. The user enters a topic for an image (example: “a cow”) and the pipeline will:

* Use a `PromptTask` to create an image generation prompt based on the topic in the style of “a polaroid photograph from the 1970s”.
* Use a `PromptImageGenerationTask` to generate the image.
* Use a `CodeExecutionTask` to display the image.

Here is an example of an image generated using this pipeline:

![boat](assets/boat.webp)

By the end of this course, you’ll be able to chat with an agent and say “Can you create 3 images for me: A truck, an ice cream cone, and a wild hedgehog”. It will then use the pipeline to generate the images and display them, exactly as you want.

## Who is this course for
This course is aimed at intermediate-level Python developers who are interested in learning about how to give Griptape Structures (Agents, Pipelines and Workflows) more complex and interesting functionality.

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

