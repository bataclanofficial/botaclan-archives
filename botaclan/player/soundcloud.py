from botaclan.constants import SOUNDCLOUD_CLIENT_ID
from discord import FFmpegPCMAudio, Embed
from discord.ext.commands import Context
from humanfriendly import format_timespan, format_number
from sclib.asyncio import SoundcloudAPI, Track
import discord


PROVIDER = "soundcloud"
PROVIDER_FRIENDLY = "Soundcloud"
OPTIONS_FFMPEG = {"options": "-vn"}


class SoundcloudSong:
    ctx: Context
    description: str
    duration: int
    friendly_duration: str
    likes: int
    stream_url: str
    thumbnail: str
    title: str
    uploader_url: str
    uploader: str
    url: str
    views: int

    def __init__(self, track: Track, ctx: Context):
        self.ctx = ctx
        self.track = track
        self.artwork = track.artwork_url
        self.description = track.description
        self.duration = track.duration
        self.duration_seconds, _ = divmod(track.duration, 1000)
        self.likes = track.likes_count
        self.plays = track.playback_count
        self.title = track.title
        self.uploader = track.user["username"]
        self.uploader_url = track.user["permalink_url"]
        self.url = track.permalink_url

    def get_message(self) -> Embed:
        return (
            Embed(
                title=self.title,
                url=self.url,
                description=f"[{self.uploader}]({self.uploader_url})",
                color=discord.Color.magenta(),
            )
            .set_footer(
                icon_url=self.ctx.message.author.avatar_url,
                text=(
                    f"{self.ctx.message.author.name}"
                    f" requested from {PROVIDER_FRIENDLY}"
                ),
            )
            .set_thumbnail(url=self.artwork)
            .add_field(
                name="Song stats",
                value="\n".join(
                    [
                        f":timer: {format_timespan(self.duration_seconds)}",
                        f":arrow_forward: {format_number(self.plays)} plays",
                        f":thumbsup: {format_number(self.likes)} likes",
                    ]
                ),
            )
        )

    async def get_audio(self) -> FFmpegPCMAudio:
        stream_url = await self.track.get_stream_url()
        return FFmpegPCMAudio(stream_url, **OPTIONS_FFMPEG)


async def new_soundcloud_song(url, ctx: Context) -> SoundcloudSong:
    api = SoundcloudAPI()
    api.client_id = SOUNDCLOUD_CLIENT_ID
    track = await api.resolve(url)
    assert type(track) is Track
    return SoundcloudSong(track, ctx)
