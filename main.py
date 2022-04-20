from typing import Any, Mapping

from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import config
from loguru import logger

logger.info("初始化FastAPI")
app = FastAPI()


def connect_to_mongodb():
    try:
        logger.info("尝试登入mongodb")
        if (config.user is None and config.password is None) or \
                (config.user == "" and config.password == ""):
            # 无密码连接
            logger.info("config.json中没有填写用户名与密码，采用无密码连接")
            mongo_client = MongoClient(
                f"mongodb://{config.host}:{config.port}/")
        else:
            logger.info("在config.json中检测到用户名与密码，采用无密码连接")
            # 有密码连接
            mongo_client = MongoClient(
                f"mongodb://{config.user}:{config.password}@{config.host}:{config.port}/")

        logger.info(f"链接信息:\n{mongo_client.server_info()}")

        logger.info(f"接入数据库{config.database}")
        mongo_db = mongo_client[config.database]
        logger.info(f"接入表{config.collection}")
        mongo_collection = mongo_db[config.collection]
        return mongo_collection
    except Exception as e:
        logger.error(f"接入失败\n{e}")
        exit(0)


logger.info("连接mongodb")
db = connect_to_mongodb()


@app.get("/")
async def root():
    return {
        "message": "Fuck You. Damn."
    }


@app.get("/beatmapset/{sid}", status_code=status.HTTP_200_OK)
async def query_beatmapsets(sid: int, response: Response):
    result: dict = db.find_one({"id": sid})
    if result is not None:
        del result["_id"]
        return result
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": 404}


@app.get("/beatmap/{bid}", status_code=status.HTTP_200_OK)
async def query_beatmap(bid: int, response: Response):
    result: dict = db.find_one({"beatmaps.id": bid})
    if result is not None:
        del result["_id"]
        return result
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": 404}
