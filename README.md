# stable-diffusion-modal-discord-bot
Run a stable diffusion model on modal and talk to it with discord

##
So far, most work here is inspired from ML examples found here: https://github.com/modal-labs/modal-examples
and:
https://realpython.com/how-to-make-a-discord-bot-python/

## Environment Set Up

HUGGINGFACE_TOKEN needs to be available to download model for:
```
secret=modal.Secret.from_name("huggingface-token")
```

Creating Hugging face Access token instructions can be found here:
https://huggingface.co/docs/hub/security-tokens

DISCORD_TOKEN needs to be available for bot use via LOCAL environment:
```
export DISCORD_TOKEN=abcdefg
```

Creating Discord bot instructions can be found here:
https://discordpy.readthedocs.io/en/stable/discord.html

### General architecture
