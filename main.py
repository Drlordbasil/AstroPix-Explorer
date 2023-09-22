import time


class Media:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def open_media(self):
        if os.path.exists(self.file_path):
            if self.get_media_type() == "image":
                img = Image.open(self.file_path)
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
        if extension.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
            return "image"
        elif extension.lower() in [".mp4", ".avi", ".mkv"]:
            return "video"
        else:
            return ""


class MediaFetcher:
    def __init__(self, source_urls: list[str], media_type: str):
        self.source_urls = source_urls
	@@ -60,55 +94,13 @@ def get_media_extension(self) -> str:
            return ""


class MediaExplorer:
    def __init__(self, media_folder: str, source_image_urls: list[str], source_video_urls: list[str]):
        self.media_folder = media_folder
        self.image_folder = os.path.join(media_folder, "images")
        self.video_folder = os.path.join(media_folder, "videos")
        self.source_image_urls = source_image_urls
        self.source_video_urls = source_video_urls

    def fetch_and_update_media(self):
        image_fetcher = MediaFetcher(self.source_image_urls, "image")
	@@ -124,7 +116,7 @@ def display_random_media(self):
        if media_files:
            random_media = random.choice(media_files)
            media_path = os.path.join(self.media_folder, random_media)
            media_item = Media(media_path)
            media_item.open_media()
        else:
            print("No media found.")
	@@ -197,16 +189,27 @@ def run(self):


class User:
    def __init__(self, name: str, source_image_urls: list[str], source_video_urls: list[str]):
        self.name = name
        self.media_folder = f"{self.name}_media"
        self.media_explorer = MediaExplorer(
            self.media_folder, source_image_urls, source_video_urls)

    def start(self):
        self.media_explorer.run()


if __name__ == "__main__":
    name = input("Enter your name: ")
    source_image_urls = [
        # Replace with real-world URLs or datasets
        "https://example.com/archivepix.html",
        "https://example.com/top100/",
    ]
    source_video_urls = [
        # Replace with real-world URLs or datasets
        "https://example.com/archivemovies.html",
        "https://example.com/popularmovies/",
    ]
    user = User(name, source_image_urls, source_video_urls)
    user.start()
