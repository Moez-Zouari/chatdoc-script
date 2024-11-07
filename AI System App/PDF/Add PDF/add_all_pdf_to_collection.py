import os
import requests
import csv
from datetime import datetime
import sys

# Append the path to the Quota folder to import get_quota
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Quota')))
from get_quota import get_quota  # Import the function to get quota

# API key and URL for document upload
api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"
upload_url = "https://api.chatdoc.com/api/v2/documents/upload"

headers = {
    "Authorization": f"Bearer {api_key}"
}

def get_collections_from_csv(collections_csv_path):
    """Retrieve collections from the CSV file."""
    collections = {}
    try:
        with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                collections[row["Collection Name"]] = row["Collection ID"]
    except FileNotFoundError:
        print(f"Error: The file '{collections_csv_path}' does not exist or no collections have been created yet.")
        return None
    return collections

def list_folders(base_path):
    """List all subfolders in the specified base path."""
    return [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

def upload_documents_from_folder(collections_csv_path):
    """Upload documents from the specified folder to the selected collection."""
    collections = get_collections_from_csv(collections_csv_path)
    
    if not collections:
        print("No collections found in the CSV.")
        return

    # Display collections and prompt user to select one
    print("Available collections:")
    for i, (collection_name, collection_id) in enumerate(collections.items(), start=1):
        print(f"{i}. {collection_name} (ID: {collection_id})")

    choice = int(input("Select a collection by number: ")) - 1
    if choice < 0 or choice >= len(collections):
        print("Invalid selection. Exiting.")
        return

    selected_collection_name, collection_id = list(collections.items())[choice]

    # List available folders in the PDF files directory
    pdf_base_path = "D:/AI Test System/PDF Files"
    available_folders = list_folders(pdf_base_path)

    if not available_folders:
        print("No folders found in the PDF files directory.")
        return

    # Display available folders and prompt user to select one
    print("Available folders for PDF documents:")
    for i, folder_name in enumerate(available_folders, start=1):
        print(f"{i}. {folder_name}")

    folder_choice = int(input("Select a folder by number: ")) - 1
    if folder_choice < 0 or folder_choice >= len(available_folders):
        print("Invalid selection. Exiting.")
        return

    selected_folder = available_folders[folder_choice]

    # Define the folder path based on the user's selection
    folder_path = os.path.join(pdf_base_path, selected_folder)

    # Check if the folder is empty or does not contain PDF files
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"The selected folder '{selected_folder}' is empty or does not contain any PDF files. Upload cancelled.")
        return

    collection_csv_path = f"D:/AI Test System/csv details/documents/{selected_collection_name.replace(' ', '_')}_details.csv"

    # Check if user wants to view quota
    check_quota = input("Do you want to check your quota before uploading documents? (yes/no): ").strip().lower()
    if check_quota == 'yes':
        get_quota()  # Call the function to display the quota

    # Confirm document upload
    confirm_upload = input("Do you really want to add documents to the collection? (yes/no): ").strip().lower()
    if confirm_upload != 'yes':
        print("Document upload canceled.")
        return  # Exit if the user does not want to upload documents

    # Proceed with uploading documents
    for filename in pdf_files:
        file_path = os.path.join(folder_path, filename)
        upload_document(collection_id, selected_collection_name, file_path, collection_csv_path)

    # Display a message indicating that the CSV file has been created or updated
    print(f"Document details logged in '{collection_csv_path}'.")

def upload_document(collection_id, collection_name, file_path, collections_csv_path):
    with open(file_path, 'rb') as file:
        files = {
            "file": (os.path.basename(file_path), file, "application/pdf")
        }
        data = {
            "collection_id": collection_id
        }
    
        response = requests.post(upload_url, headers=headers, files=files, data=data)

    if response.status_code == 200:
        document = response.json()
        document_id = document['data']['id']
        document_name = document['data']['name']
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Document '{document_name}' uploaded successfully. Document ID: {document_id}")

        log_document_details(collection_id, collection_name, document_id, document_name, upload_date, collections_csv_path)
    else:
        print("Error uploading document:", response.status_code, response.text)

def log_document_details(collection_id, collection_name, document_id, document_name, upload_date, collections_csv_path):
    file_exists = os.path.isfile(collections_csv_path)

    with open(collections_csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write header if file does not exist
        if not file_exists:
            writer.writerow(["Collection ID", "Collection Name", "Document ID", "Document Name", "Upload Date"])

        writer.writerow([collection_id, collection_name, document_id, document_name, upload_date])
    
# Example usage
collections_csv_path = "D:/AI Test System/csv details/collections/collections_details.csv"  # Path to the CSV file for collection IDs

upload_documents_from_folder(collections_csv_path)
