# Vectorizing API Docs

## Overview
We have the ability to connect to the ShotGrid API and execute commands, but the knowledge the LLM has is restricted to what it was trained on. Let's provide the LLM with access to the most recent documentation, so it can use that to get more data.

The trick is that we want to allow the LLM to get access to this data _quickly_. We want it to be able to know how to find the right commands for the types of tasks we want to execute without needing to know _exactly_ what the method is `find` or `create` or `find_one`.

Well, luckily Autodesk has provided pretty extensive API documentation available here: [https://developers.shotgridsoftware.com/python-api/reference.html#](https://developers.shotgridsoftware.com/python-api/reference.html#){target="_blank"}. There are additional pages available as well.

We can provide this documentation to the LLM by creating a **Vector Store** of docs.

## What is "Vector Storage"

You can think of vector storage as a huge, organized bookshelf in a library where each book represents a piece of information or data. In this library, instead of books being sorted by author or title, they're organized based on their content's "features" or "characteristics".

Now imagine each book has a summary that describes its key points, and these summaries are used to arrange the books on the shelves. In vector storage, this summary is like a 'vector' - a list of numbers that represent the key features of the data. These vectors help in quickly finding the right book (or data) that you need.

When you want to find information related to a specific topic, the librarian quickly scans through these summaries and finds the books that closely match what you're looking for. This is much faster than reading all the books in their entirety or going through them in random order.

In technical terms, the data is converted into vectors (numerical representations) allowing for quick and accurate searches based on similarities in the vectors.

This means I can ask for "ways to filter asset creation" "asset creation, filtering methods" and "Hey, can you filter the results for creating assets?" and get the same helpful information back!

## Vector Storage Process

The process for providing the docs to the LLM looks like this:

1. Create a Vector Database where we can store the documents. In this example, we'll use a simple [Local Vector Store Driver](https://docs.griptape.ai/stable/griptape-framework/drivers/vector-store-drivers/#local-vector-store-driver){target="_blank"}.
2. Create a [RAG Engine](https://docs.griptape.ai/stable/griptape-framework/engines/rag-engines/){target="_blank"} - an engine that's really good at searching Vector Databases
3. Create a list of URLs to vectorize.
For each URL, load the data using a [WebLoader](https://docs.griptape.ai/stable/griptape-framework/data/loaders/#web-loader){target="_blank"}.
5. For each bit of website data, upsert (update/insert) it into the Vector Store.
6. Create a [Vector Store Tool](https://docs.griptape.ai/stable/griptape-tools/official-tools/vector-store-tool/){target="_blank"} that has access to the data and the query engine.
7. Give the Vector Store Tool to the Agent.

``` mermaid
graph TB
    A(Create Vector DB)
    B(Create RAG Engine)
    C(Gather URLs)
    D(URL 1)
    E(URL 2)
    F(URL 3)
    G(Load Data)
    H(Load Data)
    I(Load Data)
    J(Upsert)
    K(Upsert)
    L(Upsert)
    M(Vector Store Tool)
    N(Agent)
    A --> B --> C
    C --> D --> G --> J --> M
    C --> E --> H --> K --> M
    C --> F --> I --> L --> M
    M --> N
    
```

### Vector Database

Let's start by creating the Vector Database. We're going to use Griptape's [LocalVectorStoreDriver](https://docs.griptape.ai/stable/griptape-framework/drivers/vector-store-drivers/#local-vector-store-driver){target="_blank"}. 

!!! tip
    You could also use [Pinecone](https://www.pinecone.io/){target="_blank"}, [Marqo](https://www.marqo.ai/){target="_blank"}, [MongoDB](https://www.mongodb.com/atlas/database){target="_blank"}, [Redis](https://redis.io/), [OpenSearch](https://opensearch.org/){target="_blank"}, or [PGVector](https://github.com/pgvector/pgvector){target="_blank"} - all are available as drivers for Griptape as described [in the documentation](https://docs.griptape.ai/stable/griptape-framework/drivers/vector-store-drivers/){target="_blank"}.

Modify `app.py` to import the required drivers. In the case of the Local Vector Store Driver, we also need an Embedding Driver and a ChatPrompt Driver. We'll use the ones from OpenAI, but you could also use one of the [other drivers](https://docs.griptape.ai/stable/griptape-framework/drivers/embedding-drivers/){target="_blank"} available for Griptape.

```python title="app.py" hl_lines="5-9"
# ...
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTimeTool
from griptape.drivers import (
    LocalVectorStoreDriver, 
    OpenAiEmbeddingDriver, 
    OpenAIChatPromptDriver
)
# ...

```

Now after the `load_dotenv()` line in `app.py`, create the vector database by instantiating `LocalVectorStoreDriver` and passing it an `embedding_driver`.

```python title="app.py" hl_lines="5-6"
# ...

load_dotenv()

# Create the vector database
vector_store_driver = LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver())

# ...
```

### Rag Engine

Now that we have a database, we need a way to query it. This will be done using Griptape's [RagEngine](https://docs.griptape.ai/stable/griptape-framework/engines/rag-engines/){target="_blank"}.

First, import the engine into Griptape by adding it to the imports section of your app.

```python title="app.py" hl_lines="3"
# ...
from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver, OpenAIChatPromptDriver
from griptape.engines.rag import RagEngine
from griptape.engines.rag.modules import PromptResponseRagModule
from griptape.engines.rag.stages import ResponseRagStage
# ...

```

Next, create the engine. Add the following lines after the creation of the `vector_store_driver`.

```python title="app.py" hl_lines="6-10"
# ...

# Create the vector database
vector_store_driver = LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver())

# Create the query engine
rag_engine = RagEngine(
    response_stage=ResponseRagStage(
        response_modules=[PromptResponseRagModule(
            prompt_driver=OpenAiChatPromptDriver(model="gpt-4o-mini")
        )]
    ),
)

# ...
```

### Gather URLs

The relevant ShotGrid API documentation is available split over six web pages. The first is a general API reference page, and the rest are in their "cookbook". We'll create a list of these.

Add the following lines after creating the query engine.

```python title="app.py" hl_lines="9-17"
# ...

# Create the query engine
rag_engine = RagEngine(
    prompt_driver=OpenAiChatPromptDriver(model="gpt-3.5-turbo"),
    vector_store_driver=vector_store_driver
)

# API Documentation
shotgrid_api_urls = [
    "https://developers.shotgridsoftware.com/python-api/reference.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/usage_tips.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/attachments.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/updating_tasks.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/task_dependencies.html",
    "https://developers.shotgridsoftware.com/python-api/cookbook/tasks/split_tasks.html",
]
# ...
```

### Load URL Content

There are a number of Loaders available for Griptape to allow you to load textual data. You can load from the web, from pdf, SQL, CSV, and more. Review all the details in our [Loader documentation](https://docs.griptape.ai/stable/griptape-framework/data/loaders/){target="_blank"}.

In this case, we will be using the WebLoader to load the data from the HTML pages.

First import the WebLoader from `griptape.loaders` by adding the `import` statement in the `import` section of your app.

```python title="app.py" hl_lines="3"
# ...
from griptape.engines.rag import RagEngine
from griptape.engines.rag.modules import PromptResponseRagModule
from griptape.engines.rag.stages import ResponseRagStage
from griptape.loaders import WebLoader
# ...

```

Then add the following lines to create a list of "artifacts" - loaded chunks of data.

```python title="app.py" hl_lines="8-11"
# ...

# API Documentation
shotgrid_api_urls = [
    # ...
]

# Load the API documentation
artifacts = []
for url in shotgrid_api_urls:
    artifacts.append(WebLoader().load(url))

# ...
```

### Upsert Content

Now we'll upsert the data into the database.

!!! question "What's an 'upsert?'"
    Upsert is a great word - it is a combination of "insert" and "update". It's used frequently in databases to mean "Hey.. here's some data. Insert a new record into the database if doesn't exist, or update the record if it does."

    Not only is it a great concept because it simplifies the process of ensuring the database contains a specific record, but it also is an awesome word to pull out at dinner parties.

In order to give the database the right information, we'll need to provide a namespace to operate in, then we can upsert into that namespace.

```python title="app.py" hl_lines="8-12"
# ...

# Load the API documentation
artifacts = []
for url in shotgrid_api_urls:
    artifacts.append(WebLoader().load(url))

# Upsert documentation  into the vector database
namespace = "shotgrid_api"

for artifact in artifacts:
    vector_store_driver.upsert_text_artifacts({namespace: artifact})

# ...
```

### Vector Store Tool

Now we need to create the VectorStoreTool. This will be the Tool we provide to the Agent that tells it how to access the vector database. Much like the ShotGridTool, the VectorStoreTool has a method that allows it to search vector databases.

Because the VectorStoreTool is a Griptape Tool, you can add it to the `import` line where we're already importing `DateTimeTool`

```python title="app.py" hl_lines="4"
# ...

from griptape.utils import Chat
from griptape.tools import DateTimeTool, VectorStoreTool

# ...
```

We can instantiate the Tool in `app.py` after upserting the data. We'll provide a `description` so the LLM knows when to use it, and also access to the `rag_engine` and `namespace`. 

```python title="app.py" hl_lines="9-15"
# ...

# Upsert documentation  into the vector database
namespace = "shotgrid_api"

for artifact in artifacts:
    vector_store_driver.upsert_text_artifacts({namespace: artifact})

# Instantiate the Vector Store Tool
vector_store_tool = VectorStoreTool(
    description="Contains information about ShotGrid api. Use it to help with ShotGrid client requests.",
    vector_store_driver=vector_store_driver,
    query_params={"namespace": namespace},
    off_prompt=False,
)

# ...
```

### Give to Agent

Lastly, let's give the `vector_store_tool` to the Agent so it can use it.

```python title="app.py" hl_lines="8"
# ...

# Instantiate the agent
agent = Agent(
    tools=[
        DateTimeTool(off_prompt=False),
        shotgrid_tool,
        vector_store_tool
        # ReverseStringTool(off_prompt=False),
    ],
    stream=True
)

# ...
```

### Try it out

A great way to test is to ask a specific question that the Agent would do better at when reading the supplied documentation.

For example, there is documentation on how [ShotGrid Thinks when updating task dates](https://developers.shotgridsoftware.com/python-api/cookbook/tasks/updating_tasks.html){target="_blank"}.

If you ask the question: "Tell me how ShotGrid thinks about updating task dates and what are the general rules?"

When provided with the API documentation, the Agent will do the following:
```json
Thought: To answer this question, I need to search the ShotGrid API documentation for   
information about updating task dates. I will use the VectorStoreTool action to do    
this.                                                                                   

Action:                                                                                 
{                                                                                       
    "name": "VectorStoreTool",
    "path": "search",
    "input": {
        "values": {
            "query": "ShotGrid API update task dates" 
        }
    }                                                         
}                                                                                       
```

... and then proceed to return a bunch of extremely helpful information.

If you don't provide the API documentation and ask the same question, it gets confused and doesn't provide the right answer. It even hallucinates the ShotGrid method that doesn't exist:

```json
Thought: To answer this question, I need to use the ShotGridTool action to execute the  
ShotGrid method that provides information about updating task dates.

Action:
{
    "name": "ShotGridTool",
    "path": "meta_method",
    "input": { 
        "values":{
            "method": "get_task_date_update_rules", 
            "params":[]
        }        
    }   
}                                                                                       

Subtask 6688154d58ab4dd687680ff1c3081ca4
Response: 'Shotgun' object has no attribute 'get_task_date_update_rules'                
```

## Code Review

We have certainly improved our Agent in this example - providing it with greater context and knowledge about how to interact with the ShotGridTool. Let's review `app.py` and see all the changes that were made.

```python linenums="1" title="app.py"
--8<-- "docs/courses/shotgrid-tool/assets/code_reviews/08/app.py"
```

---
## Next Steps
While adding access to the API documentation has improved the performance of the agent significantly, we can keep improving it by providing some Rules and Rulesets, ensuring the agent knows when to use the VectorStore, and also giving it hints as to how to use the API more efficiently. That will be coming up in the [next section](09_rules.md).
