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
## Create the Ruleset

Our first step will be to create the Ruleset for the agent. This ruleset will contain all the rules we will give it.

In `app.py` find the area of the code where you instantiate the agent, and insert the ruleset before it.

```python title="app.py" hl_lines="3-6"
# ...

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent"
)

# Instantiate the agent
# ...
```

## Rules

### Act as...

We want the agent to have the correct context for its work, so the first ruleset will tell it to act as a studio coordinator who is an expert in Autodesk ShotGrid

Create a parameter for `rules`, and then add this first rule to the list of rules:

```python title="app.py" hl_lines="6-8"
# ...

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        Rule("Act as a studio coordinator who is an expert with Autodesk ShotGrid"),
    ],
)

# ...
```

### Main objective

Sometimes it's helpful to remind the LLM what its main objective is. In this case, we want to remind it that we want it to update ShotGrid using the ShotGridTool.

```python title="app.py" hl_lines="8-10"
# ...

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        Rule("Act as a studio coordinator who is an expert with Autodesk ShotGrid"),
        Rule(
            "Your main objective is to find and update information in ShotGrid using the ShotGridTool"
        ),
    ],
)

# ...
```

### Vector Database

Now let's remind it that it should use the VectorStoreClient when it needs information about how to use the API. This will ensure the most up-to-date and accurate use of the API.

Note: This rule is multiple lines long, so we're going to use a Python function `dedent` that will allow us to keep the code looking nice.

First, import `dedent` in your `imports` section of the code.

```python title="app.py"
# ...

from textwrap import dedent

# ...
```

Then, add the new rule:

```python title="app.py" hl_lines="8-17"
# ...

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        # ...
        Rule(
            dedent(
                """
            For specific information about how to use ShotGrid API activities, the 
            VectorStoreClient should be used. Take the necessary time to consult the 
            VectorStoreClient to ensure the most accurate and context-aware decisions 
            when interacting with the ShotGridTool and API.
            """
            )
        ),
    ],
)

# ...
```

### Batch mode

ShotGrid provides access to a `batch` method that allows you to perform multiple create, update, and delete operations in a single request. Each operation in the batch is specified as a dictionary, and the operations are performed in the order they are provided.

We would like to ensure the Agent uses batch mode when appropriate. 

```python title="app.py" hl_lines="8-16"
# ...

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        # ...
        Rule(
            dedent(
                """
            Always use the ShotGrid batch() method when performing multiple create, update, or delete operations in ShotGrid.
            This should be done in a single request to improve efficiency and speed. 
            Batch method uses "request_type", "entity_type", and "entity_id".
            Failure to use the batch() method in these instances will be considered a violation of the rules."""
            )
        ),
    ],
)
```

!!! tip
    While working on the rule for batch mode, I found that the LLM was sometimes not using it and would jump to
just using create or update methods instead. I asked the agent for a good rule to enforce using the `batch` method, and it came up with this very strict rule.

    And .. it worked! Sometimes just asking the LLM for the best rule provides excellent results.

### Every task

Lastly, one final rule is to ensure the Agent uses the ShotGrid and doesn't just pretend to use it.


```python title="app.py" hl_lines="8-17"
# ...

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        # ...
        Rule(
            dedent(
                """
            When asked to find, list, create, update, delete, retrieve details of entities, 
            update task status, update task data, list task assignments, retrieve the history of changes to 
            entities, manage versions of assets, manage project timelines, track project 
            progress, manage notes and reviews, manage user roles and permissions, or 
            integrate with other tools and workflows, the ShotGrid Client API is always used."""
            )
        )
    ]
)

# ...
```

### Full list of rules

Here are all the rules.

```python title="app.py"
# ...

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        Rule("Act as a studio coordinator who is an expert with Autodesk ShotGrid"),
        Rule(
            "Your main objective is to find and update information in ShotGrid using the ShotGridTool"
        ),
        Rule(
            dedent(
                """
            For specific information about how to use ShotGrid API activities, the 
            VectorStoreClient should be used. Take the necessary time to consult the 
            VectorStoreClient to ensure the most accurate and context-aware decisions 
            when interacting with the ShotGridTool and API.
            """
            )
        ),
        Rule(
            dedent(
                """
            Always use the ShotGrid batch() method when performing multiple create, update, or delete operations in ShotGrid.
            This should be done in a single request to improve efficiency and speed. 
            Batch method uses "request_type", "entity_type", and "entity_id".
            Failure to use the batch() method in these instances will be considered a violation of the rules."""
            )
        ),
        Rule(
            dedent(
                """
            When asked to find, list, create, update, delete, retrieve details of entities, 
            update task status, update task data, list task assignments, retrieve the history of changes to 
            entities, manage versions of assets, manage project timelines, track project 
            progress, manage notes and reviews, manage user roles and permissions, or 
            integrate with other tools and workflows, the ShotGrid Client API is always used."""
            )
        ),
    ],
)

# ...
```
## Giving the rules to the Agent

The rules won't make any difference if you don't give them to the Agent. Let's do that now.

```python title="app.py" hl_lines="11"
# ...

# Instantiate the agent
agent = Agent(
    tools=[
        DateTime(off_prompt=False),
        shotgrid_tool,
        vector_store_tool
        # ReverseStringTool(off_prompt=False),
    ],
    rulesets=[shotgrid_agent_ruleset],
)

# ...
```

## Try it out

Go ahead and interact with the agent. Work with different projects, create and update assets, and try and create tasks. As you are working with it, figure out where the agent isn't performing as expected, and update rules and rulesets to do exactly what you want it to do. Refine and iterate until you're happy with the results.

## Clean up

Before moving on to the next section, let's remove some unused code from our app. We are no longer using the ReverseStringTool, so you can happily remove it from the `imports` section, and also remove it from your Agent.

## Code Review

Nice work in this section - we've added rules to ensure the agent behaves as expected, using the tools we've given it. Let's take a look at the current state of the app.

```python linenums="1" title="app.py" hl_lines="2 11 70-107 112"
from dotenv import load_dotenv
from textwrap import dedent
import os

from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTime, VectorStoreClient
from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver
from griptape.engines import VectorQueryEngine
from griptape.loaders import WebLoader
from griptape.rules import Rule, Ruleset

from shotgrid_tool import ShotGridTool

load_dotenv()

# Create the vector database
vector_store_driver = LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver())

# Create the query engine
query_engine = VectorQueryEngine(vector_store_driver=vector_store_driver)

# API Documentation
shotgrid_api_urls = [
    "https://developers.shotgridsoftware.com/python-api/reference.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/usage_tips.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/attachments.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/updating_tasks.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/task_dependencies.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/split_tasks.html",
]

# Load the API documentation
artifacts = []
for url in shotgrid_api_urls:
    artifacts.append(WebLoader().load(url))

# Upsert documentation  into the vector database
namespace = "shotgrid_api"

for artifact in artifacts:
    query_engine.vector_store_driver.upsert_text_artifacts({namespace: artifact})

# Instantiate the Vector Store Client
vector_store_tool = VectorStoreClient(
    description="Contains information about ShotGrid api. Use it to help with ShotGrid client requests.",
    query_engine=query_engine,
    namespace=namespace,
    off_prompt=False,
)

SHOTGRID_URL = os.getenv("SHOTGRID_URL")
SHOTGRID_API_KEY = os.getenv("SHOTGRID_API_KEY")
SHOTGRID_SCRIPT = "Griptape API"
SHOTGRID_USER = os.getenv("SHOTGRID_USER")
SHOTGRID_PASSWORD = os.getenv("SHOTGRID_PASSWORD")


# Instantiate the tool
shotgrid_tool = ShotGridTool(
    base_url=SHOTGRID_URL,
    api_key=SHOTGRID_API_KEY,
    script_name=SHOTGRID_SCRIPT,
    user_login=SHOTGRID_USER,
    user_password=SHOTGRID_PASSWORD,
    login_method="user",
    off_prompt=False,
)

# Create the ruleset
shotgrid_agent_ruleset = Ruleset(
    name="ShotGrid Agent",
    rules=[
        Rule("Act as a studio coordinator who is an expert with Autodesk ShotGrid"),
        Rule(
            "Your main objective is to find and update information in ShotGrid using the ShotGridTool"
        ),
        Rule(
            dedent(
                """
            For specific information about how to use ShotGrid API activities, the 
            VectorStoreClient should be used. Take the necessary time to consult the 
            VectorStoreClient to ensure the most accurate and context-aware decisions 
            when interacting with the ShotGridTool and API.
            """
            )
        ),
        Rule(
            dedent(
                """
            Always use the ShotGrid batch() method when performing multiple create, update, or delete operations in ShotGrid.
            This should be done in a single request to improve efficiency and speed. Batch method uses "request_type", "entity_type", and "entity_id".
            Failure to use the batch() method in these instances will be considered a violation of the rules."""
            )
        ),
        Rule(
            dedent(
                """
            When asked to find, list, create, update, delete, retrieve details of entities, 
            update task status, update task data, list task assignments, retrieve the history of changes to 
            entities, manage versions of assets, manage project timelines, track project 
            progress, manage notes and reviews, manage user roles and permissions, or 
            integrate with other tools and workflows, the ShotGrid Client API is always used."""
            )
        ),
    ],
)

# Instantiate the agent
agent = Agent(
    tools=[DateTime(off_prompt=False), shotgrid_tool, vector_store_tool],
    rulesets=[shotgrid_agent_ruleset],
)

# Start chatting
Chat(agent).start()

```

---
## Next Steps
...