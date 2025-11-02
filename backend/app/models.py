from datetime import date
from uuid import UUID
from pydantic import BaseModel

class UserDetails(BaseModel):
    user_name: str
    name: str                                                                

class WatchlistDetails(BaseModel):
    title: str
    url: str
    deadline: date
