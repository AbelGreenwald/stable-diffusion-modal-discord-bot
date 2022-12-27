import discord
import io
from PIL import Image
from io import BytesIO
filepath = "christmas.png"

im = Image.new(mode="RGB", size=(2000, 2000))

print("size: " + str(im.size))

with io.BytesIO() as buf:
    im.save(buf, format="PNG")
    buf.seek(0)
    file = discord.File(fp=buf)
    # Convert PIL Image to PNG byte array.
    #with io.BytesIO() as buf:
    #    image.save(buf, format="PNG")
#await message.channel.send(file=picture)


#client.run("MTA1Njk5NTI4NDc4MzIwMjQwNg.G_5Wn5._0rGW_ENAqlHxi75O6wIXDhVHgb9TopJ6B3PUg")#os.environ["DISCORD_TOKEN"])
