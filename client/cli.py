import argparse
import os
import shutil

STORAGE_DIR = "storage"

def upload(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

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

def main():
    # Create parser
    parser = argparse.ArgumentParser(
        description="Decentralized File Storage CLI\n\nCommands: upload <file>, download <file_hash>, list"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload a file")
    upload_parser.add_argument("file", help="Path to the file to upload")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download a file by name or hash")
    download_parser.add_argument("file_name", help="File name or hash to download")

    # List command
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
