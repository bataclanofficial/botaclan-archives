from fastapi import FastAPI
from botaclan.constants import (
    HEALTHCHECK_HOST,
    HEALTHCHECK_PORT,
    LOG_UVICORN_LEVEL,
)
import uvicorn
import logging

log = logging.getLogger(__name__)
app = FastAPI()


def create_server():
    config = uvicorn.Config(
        "botaclan.healthcheck.server:app",
        host=HEALTHCHECK_HOST,
        log_config=None,
        log_level=LOG_UVICORN_LEVEL,
        loop="asyncio",
        port=HEALTHCHECK_PORT,
    )
    return uvicorn.Server(config=config)


@app.get("/")
def read_root():
    return "Nothing to be found here"
