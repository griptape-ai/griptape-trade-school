# Learn Griptape Workflows through Cinematic Comparison

## Course Description
Griptape Workflows allow you to create complicated parent-child task relationships, where one task won't begin until all it's parent tasks have completed. Using movie narratives as our backdrop, you'll gain practical experience in establishing inter-task connections and seeing how they collaboratively weave a coherent story. Ideal for those keen on understanding the intricacies of Griptape's Workflows while engaging in a compelling thematic exploration.

## What you will create
Below you can see a representation of the workflow graph we will create in the course, where you will pass rough descriptions of movies, then for each movie a series of tasks will be executed:

1. Get the actual name of the movie.
2. Search the web and get a very short description of the movie.
    
Finally, once all tasks are finished, a final comparison task will be executed of the three movies and output the results.


``` mermaid
graph TB
    A["<h4>Workflow</h4>
    Given some rough movie descriptions,
    describe their similarities.
    <br>"] --> AB(["A boy finds an alien"]):::Result
    AB --> B("<b>PromptTask</b>: Get Name"):::PromptTask
    
    A --> AC(["Black and white movie turns color"]):::Result
    AC --> C("<b>PromptTask</b>: Get Name"):::PromptTask

    A --> AD(["Kid suddenly becomes big"]):::Result
    AD --> D("<b>PromptTask</b>: Get Name"):::PromptTask

    K("<b>PromptTask</b>: Compare Movies"):::PromptTask
    subgraph movie 1 [" "]
    B --> BE([E.T.]):::Result
    BE --> E("<b>ToolkitTask</b>: Get Description"):::ToolkitTask
    E --> HK(["A troubled child summons the 
        courage to help a friendly alien ..."]):::Result
    end

    subgraph movie 2 [" "]
    C --> CF([Wizard of Oz]):::Result
    CF --> F("<b>ToolkitTask</b>: Get Description"):::ToolkitTask
    F --> IK(["A classic film from 1939 in which young      
        Dorothy Gale and her dog Toto ..."]):::Result

    end
    subgraph movie 3 [" "]
    D --> CG([Big]):::Result
    CG --> G("<b>ToolkitTask</b>: Get Description"):::ToolkitTask
    G --> JK(["After wishing to be made big, 
        a teenage boy wakes ..."]):::Result
    end
    HK ---> K
    IK ---> K
    JK ---> K

    K --> L(["All three movies:
    <i>E.T. the Extra-Terrestrial</i>,<i>The Wizard of Oz</i>,and <i>Big</i>, 
            share a common theme of fantastical journeys and adventures.    
            They all involve characters who are thrust into extraordinary 
            circumstances that are far removed from their normal lives."]):::Result

    classDef PromptTask stroke:#A00
    classDef ToolkitTask stroke:#0A0
    classDef Result fill:#555,stroke:#555

```

## Who is this course for?
This course is aimed at **intermediate** level Python developers who are interested in learning about Griptape Workflows and how to handle parent/child task relationships. 

## Prerequisites
Before beginning this course, you will need:

- An OpenAI API Key (available here: https://beta.openai.com/account/api-keys)
- Python3.9+ installed on your machine
- An IDE (such as Visual Studio Code or PyCharm) to write and manage your code

If you don't have those items available, it's highly recommended you go through the [Griptape Setup - Visual Studio Code](../../setup/index.md) course to set up your environment.

## Course Outline
The course will cover:

* Creating your first workflow
* Making it scalable
* Handling inputs with Jinja2 templates
* Using the WebScraper tool
* Understanding Workflow Outputs

## Useful Resources
These resources will provide additional information and context throughout the course:

- [Griptape Documentation](https://github.com/griptape-ai/griptape)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/en/3.1.x/)


---
## Next Steps

Get yourself all setup and ready by moving on to [Setup](01_setup.md).