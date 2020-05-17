from fastapi import FastAPI
import botaclan.constants
import uvicorn
import logging

log = logging.getLogger(__name__)
app = FastAPI()


def create_server():
    config = uvicorn.Config(
        "botaclan.healthcheck.server:app",
        host=botaclan.constants.HEALTHCHECK_HOST,
        log_config=None,
        log_level=botaclan.constants.LOG_UVICORN_LEVEL,
        loop="asyncio",
        port=botaclan.constants.HEALTHCHECK_PORT,
    )
    return uvicorn.Server(config=config)


@app.get("/")
def read_root():
    return "Nothing to be found here"
