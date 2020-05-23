from botaclan.constants import (
    HEALTHCHECK_HOST,
    HEALTHCHECK_PORT,
    LOG_UVICORN_LEVEL,
)
import logging
import uvicorn


log = logging.getLogger(__name__)


def create_server() -> uvicorn.Server:
    config = uvicorn.Config(
        "botaclan.healthcheck.routes:app",
        host=HEALTHCHECK_HOST,
        log_config=None,
        log_level=LOG_UVICORN_LEVEL,
        loop="asyncio",
        port=HEALTHCHECK_PORT,
    )
    return uvicorn.Server(config=config)
