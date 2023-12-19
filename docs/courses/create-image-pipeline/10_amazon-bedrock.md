# Amazon Bedrock

## Overview

Amazon Bedrock offers a couple of different image generation models, and thus the method of using them is slightly different than DALL·E 3 and Leonardo.Ai.

Instead of just importing one driver, you import `AmazonBedrockImageGenerationDriver` and then the model driver: `AmazonBedrockStableDiffusionImageGenerationModelDriver` or `AmazonBedrockTitanImageGenerationModelDriver`.

We'll get into the specifics, but first it's important to ensure you have access to Amazon Bedrock, as it's a requirement to use either of these two models.

### AWS Access

* Ensure you have an AWS account
* Ensure you have access to the appropriate model by following the [Amazon Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html){target="_blank"}
* Add the following environment variables to your `.env` file:
    * `AWS_REGION_NAME`
    * `AWS_ACCESS_KEY_ID`
    * `AWS_SECRET_ACCESS_KEY`

### boto3

You'll need to use `boto3` to access Amazon Bedrock. 

To install `boto3` by going to your terminal inside Visual Studio Code and:

* If using `pip`, type:
    ```bash
    pip install boto3
    ```
* If using `poetry` type:
    ```bash
    poetry add boto3
    ```

## Import

Let's import boto3, os, and all three drivers, and then we'll discuss their differences.

In your `app.py` imports section, add the three drivers:

```python
# ...

import boto3
import os

# ...

from griptape.drivers import (
    AmazonBedrockImageGenerationDriver,
    AmazonBedrockStableDiffusionImageGenerationModelDriver,
    AmazonBedrockTitanImageGenerationModelDriver
)

# ...

```

## Create a session

You will need a `boto3` session to pass to `AmazonBedrockImageGenerationDriver`. I recommend you create this after the `# Variables` section of your code:

```python
# ...

# Boto3
session = boto3.Session(
    region_name=os.getenv("AWS_REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

# ...
```

## Image Driver

To create the Image Driver, you're going to specify three attributes:

* `session` : This is the boto3 session you created earlier.
* `model` : This is the particular model you will be using. The list of models you have available to your account is in the AWS Console [here](https://us-east-1.console.aws.amazon.com/bedrock/modelaccess). Here are some examples you may have access to:
    * `amazon.titan-image-generator-v1`
    * `stability.stable-diffusion-xl-v0`
    !!! tip
        To get a list of all the models you have access to, you can add the following code after you defined `session`:
        ```python
        bedrock = session.client("bedrock")
        models = bedrock.list_foundation_models()
        for model in models["modelSummaries"]:
            if model["outputModalities"] == ["IMAGE"]:
                print(model["modelId"])    
        ```

        This will print a list of all models you should be able to use. 
* `image_generation_model_driver` : This is the specific Model Driver Class you imported above.

Here's an example of a simple driver using Stable Diffusion:

```python
image_driver = AmazonBedrockImageGenerationDriver(
    session=session,
    model="stability.stable-diffusion-xl-v0",
    image_generation_model_driver=AmazonBedrockStableDiffusionImageGenerationModelDriver(),
)
```

!!! important
    You must specify the correct `model` for the `image_generation_model_driver` you're using.

Below is the full list of attributes available.

```yaml
model: Bedrock model ID.
session: boto3 session.
bedrock_client: Bedrock runtime client.
image_width: Width of output images. Defaults to 512 and must be a multiple of 64.
image_height: Height of output images. Defaults to 512 and must be a multiple of 64.
seed: Optionally provide a consistent seed to generation requests, increasing consistency in output.
image_generation_model_driver: Image Generation Model Driver to use.
```



## Next Step
You now have a working pipeline for creating and displaying an image. Now we'll start taking a look at some of the options available to us with each of the Image Generation Drivers available in Griptape. 