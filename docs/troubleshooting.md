# Troubleshooting

This page will offer solutions to problems that people have run into. If the solution to your problem isn't here, please feel free to submit a [bug](https://github.com/griptape-ai/griptape-trade-school/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=), or chat with us on [Discord](https://discord.gg/gnWRz88eym).

## No module named griptape.core

If you are seeing certain errors relating to Griptape modules not being available, it may be an issue with your Griptape installation. 

![No module named griptape.core](assets/img/troubleshooting/module_not_found.png)

To resolve this, try the following steps:

1. Open a Terminal in your editor.
2. Using `pip`, *uninstall* Griptape.
    ``` bash
    pip uninstall griptape -y
    ```
3. *Reinstall* Griptape.
    ``` bash
    pip install griptape -y
    ```

This should clean up any install issues and allow you to use Griptape with the latest version.

