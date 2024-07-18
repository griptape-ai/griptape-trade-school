# Adding ShotGrid Methods

## Overview
You can now authenticate with ShotGrid via API and by Username/Password. At the moment, your application only verifies that it can connect to ShotGrid, it doesn't do much else.
In this section, we will add a method that allows you to do much, much more.

## ShotGrid Methods

ShotGrid comes with a number of methods to create, find, update, delete, and much more. Here's a small list of methods, with the [entire list](https://developers.shotgridsoftware.com/python-api/reference.html#shotgrid-methods){target="_blank"} available in their documentation.

|Method|Description| 
|------|-----------|
|`Shotgun.create` | Create a new entity of the specified entity_type| 
|`Shotgun.find`   | Finds entities matching the given filters |
|`Shotgun.update` | Update the specified entity with the supplied data |
|`Shotgun.delete` | Retire (delete) a specified entity. |
|`Shotgun.upload_thumbnail` | Upload a file from a local path and assign it as a thumbnal for the entity |
|`Shotgun.summarize` | Summarize field data returned by a query. |

As you can see, there are a number of various methods we can use, and we _could_ create an activity/method for each one of these. However, our Tool would get large, and end up being somewhat difficult to maintain. There would also be quite a lot of repetitive code, with each method importing the ShotGrid library and connecting.

Instead, we'll introduce a method to create a more "generic" Tool, that will utilize the LLM's knowledge of the ShotGrid API to generate the correct commands.

## Create `meta_method`

We're going to call this new method, the **Meta Method**. This method will allow you to execute _any_ of the methods ShotGrid offers.

### Description and Name
First, in `shotgrid_tool/tool.py` make the following changes:

1. Change the description in the activity to "Can be used to execute ShotGrid methods"
2. Re-name the method we currently have in the Tool from `get_session_token` to `meta_method`

```python title="shotgrid_tool/tool.py" hl_lines="5 8"
# ...

    @activity(
        config={
            "description": "Can be used to execute ShotGrid methods.",
        }
    )
    def meta_method(self, _: dict) -> TextArtifact | ErrorArtifact:
        import shotgun_api3

# ...

```

### Parameters

Next, we'll need to add some parameters to the method. These will be things like - telling `meta_method` which ShotGrid method to call, and what `data` to pass it.

For example, if we want to call the `find` method to find all character assets in Project 155, and return the id, the name, and the description, we'd want to call it like this:

```python
sg.find(
    "Asset", 
    [
        ['project', 'is', {'type': 'Project', 'id': 155}],
        ['sg_asset_type', 'is', 'Character']
    ],
    ['id', 'code', 'description']
    )
```

Or, if we wanted to delete a shot we'd call it this way:
```python
sg.delete("Shot", 2557)
```

So we need to pass the `method` (`find`, `delete`, `update`, etc), and the `data`- a dict of various parameters, depending on the type of method.

This involves updating the activity schema and telling the method itself to accept a list of `params`.

### Update Schema

Update the schema to accept two different parameters: `method` and `params`. We'll make sure we describe them well, giving the LLM proper context as to how to use the parameters.

```python title="shotgrid_tool/tool.py" hl_lines="6-17"
# ...

    @activity(
        config={
            "description": "Can be used to execute ShotGrid methods.",
            "schema": Schema(
                {
                    Literal(
                        "method",
                        description="Shotgrid method to execute. Example: find_one, find, create, update, delete, revive, upload_thumbnail",
                    ): str,
                    Literal(
                        "params",
                        description="Dictionary of parameters to pass to the method.",
                    ): list,
                }
            ),

        }
    )

# ...
```

### Update the method

Now we'll add the `params` parameter to `meta_method`. Replace `_: dict` with `params: dict`.

```python  title="shotgrid_tool/tool.py"  hl_lines="3"
# ...

    def meta_method(self, params: dict) -> TextArtifact | ErrorArtifact:

# ...
```

### Add method logic

We can now add the logic to the method that defines how we use the parameters we've just passed. Using a parameter within a Griptape Tool is pretty straightforward, you just access it with `params["values"][PARAMATER]`. For example, if I want the name of the method we passed, I can do `params["values"]["method"]`. Or if I want the parameters, I can query `params["values"]["params"]`.

So in this method, we're going to do the following:

1. Get the name of the method passed, and use that to find the _ShotGrid method object_ that we will be able to call (`sg.find`, `sg.delete`, `sg.update`, etc). 
2. Get the parameters.
3. Execute the method with the given parameters. Because ShotGrid parameters require a `dict`, we want to "unpack" the list of items given into individual arguments. This can be done using the `*` notation.
4. Return the result as a string.

```python title="shotgrid_tool/tool.py" hl_lines="16-25"
# ...
    def meta_method(self, params: dict) -> TextArtifact | ErrorArtifact:
        import shotgun_api3

        try:
            if self.login_method == "api_key":
                sg = shotgun_api3.Shotgun(
                    # ...
                )

            else:
                sg = shotgun_api3.Shotgun(
                    # ...
                )

            # Get the method name from the params
            sg_method = getattr(sg, params["values"]["method"])

            # Get the params from the params
            sg_params = params["values"]["params"]

            # Execute the method with the params
            sg_result = sg_method(*sg_params)

            return TextArtifact(str(sg_result))  # Return the results of the connection

        except Exception as e:
            # ...
# ...
```

### Test it out - Find

Let's perform a quick test. One good thing to do is list all the projects available to the current user.

Normally you'd have to figure out the filter for the `sg.find` command, but in our case we can simply ask the chatbot - "What projects do I have access to?"

!!! quote
    What projects do I have access to?

```text
User: What projects do I have access to?
processing...
[12/06/23 06:15:23] INFO     ToolkitTask 974a92cff534416ea06eda9c21519461                                            
                             Input: What projects do I have access to?                                               
[12/06/23 06:15:36] INFO     Subtask c6d98edf1bab48e9a7fc0e4f7e151f73                                                
                             Thought: To find out what projects the user has access to, I need to use the            
                             ShotGridTool action with the "find" method. The "find" method will return all the       
                             projects that the user has access to.                                                   
                                                                                                                     
                             Action:                                                                                 
                             {                                                                                       
                               "name": "ShotGridTool",                                                               
                               "path": "meta_method",                                                                
                               "input": {                                                                            
                                 "values": {                                                                         
                                   "method": "find",                                                                 
                                   "params": ["Project", [], ["id", "name"]]                                         
                                 }                                                                                   
                               }                                                                                     
                             }                                                                                       
[12/06/23 06:15:56] INFO     Subtask c6d98edf1bab48e9a7fc0e4f7e151f73                                                
                             Response: [{'type': 'Project', 'id': 63, 'name': 'Start From Scratch'}, {'type':        
                             'Project', 'id': 69, 'name': 'Motion Capture Template'}, {'type': 'Project', 'id': 70,  
                             'name': 'Demo: Animation'}, {'type': 'Project', 'id': 72, 'name': 'Demo: Game'},        
                             {'type': 'Project', 'id': 78, 'name': 'Game Template'}, {'type': 'Project', 'id': 82,   
                             'name': 'Film VFX Template'}, {'type': 'Project', 'id': 83, 'name': 'Episodic TV        
                             Template'}, {'type': 'Project', 'id': 85, 'name': 'Demo: Animation with Cuts'}, {'type':
                             'Project', 'id': 86, 'name': 'Game Outsourcing Template'}, {'type': 'Project', 'id': 87,
                             'name': 'Demo: Automotive'}, {'type': 'Project', 'id': 88, 'name': 'Automotive Design   
                             Template'}, {'type': 'Project', 'id': 89, 'name': 'Animation Template'}]                
[12/06/23 06:16:05] INFO     ToolkitTask 974a92cff534416ea06eda9c21519461                                            
                             Output: You have access to the following projects:                                      
                             1. Start From Scratch                                                                   
                             2. Motion Capture Template                                                              
                             3. Demo: Animation                                                                      
                             4. Demo: Game                                                                           
                             5. Game Template                                                                        
                             6. Film VFX Template                                                                    
                             7. Episodic TV Template                                                                 
                             8. Demo: Animation with Cuts                                                            
                             9. Game Outsourcing Template                                                            
                             10. Demo: Automotive                                                                    
                             11. Automotive Design Template                                                          
                             12. Animation Template                                                                  
Assistant: You have access to the following projects: 
1. Start From Scratch
2. Motion Capture Template
3. Demo: Animation
4. Demo: Game
5. Game Template
6. Film VFX Template
7. Episodic TV Template
8. Demo: Animation with Cuts
9. Game Outsourcing Template
10. Demo: Automotive
11. Automotive Design Template
12. Animation Template
```

Notice how you didn't need to know how to build the filter, figure out which ShotGrid method to use, or anything. The LLM figured it out for you.

Let's look at this section of the output:

```json
Thought: To find out what projects the user has access to, I need to use the            
ShotGridTool action with the "find" method. The "find" method will return all the       
projects that the user has access to.                                                   
                                                                                        
Action:                                                                                 
{                                                                                       
"name": "ShotGridTool",                                                               
"path": "meta_method",                                                                
"input": {                                                                            
    "values": {                                                                         
    "method": "find",                                                                 
    "params": ["Project", [], ["id", "name"]]                                         
    }                                                                                   
}                                                                                     
}                                                                                       

```

See how the LLM realized it needed to use the `find` method, and it created its own list of parameters to pass!

### Test it out - Create

Let's run through another example. In this case, we're going to create a new asset in one of our projects. I'll call this one "Bob" and give him a description. Be creative - come up with your own character name.

The prompt we'll give will simply be to tell it what project we want to add the asset in, what to name the character and a bit of a description.

!!! quote
    Create a new character asset for me in "Demo: Animation with Cuts". Make it named "Bob" and give it a description "Bob is a legendary hula-hoop dancer"

```text
User: Create a new character asset for me in "Demo: Animation with Cuts". Make it named "bob" and give it a description "bob is a legendary hula-hoop dancer"
processing...
[12/06/23 06:35:33] INFO     ToolkitTask 974a92cff534416ea06eda9c21519461                                            
                             Input: Create a new character asset for me in "Demo: Animation with Cuts". Make it named
                             "bob" and give it a description "bob is a legendary hula-hoop dancer"                   
[12/06/23 06:35:44] INFO     Subtask ae5a4f62df2c4b24b99170350fcd5cd8                                                
                             Thought: To create a new character asset, I need to use the ShotGridTool action with the
                             "create" method. But first, I need to find the id of the "Demo: Animation with Cuts"    
                             project.                                                                                
                                                                                                                     
                             Action: {"name": "ShotGridTool", "path": "meta_method", "input": {"values": {"method":  
                             "find_one", "params": ["Project", [["name", "is", "Demo: Animation with Cuts"]],        
                             ["id"]]}}}                                                                              
[12/06/23 06:35:47] INFO     Subtask ae5a4f62df2c4b24b99170350fcd5cd8                                                
                             Response: {'type': 'Project', 'id': 85}                                                 
[12/06/23 06:36:02] INFO     Subtask b8e1809356864a68a11144692e6823a4                                                
                             Thought: Now that I have the project id, I can use it to create a new character asset   
                             named "bob" with the description "bob is a legendary hula-hoop dancer".                 
                             Action: {"name": "ShotGridTool", "path": "meta_method", "input": {"values": {"method":  
                             "create", "params": ["Asset", {"project": {"type": "Project", "id": 85}, "code": "bob", 
                             "description": "bob is a legendary hula-hoop dancer", "sg_asset_type": "Character"}]}}} 
[12/06/23 06:36:04] INFO     Subtask b8e1809356864a68a11144692e6823a4                                                
                             Response: {'id': 1412, 'project': {'id': 85, 'name': 'Demo: Animation with Cuts',       
                             'type': 'Project'}, 'code': 'bob', 'description': 'bob is a legendary hula-hoop dancer',
                             'sg_asset_type': 'Character', 'type': 'Asset'}                                          
[12/06/23 06:36:10] INFO     ToolkitTask 974a92cff534416ea06eda9c21519461                                            
                             Output: I have created a new character asset named "bob" with the description "bob is a 
                             legendary hula-hoop dancer" in the "Demo: Animation with Cuts" project. The asset id is 
                             1412.                                                                                   
Assistant: I have created a new character asset named "bob" with the description "bob is a legendary hula-hoop dancer" in the "Demo: Animation with Cuts" project. The asset id is 1412.
```

There were some really interesting things that happened in this test!

First, the LLM realized it needed the project ID to create a new asset - but it wasn't provided with the ID. So it performed a `find_one` method first to get the ID.

```json
Thought: To create a new character asset, I need to use the ShotGridTool action with the
"create" method. But first, I need to find the id of the "Demo: Animation with Cuts"    
project.                                                                                

Action: {
    "name": "ShotGridTool", 
    "path": "meta_method", 
    "input": {
        "values": {
            "method":  "find_one",
            "params": [
                "Project", 
                    [["name", "is", "Demo: Animation with Cuts"]],
                    ["id"]
                ]
            }
        }
    }                                                                              

```

Then, once it had the ID it could use the `create` method.
Of course, it also returned valuable information we could then use to perform more actions, including the asset ID. Also, if you check on the frontend you can see the asset was indeed created with the description _and_ the name of the person who created it.

![Asset Created](assets/img/shotgrid_asset_created.png)

## Code Review

This was a short, but powerful step. We've modified our ShotGridTool to be able to use the ShotGrid API to execute any method available to it! Let's review the changes in `shotgrid_tool/tool.py`.

```python PYTEST_CHECK linenums="1" title="shotgrid_tool/tool.py" hl_lines="31-43 46 64-73"
from __future__ import annotations
from griptape.artifacts import TextArtifact, ErrorArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import define, field


@define
class ShotGridTool(BaseTool):
    """
    Parameters:
        base_url: Base URL for your your ShotGrid site
        script_name: The name for your script
        api_key: The script API key, given to you by ShotGrid
        user_login: The user login name if login_method is "user"
        user_password: The user password if login_method is "user"
        login_method: "api_key" or "user" - depending on the mode of login we want

    """

    base_url: str = field(default=str, kw_only=True)
    script_name: str = field(default=str, kw_only=True)
    api_key: str = field(default=str, kw_only=True)
    user_login: str = field(default=str, kw_only=True)
    user_password: str = field(default=str, kw_only=True)
    login_method: str = field(default="api_key", kw_only=True)

    @activity(
        config={
            "description": "Can be used to execute ShotGrid methods.",
            "schema": Schema(
                {
                    Literal(
                        "method",
                        description="Shotgrid method to execute. Example: find_one, find, create, update, delete, revive, upload_thumbnail",
                    ): str,
                    Literal(
                        "params",
                        description="Dictionary of parameters to pass to the method.",
                    ): list,
                }
            ),
        }
    )
    def meta_method(self, params: dict) -> TextArtifact | ErrorArtifact:
        import shotgun_api3

        try:
            if self.login_method == "api_key":
                sg = shotgun_api3.Shotgun(
                    self.base_url,  # ShotGrid url
                    script_name=self.script_name,  # Name of the ShotGrid script
                    api_key=self.api_key,  # ShotGrid API key
                )

            else:
                sg = shotgun_api3.Shotgun(
                    self.base_url,  # ShotGrid url
                    login=self.user_login,  # User login
                    password=self.user_password,  # User password
                )

            # Get the method name from the params
            sg_method = getattr(sg, params["values"]["method"])

            # Get the params from the params
            sg_params = params["values"]["params"]

            # Execute the method with the params
            sg_result = sg_method(*sg_params)

            return TextArtifact(str(sg_result))  # Return the results of the connection

        except Exception as e:
            return ErrorArtifact(str(e))
```

---
## Next Steps
This has been a powerful step - we can do so much now! However, the current implementation relies on the LLM having been trained on data about the ShotGrid API. What if there wasn't much knowledge about it, or if the API has been updated? In the [next section](08_vectorized_docs.md), we'll provide the Agent access to the current API docs for it to use as a reference to enhance its abilities.