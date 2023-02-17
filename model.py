from pydantic import BaseModel


class PullTag(BaseModel):
    tag: str
    domain: str
    domain_id: str
    user_id: str


class PushTags(BaseModel):
    tag1: str
    tag2: str
    domain: str
    domain_id: str
    user_id: str
