from vyper import v

v.set_env_prefix("botaclan")
v.set_env_key_replacer(".", "_")

v.bind_env("discord.guild")
v.bind_env("discord.token")

DISCORD_GUILD = v.get("discord.guild")
DISCORD_TOKEN = v.get("discord.token")
