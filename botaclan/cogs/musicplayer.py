from discord.ext.commands import Cog, Bot, Context, group, CommandError
import botaclan.player.soundcloud as sc
import botaclan.player.spotify as sptf
import botaclan.player.youtube as yt
import discord
import logging


log = logging.getLogger(__name__)


class MusicPlayer(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(name="music")
    async def player_group(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(content="Player help here")

    @player_group.command(name="join", aliases=["j"])
    async def join(self, ctx: Context):
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @player_group.command(name="quit", aliases=["q", "leave"])
    async def quit(self, ctx: Context):
        await ctx.voice_client.disconnect()

    @player_group.command(name="play", aliases=["p"])
    async def play(self, ctx: Context, *, content: str):
        if yt.PROVIDER in content:
            async with ctx.typing():
                yt_song = yt.new_youtube_song(content, ctx)
                ctx.voice_client.play(
                    discord.PCMVolumeTransformer(yt_song.get_audio()),
                    after=lambda e: log.error("Player error: %s" % e) if e else None,
                )
            await ctx.send(embed=yt_song.get_message())
        if sc.PROVIDER in content:
            async with ctx.typing():
                sc_song = await sc.new_soundcloud_song(content, ctx)
                ctx.voice_client.play(
                    discord.PCMVolumeTransformer(await sc_song.get_audio()),
                    after=lambda e: log.error("Player error: %s" % e) if e else None,
                )
            await ctx.send(embed=sc_song.get_message())
        if sptf.PROVIDER in content:
            async with ctx.typing():
                sptf_song = sptf.new_spotify_song(content, ctx)
            await ctx.send(embed=sptf_song.get_message())

    @player_group.command(name="pause")
    async def pause(self, ctx: Context):
        ctx.voice_client.pause()

    @player_group.command(name="resume")
    async def resume(self, ctx: Context):
        ctx.voice_client.resume()

    @play.before_invoke
    async def ensure_voice(self, ctx: Context):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise CommandError("Author not connected to a voice channel.")
        else:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise CommandError("Bot is already in a voice channel.")


def setup(bot: Bot) -> None:
    """Load the MusicPlayer cog."""
    bot.add_cog(MusicPlayer(bot))
    log.info("Cog loaded: MusicPlayer")
