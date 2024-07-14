import random
import time
import os
import asyncio
import requests
import discord
from dotenv import load_dotenv


class DiscordImageDownloader:
    def __init__(self, bot_token, all_channels, use_emoji=True):
        self.bot_token = bot_token
        self.channels = all_channels
        self.use_emoji = use_emoji
        self.intents = discord.Intents.all()
        self.client = discord.Client(intents=self.intents)
        self.folder_and_links = {}

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

    async def on_ready(self):
        print(f"Logged in as {self.client.user}")

        for channel_id, folder_path, limit in self.channels:
            channel = self.client.get_channel(channel_id)
            set_limit = None if limit <= 0 else limit
            async for message in channel.history(limit=set_limit):
                await self.download_images(message, folder_path)
                if self.use_emoji:
                    await message.add_reaction(u"❌")

            print(f"Link Got DONE --- {channel}")
        await self.client.close()

    def get_link(self):
        self.client.event(self.on_ready)
        self.client.run(self.bot_token)
        return self.folder_and_links

    @staticmethod
    def download_file(url, save_path):
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    file.write(chunk)

    def run(self):
        path_and_links = self.get_link()

        for folder_name, values in path_and_links.items():
            for image in values:
                file_name = image['file_name']
                file_id = image['file_id']
                file_url = image['file_url']
                file_path = os.path.join(folder_name, file_name)

                self.download_file(url=file_url, save_path=file_path)
                time.sleep(round(random.uniform(0, 1.5), 2))

            print(f"DONE --- {folder_name}")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    channels = [
        # Example format: (channel_id, folder_path, download_limit)
        (1177881888266928208, "downloaded_files", 0)
    ]
    downloader = DiscordImageDownloader(BOT_TOKEN, channels, use_emoji=True)
    downloader.run()
