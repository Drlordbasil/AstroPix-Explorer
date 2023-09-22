# Enhanced by AI:
from bs4 import BeautifulSoup
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import logging
import shutil
import os
Here are a few enhancements to your code:

1. ** Separate code into different modules**: It's a good practice to separate classes and functions into different modules for better organization and maintainability. You can create separate files for each class and import them into your main script.

2. ** Error handling**: It's important to handle errors gracefully and provide useful error messages. You can use try -except statements to catch exceptions and log appropriate error messages.

3. ** Use f-strings**: Instead of concatenating strings, you can use f-strings to make your code more readable and concise.

4. ** Use logger instead of print**: Instead of using print statements for logging, use the logging module to log informative messages. This will make it easier to track and debug issues.

5. ** Use context managers**: Use context managers, such as `with ` statements, to automatically handle file operations and ensure resources are properly managed.

6. ** Refactor media type checking**: Instead of using if -elif statements to check media type, you can use dictionary mapping to make the code more concise and extensible.

7. ** Use list comprehension**: Use list comprehension to simplify loops and make the code more readable.

8. ** Simplify code**: Simplify the code by removing unnecessary statements, variables, and imports.

Here's the enhanced version of your code:

*media.py: *
```python


class Media:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def open_media(self):
        if os.path.exists(self.file_path):
            if self.get_media_type() == "image":
                with Image.open(self.file_path) as img:
                    img.show()
            elif self.get_media_type() == "video":
                # Code to play video
                print("Video playing.")
            else:
                print("Unsupported media type.")
        else:
            print("Media not found.")

    def delete_media(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print("Media deleted.")
        else:
            print("Media not found.")

    def get_media_type(self) -> str:
        extension = os.path.splitext(self.file_path)[-1]
        media_types = {
            ".jpg": "image",
            ".jpeg": "image",
            ".png": "image",
            ".gif": "image",
            ".mp4": "video",
            ".avi": "video",
            ".mkv": "video"
        }
        return media_types.get(extension.lower(), "")


class MediaFetcher:
    def __init__(self, source_urls: list[str], media_type: str):
        self.source_urls = source_urls
        self.media_type = media_type

    def fetch_media_urls(self) -> list[str]:
        media_urls = []
        for url in self.source_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    media = soup.find_all(self.media_type, src=True)
                    media_urls.extend(
                        [item["src"] for item in media if item["src"].startswith("http")])
            except requests.RequestException as e:
                logging.error(
                    f"Error fetching {self.media_type} URLs from {url}: {str(e)}")
        return media_urls

    def save_media(self, media_urls: list[str], save_folder: str):
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        with ThreadPoolExecutor() as executor:
            for i, url in enumerate(media_urls):
                executor.submit(self.save_media_item, url, save_folder, i)

    def save_media_item(self, url: str, save_folder: str, index: int):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                item_path = os.path.join(
                    save_folder, f"{self.media_type}_{index}.{self.get_media_extension()}")
                if not os.path.exists(item_path):
                    with open(item_path, "wb") as f:
                        shutil.copyfileobj(response.raw, f)
        except requests.RequestException as e:
            logging.error(f"Error saving {self.media_type} {url}: {str(e)}")

    def get_media_extension(self) -> str:
        media_extensions = {
            "image": "jpg",
            "video": "mp4"
        }
        return media_extensions.get(self.media_type, "")


class MediaExplorer:
    def __init__(self, media_folder: str, source_image_urls: list[str], source_video_urls: list[str]):
        self.media_folder = media_folder
        self.image_folder = os.path.join(media_folder, "images")
        self.video_folder = os.path.join(media_folder, "videos")
        self.source_image_urls = source_image_urls
        self.source_video_urls = source_video_urls

    def fetch_and_update_media(self):
        image_fetcher = MediaFetcher(self.source_image_urls, "image")
        image_urls = image_fetcher.fetch_media_urls()
        image_fetcher.save_media(image_urls, self.image_folder)

        video_fetcher = MediaFetcher(self.source_video_urls, "video")
        video_urls = video_fetcher.fetch_media_urls()
        video_fetcher.save_media(video_urls, self.video_folder)

    def display_random_media(self):
        media_files = self.get_all_media_files()
        if media_files:
            random_media = random.choice(media_files)
            media_path = os.path.join(self.media_folder, random_media)
            media_item = Media(media_path)
            media_item.open_media()
        else:
            print("No media found.")

    def delete_unused_media(self):
        image_files = self.get_all_media_files(self.image_folder)
        video_files = self.get_all_media_files(self.video_folder)

        used_images, used_videos = self.get_used_media_files()

        unused_images = image_files - used_images
        unused_videos = video_files - used_videos

        self.delete_media_files(unused_images, self.image_folder)
        self.delete_media_files(unused_videos, self.video_folder)

    def cleanup_outdated_media(self, days: int = 30):
        current_time = time.time()
        self.cleanup_outdated_files(self.image_folder, current_time, days)
        self.cleanup_outdated_files(self.video_folder, current_time, days)

    def cleanup_outdated_files(self, folder: str, current_time: float, days: int):
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            if os.path.isfile(file_path):
                creation_time = os.path.getctime(file_path)
                if current_time - creation_time > days * 24 * 60 * 60:
                    os.remove(file_path)

    def delete_media_files(self, files: set[str], folder: str):
        for file_name in files:
            os.remove(os.path.join(folder, file_name))

    def get_all_media_files(self, folder: str = None) -> set[str]:
        if folder is None:
            folder = self.media_folder
        return set(os.listdir(folder))

    def get_used_media_files(self) -> tuple(set[str], set[str]):
        used_images, used_videos = set(), set()
        for url in self.source_image_urls:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                for img in soup.find_all("img", src=True):
                    image_url = img["src"]
                    if image_url.startswith("http"):
                        image_name = image_url.split("/")[-1]
                        used_images.add(image_name)

        for url in self.source_video_urls:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                for source in soup.find_all("source", src=True):
                    video_url = source["src"]
                    if video_url.startswith("http"):
                        video_name = video_url.split("/")[-1]
                        used_videos.add(video_name)

        return used_images, used_videos

    def run(self):
        available_genres = ['comedy', 'fantasy', 'action', 'triller', 'sci-fi']
        logging.basicConfig(filename='media_updater.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        for genre in available_genres:
            query = f'https://www.imdb.com/genre/{genre}'
            response = requests.get(query)
            soup = BeautifulSoup(response.content, "html.parser")
            media = soup.find_all(class_='lister-item mode-advanced')
            media_urls = [item.find('img')['src'] for item in media if item.find('img')[
                'src'].startswith("http")]
            self.media_urls = media_urls
            media_fetcher = MediaFetcher(self.media_urls, "image")
            media_files = media_fetcher.fetch_media_urls()
            media_fetcher.save_media(media_files, self.image_folder)
        self.display_random_media()
        self.cleanup_outdated_media()
        self.delete_unused_media()


class User:
    def __init__(self, name: str):
        self.name = name
        self.media_folder = f"{self.name}_media"
        self.media_explorer = MediaExplorer(
            self.media_folder, [])

    def start(self):
        self.media_explorer.run()


if __name__ == "__main__":
    name = input("Enter your name: ")
    user = User(name)
    user.start()
```

Please note that some parts of your code were not clear or had missing references, so I made educated assumptions where necessary. Adjustments may be required according to your specific requirements.
