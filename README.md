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

This package explicitly does not include Griptape so that it can be specified when running tests in the workflow

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
- Create a local .env file
    ```
    OPENAI_API_KEY=OP3NAI4PI-K3Y-1234567890ABCDEFG
    SHOTGRID_API_KEY=SGAPI-K3Y-0987654321ZYXWVUTS
    SHOTGRID_URL=https://your-shotgrid-name.shotgrid.autodesk.com
    SHOTGRID_USER=your_username@email
    SHOTGRID_PASSWORD=supersecretpassword123
    ```
- Run the following command
    ```
    act -P ubuntu-latest=catthehacker/ubuntu:act-latest --secret-file .env
    ```
