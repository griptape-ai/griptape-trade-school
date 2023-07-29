## Stage 1: Setting up your environment

Welcome to the first step of our journey into creating a conversational chatbot! In this section, we will be focusing on setting up our work environment, which is an important aspect of any coding project. 

### 1.1 Prerequisites

Before we get started, please ensure you've gone through the [Griptape Setup - Visual Studio Code](../../../100/setup/index.md) course to set up your environment.

1. **Code Editor**: We recommend using **Visual Studio Code** for this course, due to its handy features and Python support. However, if you have another favorite IDE or text editor, feel free to use that! 

2. **Python3.10+**: In this course, we'll be using some features of Python that are only available in 3.10+ (`match` statements). When they come up, I'll mention alternatives for Python 3.9.

> Note: If you're more comfortable using Poetry over pip for managing Python dependencies, feel free to use that instead. It's a powerful tool that can handle dependency resolution and package management elegantly. If you decide to go this route, you can create your project and virtual environment in one command: `poetry new chatbot_project`, and then `use poetry shell` to activate the environment.

3. **Python Environment Manager (for VS Code users)**: This extension is not a hard requirement, but it does make managing your Python environments a lot easier. 

4. **OpenAI API Key**: Our chatbot will be powered by **gpt-3.5-turbo**, which requires an API key from OpenAI. You can get your key from [OpenAI's website](https://beta.openai.com/account/api-keys).

Got everything installed? Awesome! Now, let's get started setting up our project.

### 1.2 Create a Project

Following the instructions in [Griptape Setup - Visual Studio Code ](../../../100/setup/01_setting_up_environment.md) please:
1. Create your project folder. Example: `griptape-chatbot-with-rulesets-cli`
2. Set up your virtual environment
3. Ensure you `pip install griptape griptape-tools python-dotenv`
4. Create a `.env` file with your `OPENAI_API_KEY`
5. Create your `app.py` file with the following code:

```python
from dotenv import load_dotenv

load_dotenv()
```
---

And there we have it, our coding environment is all set up! In the next section [Step 2 - Create An Agent](02_create_an_agent.md), we'll start getting our hands dirty with some code. Stay tuned!