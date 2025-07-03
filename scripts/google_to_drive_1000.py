import os
from icrawler.builtin import GoogleImageCrawler
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# =========================== USER CONFIG ===========================

# 1️⃣ List your keywords here (as many as you want)
keywords = [
    "wildlife photography",
    "tiger in jungle",
    "forest landscape"
]

# 2️⃣ Total number of images you want across all keywords
total_images = 500

# 3️⃣ Folder where images will be saved locally
local_folder = "downloads"

# 4️⃣ Your target Google Drive folder ID (must exist beforehand)
target_drive_folder_id = "YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE"

# ===================================================================

# Calculate limit per keyword
images_per_keyword = total_images // len(keywords)
cache_file = "uploaded_images_cache.txt"

# 🔑 Authenticate Google Drive
print("🔑 Authenticating Google Drive...")
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# 📁 Load uploaded cache
uploaded = set()
if os.path.exists(cache_file):
    with open(cache_file, "r") as f:
        uploaded = set(line.strip() for line in f if line.strip())

# 🔄 Process each keyword
for keyword in keywords:
    print(f"\n🔍 Crawling Google for: {keyword}")

    folder_name = keyword.replace(" ", "_")
    download_path = os.path.join(local_folder, folder_name)
    os.makedirs(download_path, exist_ok=True)

    crawler = GoogleImageCrawler(storage={"root_dir": download_path})
    crawler.crawl(keyword=keyword, max_num=images_per_keyword)

    # Upload images
    for file_name in os.listdir(download_path):
        file_path = os.path.join(download_path, file_name)
        file_key = f"{folder_name}/{file_name}"

        if file_key in uploaded:
            print(f"⏩ Skipped (cached): {file_key}")
            continue

        try:
            file_drive = drive.CreateFile({
                'title': file_name,
                'parents': [{"id": target_drive_folder_id}]
            })
            file_drive.SetContentFile(file_path)
            file_drive.Upload()
            print(f"✅ Uploaded: {file_key}")

            with open(cache_file, "a") as f:
                f.write(file_key + "\n")
            uploaded.add(file_key)

        except Exception as e:
            print(f"❌ Error uploading {file_name}: {e}")

print("\n🎉 All image categories uploaded successfully!")
