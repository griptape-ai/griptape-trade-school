# Griptape Trade School
Tutorials and Courses for [Griptape](https://github.com/griptape-ai/griptape).

# Notes when adding new courses
- Always put code in a folder called `code_reviews/` under the `docs` directory if you'd like it to be picked up by the tests
- You can insert python files into your docs with this notation:
    ````
    ```python linenums="1" title="app.py" hl_lines="11 74-77"
    --8<-- "docs/courses/chatbot-rulesets/assets/code_reviews/14/app.py"
    ```
    ````
    *Note:* Make sure the path is relative to the `base_dir` so in this case `docs`

## Some fun things we should look into for Snippets
- [Sections](https://github.com/squidfunk/mkdocs-material/discussions/4373)
- [Line Numbers](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/#snippet-lines)


# Run Tests Locally

This package explicitly does not include Griptape so that it can be specified when running tests in the workflow. It is installed with the `test` extra via poetry. If you need to update the version of griptape installed, then update the `pyproject.toml`

First copy `.env.example` to `.env` and fill out the keys required. Then run the following.

```
make install
```

```
make test
```

# Run GitHub Action locally

- Install [Act](https://github.com/nektos/act)
    ```
    brew install act
    ```

    For Windows use [choco](https://github.com/chocolatey/choco) instead of brew
    ```
    choco install act-cli
    ```
- Create a local `.env` file from the `.env.example` and fill out the keys required
- Run the following command
    ```
    act -P ubuntu-latest=catthehacker/ubuntu:act-latest --secret-file .env
    ```
