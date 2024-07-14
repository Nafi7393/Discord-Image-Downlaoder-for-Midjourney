import random
import time
from dotenv import load_dotenv
import discord
import os
import requests

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


class DiscordImageDownloader:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.client = discord.Client(intents=discord.Intents.all())
        self.folder_and_links = {}

    def run(self):
        @self.client.event
        async def on_ready():
            print(f"Logged in as {self.client.user}")

        self.client.run(self.bot_token)

    def add_channel(self, channel_id, folder_path):
        self.folder_and_links[channel_id] = folder_path

    async def download_images(self, message, folder):
        if folder not in self.folder_and_links:
            self.folder_and_links[folder] = []
        for attachment in message.attachments:
            file_name = f"{attachment.filename}"
            file_id = f"{attachment.id}"
            file_url = f"{attachment.url}"

            self.folder_and_links[folder].append({
                "file_name": file_name,
                "file_id": file_id,
                "file_url": file_url
            })

    async def process_channel(self, channel_id):
        channel = self.client.get_channel(channel_id)
        folder_path = self.folder_and_links[channel_id]

        async for message in channel.history(limit=None):
            await self.download_images(message, folder_path)
            await message.add_reaction(u"❌")

        print(f"Link Got DONE --- {channel}")

    def download_file(self, url, save_path):
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    file.write(chunk)

    def save_files(self):
        for folder_name, values in self.folder_and_links.items():
            for image in values:
                file_name = image['file_name']
                file_id = image['file_id']
                file_url = image['file_url']
                file_path = os.path.join(folder_name, file_name)

                self.download_file(url=file_url, save_path=file_path)
                time.sleep(round(random.uniform(0, 1.5), 2))

            print(f"DONE --- {folder_name}")


if __name__ == "__main__":
    bot = DiscordImageDownloader(BOT_TOKEN)

    bot.add_channel(1177881888266928208, "downloaded_files")

    # Run the bot and process the channel
    bot.run()

    # After the bot has processed the channel, save the files
    bot.save_files()
