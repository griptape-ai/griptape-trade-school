# Vectorizing API Docs

## Overview
We have the ability to connect to the ShotGrid API and execute commands, but the knowledge the LLM has is restricted to what it was trained on. Let's provide the LLM with access to the most recent documentation, so it can use that to get more data.

The trick is that we want to allow the LLM to get access to this data _quickly_. We want it to be able to know how to find the right commands for the types of tasks we want to execute without needing to know _exactly_ that the method is `find` or `create` or `find_one`.

Well, luckily Autodesk has provided pretty extensive API documentation available here: [https://developers.shotgridsoftware.com/python-api/reference.html#](https://developers.shotgridsoftware.com/python-api/reference.html#). There are additional pages available as well.

We can provide this documentation to the LLM by creating a **Vector Store** of docs.

## What is "Vector Storage"

You can think of vector storage like a huge, organized bookshelf in a library where each book represents a piece of information, or data. In this library, instead of books being sorted by author or title, they're organized based on their content's "features" or "characteristics".

Now imagine each book has a summary that describes its key points, and these summaries are used to arrange the books on the shelves. In vector storage, this summary is like a 'vector' - a list of numbers that represent the key features of the data. These vectors help in quickly finding the right book (or data) that you need.

When you want to find information related to a specific topic, the librarian quickly scans through these summaries and finds the books that closely match what you're looking for. This is much faster than reading all the books in their entirety, or going through it in random order.

In technical terms, the data is converted into vectors (numerical representations) allowing for quick and accurate searches based on similarities in the vectors.

This means I can ask for "ways to filter asset creation" and "asset creation, filtering methods" and "hey, can you filter the results for creating assets?" and get the same helpful information back!

## Vector Storage Process

The process for providing the docs to the LLM looks like this:

1. Create a Vector Database where we can store the documents. In this example we'll use a simple [Local Vector Store Driver](https://docs.griptape.ai/en/latest/griptape-framework/data/vector-store-drivers/#local-vector-store-driver).
2. Create a [Vector Query Engine](https://docs.griptape.ai/en/latest/griptape-framework/data/query-engines/#vectorqueryengine) - an engine that's really good at searching Vector Databases
3. Create a list of URLs to vectorize.
4. For each url, load the data using a [WebLoader](https://docs.griptape.ai/en/latest/griptape-framework/data/loaders/#web-loader).
5. For each bit of website data, upsert (update/insert) it into the Vector Store.
6. Create a [Vector Store Client (Tool)](https://docs.griptape.ai/en/latest/griptape-tools/official-tools/vector-store-client/) that has access to the data and the query engine.
7. Give the Vector Store Client to the Agent.

``` mermaid
graph TB
    A(Create Vector DB)
    B(Create Vector Query Engine)
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
    M(Vector Store Client)
    N(Agent)
    A --> B --> C
    C --> D --> G --> J --> M
    C --> E --> H --> K --> M
    C --> F --> I --> L --> M
    M --> N
    
```

### Vector Database

Let's start by creating the Vector Database. We're going to use Griptape's [LocalVectorStoreDriver](https://docs.griptape.ai/en/latest/griptape-framework/data/vector-store-drivers/#local-vector-store-driver). 

!!! tip
    You could also use [Pinecone](https://www.pinecone.io/), [Marqo](https://www.marqo.ai/), [MongoDB](https://www.mongodb.com/atlas/database), [Redis](https://redis.io/), [OpenSearch](https://opensearch.org/), or [PGVector](https://github.com/pgvector/pgvector) - all are available as drivers for Griptape as described [in the documentation](https://docs.griptape.ai/en/latest/griptape-framework/data/vector-store-drivers/).

Modify `app.py` to import the required drivers. In the case of the the Local Vector Store Driver we also need an Embedding Driver. We'll use the one from OpenAI, but you could also use one of the [other drivers](https://docs.griptape.ai/en/latest/griptape-framework/data/embedding-drivers/) available for Griptape.

```python title="app.py" hl_lines="5"
# ...
from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTime
from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver
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

### Vector Query Engine

Now that we have a database, we need a way to query it. This will be done using Griptape's [VectorQueryEngine](https://docs.griptape.ai/en/latest/griptape-framework/data/query-engines/#vectorqueryengine) which takes a `vector_store_driver`. Luckily we just created one!

First import the engine into Gritpape by adding it to the imports section of your app.

```python title="app.py" hl_lines="3"
# ...
from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver
from griptape.engines import VectorQueryEngine
# ...

```

Next, create the engine. Add the following lines after the creation of the `vector_store_driver`.

```python title="app.py" hl_lines="6-7"
# ...

# Create the vector database
vector_store_driver = LocalVectorStoreDriver(embedding_driver=OpenAiEmbeddingDriver())

# Create the query engine
query_engine = VectorQueryEngine(vector_store_driver=vector_store_driver)

# ...
```

### Gather URLs

The relevant ShotGrid API documentation is available split over six web pages. The first is a general api reference page, and the rest are in their "cookbook". We'll create a list of these.

Add the following lines after creating the query engine.

```python title="app.py" hl_lines="6-14"
# ...

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
# ...
```

### Load URL Content

There are a number of Loaders available for Griptape to allow you to load textual data. You can load from the web, from pdf, sql, csv, and more. Review all the details in our [Loader documentation](https://docs.griptape.ai/en/latest/griptape-framework/data/loaders/).

In this case, we will be using the WebLoader to load the data from the HTML pages.

First import the WebLoader from `griptape.loaders` by adding the `import` statement in the `import` section of your app.

```python title="app.py" hl_lines="3"
# ...
from griptape.engines import VectorQueryEngine
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
    query_engine.vector_store_driver.upsert_text_artifacts({namespace: artifact})

# ...
```

### Vector Store Client

Now we need to create the VectorStoreClient. This will be the tool we provide to the Agent that tells it how to access the vector database. Much like the ShotGridTool, the VectorStoreClient has a method that allows it to search vector databases.

Because the VectorStoreClient is a Griptape Tool, you can add it to the `import` line where we're already importing `DateTime`

```python title="app.py" hl_lines="4"
# ...

from griptape.utils import Chat
from griptape.tools import DateTime, VectorStoreClient

# ...
```

We can instantiate the tool in `app.py` after upserting the data. We'll provide a `description` so the LLM knows when to use it, and also access to the `query_engine` and `namespace`. 

```python title="app.py" hl_lines="9-15"
# ...

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

# ...
```

### Give to Agent

Lastly, let's give the `vector_store_tool` to the Agent so it can use it.

```python title="app.py" hl_lines="8"
# ...

# Instantiate the agent
agent = Agent(
    tools=[
        DateTime(off_prompt=False),
        shotgrid_tool,
        vector_store_tool
        # ReverseStringTool(off_prompt=False),
    ]
)

# ...
```

### Try it out

A great way to test is to ask a specific question that the Agent would do better at when reading the supplied documentation.

For example, there is documentation on how [ShotGrid Thinks when updating task dates](https://developers.shotgridsoftware.com/python-api/cookbook/tasks/updating_tasks.html).

If you ask the question: "Tell me how ShotGrid thinks about updating task dates and what are the general rules?"

When provided with the api documentation, the Agent will do the following:
```json
Thought: To answer this question, I need to search the ShotGrid API documentation for   
information about updating task dates. I will use the VectorStoreClient action to do    
this.                                                                                   

Action:                                                                                 
{                                                                                       
    "name": "VectorStoreClient",
    "path": "search",
    "input": {
        "values": {
            "query": "ShotGrid API update task dates" 
        }
    }                                                         
}                                                                                       
```

... and then proceed to return a bunch of extremely helpful information.

If you don't provide the api documentations and ask the same question, it gets confused and doesn't provide the right answer. It even hallucinates ShotGrid method that doesn't exist:

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

We have certainly improved our Agent in this example - providing it greater context and knowlege about how to interact with the ShotGridTool. Let's review `app.py` and see all the changes that were made.

```python linenums="1" title="app.py" hl_lines="6-9 16-17 19-20 22-30 32-35 37-38 40-41 43-49 74"
from dotenv import load_dotenv
import os

from griptape.structures import Agent
from griptape.utils import Chat
from griptape.tools import DateTime, VectorStoreClient
from griptape.drivers import LocalVectorStoreDriver, OpenAiEmbeddingDriver
from griptape.engines import VectorQueryEngine
from griptape.loaders import WebLoader

from reverse_string_tool import ReverseStringTool
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

# Instantiate the agent
agent = Agent(
    tools=[
        DateTime(off_prompt=False),
        shotgrid_tool,
        vector_store_tool
        # ReverseStringTool(off_prompt=False),
    ]
)

# Start chatting
Chat(agent).start()
```

---
## Next Steps
This has been a powerful step - we can do so much now! However, the current implementation relies on the LLM having been trained on data about the ShotGrid api. What if there wasn't much knowledge about it, or if the API has been updated? In the [next section](08_vectorized_docs.md), we'll provide the Agent access to the current API docs for it to use as reference to enhance it's abilities.