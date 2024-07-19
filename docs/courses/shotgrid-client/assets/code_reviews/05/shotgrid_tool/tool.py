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
    """

    base_url: str = field(default=str, kw_only=True)
    script_name: str = field(default=str, kw_only=True)
    api_key: str = field(default=str, kw_only=True)

    @activity(
        config={
            "description": "Can be used to get the active session token from ShotGrid",
        }
    )
    def get_session_token(self, _: dict) -> TextArtifact | ErrorArtifact:
        import shotgun_api3

        try:
            sg = shotgun_api3.Shotgun(
                self.base_url,  # ShotGrid url
                script_name=self.script_name,  # Name of the ShotGrid script
                api_key=self.api_key,  # ShotGrid API key
            )
            return TextArtifact(
                sg.get_session_token()
            )  # Return the results of the connection

        except Exception as e:
            return ErrorArtifact(str(e))