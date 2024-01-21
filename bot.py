import logging
import os
import re

import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


SINGLE_EMOJI_REGEX = re.compile(
    r"""
    ^               # Start of string
    (?!<.*<)        # Negative lookahead to ensure there is not more than one '<' at the beginning
    <               # Emoji opening delimiter
    (a)?            # Optional 'a' for animated emoji
    :               # Colon delimiter
    (.+?)           # Emoji name
    :               # Colon delimiter
    ([0-9]{15,21})  # Emoji ID
    >               # Emoji closing delimiter
    $               # End of string
    """,
    re.VERBOSE,
)


@tasks.loop(minutes=1.0)
async def change_status() -> None:
    await client.change_presence(activity=discord.Game(name=f"{len(client.guilds)}개의 서버와 함께"))


@client.event
async def on_ready() -> None:
    change_status.start()
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if not message.guild or message.author.bot:
        return

    if (m := SINGLE_EMOJI_REGEX.match(message.content)):
        embed = discord.Embed(
            color = message.author.color if message.author.color != discord.Colour.default() else discord.Colour.greyple()
        )
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)
        emoji_id = m.group(3)
        extension = ".gif" if m.group(1) else ".png"
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{emoji_id}{extension}")

        try:
            await message.delete()
            await message.channel.send(embed=embed, reference=message.reference, mention_author=False)
        except discord.Forbidden:
            pass
        except Exception as e:
            log.exception("%s", e)


client.run(os.getenv('TOKEN'))
