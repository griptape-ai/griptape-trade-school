## Overview

Setting up our development environment correctly is vital for smooth and successful Python coding. In this stage, we'll go through all the necessary installations and configurations.

<iframe src="https://www.youtube.com/embed/saFi2Hztb4o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
## Installing Python

![python logo](assets/img/python.png){ align=right } Just like you need a solid board to skate on, we need the Python programming language to start our coding journey.

!!! info
    Griptape requires a minimum Python version of 3.9, but feel free to install a more recent version if you wish. 

### Windows or Linux

1. Head over to the [official Python downloads page](https://www.python.org/downloads/)
2. Click on the button that says "Python 3.9.x" (or the most recent 3.9 version) to download the installer
3. Run the installer, and make sure to check the box that says "Add Python 3.9 to PATH" before you click "Install Now"

### macOS

If you have [Homebrew](https://brew.sh) installed:

1. Open your terminal
2. Run the `command brew install python@3.9`
3. After the installation is complete, run brew link python@3.9

!!! info

    If you don't have Homebrew, you can install Python from the official website as mentioned above.
 

!!! success "You did it!"
    Congratulations, you've got Python!

## Visual Studio Code
### Installing 

A good skatepark provides the environment for perfecting your tricks. In the same way, Visual Studio Code (VS Code) provides the perfect environment for our Python coding.

1. Go to the [VS Code download page](https://code.visualstudio.com/Download)
2. Download the version appropriate for your OS (Windows, Linux, or macOS)
3. Run the installer and follow the prompts

!!! success
    VS Code is now installed!

### Creating the Project Folder
Before we dive into coding, let's create a dedicated space for our project. Like how skateboarders need a clean, flat area to skate, we need a clean, organized directory for our project.

First, you'll want to create a new folder on your computer where all the code for this project will live. You can create this folder anywhere you like. Here's how you can do it via your **Terminal**:

```bash
mkdir griptape-starter
cd griptape-starter
```

This creates a new folder called "griptape_intro" and moves into it.

Alternatively, feel free to open up **Visual Studio Code** and create a new folder:
1. Choose **File -> Open Folder..**
1. Choose **New Folder**
1. Enter the name of your new folder. Example: `griptape-starter`
1. Choose **Create**
1. Double-click on the newly created folder to open it.

## Virtual Environments 
### Using VS Code's Python Environment Manager

Python virtual environments are essential tools for keeping your projects organized and isolated. They allow each project to have its own set of dependencies, ensuring that different projects won't interfere with each other, which is vital when different projects require different versions of the same library. By using virtual environments, you can maintain a clean, conflict-free workspace for each project, making it easier to manage your code and troubleshoot any issues.

Many developers use their **terminal** to manage their Python virtual environments. As this is a beginner level course, we'll use an Extension inside VS Code instead because it makes this a little bit easier.

1. With VS Code open, go to the Extensions tab, or choose **View --> Extensions**
3. Search for `Python Environment Manager`, or go to [Python Environment Manager](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager) in your web browser.
4. Choose `Install`
5. Open the Command Palette (`Ctrl`+`Shift`+`P` on Windows/Linux, `Cmd`+`Shift`+`P` on macOS), or choose **View --> Command Palette..**
2. Search for `Python: Create Environment` and you should see it come up at the top of the command list.
    ![Alt text](assets/img/01_python_create_environment.png)

3. Hit **return** with that item selected and choose `.Venv: Creates a '.venv' virtual environment in the current workspace`

    ![Alt text](assets/img/01_venv.png)

4. Then choose a python version.

    ![Alt text](assets/img/01_picking_python.png)

    > Note: This will create the virtual environment for you within the current directory. 

    * This creates a new virtual environment in a folder called `.venv` and activates the environment for you.


Now you've set up your Python environment for this project. This way, anything you install or change in Python won't affect other projects.

### Confirm it's working

To be sure that your virtual environment is set up correctly, we'll check by opening a Terminal. If everything is set correctly, you'll see `.venv` in your terminal prompt.

1. Open the terminal in VS Code by clicking on `Terminal -> New Terminal`

![Alt text](assets/img/01_griptape-starter-terminal.png)

!!! Note
    You should see `.venv` in your prompt. If you don't see it, please run through the previous documentation to try again. 

----
## Next Step

You now have Python and VS Code installed, and you've got a working virtual environment! In the [next section](02_openai.md), we'll set up your OpenAI API key so you can communicate with their large language model. 