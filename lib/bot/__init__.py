from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord import Embed
from discord import File
from discord import Intents

from datetime import datetime as dt
from dotenv import load_dotenv

import os
import requests

import tts_config

load_dotenv()


class Bot(BotBase):
    def __init__(self):
        self.command_prefix = os.getenv("MOTIONEYEBOT_DISCORD_COMMAND_PREFIX")
        self.camera_ip = os.getenv("MOTIONEYEBOT_DISCORD_CAMERA_IP")
        self.snapshot_url = os.getenv("MOTIONEYEBOT_DISCORD_SNAPSHOT_URL")
        self.stream_url = os.getenv("MOTIONEYEBOT_DISCORD_STREAM_URL")
        self.channel_id = int(os.getenv("MOTIONEYEBOT_DISCORD_CHANNEL_ID"))

        if tts_config.use_offline:
            if tts_config.use_offline:
                self.tts_command = f"{tts_config.shell} {tts_config.simple_google_tts_path} -p {tts_config.offline_language_code} \"{tts_config.motion_message}\""
            else:
                self.tts_command = f"{tts_config.shell} {tts_config.simple_google_tts_path} {tts_config.offline_language_code} \"{tts_config.motion_message}\""

        self.ready = False

        try:
            os.environ['TZ'] = os.getenv("MOTIONEYEBOT_DISCORD_TIMEZONE")
        except Exception as e:
            print(e)
            print("DISCORD_BOT_TIMEZONE: Invalid Timezone")
            print("Please review valid timezones for this environment")
            exit(1)
        
        super().__init__(
            command_prefix=self.command_prefix,
            intents=Intents.all()
        )


    def setup(self):
        print("<Running Setup>")
        for filename in os.listdir('lib/cogs'):
            if filename.endswith(".py"):
                cog = filename[:-3]
                self.load_extension(f"lib.cogs.{cog}")
                print(f"> Cog {cog} loaded")
        print("<Setup complete>")


    def run(self, version):
        self.VERSION = version
        
        self.setup()

        print("<Bot connecting>")
        super().run(os.getenv("MOTIONEYEBOT_DISCORD_TOKEN"), reconnect=True)


    def simple_google_tts(self):
        if tts_config.use_simple_google_tts:
            os.system(self.tts_command)


    async def send_snapshot(self, ctx):
        image_downloads_dir = 'image_downloads'
        dirlist = os.listdir(image_downloads_dir)

        # Delete out previous images
        for img in dirlist:
            if img.endswith('.jpeg'):
                os.remove(os.path.join(image_downloads_dir, img))

        filename = f"snapshot-{dt.now().strftime('%m-%d-%yT%H-%M-%S%f')}.jpeg"
        jpeg_path = os.path.join(image_downloads_dir, filename)
        with open(jpeg_path, 'wb') as jpeg:
            jpeg.write(requests.get(self.snapshot_url).content)

        embed = Embed(
            title=f"Snapshot {dt.now().strftime('%m/%d/%y %H:%M:%S')}",
            colour=ctx.author.colour
        )
        file = File(jpeg_path)
        embed.set_image(url=f"attachment://{filename}")

        await ctx.channel.send(embed=embed, file=file)

    
    async def send_stream(self, ctx):
        embed = Embed(
            title="Camera Stream URL",
            description=f"{self.stream_url}",
            colour=ctx.author.colour
        )
        await ctx.channel.send(embed=embed)


    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Command error")
        raise # Raise error in shell for more detail.


    async def on_command_error(self, ctx, exc):
        print(exc)
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc


    async def on_message(self, message):
        if message.content.lower().startswith("motion detected") and message.author.bot:
            self.simple_google_tts()
            await self.send_snapshot(message)

        if not message.author.bot:
            await self.process_commands(message)


    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print("<Bot connected>")
        else:
            print("<Bot reconnected>")


bot = Bot()