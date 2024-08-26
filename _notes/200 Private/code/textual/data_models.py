from pydantic import BaseModel

class AIResponse(BaseModel):
    name: str
    url: str
    topic: str

class AIResponseList(BaseModel):
    responses: list[AIResponse]
