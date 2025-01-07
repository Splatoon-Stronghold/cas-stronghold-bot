# Bot installation dev


Go to [https://discord.com/developers/applications/](https://discord.com/developers/applications/) and
create a new application you will have your APPLICATION_ID

In [https://discord.com/developers/applications/APPLICATION_ID/installation](https://discord.com/developers/applications/APPLICATION_ID/installation):
go to `Installation Contexts`, make sure that you have checked `Guild Install`, you can
use also `User Install` option if you wanna interact with the bot internally

In `Install Link` you will have something like this: `https://discord.com/oauth2/authorize?client_id=APPLICATION_ID`

Using that URL will lead to your Discord and will let you decide where to add
your bot

In `Default Install Settings` make sure that you have the `Scopes` and `Permission`

In [https://discord.com/developers/applications/APPLICATION_ID/bot](https://discord.com/developers/applications/APPLICATION_ID/bot) you can
get the `DISCORD_TOKEN` it is required for using your bot, it will be shown once, make sure
you store it

In `Privileged Gateway Intents` make sure you have `Presence Intent
`, `Server Members Intent` and `Message Content Intent` options must
be checked in order to work with intents required for publish and logging

Make sure that you use the `Install Link` for adding the bot to your Discord guilds
