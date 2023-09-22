import requests
from bs4 import BeautifulSoup
from PIL import Image
import random
import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
import time


class ImageFetcher:
    def __init__(self, source_urls):
        self.source_urls = source_urls

    def fetch_image_urls(self):
        image_urls = []
        for url in self.source_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    images = soup.find_all("img", src=True)
                    for img in images:
                        image_url = img["src"]
                        if image_url.startswith("http"):
                            image_urls.append(image_url)
            except requests.RequestException as e:
                logging.error(
                    f"Error fetching image URLs from {url}: {str(e)}")
        return image_urls

    def save_images(self, image_urls, save_folder):
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        with ThreadPoolExecutor() as executor:
            for i, url in enumerate(image_urls):
                executor.submit(self.save_image, url, save_folder, i)

    def save_image(self, url, save_folder, index):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(save_folder, f"image_{index}.jpg")
                if not os.path.exists(image_path):
                    with open(image_path, "wb") as f:
                        shutil.copyfileobj(response.raw, f)
        except requests.RequestException as e:
            logging.error(f"Error saving image {url}: {str(e)}")


class CosmicImage:
    def __init__(self, image_path):
        self.image_path = image_path

    def display_image(self):
        if os.path.exists(self.image_path):
            img = Image.open(self.image_path)
            img.show()
        else:
            print("Image not found.")

    def delete_image(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
            print("Image deleted.")
        else:
            print("Image not found.")


class CosmicExplorer:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.source_urls = [
            # Replace with real-world URLs or datasets
            "https://example.com/archivepix.html",
            "https://example.com/top100/",
        ]

    def fetch_and_update_images(self):
        fetcher = ImageFetcher(self.source_urls)
        image_urls = fetcher.fetch_image_urls()
        fetcher.save_images(image_urls, self.image_folder)

    def display_random_image(self):
        images = os.listdir(self.image_folder)
        if images:
            random_image = random.choice(images)
            image_path = os.path.join(self.image_folder, random_image)
            cosmic_image = CosmicImage(image_path)
            cosmic_image.display_image()
        else:
            print("No images found.")

    def cleanup_outdated_images(self, days=30):
        current_time = time.time()
        for file_name in os.listdir(self.image_folder):
            file_path = os.path.join(self.image_folder, file_name)
            if os.path.isfile(file_path):
                creation_time = os.path.getctime(file_path)
                if current_time - creation_time > days * 24 * 60 * 60:
                    os.remove(file_path)

    def delete_unused_images(self):
        images = set(os.listdir(self.image_folder))
        used_images = set()
        for url in self.source_urls:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                for img in soup.find_all("img", src=True):
                    image_url = img["src"]
                    if image_url.startswith("http"):
                        image_name = image_url.split("/")[-1]
                        used_images.add(image_name)
        unused_images = images - used_images
        for unused_image in unused_images:
            os.remove(os.path.join(self.image_folder, unused_image))

    def run(self):
        logging.basicConfig(filename='image_fetcher.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.fetch_and_update_images()
        self.display_random_image()
        self.cleanup_outdated_images()
        self.delete_unused_images()


if __name__ == "__main__":
    image_folder = "cosmic_images"
    explorer = CosmicExplorer(image_folder)
    explorer.run()
