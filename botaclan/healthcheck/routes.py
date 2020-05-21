from botaclan.bot import Botaclan
from botaclan.constants import DISCORD_GUILD_ID
from fastapi import FastAPI, status, Response
import botaclan
import logging


log = logging.getLogger(__name__)
app = FastAPI(title=botaclan.__name__, version=botaclan.__version__)


@app.get("/")
async def read_root():
    return {"status": "Healthcheck server running"}


@app.get("/favicon.ico", status_code=status.HTTP_204_NO_CONTENT)
def ignore_favicon():
    pass


@app.get("/liveness", status_code=status.HTTP_200_OK)
async def read_liveness(response: Response):
    statuses = {"discord": healthcheck_discord(botaclan.bot.running_bot)}
    if not all(statuses.values()):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    log.debug(f"{statuses}")
    return statuses


def healthcheck_discord(bot: Botaclan) -> bool:
    return bot.get_guild(DISCORD_GUILD_ID) is not None
