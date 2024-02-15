from typing import TypedDict, Literal
import json

Role = Literal["system", "user", "assistant"]
CodeResponseError = Literal["LanguageNotRecognizedError", "NoCodeRequestedError"]

class Message(TypedDict):
    role: Role
    content: str

class CodeFunctions(TypedDict):
    main_code: str
    unit_tests: str

class CodeResponse(TypedDict):
    language: str
    code: CodeFunctions
    Error: CodeResponseError


def parse_json(message: Message):
    return json.loads(message["content"].strip())