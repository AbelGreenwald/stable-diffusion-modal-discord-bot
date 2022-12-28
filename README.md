# stable-diffusion-modal-discord-bot
Run a stable diffusion model on modal and talk to it with discord

##
Most work here is inspired from the ML and slack examples found here: 
https://github.com/modal-labs/modal-examples

## Environment Set Up

A Modal Account:
https://modal.com

HUGGINGFACE_TOKEN needs to be available as a modal secret to download the model for:
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

## General architecture

discord api -> local machine -> modal.com GPU docker -> local machine -> discord

This chat bot listenes to all messages in a discord "guild" and responds to any messages that have a `$stable-diffusion` prefix.  Any text after this prefix is used later by the Stable Diffusion text-to-image inference model.

Discord uses websockets for bot communication, which necessitated the use of asyncio for event handling.

## Running it
```
python stable-diffusion-batch.py
2022-12-26T23:48:28-0600 PyNaCl is not installed, voice will NOT be supported
2022-12-26 23:48:28 INFO     discord.client logging in using static token
2022-12-26T23:48:28-0600 logging in using static token
2022-12-26 23:48:29 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: 0fc0124ed53de950042cde3f013f3970).
2022-12-26T23:48:29-0600 Shard ID None has connected to Gateway (Session ID: 0fc0124ed53de950042cde3f013f3970).
We have logged in as stable-diffusion
```

## TODO
This was a POC of sorts on my part that ended up going so well I was able to just make it work.  Fairly impressed with modal.com. However, there's still much to do:
1. ~Secure the bot, I think I'ts wide open for people to add right now (approved on discord guild admin side not bot's).  This work will require Oauth2 work~
2. General improvements to ML function.  skys the limit here but I think a bit slower for larger images might be nice.
3. Figure out a way rerun a pervious model with new inputs (ML expert here would be helpful, also will need some kind of persistant state somewhere)
4. Save or set Seeds?
5. More I'm sure...
