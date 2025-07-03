from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# 🔑 Step 1: Authenticate
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # This opens your browser to log into your Google account

# ✅ Step 2: Create Google Drive interface
drive = GoogleDrive(gauth)

# 📝 Step 3: Create and upload a file
file = drive.CreateFile({'title': 'test_upload.txt'})
file.SetContentString("Hello from Python Drive API!")
file.Upload()

print("✅ File uploaded successfully to your Google Drive.")
