As with any project, the first step is setting up your environment. Let's get started by ensuring you have a project structure ready to work with.

### Prerequisites

!!! Tip "Important"
    Since this is an **intermediate level** course, please ensure you've gone through the [Griptape Setup - Visual Studio Code](../../setup/index.md) course to set up your environment. We will be starting from the code at that point.

1. **Code Editor**: We recommend using **Visual Studio Code** for this course, due to its handy features and Python support. However, if you have another favorite IDE or text editor, feel free to use that! 

2. **Python3.9+**: Griptape requires Python 3.9+.

3. **Python Environment Manager (for VS Code users)**: This extension is not a hard requirement, but it does make managing your Python environments a lot easier. 

4. **OpenAI API Key**: Our chatbot will be powered by **gpt-4**, which requires an API key from OpenAI. You can get your key from [OpenAI's website](https://beta.openai.com/account/api-keys).

Got everything installed? Awesome! Now, let's get started setting up our project.

### Create a Project

Following the instructions in [Griptape Setup - Visual Studio Code ](../../setup/01_setting_up_environment.md) please:

1. Create your project folder. Example: `griptape-compare-movies-workflow`
2. Set up your virtual environment
3. Ensure you `pip install griptape python-dotenv`
4. Create a `.env` file with your `OPENAI_API_KEY`
5. Create your `app.py` file with the following code:

```py title="app.py" linenums="1"
from dotenv import load_dotenv

load_dotenv() # Load your environment
```

---
## Next Steps
And there we have it, environment is all set up! In the next section [Concepts](02_concepts.md), we'll dive deeper into understanding the concepts of Pipelines, Workflows, and Tasks.