from discord import FFmpegPCMAudio, Embed
from discord.ext.commands import Context
from humanfriendly import format_timespan, format_number
from typing import Dict
import discord
import youtube_dl


youtube_dl.utils.bug_reports_message = lambda: ""

PROVIDER = "youtube"
PROVIDER_FRIENDLY = "YouTube"

OPTIONS_FFMPEG = {"options": "-vn"}
OPTIONS_YOUTUBE_DL = {
    "audioformat": "mp3",
    "default_search": "auto",
    "extractaudio": True,
    "format": "bestaudio/best",
    "ignoreerrors": False,
    "logtostderr": False,
    "no_warnings": True,
    "nocheckcertificate": True,
    "noplaylist": True,
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "quiet": True,
    "restrictfilenames": True,
    "source_address": "0.0.0.0",
}


class YoutubeSong:
    ctx: Context
    data: Dict
    description: str
    dislikes: int
    duration_seconds: int
    likes: int
    stream_url: str
    thumbnail: str
    title: str
    uploader_url: str
    uploader: str
    url: str
    views: int

    def __init__(self, data: Dict, ctx: Context):
        self.ctx = ctx
        self.data = data
        self.description = data.get("description")
        self.dislikes = data.get("dislike_count")
        self.duration_seconds = int(data.get("duration"))
        self.likes = data.get("like_count")
        self.stream_url = data.get("url")
        self.thumbnail = data.get("thumbnail")
        self.title = data.get("title")
        self.uploader = data.get("uploader")
        self.uploader_url = data.get("uploader_url")
        self.url = data.get("webpage_url")
        self.views = data.get("view_count")

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
            .set_thumbnail(url=self.thumbnail)
            .add_field(
                name="Song stats",
                value="\n".join(
                    [
                        f":timer: {format_timespan(self.duration_seconds)}",
                        f":eye: {format_number(self.views)} views",
                        f":thumbsup: {format_number(self.likes)} likes",
                        f":thumbsdown: {format_number(self.dislikes)} dislikes",
                    ]
                ),
            )
        )

    def get_audio(self) -> FFmpegPCMAudio:
        return FFmpegPCMAudio(self.stream_url, **OPTIONS_FFMPEG)


def new_youtube_song(url, ctx: Context) -> YoutubeSong:
    with youtube_dl.YoutubeDL(OPTIONS_YOUTUBE_DL) as ytdl:
        data = ytdl.extract_info(url, download=False)
    if "entries" in data:
        data = data["entries"][0]
    return YoutubeSong(data, ctx)
