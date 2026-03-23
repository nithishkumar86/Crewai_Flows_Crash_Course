from pydantic import BaseModel


class BlogState(BaseModel):
    topic: str = ""
    blog: str = ""
    feedback: str = ""
    approved: bool = False
    iteration: int = 0
    flow_id: str = ""