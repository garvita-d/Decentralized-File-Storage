import argparse
import os
import shutil

<<<<<<< HEAD
def upload_file(file_path):
   
=======
STORAGE_DIR = "storage"

def upload(file_path):
>>>>>>> origin/frontend
    if not os.path.exists(file_path):
        print(f" File not found: {file_path}")
        return
<<<<<<< HEAD
    print(f"Uploaded file: {file_path}")
  

def download_file(file_id):
   
    downloads_dir = "downloads"
    os.makedirs(downloads_dir, exist_ok=True)

    safe_id = re.sub(r'[^A-Za-z0-9_.-]', '_', file_id)

    file_path = os.path.join(downloads_dir, f"{safe_id}.txt")

    with open(file_path, "w") as f:
        f.write(f"Dummy content for file ID: {file_id}\n")

    print(f"Downloaded '{file_id}' → {file_path}")

def list_files():
    print("📁 Files available (simulated):")
    print("- ScAN.main")
    print("- file123")
    print("- file456")
=======

    os.makedirs(STORAGE_DIR, exist_ok=True)
    file_name = os.path.basename(file_path)
    dest_path = os.path.join(STORAGE_DIR, file_name)
    shutil.copy(file_path, dest_path)
    print(f"✅ Uploaded {file_name} successfully! Stored in '{STORAGE_DIR}/'")

def download(file_name):
    source_path = os.path.join(STORAGE_DIR, file_name)
    if not os.path.exists(source_path):
        print(f"❌ File not found in storage: {file_name}")
        return

    dest_path = os.path.join(os.getcwd(), f"downloaded_{file_name}")
    shutil.copy(source_path, dest_path)
    print(f"📥 Downloaded {file_name} successfully to {dest_path}")

def list_files():
    if not os.path.exists(STORAGE_DIR):
        print("📂 No files uploaded yet.")
        return
    files = os.listdir(STORAGE_DIR)
    if not files:
        print("📂 No files uploaded yet.")
        return
    print("📄 Uploaded files:")
    for f in files:
        print(f"- {f}")
>>>>>>> origin/frontend

def main():
    # Create parser
    parser = argparse.ArgumentParser(
        description="Decentralized File Storage CLI\n\nCommands: upload <file>, download <file_hash>, list"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

  
    upload_parser = subparsers.add_parser("upload", help="Upload a file")
    upload_parser.add_argument("file", help="Path to the file to upload")

<<<<<<< HEAD
    
    download_parser = subparsers.add_parser("download", help="Download a file by ID")
    download_parser.add_argument("file_id", help="ID of the file to download")
=======
    # Download command
    download_parser = subparsers.add_parser("download", help="Download a file by name or hash")
    download_parser.add_argument("file_name", help="File name or hash to download")
>>>>>>> origin/frontend

    
    subparsers.add_parser("list", help="List all uploaded files")

    args = parser.parse_args()

    if args.command == "upload":
        upload(args.file)
    elif args.command == "download":
        download(args.file_name)
    elif args.command == "list":
        list_files()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
