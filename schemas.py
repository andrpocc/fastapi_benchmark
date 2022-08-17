from datetime import datetime

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class GGAIn(BaseModel):
    login: str
    start: datetime
    end: datetime


class GGaOut(BaseModel):
    session: str
    h: float
    b: float
    l: float

    class Config:
        orm_mode = True


class GGaOutOrjson(BaseModel):
    session: str
    h: float
    b: float
    l: float

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        orm_mode = True
