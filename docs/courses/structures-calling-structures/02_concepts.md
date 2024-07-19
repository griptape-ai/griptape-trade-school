# Understanding Structure Run Drivers

![Capybara understanding](assets/capybara_understanding.webp)

Before moving too quickly into the course, let’s quickly go over how Structure Run Drivers work in Griptape.

## Key Concepts:

### What is a Structure?

In Griptape, a "Structure" refers to an `Agent`, a `Pipeline`, or a `Workflow`.

### What is a Run Driver?

A Run Driver is responsible for executing these Structures. It determines where and how the structure will be run. For example, it could execute code directly on your local machine, or on a remote server managed by Griptape’s cloud services.

### Types of Structure Run Drivers

#### `LocalStructureRunDriver`
The `LocalStructureRunDriver` is used for executing Structures within the same local environment as the one executing code. This is particularly useful during development and testing phases where you might need quick feedback without the complexities of networked environments.

**Example Use Case:**

* A local testing pipeline that processes data and performs some functions without needing external resources.
* An image generation pipeline that creates images in a certain style, and does something useful with them.
* An agent with a specific ruleset and tools it has access to.

#### `GriptapeCloudStructureRunDriver`

The `GriptapeCloudStructureRunDriver` enables Structures to run in the Griptape Cloud. This is ideal for production environments or when you need to scale operations beyond a single local system.

**Example Use Case:**

* A deployment scenario where data processing needs to be handled in a scalable, managed cloud environment, benefiting from the robustness and distributed nature of cloud resources.

### How It Works:

You set up a structure as a function in python that returns the structure. Then, you give the structure to either the `LocalStructureRunDriver` or `GriptapeCloudStructureRunDriver`. Then use the `StructureRunClient` or `StructureRunTask` to execute it.

Here’s a simple example of an Agent that has a ruleset to analyze a sentence to see if its got proper grammar. We’ll create a `LocalStructureRunDriver` for it, give that to the `StructureRunClient`, and pass that as a tool to another agent. Don’t worry about copying this example directly, just read through it and see if it makes sense.

```python
--8<-- "docs/courses/structures-calling-structures/assets/code_reviews/02/how_it_works.py"
```

Here is the output from the logs from chatting with the agent. Notice how it will use the grammar_agent only when we ask it to. Pay close attention to the section of the log where it shows `Actions:`. This is where the first agent calls the second one as a tool:

```bash
User: Good morning, my friend!

Thinking...
[05/08/24 05:51:52] INFO     ToolkitTask 2775ae9d64074509a64fefe9d6b272ae                                                   
                             Input: Good morning, my friend!                                                                
[05/08/24 05:51:55] INFO     ToolkitTask 2775ae9d64074509a64fefe9d6b272ae                                                   
                             Output: Good morning! How can I assist you today?                                              

Assistant: Good morning! How can I assist you today?

User: Can you tell me if this is correct grammar? "Well, today it's a grate day, hahHAH!"

Thinking...
[05/08/24 05:52:13] INFO     ToolkitTask 2775ae9d64074509a64fefe9d6b272ae                                                   
                             Input: Can you tell me if this is correct grammar? "Well, today it's a grate day, hahHAH!"     
[05/08/24 05:52:21] INFO     Subtask 738e357edac148dcb031349cf241dde8                                                       
                             Thought: The user wants to know if the sentence "Well, today it's a grate day, hahHAH!" is     
                             grammatically correct. I will use the Grammar Agent to check the grammar of the sentence.      
                                                                                                                            
                             Actions: [                                                                                     
                               {                                                                                            
                                 "name": "Grammar Agent",                                                                   
                                 "path": "run_structure",                                                                   
                                 "input": {                                                                                 
                                   "values": {                                                                              
                                     "args": ["Well, today it's a grate day, hahHAH!"]                                      
                                   }                                                                                        
                                 },                                                                                         
                                 "tag": "grammar_check_1"                                                                   
                               }                                                                                            
                             ]                                                                                              
[05/08/24 05:52:21] INFO     PromptTask 5a29e7d450e142e18e4d28ab918ddfec                                                    
                             Input: Well, today it's a grate day, hahHAH!                                                   
[05/08/24 05:52:32] INFO     PromptTask 5a29e7d450e142e18e4d28ab918ddfec                                                    
                             Output: Your sentence has a few errors. Here's a corrected version: "Well, today is a great    
                             day, haha!"                                                                                    
                                                                                                                            
                             Here's the breakdown of the corrections:                                                       
                                                                                                                            
                             1. "it's" should be "is". The contraction "it's" stands for "it is" or "it has", but in this   
                             context, you're trying to say "today is", so the correct word is "is".                         
                             2. "grate" should be "great". "Grate" is a verb that means to shred or a noun that refers to a 
                             metal framework. The word you're looking for is "great", which is an adjective that means very 
                             good or of high quality.                                                                       
                             3. "hahHAH" should be "haha". The standard way to write laughter in English is "haha" or "ha   
                             ha".                                                                                           
                                                                                                                            
                             Keep practicing! You're doing well, and every mistake is an opportunity to learn.              
[05/08/24 05:52:33] INFO     Subtask 738e357edac148dcb031349cf241dde8                                                       
                             Response: Output of "Grammar Agent.run_structure" was stored in memory with memory_name        
                             "TaskMemory" and artifact_namespace "f9c4dc565bd342bf860a2f6654320e75"                         
[05/08/24 05:52:40] INFO     Subtask aaa30a518e2f4c888c755301fa90872c                                                       
                             Thought: The Grammar Agent has checked the sentence and stored the result in memory. I will now
                             retrieve this information from the memory to provide the user with an answer.                  
                             Actions: [{"name": "TaskMemoryClient", "path": "query", "input": {"values": {"memory_name":    
                             "TaskMemory", "artifact_namespace": "f9c4dc565bd342bf860a2f6654320e75", "query": "What is the  
                             result of the grammar check?"}}, "tag": "query_grammar_check_1"}]                              
[05/08/24 05:52:45] INFO     Subtask aaa30a518e2f4c888c755301fa90872c                                                       
                             Response: The result of the grammar check is a corrected sentence: "Well, today is a great day,
                             haha!" The corrections include changing "it's" to "is", "grate" to "great", and "hahHAH" to    
                             "haha".                                                                                        
[05/08/24 05:52:49] INFO     ToolkitTask 2775ae9d64074509a64fefe9d6b272ae                                                   
                             Output: The corrected version of your sentence is: "Well, today is a great day, haha!" The     
                             corrections include changing "it's" to "is", "grate" to "great", and "hahHAH" to "haha".       

Assistant: The corrected version of your sentence is: "Well, today is a great day, haha!" The corrections include changing "it's" to "is", "grate" to "great", and "hahHAH" to "haha".
```

This is merely a quick example - check out the log here:

```
[05/08/24 05:52:21] INFO     Subtask 738e357edac148dcb031349cf241dde8                                                       
                             Thought: The user wants to know if the sentence "Well, today it's a grate day, hahHAH!" is     
                             grammatically correct. I will use the Grammar Agent to check the grammar of the sentence.      
                                                                                                                            
                             Actions: [                                                                                     
                               {                                                                                            
                                 "name": "Grammar Agent",                                                                   
                                 "path": "run_structure",                                                                   
                                 "input": {                                                                                 
                                   "values": {                                                                              
                                     "args": ["Well, today it's a grate day, hahHAH!"]                                      
                                   }                                                                                        
                                 },                                                                                         
                                 "tag": "grammar_check_1"                                                                   
                               }                                                                                            
                             ]                                                                                              
```

As you can see, the Agent decides to use the `Grammar Agent`, passing the argument "Well, today it's a grate day, hahHAH!". It gets the response back from the structure, and explains to the user the correct feedback:

```
Assistant: The corrected version of your sentence is: "Well, today is a great day, haha!" The corrections include changing "it's" to "is", "grate" to "great", and "hahHAH" to "haha".

```

---
## Next Steps
In the [next section](03_image_pipeline.md), we'll take the image pipeline from the other course and adjust it so it can be passed to an agent.
