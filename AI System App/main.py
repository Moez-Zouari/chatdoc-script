import os
import subprocess
import requests
import csv
from datetime import datetime
import re
import json


# Define API variables here
api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Your API key
documents_csv_path = "D:/AI Test System/csv details/documents"  # Path to CSV file containing document details

# Path to the CSV file for collection IDs
collections_csv_path = "D:/AI Test System/csv details/collections/collections_details.csv"

# File paths and patterns
questions_folder = 'D:/AI Test System/Source Files'  # Path to the folder containing source files
file_pattern = r'^\d{4}prompt\.md$'  # Regular expression pattern for matching files (e.g., 0001prompt.md)

# Parameters for commit message and Git repository
commit_message = "Update files"  # Commit message to use when pushing changes
remote_url = "https://git.intern.lauterbach.com/mzouari/AIPromptManagementSystem.git"  # Remote Git repository URL
username = "mzouari"  # Your Git username
token = "36b00d788950edf7f2ac01360595c3ed1875b9b0"  # Your Git authentication token (use with caution)
branch = "main"  # The branch to commit to (default: "main")

# Folder path containing PDF files for upload
folder_path = "D:\\AI Test System\\PDF Files"  # Path to the folder where PDF files are stored

# API URLs for uploading documents and managing collections
upload_url = "https://api.chatdoc.com/api/v2/documents/upload"  # API URL for document upload
api_url = "https://api.chatdoc.com/api/v2/questions/multi-documents"  # API URL for multi-document question queries
collection_url = "https://api.chatdoc.com/api/v2/collections"  # API URL for creating a new collection

# HTTP headers for API requests
headers = {
    "Authorization": f"Bearer {api_key}"  # Authorization header using Bearer token
}

#################################################################################################################################
#################################################################################################################################
                                                        # Create Collections #
#################################################################################################################################
#################################################################################################################################
# ============================
# Create New Collection
# ============================
def create_collection(collection_name):
    """
    Create a new collection in ChatDoc.
    
    Parameters:
    - collection_name: The name of the collection to be created.
    
    Returns:
    - The ID and name of the created collection if successful, None otherwise.
    """
    data = {"name": collection_name}
    response = requests.post(collection_url, headers=headers, json=data)

    if response.status_code == 200:
        collection = response.json()
        print(f"Collection '{collection['data']['name']}' created successfully with ID: {collection['data']['id']}")
        return collection['data']['id'], collection['data']['name']  # Return both ID and name
    else:
        print("Error:", response.status_code, response.text)
        return None, None

def store_collection_details(collection_id, collection_name, csv_path='D:/AI Test System/csv details/collections/collections_details.csv'):
    """
    Store the collection ID, name, and creation date in a CSV file.
    
    Parameters:
    - collection_id: The ID of the collection to be stored.
    - collection_name: The name of the collection to be stored.
    - csv_path: Path to the CSV file where details will be stored.
    """
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(csv_path)

    # Open the CSV file in append mode
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header only if the file does not exist
        if not file_exists:
            writer.writerow(['Collection ID', 'Collection Name', 'Creation Date'])
        
        # Write the collection details
        writer.writerow([collection_id, collection_name, creation_date])
    
    print(f"Collection details stored in '{csv_path}'.")

def create_new_collection():
    """ 
    Create a new collection by confirming with the user and getting the name. 
    """
    # Confirm with the user before proceeding
    confirmation = input("Do you really want to create a new collection? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        # Prompt the user to enter the collection name
        collection_name = input("Enter the name for the new collection: ")
        collection_id, collection_name = create_collection(collection_name)
        if collection_id:
            store_collection_details(collection_id, collection_name)
    else:
        print("Collection creation canceled.")
        
# ============================
# Get All Collections
# ============================
def get_all_created_collections(collections_csv_path):
    """
    Retrieves and displays collections from a CSV file, including duplicates and creation dates.
    
    Parameters:
    collections_csv_path (str): The path to the CSV file containing collection details.
    
    This function reads the collection details from the specified CSV file, including the collection name, 
    ID, and creation date. If the file is found, it displays all the collections in a readable format.
    In case the file is not found or an error occurs, it handles the exception and prints an appropriate message.
    It returns a list of collections as tuples (name, ID, creation date).
    """
    collections = []  # Initialize an empty list to store collection details

    try:
        # Open the CSV file for reading in 'r' mode (read mode)
        with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)  # Read the file as a dictionary

            # Iterate through each row in the CSV and append collection details to the list
            for row in reader:
                collections.append((row["Collection Name"], row["Collection ID"], row["Creation Date"]))

    except FileNotFoundError:
        # Handle case where the CSV file doesn't exist
        print(f"Error: The CSV collections details file '{collections_csv_path}' does not exist, or no collections have been created yet.")
        return collections  # Return empty list if file is not found
    except Exception as e:
        # Handle other unexpected errors
        print(f"An error occurred: {e}")
        return collections  # Return empty list in case of an error

    # Display the collections in a presentable format if any collections exist
    if collections:
        print("\n=== List of Collections ===")
        for name, collection_id, creation_date in collections:
            print(f"Collection Name: {name} | Collection ID: {collection_id} | Creation Date: {creation_date}")
        print("===========================")
    else:
        # Inform the user if no collections are found
        print("No collections found.")

    # Return the list of collections (empty or populated)
    return collections


#################################################################################################################################
#################################################################################################################################
                                                        # Manage Collections #
#################################################################################################################################
#################################################################################################################################

    
# ============================
# Get Quota
# ============================
def get_quota():
    # API URL to retrieve the quota
    api_url = "https://api.chatdoc.com/api/v2/users/quota"
    # Send the GET request to obtain the quota
    response = requests.get(api_url, headers=headers)

    # Check the response
    if response.status_code == 200:
        quota_info = response.json()
        
        # Extract relevant information
        package_info = quota_info.get('data', {}).get('package', {})
        question_info = package_info.get('question', {})
        elite_page_info = package_info.get('elite_page', {})
        
        # Formatted display
        print("Quota Information:")
        print(f"- Max Questions: {question_info.get('max_count', 0)}")
        print(f"- Questions Used: {question_info.get('used_count', 0)}")
        print(f"- Max Elite Pages: {elite_page_info.get('max_count', 0)}")
        print(f"- Elite Pages Used: {elite_page_info.get('used_count', 0)}")
    else:
        print("Error:", response.status_code, response.text)
        
        
# ============================
# Add all PDFs to collection
# ============================
def get_collections_from_csv(collections_csv_path):
    """Retrieve collections from the CSV file."""
    collections = {}
    try:
        with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                collections[row["Collection Name"]] = row["Collection ID"]
    except FileNotFoundError:
        print(f"Error: The CSV collections details file {collections_csv_path} does not exist, or no collections have been created yet.")
        return None
    return collections

def list_folders(base_path):
    """List all subfolders in the specified base path."""
    return [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

def upload_documents_from_folder(collections_csv_path):
    """Upload documents from the specified folder to the selected collection."""
    collections = get_collections_from_csv(collections_csv_path)
    
    if not collections:
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
    """
    Logs the details of a document into a CSV file. If the CSV file does not exist, it will create a new one and write the headers.
    This function appends the document details to the specified CSV file, including the collection ID, collection name,
    document ID, document name, and upload date. If the file does not exist, it creates the file and writes the header row.
    """
    # Check if the CSV file already exists
    file_exists = os.path.isfile(collections_csv_path)

    # Open the CSV file in append mode
    with open(collections_csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header if the file does not exist
        if not file_exists:
            writer.writerow(["Collection ID", "Collection Name", "Document ID", "Document Name", "Upload Date"])

        # Write the document details as a new row in the CSV file
        writer.writerow([collection_id, collection_name, document_id, document_name, upload_date])


# =======================================
# Add PDF By Name To Collection
# =======================================
def upload_document_from_folder(collections_csv_path):
    """Upload a specified document from the selected folder to the selected collection."""
    collections = get_collections_from_csv(collections_csv_path)
    
    if not collections:
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

    # Ask for the specific document name to upload
    document_name = input("Enter the name of the PDF document to upload (with extension): ").strip()
    file_path = os.path.join(folder_path, document_name)

    # Check if the document exists
    if not os.path.isfile(file_path):
        print(f"The document '{document_name}' does not exist in the selected folder. Upload cancelled.")
        return

    collection_csv_path = f"D:/AI Test System/csv details/documents/{selected_collection_name.replace(' ', '_')}_details.csv"

    # Check if user wants to view quota
    check_quota = input("Do you want to check your quota before uploading documents? (yes/no): ").strip().lower()
    if check_quota == 'yes':
        get_quota()  # Call the function to display the quota

    # Confirm document upload
    confirm_upload = input("Do you really want to add this document to the collection? (yes/no): ").strip().lower()
    if confirm_upload != 'yes':
        print("Document upload canceled.")
        
        return  # Exit if the user does not want to upload documents

    # Proceed with uploading the specified document
    upload_document(collection_id, selected_collection_name, file_path, collection_csv_path)

    # Display a message indicating that the CSV file has been created or updated
    print(f"Document details logged in '{collection_csv_path}'.")


# ============================
# Get All Pdf Id From Csv
# ============================
def get_all_pdfs(collections_csv_path):
    """
    Lists all PDF document names and IDs in the specified CSV file.

    Parameters:
    - collections_csv_path: Path to the CSV file containing document details.

    Returns:
    - A list of document details (name and ID) if the file exists and has content, None otherwise.
    """
    if not os.path.isfile(collections_csv_path):
        print(f"The specified CSV file '{collections_csv_path}' does not exist.")
        return None
    
    documents = []
    
    with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Check if the file has content
        rows = list(reader)
        if not rows:
            print("The CSV file is empty.")
            return None
        
        # Extract document names and IDs
        for row in rows:
            document_name = row.get("Document Name")
            document_id = row.get("Document ID")
            if document_name and document_id:
                documents.append((document_name, document_id))
    
    return documents

def print_pdf_list(documents):
    """
    Prints the list of PDF documents and their IDs in a numbered format.

    Parameters:
    - documents: A list of tuples containing (document_name, document_id).
    """
    total_pdfs = len(documents)
    print(f"Total number of PDF documents: {total_pdfs}")
    
    print("List of PDF documents:")
    for index, (name, doc_id) in enumerate(documents, start=1):
        print(f"{index}. {name}")
        

# ============================
# Get Pdf By Id
# ============================
def get_all_pdfs_from_directory(documents_csv_path):
    """
    Lists all PDF document names and IDs from all CSV files in the specified directory.

    Parameters:
    - documents_csv_path: Path to the directory containing CSV files with document details.

    Returns:
    - A dictionary where keys are collection names and values are lists of document details (name and ID).
    """
    if not os.path.isdir(documents_csv_path):
        print(f"Specified directory does not exist: {documents_csv_path}")
        return None

    collections = {}
    
    # Iterate through all CSV files in the directory
    for filename in os.listdir(documents_csv_path):
        if filename.endswith('.csv'):
            collections_csv_path = os.path.join(documents_csv_path, filename)
            collection_name = os.path.splitext(filename)[0]  # Use the file name without extension as collection name
            
            documents = []
            with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                
                # Check if the file has content
                rows = list(reader)
                if not rows:
                    print(f"The CSV file '{filename}' is empty.")
                    continue


                # Extract document names and IDs
                for row in rows:
                    document_name = row.get("Document Name")
                    document_id = row.get("Document ID")
                    if document_name and document_id:
                        documents.append((document_name, document_id))
            
            # Only add non-empty collections
            if documents:
                collections[collection_name] = documents

    return collections  # Return the dictionary of collections

def print_collections(collections):
    """
    Prints the list of collections in a numbered format.

    Parameters:
    - collections: A dictionary where keys are collection names and values are lists of tuples (document_name, document_id).
    """
    print("Available Collections:")
    if collections:
        for index, collection_name in enumerate(collections.keys(), start=1):
            print(f"{index}. {collection_name}")
        print()  # Add an empty line for better readability
    else:
        print("No collections found.")

def print_documents(collection_name, documents):
    """
    Prints the list of PDF documents and their IDs for a specific collection.

    Parameters:
    - collection_name: The name of the collection.
    - documents: A list of tuples containing (document_name, document_id).
    """
    print(f"Documents in '{collection_name}':")
    total_documents = len(documents)
    print(f"Total number of documents: {total_documents}")  # Display the total number of documents
    for index, (name, doc_id) in enumerate(documents, start=1):
        print(f"  {index}. {name}")
    print()  # Add an empty line for better readability

def get_document(api_key, document_id):
    """
    Retrieves a document's details from ChatDoc API using the document ID.

    Parameters:
    - api_key: Your API key for authentication.
    - document_id: The ID of the document to retrieve.

    Returns:
    - The document details if successful, None otherwise.
    """
    # Define the API URL with the user-provided document ID
    api_url = f"https://api.chatdoc.com/api/v2/documents/{document_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Send the request
    response = requests.get(api_url, headers=headers)

    # Check the response status
    if response.status_code == 200:
        return response.json()  # Return the document details
    elif response.status_code == 404:
        print("Error: The document with the specified ID was not found.")
    else:
        print(f"Error retrieving the document: {response.status_code}, {response.text}")
    return None

def format_document_details(document_details):
    """
    Formats and displays the document details.

    Parameters:
    - document_details: The details of the document returned from the API.
    """
    if document_details and 'data' in document_details:
        data = document_details['data']
        print("Document Details:")
        print(f"  ID: {data.get('id')}")
        print(f"  Name: {data.get('name')}")
        print(f"  Status: {data.get('status')}")
        print(f"  Type: {data.get('type')}")
        created_at = datetime.fromtimestamp(data.get('created_at')).strftime('%Y-%m-%d %H:%M:%S') if data.get('created_at') else "N/A"
        print(f"  Created at: {created_at}")
        print(f"  OCR Type: {data.get('ocr_type')}")
    else:
        print("No document details available.")
    
# ===================================
# Delete All Pdfs In Give Collection
# =================================== 
def list_collection_files(documents_csv_path):
    """
    Lists all CSV files in the specified directory, excluding 'collections_details.csv'.

    Parameters:
    - documents_csv_path: Path to the directory containing collection CSV files.

    Returns:
    - A dictionary with collection file names (without '_details.csv') as keys and full file paths as values.
    """
    collection_files = {}
    
    # Check if the directory exists
    if not os.path.exists(documents_csv_path):
        print("The directory for collection files does not exist. Please check the path.")
        return collection_files
    
    for filename in os.listdir(documents_csv_path):
        if filename.endswith("_details.csv") :
            collection_name = filename.replace("_details.csv", "")
            collection_files[collection_name] = os.path.join(documents_csv_path, filename)
    
    return collection_files

def delete_all_documents_in_collection(api_key, csv_file_path):
    """
    Delete all documents in a collection and remove the CSV file if all deletions are successful.

    Parameters:
    - api_key: The API key for authentication.
    - csv_file_path: Path to the CSV file storing document details.
    """
    if not os.path.exists(csv_file_path):
        print("The CSV file does not exist. No deletions to perform.")
        return

    # Ask for confirmation before deleting documents
    confirm = input("Are you sure you want to delete all documents in the collection? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Deletion canceled.")
        return

    # Read document IDs from the CSV file
    document_ids = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)  # Skip the header row
        for row in reader:
            document_ids.append(row[2])  # Assuming document_id is in the 3rd column

    # Loop through document IDs and delete each document
    for document_id in document_ids:
        delete_document(api_key, document_id)

    # Delete the CSV file since the collection is now empty
    os.remove(csv_file_path)
    print(f"All documents have been deleted, and the CSV file '{csv_file_path}' has been removed.")

def delete_document(api_key, document_id):
    """
    Delete a single document using the API.

    Parameters:
    - api_key: The API key for authentication.
    - document_id: The ID of the document to delete.
    """
    api_url = f"https://api.chatdoc.com/api/v2/documents/{document_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(api_url, headers=headers)
    
    if response.status_code == 200:
        print(f"Document {document_id} deleted successfully.")
    else:
        print(f"Error deleting document {document_id}: {response.status_code}, {response.text}")
                
# ============================
# Delete Pdf By Id 
# ============================ 
def select_collection(documents_csv_path):
    """
    Display available collections and prompt the user to select one.
    Returns the path to the CSV file of the chosen collection.
    """
    collection_files = list_collection_files(documents_csv_path)
    
    if not collection_files:
        print(f"Error: The CSV document details file in '{documents_csv_path}' does not exist, or no collections have been created yet.")
        return None

    print("Available collections:")
    for idx, name in enumerate(collection_files, start=1):
        print(f"{idx}. {name}")
    
    choice = input("Select the collection number from which you want to delete a document: ").strip()
    try:
        choice = int(choice)
        collection_name = list(collection_files.keys())[choice - 1]
        return collection_files[collection_name]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")
        return None

def delete_single_document(api_key, documents_csv_path):
    """
    Prompts the user to delete a document by ID with confirmation, checks for existence, and removes from CSV if found.
    """
    csv_file_path = select_collection(documents_csv_path)
    if not csv_file_path:
        return  # Exit if no valid collection is chosen

    pdf_documents = get_all_pdfs(csv_file_path)
    if not pdf_documents:
        print("There are no PDF documents in the selected collection.")
        return

    print_pdf_list(pdf_documents)
    
    document_number = input("Please enter the number of the document to delete: ").strip()
    try:
        document_number = int(document_number)
        if document_number < 1 or document_number > len(pdf_documents):
            print("Invalid number. Please choose a valid document number.")
            return
        document_id = pdf_documents[document_number - 1][1]
        document_name = pdf_documents[document_number - 1][0]
    except ValueError:
        print("Please enter a valid number.")
        return

    confirm = input(f"Are you sure you want to delete the document '{document_name}' (ID: {document_id})? (yes/no): ").strip().lower()
    if confirm == "yes":
        delete_document_by_id(api_key, document_id, csv_file_path)
    else:
        print("Deletion canceled.")

def delete_document_by_id(api_key, document_id, csv_file_path):
    """
    Deletes a document via the API and removes its entry from the CSV file if successful.
    """
    api_url = f"https://api.chatdoc.com/api/v2/documents/{document_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.delete(api_url, headers=headers)
    
    if response.status_code == 200:
        print("Document deleted from the collection successfully.")
        remove_document_from_csv(document_id, csv_file_path)
    else:
        print(f"Failed to delete the document from the collection. Status code: {response.status_code}, Message: {response.text}")

def remove_document_from_csv(document_id, csv_file_path):
    """
    Remove the entry of a document from the CSV file based on document ID.
    """
    temp_file_path = "temp.csv"
    
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file, \
         open(temp_file_path, mode='w', newline='', encoding='utf-8') as temp_file:
        
        reader = csv.reader(csv_file)
        writer = csv.writer(temp_file)
        
        headers = next(reader)
        writer.writerow(headers)
        
        rows_written = 0
        for row in reader:
            if row[2] != document_id:
                writer.writerow(row)
                rows_written += 1

    os.replace(temp_file_path, csv_file_path)
    
    if rows_written == 0:
        os.remove(csv_file_path)
        print("CSV file was empty after deletion and has been removed.")
    else:
        print("Document entry removed from CSV file.")

#################################################################################################################################
#################################################################################################################################
                                  # Send Question to ChatDOC and Receive Replies and Commit Files #
#################################################################################################################################
#################################################################################################################################

def send_request(payload):
    response = requests.post(
        api_url,
        json=payload,
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    )
    return response

def process_response(response):
    raw_data = response.text.split('data: ')
    answers = []
    question_id = None
    pdf_upload_id = None  # Renamed for clarity

    for entry in raw_data:
        if entry.strip():
            try:
                answer_data = json.loads(entry.strip())
                if 'id' in answer_data:
                    question_id = answer_data['id']
                if 'answer' in answer_data:
                    answers.append(answer_data['answer'])
                if 'source_info' in answer_data:
                    source_info = answer_data['source_info']
                    # Retrieve the upload_id from source_info
                    if source_info and 'upload_id' in source_info[0]:
                        pdf_upload_id = source_info[0]['upload_id']
            except json.JSONDecodeError:
                print('JSON decoding error:', entry)

    full_answer = ''.join(answers)
    return full_answer, question_id, pdf_upload_id  # Return pdf_upload_id

def create_question(question_text, document_ids):
    if isinstance(document_ids, list) and document_ids:
        upload_ids = document_ids  # List of document IDs
    else:
        print("Invalid document IDs provided.")
        return

    # Create the payload for the request
    payload = {
        'question': question_text,
        'upload_ids': upload_ids  # Include all document IDs
    }

    response = send_request(payload)

    if response.status_code == 200:
        full_answer, question_id, pdf_source_info_id = process_response(response)
        return full_answer, question_id, pdf_source_info_id
    else:
        try:
            print('Request error:', response.json())
        except ValueError:
            print('Non-JSON request error:', response.text)

def read_questions_in_file(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'## Prompt\s*(.*?)\s*## Prompt provided by', content, re.DOTALL)
    return match.group(1).strip() if match else None

def read_questions_from_folder(folder, file_pattern):
    questions = []
    
    for file_name in os.listdir(folder):
        if re.match(file_pattern, file_name):
            file_path = os.path.join(folder, file_name)
            question = read_questions_in_file(file_path)
            if question:
                questions.append((file_path, question))

    return questions

def check_collections_in_csv(collection_names, document_folder):
    existing_collections = {}
    missing_collections = []
    documents_id = []

    for collection_name in collection_names:
        collection_file_path = os.path.join(document_folder, f"{collection_name}_details.csv")
        
        try:
            with open(collection_file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                collection_docs = [row["Document ID"].strip() for row in reader]
                
                documents_id.extend(collection_docs)
                existing_collections[collection_name] = collection_file_path

        except FileNotFoundError:
            missing_collections.append(collection_name)
        except IOError as e:
            print(f"Error reading CSV file {collection_file_path}: {e}")

    return existing_collections, missing_collections, documents_id

def extract_collections_from_response(question_file_path):
    question_number = os.path.basename(question_file_path).split('prompt.md')[0]
    response_file_path = os.path.join(os.path.dirname(question_file_path), f"{question_number}response.md")
    
    collections = []
    config_section = False

    try:
        with open(response_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if '## Test Configuration' in line:
                    config_section = True
                elif line.startswith('## ') and config_section:
                    break
                elif config_section:
                    collections += re.findall(r'\b\w+_set\b', line)
    except FileNotFoundError:
        print(f"File not found: {response_file_path}")
    except IOError as e:
        print(f"Error reading file {response_file_path}: {e}")

    return collections

def find_pdf_name_by_upload_id(upload_id, document_folder):
    for csv_file in os.listdir(document_folder):
        if csv_file.endswith("_details.csv"):
            collection_file_path = os.path.join(document_folder, csv_file)
            try:
                with open(collection_file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Document ID"].strip() == upload_id:
                            return row["Document Name"].strip()  # Returns the PDF file name
            except Exception as e:
                print(f"Error reading file {collection_file_path}: {e}")
    return None  # If file name is not found

def store_response_in_file(question_num, question, response, pdf_name):
    """Rewrites the response and date in the output file specific to the question."""
    date_response = datetime.now().strftime("%b %d %Y")
    
    file_name = f"{str(question_num).zfill(4)}ra_notebooklm.md"  # Create the file name with zfill
    file_path = os.path.join('D:/AI Test System/Source Files', file_name)
    
    # Rewrite the file, clearing any previous content and storing the new data
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"## NotebookLM Version\n")
        f.write(f"{date_response}\n")  # Write the version and date
        f.write(f"## Response\n")  # Write the response header
        f.write(f"{response}\n")  # Write the response
        f.write(f"## Links\n")  # Write the empty links section
        f.write(f"{pdf_name}\n\n")  # Separator line

def display_read_questions(questions):
    print("\n--- Reading Questions ---\n")
    print("Reading questions from files:")
    for question_file, _ in questions:
        print(f"- {question_file}")

def display_details(questions_data):
    print("\n--- Question Details ---\n")
    for question_data in questions_data:
        file_name = os.path.basename(question_data['file'])
        print(f"Question {question_data['number']} : File {file_name}")
        print(f"- Question : {question_data['text']}")
        print(f"- Available collections : {', '.join(question_data['collections'])}")
        print(f"- Answer : {question_data['answer']}")
        print(f"- PDF file name : {question_data['pdf_name']}")
        print("-" * 50 + "\n")
    print("\n--- End of display ---\n")

def commit_and_push_changes(questions_folder, commit_message, remote_url, username, token, branch="main"):
    """
    Commits and pushes all modified files to a specified Git repository.
    Configures the remote URL if not already set.
    """
    try:
        os.chdir(questions_folder)

        # Check if a remote is already configured
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        remotes = result.stdout.strip()
        if remote_url not in remotes:
            print(f"Remote not configured. Adding remote URL: {remote_url}")
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        else:
            print(f"Remote URL already configured: {remote_url}")

        # Check for modified files
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        modified_files = result.stdout.strip()

        if not modified_files:
            print("No changes detected. Nothing to commit.")
            return

        # Add all changes
        subprocess.run(['git', 'add', '--all'], check=True)
        
        # Include the current date in the commit message
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_commit_message = f"{commit_message} - {current_date}"

        # Commit the changes
        subprocess.run(['git', 'commit', '-m', full_commit_message], check=True)

        # Format the push command with token authentication
        push_command = f'https://{username}:{token}@{remote_url[8:]}'

        # Push to the remote repository
        subprocess.run(['git', 'push', '-u', push_command, branch], check=True)

        print(f"Changes committed and pushed successfully to branch '{branch}' with message: '{full_commit_message}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")   
         
# ============================
# Menu and main logic
# ============================
def display_main_menu():
    """Display the main menu."""
    print("\n========== Main Menu ==========")
    print("1. Create Collection                - Create a new collection")
    print("2. Manage Collections               - Manage existing collections")
    print("3. Send Questions                   - Send Questions to ChatDOC")
    print("4. Exit                             - Close the program")
    print("===================================\n")
    
def display_collection_menu():
    print("\n========== Main Menu ==========")
    print("1. Display All Collections Details  - View available collections")
    print("2. Display Quota Information        - View available storage quota")
    print("3. List All PDF Documents           - Show all PDFs in the system")
    print("4. Get PDF Details by ID            - Retrieve details for a specific PDF")
    print("5. Add All PDFs to a Collection     - Upload all PDFs in a folder to a collection")
    print("6. Add PDF by Name                  - Upload a single PDF by name")
    print("7. Delete PDF by ID                 - Remove a specific PDF using its ID")
    print("8. Delete All PDFs in Collection    - Clear all PDFs from a collection")
    print("9. Return to Main Menu              - Go back to the main menu")
    print("===================================\n")

def main():
    while True:
        display_main_menu()
        choice = input("Please select an option: ")
        
        if choice == '1':
            create_new_collection()
        
        elif choice == '2':
            while True:
                display_collection_menu()
                collection_choice = input("Please choose a management option: ")
                if collection_choice == '1':
                    get_all_created_collections(collections_csv_path)  # Call the function to get all created collections
                    
                    
                elif collection_choice == '2':
                    get_quota()  # Call the function to get quota info
                    
                    
                elif collection_choice == "3":
                    collections = get_all_pdfs_from_directory(documents_csv_path)
                    if collections:
                        print_collections(collections)
                        
                        collection_choice = input("Please enter the number of the collection you want to view: ")
                        
                        try:
                            collection_index = int(collection_choice) - 1
                            collection_name = list(collections.keys())[collection_index]
                            documents = collections[collection_name]
                            print_documents(collection_name, documents)

                        except (ValueError, IndexError):
                            print("Invalid input. Please enter a valid number.")
                    else:
                        print(f"Error: The CSV document details file in '{documents_csv_path}' does not exist, or no collections have been created yet.")
                
                elif collection_choice == "4":
                    collections = get_all_pdfs_from_directory(documents_csv_path)
                    if collections:  # Only proceed if collections were found
                        print_collections(collections)  # Display collections
                        
                        # Ask the user to select a collection by its number
                        collection_choice = input("Please enter the number of the collection you want to view: ")
                        
                        # Validate input
                        try:
                            collection_index = int(collection_choice) - 1  # Convert to zero-based index
                            collection_name = list(collections.keys())[collection_index]
                            documents = collections[collection_name]
                            print_documents(collection_name, documents)  # Show documents in the selected collection
                            
                            # Ask the user to select a document by its number
                            document_choice = input("Please enter the number of the document you want to view details for: ")
                            
                            # Validate input
                            document_index = int(document_choice) - 1  # Convert to zero-based index
                            if 0 <= document_index < len(documents):
                                document_name, document_id = documents[document_index]
                                document_details = get_document(api_key, document_id)
                                format_document_details(document_details)
                            else:
                                print("Invalid selection. Please enter a valid number.")
                        except (ValueError, IndexError):
                            print("Invalid input. Please enter a valid number.")
                    else:
                        print(f"Error: The CSV document details file in '{documents_csv_path}' does not exist, or no collections have been created yet.")
                    
                    
                elif collection_choice == "5":
                    upload_documents_from_folder(collections_csv_path)
                
                
                elif collection_choice == "6":
                    upload_document_from_folder(collections_csv_path)  # Appeler la fonction d'upload avec la collection sélectionnée

                            
                elif collection_choice == '7':
                    delete_single_document(api_key, documents_csv_path)  # Call the delete document function    
                
                
                elif collection_choice == '8':
                    collection_files = list_collection_files(documents_csv_path)
                    if collection_files:
                        print("Available collections:")
                        for i, collection_name in enumerate(collection_files.keys(), start=1):
                            print(f"{i}. {collection_name}")
                        
                        # Let the user choose a collection
                        choice = input("Please enter the number of the collection you want to delete all documents from: ")
                        
                        try:
                            selected_index = int(choice) - 1  # Convert to zero-based index
                            if 0 <= selected_index < len(collection_files):
                                collection_name = list(collection_files.keys())[selected_index]
                                csv_file_path = collection_files[collection_name]
                                
                                # Delete all documents in the selected collection
                                delete_all_documents_in_collection(api_key, csv_file_path)
                            else:
                                print("Invalid selection. Please enter a valid number.")
                        except ValueError:
                            print("Invalid input. Please enter a number.") 
                    else:
                        print(f"Error: The CSV document details file in '{documents_csv_path}' does not exist, or no collections have been created yet.")
                        
                        
                elif collection_choice == '9':
                    break  # Go back to the main menu
                else:
                    print("Invalid choice. Please enter a valid option.")
                    
        elif choice == '3':
            confirmation = input(
                "Are you sure you want to send the questions to ChatDoc? Type 'yes' to proceed or 'no' to return to the main menu: "
            ).strip().lower()

            if confirmation != 'yes':
                print("\nReturning to the main menu...\n")
                # display_main_menu()
                continue
                  
            questions = read_questions_from_folder(questions_folder, file_pattern)
            questions_data = []
            # Display read questions
            display_read_questions(questions)
    
            print("\n--- Sending Questions ---\n")
            for question_file_path, question_text in questions:
                question_number = os.path.basename(question_file_path).split('prompt.md')[0]
                
                collection_names = extract_collections_from_response(question_file_path)
                
                existing_collections, missing_collections, documents_id = check_collections_in_csv(collection_names, documents_csv_path)
                
                # Prepare data for detailed display
                question_data = {
                    'number': question_number,
                    'file': question_file_path,
                    'text': question_text,
                    'collections': collection_names,
                    'answer': "Awaiting response...",  # Placeholder for the answer
                    'pdf_upload_id': None,  # Key for PDF upload ID
                    'pdf_name': None  # PDF file name
                }
                questions_data.append(question_data)
        
                if documents_id:
                    print(f"\nSending question: {question_text}")
                    full_answer, question_id, pdf_upload_id = create_question(question_text, documents_id)
                    question_data['answer'] = full_answer
                    print(f"Question ID: {question_id}\n")
                    if full_answer:
                        question_data['answer'] = full_answer
                        question_data['pdf_upload_id'] = pdf_upload_id
                        
                        # Find the PDF file name
                        pdf_name = find_pdf_name_by_upload_id(pdf_upload_id, documents_csv_path)
                        question_data['pdf_name'] = pdf_name
                        
                store_response_in_file(question_number, question_text, full_answer, pdf_name)
            
            # Display details of processed questions
            display_details(questions_data)
            
            # Commit the changes in Git
            commit_and_push_changes(questions_folder, commit_message, remote_url, username, token, branch)

             
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()
    