import discord
import asyncio
import argparse

# Replace with your bot token
BOT_TOKEN = 'BOT_TOKEN'
# Replace with your channel ID
CHANNEL_ID = CHANNEL_ID

class LogBot(discord.Client):
    def __init__(self, log_message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None
        self.log_message = log_message

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.channel = self.get_channel(CHANNEL_ID)
        if self.channel is None:
            print(f"Could not find channel with ID {CHANNEL_ID}")
        else:
            print(f"Channel found: {self.channel.name}")
            await self.send_log(self.log_message)
            await self.close()

    async def send_log(self, log_message):
        if self.channel:
            await self.channel.send(log_message)
        else:
            print("Channel not found or bot not ready")

async def main(log_message):
    intents = discord.Intents.default()
    intents.messages = True
    bot = LogBot(log_message, intents=intents)

    async with bot:
        await bot.start(BOT_TOKEN)

def log_to_discord(log_message):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(log_message))
    loop.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a log message to a Discord channel.')
    parser.add_argument('message', type=str, help='The log message to send to the Discord channel')

    args = parser.parse_args()
    log_to_discord(args.message)