import requests
from bs4 import BeautifulSoup
from PIL import Image
import random
import os
import shutil


class ImageFetcher:
    def __init__(self, source_urls):
        self.source_urls = source_urls

    def fetch_image_urls(self):
        image_urls = []
        for url in self.source_urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            images = soup.find_all("img", src=True)
            for img in images:
                image_url = img["src"]
                if image_url.startswith("http"):
                    image_urls.append(image_url)
        return image_urls

    def save_images(self, image_urls, save_folder):
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        for i, url in enumerate(image_urls):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(save_folder, f"image_{i}.jpg")
                with open(image_path, "wb") as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
            del response


class CosmicExplorer:
    def __init__(self, image_folder):
        self.image_folder = image_folder

    def fetch_and_update_images(self):
        fetcher = ImageFetcher(
            [
                "https://example.com/archivepix.html",  # Replace with real-world URLs or datasets
                "https://example.com/top100/",
            ]
        )
        image_urls = fetcher.fetch_image_urls()
        fetcher.save_images(image_urls, self.image_folder)

    def display_random_image(self):
        images = os.listdir(self.image_folder)
        if images:
            random_image = random.choice(images)
            image_path = os.path.join(self.image_folder, random_image)
            img = Image.open(image_path)
            img.show()
        else:
            print("No images found.")

    def run(self):
        self.fetch_and_update_images()
        self.display_random_image()


if __name__ == "__main__":
    image_folder = "cosmic_images"
    explorer = CosmicExplorer(image_folder)
    explorer.run()
