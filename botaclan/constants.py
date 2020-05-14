from vyper import v
import logging

v.set_env_prefix("botaclan")
v.set_env_key_replacer(".", "_")

v.bind_env("command.prefix")
v.bind_env("discord.guild.id")
v.bind_env("discord.token")
v.bind_env("feature.roulette")
v.bind_env("log.level")

v.set_default("command.prefix", "~b ")
v.set_default("feature.roulette", True)
v.set_default("log.level", logging.INFO)

COMMAND_PREFIX = v.get_string("command.prefix")
DISCORD_GUILD_ID = v.get_int("discord.guild.id")
DISCORD_TOKEN = v.get_string("discord.token")
FEATURE_ROULETTE = v.get_bool("feature.roulette")
LOG_LEVEL = v.get_int("log.level")
