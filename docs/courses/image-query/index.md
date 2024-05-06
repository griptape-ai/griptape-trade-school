# An ImageQuery SEO Bonanza!

## Course Description
Today, we’re going to create something useful for anyone juggling digital content: a Griptape workflow that processes a directory full of images, and outputs a text file for each. These aren't just any text files—they're packed with things like SEO descriptions, keywords, alt-text, captions, and even a HTML snippet. If you don’t know what any of that means – that’s totally fine, I might’ve had to research some terms myself. 

By the end of this course, you'll be able to easily and quickly generate cards like these, and a bunch of helpful tags, keywords, and more.

![Vintage beach scene with beach umbrella and sandcastle](assets/example_img.png)




### What is SEO?
First, let’s talk about SEO, which stands for **Search Engine Optimization**. Don’t get this confused with the *Spaghetti Enthusiast Organization*. That route will lead to very different pasta-bilities. The real SEO is the art of tweaking your content so that it’s more understandable and attractive to search engines like Google. Why is this important? Well, good SEO can make the difference between your content remaining unseen and it reaching the wide audience it deserves. 

### Using an LLM
By using an LLM, or Large Language Model, to automate this, we're not just saving heaps of time; we're also harnessing sophisticated AI to generate nuanced and effective text that can boost your search rankings. The file bellow is an example of the type of data you'll be able to generate automatically, simply by asking your script to evaluate an image.

```yaml title="beach.yml"
title: Nostalgic Beach Scene
image_path: ./images/beach.png
description: |
A nostalgic beach scene with a vintage filter, featuring a large beach umbrella, a detailed sandcastle, and beachgoers engaged in typical seaside activities.
alt_text: Vintage beach scene with beach umbrella and sandcastle
keywords: ["beach", "vintage", "sandcastle"]
caption: A nostalgic day at the beach with friends and family.
example_html: |
    <div class="col">
        <div class="card shadow">
        <img src="./images/beach.png" class="card-img-top h-50" style="object-fit: cover" alt="Vintage beach scene with beach umbrella and sandcastle">
        <div class="card-body">
            <h5 class="card-title fw-light fs-5">Nostalgic Beach Scene</h5>
            <p class="card-subtitle fw-light text-body-secondary opacity-75">A nostalgic day at the beach with friends and family.</p>
        </div>
        <footer class="card-footer text-size-sm">
            <a href="#beach" class="btn btn-outline btn-sm">#beach</a>
            <a href="#vintage" class="btn btn-outline btn-sm">#vintage</a>
            <a href="#sandcastle" class="btn btn-outline btn-sm">#sandcastle</a>
        </footer>
        </div>
    </div>
```

So, stick around as we dive into how this Griptape workflow can transform your digital assets into SEO gold, making your content work smarter, not harder.

## Who is this course for

* **Intermediate-Level Python Developers**: If you have a solid grounding in Python and are looking to broaden your skill set, this course will introduce you to the exciting world of Griptape Tools. It's perfect for those who want to learn how to develop and implement these tools in various contexts, adding a valuable dimension to their programming expertise.

* **Web Developers**: People interested in speeding up their web development process and would like to automate some really repetitive and somewhat complicated tasks.

## Prerequisites
Before beginning this course, you will need:

- An OpenAI API Key (available from [OpenAI's website](https://beta.openai.com/account/api-keys){target="_blank"})
- Python3.11+ installed on your machine
- An IDE (such as Visual Studio Code or PyCharm) to write and manage your code

If you don't have those items available, it's highly recommended you go through the [Griptape Setup - Visual Studio Code](../../setup/index.md) course to set up your environment.

## Course Outline
The course will cover:

* Creating a simple Agent to chat with
* Using Griptape's ImageQuery Tool
* Controlling the output format
* Saving output to files
* Creating a Workflow to parallelize the actions
* Using a template for consistency of results

## Useful Resources and Links

- [Griptape Documentation](https://github.com/griptape-ai/griptape){target="_blank"}
- [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}
- [The Beginner's Guide to SEO](https://moz.com/beginners-guide-to-seo){target="_blank"}


---
## Next Steps

Get yourself all set up and ready by moving on to [Setup](01_setup.md).

