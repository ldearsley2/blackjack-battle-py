from pydantic import BaseModel


class Connection(BaseModel):
    url: str