from botaclan.constants import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from discord import FFmpegPCMAudio, Embed
from discord.ext.commands import Context
from humanfriendly import format_timespan
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Dict, List
import botaclan
import discord
import spotify
import spotipy


PROVIDER = "spotify"
PROVIDER_FRIENDLY = "Spotify"

OPTIONS_FFMPEG = {"options": "-vn"}


class SpotifySong:
    ctx: Context
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

    def __init__(self, track: spotify.Track, ctx: Context):
        self.ctx = ctx
        self.track = track
        self.artists = convert_artists_to_markdown_string(track.get("artists"))
        self.duration_seconds, _ = divmod(track.get("duration_ms"), 1000)
        self.name = track.get("name")
        self.thumbnail = track.get("album").get("images")[0].get("url")
        self.uri = track.get("uri")
        self.url = track.get("external_urls").get("spotify")

    def get_message(self) -> Embed:
        return (
            Embed(
                title=self.name,
                url=self.url,
                description=self.artists,
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
                value="\n".join([f":timer: {format_timespan(self.duration_seconds)}"]),
            )
        )

    def get_audio(self) -> FFmpegPCMAudio:
        return FFmpegPCMAudio(self.stream_url, **OPTIONS_FFMPEG)


def new_spotify_song(url, ctx: Context) -> SpotifySong:
    spotipy_session = get_spotipy_session(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    track = spotipy_session.track(url)
    return SpotifySong(track, ctx)


def get_pyspotify_session(client_id: str, client_secret: str) -> spotify.Session:
    config = spotify.Config()
    config.user_agent = f"{botaclan.__name__} {botaclan.__version__}"

    session = spotify.Session(config)
    session.login(client_id, client_secret)
    session.preferred_bitrate(spotify.Bitrate.BITRATE_320k)
    return session


def get_spotipy_session(client_id: str, client_secret: str) -> spotipy.Spotify:
    creds = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=creds)


def convert_artists_to_markdown_string(artists: List[Dict]) -> str:
    markdown_artists = []
    for artist in artists:
        name = artist.get("name")
        url = artist.get("external_urls").get("spotify")
        markdown_artists.append((f"[{name}]({url})"))
    return ",".join(markdown_artists)
