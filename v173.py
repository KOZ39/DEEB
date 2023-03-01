import re
import traceback

import discord

EMOJI_REGEX = r"^<(a)?:(.+?):([0-9]{15,21})>$"

client = discord.Client()


@client.event
async def on_ready() -> None:
    print(f"{client.user} Online!")


@client.event
async def on_message(message: discord.Message) -> None:
    if not message.guild and message.author.bot:
        return

    if (m := re.match(EMOJI_REGEX, message.content)):
        try:
            color = message.author.color if message.author.color != discord.Colour.default() else 0xffffff
            ext = "gif" if m.group(1) else "png"

            embed = discord.Embed(color=color)
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
            embed.set_image(url=f"https://cdn.discordapp.com/emojis/{m.group(3)}.{ext}")
            #embed.set_footer(text=m.group(2))

            await message.delete()
            await message.channel.send(embed=embed, reference=message.reference, mention_author=False)
        except:
            #traceback.print_exc()
            pass


client.run('<DISCORD_CLIENT_TOKEN>')
