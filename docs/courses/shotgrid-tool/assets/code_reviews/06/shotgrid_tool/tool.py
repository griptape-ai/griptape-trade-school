from __future__ import annotations
from griptape.artifacts import TextArtifact, ErrorArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
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

    base_url: str = field(default=str, kw_only=True)
    script_name: str = field(default=str, kw_only=True)
    api_key: str = field(default=str, kw_only=True)
    user_login: str = field(default=str, kw_only=True)
    user_password: str = field(default=str, kw_only=True)
    login_method: str = field(default="api_key", kw_only=True)

    @activity(
        config={
            "description": "Can be used to get the active session token from ShotGrid",
        }
    )
    def get_session_token(self, _: dict) -> TextArtifact | ErrorArtifact:
        import shotgun_api3

        try:
            if self.login_method == "api_key":
                print("Logging in with API Key")
                sg = shotgun_api3.Shotgun(
                    self.base_url,  # ShotGrid url
                    script_name=self.script_name,  # Name of the ShotGrid script
                    api_key=self.api_key,  # ShotGrid API key
                )

            else:
                print("Logging in as a User")
                sg = shotgun_api3.Shotgun(
                    self.base_url,  # ShotGrid url
                    login=self.user_login,  # User login
                    password=self.user_password,  # User password
                )

            return TextArtifact(sg.get_session_token())  # Return the results of the connection

        except Exception as e:
            return ErrorArtifact(str(e))
