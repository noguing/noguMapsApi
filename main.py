from fastapi import FastAPI, status, HTTPException
from pymongo import MongoClient
from loguru import logger

import config

tags_metadata = [
    {
        "name": "来搞笑的",
        "description": "tag的描述"
    },
    {
        "name": "单铺面查询",
        "description": "通过sid或bid查询单个铺面"
    },
    {
        "name": "多铺面查询",
        "description": "还没有"
    }
]

logger.info("初始化FastAPI")
app = FastAPI(title="NoguMapsApi",
              description="一个没人用的铺面搜索api",
              openapi_url="/api/openapi.json",
              docs_url="/api/docs",
              redoc_url=None,
              version="0.0.1.22420_alpha",
              terms_of_service="没有官网😅",
              contact={
                  "name": "FrZ",
                  "email": "adsicmes@foxmail.com"
              },
              openapi_tags=tags_metadata
              )


def connect_to_mongodb():
    try:
        logger.info("尝试登入mongodb")
        if (config.user is None and config.password is None) or \
                (config.user == "" and config.password == ""):
            # 无密码连接
            logger.info("config中没有填写用户名与密码，采用无密码连接")
            mongo_client = MongoClient(
                f"mongodb://{config.host}:{config.port}/")
        else:
            logger.info("在config中检测到用户名与密码，采用无密码连接")
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


@app.get("/",
         status_code=status.WS_1013_TRY_AGAIN_LATER,
         summary="sb😅😅😅",
         description="屁用没有",
         tags=["来搞笑的"],
         response_description="傻逼，看你吗呢"
         )
async def root():
    return {
        "message": "Fuck You. Damn."
    }


@app.get("/beatmapset/{sid}",
         status_code=status.HTTP_200_OK,
         summary="按sid查询铺面",
         description="返回ppyApiV2格式json",
         tags=["单铺面查询"],
         response_description="请求成功"
         )
async def query_beatmapsets(sid: int):
    logger.info("")
    result: dict = db.find_one({"id": sid})
    if result is not None:
        del result["_id"]
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beatmapset not found!")


@app.get("/beatmap/{bid}",
         status_code=status.HTTP_200_OK,
         summary="按bid查询铺面",
         description="返回ppyApiV2格式json",
         tags=["单铺面查询"],
         response_description="请求成功"
         )
async def query_beatmap(bid: int):
    result: dict = db.find_one({"beatmaps.id": bid})
    if result is not None:
        del result["_id"]
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beatmap not found!")
