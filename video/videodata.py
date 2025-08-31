from pydantic.dataclasses import dataclass


@dataclass
class Song:
    name: str
    singer: str
    clip_path: str
    context_path: str
