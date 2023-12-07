# Tools with Pipelines

## Overview

Interacting with the ShotGrid Tool via a chatbot is one way of working with it, but frequently you'll want to run tasks in a more directed flow. For example, what if you wanted to generate a thumbnail image for a newly created asset?

Using a Griptape Pipeline, you can execute a series of tasks consistently, instead of trying to direct an Agent. For example, you can build a Pipeline that will:

1. When given an asset ID, look up the name and description from ShotGrid using the ShotGrid Tool.
2. Generate a prompt for an Image Generation engine to create a thumbnail image in a particular style.
3. Create the thumbnail.
4. Use the ShotGrid Tool to upload the thumbnail back to the asset.

In this section, we'll build this exact flow. Note, that this is a bit more of an advanced flow.

## Importing 

We will need some of the following Gritpape Classes for this to work



## Code Review


---
## Next Steps
...