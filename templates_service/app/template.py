from pydantic import BaseModel

class CreateTemplateModel(BaseModel):
    title: str
    body: str

class Template:
    def __init__(self, id: int, title: str, body: str) -> None:
        self.id = id
        self.title = title
        self.body = body