from __future__ import annotations
from griptape.artifacts import TextArtifact, ErrorArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import define


@define
class ReverseStringTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to reverse a string",
            "schema": Schema({Literal("input", description="The string to be reversed"): str}),
        }
    )
    def reverse_string(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        try:
            return TextArtifact(input_value[::-1])

        except Exception as e:
            return ErrorArtifact(str(e))

    @activity(
        config={
            "description": "Can be used to reverse a sentence",
            "schema": Schema({Literal("input", description="The sentence to be reversed"): str}),
        }
    )
    def reverse_sentence(self, params: dict) -> TextArtifact | ErrorArtifact:
        input_value = params["values"].get("input")

        try:
            # Splitting the sentence into words
            words = input_value.split()

            # Reversing the list of words
            reversed_words = words[::-1]

            # Joining the reversed words back into a sentence
            reversed_sentence = " ".join(reversed_words)

            return TextArtifact(reversed_sentence)

        except Exception as e:
            return ErrorArtifact(str(e))
