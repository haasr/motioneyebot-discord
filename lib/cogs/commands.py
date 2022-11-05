from typing import Optional
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions


def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for k,v in command.params.items():
        if k not in ('self', 'ctx'):
            params.append(f"[{k}]" if "NoneType" in str(v) else f"<{k}>")
    params = ' '.join(params)
    return f"```{cmd_and_aliases} {params}```"


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        super().__init__(data, per_page=4)

    def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        data_len = len(self.entries)
        embed = Embed(
            title='Help',
            description="Welcome to motioneyebot's help dialog!",
            colour=self.ctx.author.colour
        )
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(
            text=(
                f"{offset:,} - {min(data_len, offset+self.per_page-1):,} of " \
                f" {data_len:,} commands."
            )
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []
        for entry in entries:
            fields.append((entry.brief or "No description", syntax(entry)))

        return self.write_page(menu, fields)


class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')


    @Cog.listener()
    async def on_ready(self):
        print("> Commands cog ready")


    async def cmd_help(self, ctx, command):
        embed = Embed(
                        title=f"Help with `{command}`",
                        description=syntax(command),
                        colour=ctx.author.colour
                    )
        # Could use command.brief or command.help
        embed.add_field(name="Command description", value=command.brief)
        await ctx.send(embed=embed)


    @command(name='help', aliases=['h'],
                brief="See commands, their options, and usage.")
    async def show_help(self, ctx, cmd: Optional[str]):
        """Shows commands and their usage."""
        if cmd is None:
            menu = MenuPages(
                source=HelpMenu(ctx, list(self.bot.commands)),
                delete_message_after=True,
                timeout=60.0
            )
            await menu.start(ctx)
        else:
            if command := get(self.bot.commands, name=cmd):
                await self.cmd_help(ctx, command)
            else:
                await ctx.channel.send("That command does not exist.")


    @command(name='clear', aliases=['cls'],
                brief="Clear the last <amount> messages from the screen (default is 5).")
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)


    @command(name='snap', brief="Send a recent snapshot from the camera")
    async def snap(self, ctx):
        await self.bot.send_snapshot(ctx)


    @command(name='stream', brief="Send URL to camera live stream")
    async def stream(self, ctx):
        await self.bot.send_stream(ctx)


def setup(bot):
    bot.add_cog(Commands(bot))