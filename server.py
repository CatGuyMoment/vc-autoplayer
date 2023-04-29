token = "[discord bot token]"
import discord
from discord.ext import commands,tasks
import yt_dlp as youtube_dl
from discord.utils import get
import os
from os import walk
import urllib.parse, urllib.request, re
from pygame import mixer, _sdl2 as devicer
import time
elevatorplaying = False
api_service_name = "youtube"
api_version = "v3"
queuelist = []
client = commands.Bot(command_prefix="!",intents=discord.Intents.all())
mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],}

# mixer.init()
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
def checkindex(list,object):
   try:
        list.index(object)
   except:
    return False
   else:
    return True
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        print(loop)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        print(data)
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename    
        
@client.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
@client.command()
async def start(ctx,search):
    print("gonna start soon")
    while checkindex(queuelist,search):
        time.sleep(3)
        print("cmon load already")
    mixer.music.load(search+".mp3")
    mixer.music.play()
@client.command()
async def yt(ctx,search):
        d = os.getcwd()
        search2 = search
        print(search)
        query_string = urllib.parse.urlencode({'search_query': search2})
        print('http://www.youtube.com/results?' + query_string)
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?' + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})",
                                    htm_content.read().decode())
        print(search_results)
        urlv2 = 'http://www.youtube.com/watch?v=' + search_results[0]
        print(urlv2)
        if True:   
            server = ctx.message.guild
            voice_channel = server.voice_client
            print(voice_channel)
            if True:
               print("is it even getting here?")
               themp3 = ytdl.download([urlv2])
               print("its alive?")
               for (dirpath, dirnames, filenames) in walk(d):
                print(filenames)
                
               for i in filenames:
                    if i != "gaming.py" and i != "gaming.lua" and i != "waiting.mp3":
                        if len(queuelist) != 0:
                            
                            if not checkindex(queuelist,i):
                                print("selecting this fellow",i)
                                os.rename(i, search+'.mp3')
                                break
                        else:
                            queuelist.append(i)
                            print("selecting this fellow",i)
                            os.rename(i, search+'.mp3')
                            break  
              
            await ctx.send('**Queued:**' + search)
            if mixer.music.get_busy() == False:
                mixer.music.load(search+".mp3")
                mixer.music.play()
@client.event 
async def on_message(message):
    ctx = await client.get_context(message)
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    print(f'Message {user_message} by {username} on {channel}')
    if ctx.valid:
        await client.invoke(ctx)      
client.run(token)
