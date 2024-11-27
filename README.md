# 🖼️ IMGScrapper

**IMGScrapper** is a Python-based image scraper that allows you to download multiple images from the web 🚀

![image](https://github.com/user-attachments/assets/de1acedb-f2a7-487a-a576-6a7466ecb50c)

---

## 🎯 Features
- 📸 **Smart Image Filtering**: Automatically skips low-quality images like icons (16x16 or 32x32) and SVG files
- ⚡ **Flexible Downloads**: Ensures the exact number of images requested by the user, even when errors occur
- 🕵️‍♂️ **Web Automation**: Uses Selenium for robust and precise image scraping

## 🚀 How to Install

Make sure you have **Python 3** installed. You can download it from [Python's official website](https://www.python.org/)

### Installation Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/zaheyanez/IMGScrapper.git
   cd IMGScrapper
2. Install the required dependencies:
    ```bash
   pip install -r requirements.txt
3. Run the script:
   ```bash
   py imgscrapper.py

## 🛠 How It Works

When you input your search terms, the scraper will use **Selenium** to collect images for the given terms. It skips common errors like social media icons, excludes `.svg` files, and ensures that the number of images you requested is downloaded (even if some errors occur).

> ⚠️ **NOTE**: This project is intended to be used for datasets or similar purposes. It doesn't download HD quality images

## 🗑️ Destroy Images

You can also destroy downloaded images by selecting the `Destroy Images` option. This will overwrite and delete images from your specified folder. Once deleted, they cannot be recovered

## 📚 License
Project under MIT license
