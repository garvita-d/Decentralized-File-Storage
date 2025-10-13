import argparse
import os
import sys
import re

def upload_file(file_path):
   
    if not os.path.exists(file_path):
        print(f" File not found: {file_path}")
        return
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

def main():
    parser = argparse.ArgumentParser(description="Decentralized File Storage CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

  
    upload_parser = subparsers.add_parser("upload", help="Upload a file")
    upload_parser.add_argument("file_path", help="Path to the file to upload")

    
    download_parser = subparsers.add_parser("download", help="Download a file by ID")
    download_parser.add_argument("file_id", help="ID of the file to download")

    
    subparsers.add_parser("list", help="List all uploaded files")

    args = parser.parse_args()

    if args.command == "upload":
        upload_file(args.file_path)
    elif args.command == "download":
        download_file(args.file_id)
    elif args.command == "list":
        list_files()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
