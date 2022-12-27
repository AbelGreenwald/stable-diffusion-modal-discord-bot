import asyncio
import io
import os
import typer

import modal.aio

MODEL_ID = "runwayml/stable-diffusion-v1-5"
CACHE_PATH = "/vol/cache"

stub = modal.aio.AioStub("stable-diffusion-batch")
app = typer.Typer()
volume = modal.SharedVolume().persist("stable-diffusion-model-vol")

@stub.function(
    gpu="A10G",
    image=(
        modal.Image.debian_slim()
        .run_commands("pip install torch --extra-index-url https://download.pytorch.org/whl/cu117")
        .pip_install("diffusers", "transformers", "scipy", "ftfy", "accelerate")
    ),
    shared_volumes={CACHE_PATH: volume},
    secret=modal.Secret.from_name("huggingface-token"),
)
def run_stable_diffusion(prompt: str):
    """Generates Stable Diffusion image

    Parameters:
    prompt (str): text input used by text-to-image diffusion model

    Returns:
    Image:Returning value

   """
    from diffusers import StableDiffusionPipeline
    from torch import float16

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        use_auth_token=os.environ["HUGGINGFACE_TOKEN"],
        revision="fp16",
        torch_dtype=float16,
        cache_dir=CACHE_PATH,
        device_map="auto",
    )

    image = pipe(prompt, num_inference_steps=100).images[0]
    print("Image size: " + str(image.size))
    return image

def serve_discord_bot():
    """Connects to Discord api (web sockets), listens for
    $stable-diffusion message prefix, calls run_stable_diffusion with recieved
    text, formats and sends image to discord.
    """
    import discord
    from PIL import Image
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith('$stable-diffusion'):
            text = message.content[len('$stable-diffusion'):]
            await message.channel.send(f'recieved{text}. Generating art...')
            async with stub.run():
                raw_image = await run_stable_diffusion(text)
                with io.BytesIO() as img_buffer:
                    raw_image.save(img_buffer, format="PNG")
                    img_buffer.seek(0)
                    discord_imge = discord.File(fp=img_buffer, filename="stable_diffusion.png", description=text)
            await message.channel.send(file=discord_imge)
    client.run(os.environ["DISCORD_TOKEN"])

if __name__ == "__main__":
    asyncio.run(serve_discord_bot())
