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

    base_url: str = field(factory=str, kw_only=True)
    script_name: str = field(factory=str, kw_only=True)
    api_key: str = field(factory=str, kw_only=True)
    user_login: str = field(factory=str, kw_only=True)
    user_password: str = field(factory=str, kw_only=True)
    login_method: str = field(default="api_key", kw_only=True)

    @activity(
        config={
            "description": "Can be used to execute ShotGrid methods.",
            "schema": Schema(
                {
                    Literal(
                        "sg_method_name",
                        description="Shotgrid method to execute. Example: find_one, find, create, update, delete, revive, upload_thumbnail",
                    ): str,
                    Literal(
                        "sg_params",
                        description="Dictionary of parameters to pass to the method.",
                    ): list[str],
                }
            ),
        }
    )
    def meta_method(self, sg_method_name: str, sg_params: list[str]) -> TextArtifact | ErrorArtifact:
        import shotgun_api3  # pyright: ignore[reportMissingImports]

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
            sg_method = getattr(sg, sg_method_name)

            # Execute the method with the params
            sg_result = sg_method(*sg_params)

            return TextArtifact(str(sg_result))  # Return the results of the connection

        except Exception as e:
            return ErrorArtifact(str(e))
