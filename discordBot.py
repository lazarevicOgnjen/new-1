import os, sys, discord

client = discord.Client(intents=discord.Intents.default())
kanal_id, forum_url, slika_path, token = sys.argv[1], sys.argv[2], sys.argv[3], os.environ["DISCORD_BOT_TOKEN"]

@client.event
async def on_ready():
    ch = await client.fetch_channel(int(kanal_id))
    async for msg in ch.history(limit=1): await msg.delete()
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Otvori forum", url=forum_url))
    
    file = discord.File(slika_path)
    await ch.send("Forum je ažuriran !", file=file, view=view)
    await client.close()

client.run(token)
