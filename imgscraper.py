import os
import random
import requests
import re
import time
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import io
from colorama import Fore, Style, init

init(autoreset=True)

def show_banner():
    """Display ASCII banner with colors"""
    title = Fore.MAGENTA + r"""
 ________  ________  _____                                
|_   _|  \/  |  __ \/  ___|                               
  | | | .  . | |  \/\ `--.  ___ _ __ __ _ _ __   ___ _ __ 
  | | | |\/| | | __  `--. \/ __| '__/ _` | '_ \ / _ \ '__|
 _| |_| |  | | |_\ \/\__/ / (__| | | (_| | |_) |  __/ |   
 \___/\_|  |_/\____/\____/ \___|_|  \__,_| .__/ \___|_|   
                                         | |              
                                         |_|               
"""
    version = Fore.YELLOW + "v1.0.0"
    made_by = Fore.YELLOW + "By Zaheyanez"
    print(title)
    print(version)
    print(made_by)


def validate_integer(prompt, minimum, maximum):
    """Validate integer input"""
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            else:
                print(f"{Fore.RED}[!] The number must be between {minimum} and {maximum}.{Fore.WHITE}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Fore.WHITE}")


def destroy_images(folder):
    """Overwrite and delete images in the specified folder"""
    if not os.path.exists(folder):
        print(f"{Fore.RED}[!] The folder does not exist. Please check the name and try again.{Fore.WHITE}")
        return

    files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    if not files:
        print(f"{Fore.RED}[!] No images found in the folder.{Fore.WHITE}")
        return

    print(f"\nFound {len(files)} images in {folder}.")
    confirm = input("Are you sure you want to permanently destroy these images? (y/n): ").strip().lower()
    if confirm != "y":
        print(f"{Fore.RED}[!] Operation canceled.{Fore.WHITE}")
        return

    for file in files:
        file_path = os.path.join(folder, file)
        try:
            with open(file_path, "wb") as f:
                for _ in range(3):
                    f.write(os.urandom(os.path.getsize(file_path)))
            os.remove(file_path)
            print(f"{Fore.YELLOW}[*] Image destroyed: {file}{Fore.WHITE}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error destroying {file}: {e}{Fore.WHITE}")

    print(f"{Fore.GREEN}[+] Image destruction process completed.{Fore.WHITE}")


def fetch_image_urls(terms, max_images):
    """Fetch image URLs using Google Images and Selenium"""
    print(f"{Fore.YELLOW}[*] Searching for images with terms: {terms}...{Fore.WHITE}")
    query = "+".join(terms.split(", "))
    url = f"https://www.google.com/search?tbm=isch&safe=off&q={query}"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    image_count = 0
    while image_count < max_images:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)
        image_count = len(driver.find_elements(By.TAG_NAME, "img"))
        if image_count >= max_images:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    images = soup.find_all("img")
    urls = [img["src"] for img in images if "src" in img.attrs and img["src"].startswith("http")]
    print(f"{Fore.YELLOW}[*] Found {len(urls)} images.{Fore.WHITE}")
    return urls[:max_images]


def download_images(urls, folder, max_images):
    """Download images from the provided URLs"""
    downloaded = 0
    for idx, url in enumerate(urls):
        if downloaded >= max_images:
            break
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            if url.endswith(".svg") or "image/svg+xml" in response.headers.get("Content-Type", ""):
                print(f"\n{Fore.YELLOW}[*] Skipping SVG: {url}{Fore.WHITE}\n")
                continue

            img = Image.open(io.BytesIO(response.content))
            if img.width <= 32 and img.height <= 32:
                print(f"{Fore.YELLOW}[*] Skipping small image ({img.width}x{img.height}): {url}{Fore.WHITE}")
                continue

            ext = re.search(r'\.\w+$', url)
            extension = ext.group() if ext else ".jpg"
            file_name = f"image_{downloaded + 1}{extension}"
            file_path = os.path.join(folder, file_name)

            with open(file_path, "wb") as f:
                f.write(response.content)
            downloaded += 1
            print(f"{Fore.YELLOW}[{downloaded}/{max_images}]{Fore.WHITE} Image saved: {Fore.MAGENTA}{file_name}{Fore.WHITE}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error downloading image ({idx+1}): {e}{Fore.WHITE}")

    if downloaded < max_images:
        print(f"{Fore.RED}[!] Only {downloaded} out of {max_images} requested images were downloaded.{Fore.WHITE}")


def main():
    """Main function."""
    show_banner()
    base_folder = os.path.join(os.getcwd(), "scrapped")
    os.makedirs(base_folder, exist_ok=True)

    while True:
        """Display menu options"""
        print(f" ")
        options = [
            (1, "New Dataset"),
            (2, "Destroy Images"),
            (3, "Exit"),
        ]
        for number, text in options:
            print(f"{Fore.YELLOW}[{number}] {Fore.WHITE}{text}")
        
        choice = input("\n[-] Choose an option: ")

        if choice == "1":
            max_images = validate_integer(f"[-] Number of {Fore.MAGENTA}images{Fore.WHITE} (1-1000): ", 1, 1000)
            folder_name = input(f"[-] Folder {Fore.MAGENTA}name{Fore.WHITE}: ")
            dataset_folder = os.path.join(base_folder, folder_name)
            os.makedirs(dataset_folder, exist_ok=True)

            terms = input(f"[-] Search {Fore.MAGENTA}terms{Fore.WHITE} (comma-separated): ")
            urls = fetch_image_urls(terms, max_images * 2)
            if urls:
                print(f"\n{Fore.YELLOW}[*] Downloading {max_images} images to {dataset_folder}...\n{Fore.WHITE}")
                download_images(urls, dataset_folder, max_images)
                print(f"\n{Fore.GREEN}[+] Download completed!{Fore.WHITE}\n")
            else:
                print(f"{Fore.RED}[!] No images found for the given terms.{Fore.WHITE}")

        elif choice == "2":
            folder_name = input("Folder name within 'scrapped': ")
            target_folder = os.path.join(base_folder, folder_name)
            destroy_images(target_folder)

        elif choice == "3":
            print(f"{Fore.MAGENTA}[-] Goodbye!{Fore.WHITE}")
            break

        else:
            print(f"{Fore.RED}[!] Invalid option. Please try again.{Fore.WHITE}")


if __name__ == "__main__":
    main()
