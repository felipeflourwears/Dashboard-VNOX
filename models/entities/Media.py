from dataclasses import dataclass

@dataclass
class Media:
    id: int
    title: str
    size: int
    tags: list