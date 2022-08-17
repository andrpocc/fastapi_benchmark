import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_utils.timing import add_timing_middleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.expressions import Q

import orm
import schemas
from models import GGAUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
add_timing_middleware(app, record=logger.info, prefix="app")

register_tortoise(
    app,
    config=orm.TORTOISE_ORM,
)


@app.post("/orm/model/default/", response_model=list[schemas.GGaOut])
async def get_by_orm_model_default(user: schemas.GGAIn):
    messages = await GGAUser.filter(name=user.login)
    return messages


@app.post("/orm/model/orjson/", response_model=list[schemas.GGaOutOrjson])
async def get_by_orm_model_orjson(user: schemas.GGAIn):
    messages = await GGAUser.filter(name=user.login)
    return messages


@app.post("/orm/values/response", response_model=list[schemas.GGaOutOrjson])
async def get_by_orm_response(user: schemas.GGAIn):
    messages = await GGAUser.filter(
        Q(name=user.login), Q(time__range=[user.start, user.end])
    ).values_list("session", "time", "h", "b", "l")
    return ORJSONResponse(content=messages)
