import re
#import traceback

import discord

SINGLE_EMOJI_REGEX = re.compile(
    r"""
    ^          # Start of string
    (?!<.*<)   # Negative lookahead to ensure there is not more than one '<' at the beginning
    <          # Emoji opening delimiter
    (a)?       # Optional 'a' for animated emojis
    :          # Colon delimiter
    (.+?)      # Emoji name
    :          # Colon delimiter
    ([0-9]{15,21})  # Emoji ID
    >          # Emoji closing delimiter
    $          # End of string
    """,
    re.VERBOSE,
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"{client.user} Online!")


@client.event
async def on_message(message: discord.Message) -> None:
    if not message.guild or message.author.bot:
        return None

    if (m := SINGLE_EMOJI_REGEX.match(message.content)):
        try:
            color = message.author.color if message.author.color != discord.Colour.default() else 0xffffff
            ext = ".gif" if m.group(1) else ".png"

            embed = discord.Embed(color=color)
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)
            embed.set_image(url=f"https://cdn.discordapp.com/emojis/{m.group(3)}{ext}")
            #embed.set_footer(text=m.group(2))

            await message.delete()
            await message.channel.send(embed=embed, reference=message.reference, mention_author=False)
        except:
            #traceback.print_exc()
            pass


client.run('<DISCORD_CLIENT_TOKEN>')
