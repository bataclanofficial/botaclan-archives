from vyper import v
import logging

v.set_env_prefix("botaclan")
v.set_env_key_replacer(".", "_")

v.bind_env("discord.guild")
v.bind_env("discord.token")
v.bind_env("log.level")

v.set_default("log.level", logging.INFO)

DISCORD_GUILD = v.get("discord.guild")
DISCORD_TOKEN = v.get("discord.token")
LOG_LEVEL = v.get_int("log.level")
