from ast import alias
import discord
from discord.ext import commands
import os
from sys import platform
import youtube_dl

from youtube_dl import YoutubeDL
# TODO: this is lazy, and needs to be done in a better place
PROJECT_BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")

EXECUTABLE_FOLDER = os.path.join(PROJECT_BASE_DIR, "executables")

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn',
                  'executable': os.path.join(EXECUTABLE_FOLDER, "ffmpeg.exe") if platform == "win32"\
                                    else os.path.join(EXECUTABLE_FOLDER, "ffmpeg")}
YDL_OPTIONS = {'format': "bestaudio"}

class music(commands.Cog):
    def __init__(self, client):
        print(PROJECT_BASE_DIR)
        print(EXECUTABLE_FOLDER)
        self.client = client

        # all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None


    @classmethod
    async def get_youtube_audio(cls, song_url: str):
        """
        Get the audio file generated by FFMPEG executable

        :param song_url: Youtube url of the song to process
        :return: tuple of (audio file, song name, url used by ffmpeg executable for streaming)
        """
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(song_url, download=False)
            ffmpeg_url = info['formats'][0]['url']
            song_name = info['title']

            audio_source = await discord.FFmpegOpusAudio.from_probe(ffmpeg_url, **FFMPEG_OPTIONS)
            return (audio_source, song_name, ffmpeg_url)


    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Get into a voice channel first..")

        voice_channel = ctx.author.voice.channel
        self.client.current_channel = voice_channel
        bot_current_voice_channel = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        if not bot_current_voice_channel:
            if ctx.voice_client is None:
                self.vc = await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
                self.vc = ctx.voice_client

            # audio_source = music.fetch_audio_source(sound_bite='vine-boom.mp3')
            # if not vc.is_playing():
            #     vc.play(audio_source, after=None)
        else:
            # already connected
            pass


    # searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                # in case we fail to connect
                if self.vc is None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command()
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(
                    "Could not download the song. Incorrect format try another keyword. This could be due to playlist "
                    "or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])

                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command()
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command()
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command()
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            # try to play next in the queue if it exists
            await self.play_music(ctx)

    @commands.command()
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command()
    async def clear(self, ctx):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")

    @commands.command()
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()


async def setup(client):
    await client.add_cog(music(client))
