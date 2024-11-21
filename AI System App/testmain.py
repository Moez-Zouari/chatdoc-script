# Script Description:
# This script is designed to manage and interact with a document collection system. 
# It allows users to create collections, upload and delete documents, check quotas, 
# and send questions to ChatDoc via the API. The script receives a response from ChatDoc 
# and stores it in a Markdown file. After each execution, it commits the changes made to the 
# files in the Git repository. 
# 
# The script provides a menu-based interface with various options to manage collections 
# and documents, interact with the API, and view details related to collections and documents.
#
# Version: 1.0
# Created on: 20/11/2024
# Creator: Moez Zouari (MOZ)

import os
import subprocess
import requests
import csv
from datetime import datetime
import re
import json


# Define API variables here
api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Your API key

# Path to CSV file containing document details
documents_csv_path = "D:/AI Test System/csv details/documents"  

# Path to the CSV file for collection IDs
collections_csv_path = "D:/AI Test System/csv details/collections/collections_details.csv"

# Folder path containing PDF files for upload
folder_path = "D:\\AI Test System\\PDF Files"  # Path to the folder where PDF files are stored

# File paths and patterns
questions_folder = 'D:/AI Test System/Source Files'  # Path to the folder containing source files
file_pattern = r'^\d{4}prompt\.md$'  # Regular expression pattern for matching files (e.g., 0001prompt.md)

# Parameters for commit message and Git repository
commit_message = "Update files"  # Commit message to use when pushing changes
remote_url = "https://git.intern.lauterbach.com/mzouari/AIPromptManagementSystem.git"  # Remote Git repository URL
username = "mzouari"  # Your Git username
token = "36b00d788950edf7f2ac01360595c3ed1875b9b0"  # Your Git authentication token (use with caution)
branch = "main"  # The branch to commit to (default: "main")


# API URLs for uploading documents and managing collections
upload_url = "https://api.chatdoc.com/api/v2/documents/upload"  # API URL for uploading documents to the server
question_url = "https://api.chatdoc.com/api/v2/questions/multi-documents"  # API URL for sending multi-document questions and queries
collection_url = "https://api.chatdoc.com/api/v2/collections"  # API URL for creating a new collection in the system
quota_url = "https://api.chatdoc.com/api/v2/users/quota"  # API URL to retrieve the user's quota information
document_url = "https://api.chatdoc.com/api/v2/documents/"  # API URL for accessing and managing specific documents by their ID

# HTTP headers for API requests
headers = {
    "Authorization": f"Bearer {api_key}"  # Authorization header using Bearer token
}


#################################################################################################################################
                                                        # Create Collections #
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
    This function prompts the user for confirmation to create a new collection.
    If confirmed, it asks for the collection name, creates the collection using the provided name,
    and stores the collection's details. If the user cancels the operation, it will notify them.
    """
    # Confirm with the user before proceeding
    confirmation = input("Do you really want to create a new collection? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        # Prompt the user to enter the collection name
        collection_name = input("Enter the name for the new collection: ")
        
        # Call the function to create the collection and get the collection ID and name
        collection_id, collection_name = create_collection(collection_name)
        
        # If the collection was successfully created, store its details
        if collection_id:
            store_collection_details(collection_id, collection_name)
    else:
        # Notify the user that the creation process was canceled
        print("Collection creation canceled.")

#################################################################################################################################       
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
                                                        # Manage Collections #
#################################################################################################################################


    
# ============================
# Get Quota
# ============================
def get_quota():
    """
    Retrieves the user's quota information from the ChatDoc API and displays it in a formatted manner.
    The function sends a GET request to the ChatDoc API to fetch the quota details and then extracts
    relevant information such as the maximum number of questions, questions used, max elite pages, and elite pages used.
    """

    # Send the GET request to obtain the quota
    response = requests.get(quota_url, headers=headers)

    # Check the response status
    if response.status_code == 200:
        # Parse the JSON response to extract quota details
        quota_info = response.json()
        
        # Extract relevant package information
        package_info = quota_info.get('data', {}).get('package', {})
        question_info = package_info.get('question', {})
        elite_page_info = package_info.get('elite_page', {})
        
        # Display formatted quota information
        print("Quota Information:")
        print(f"- Max Questions: {question_info.get('max_count', 0)}")
        print(f"- Questions Used: {question_info.get('used_count', 0)}")
        print(f"- Max Elite Pages: {elite_page_info.get('max_count', 0)}")
        print(f"- Elite Pages Used: {elite_page_info.get('used_count', 0)}")
    else:
        # If the request failed, print the error status and message
        print("Error:", response.status_code, response.text)

        
#################################################################################################################################       
# ============================
# Add all PDFs to collection
# ============================
def get_collections_from_csv(collections_csv_path):
    """Retrieve collections from the CSV file and store them in a dictionary with collection names as keys and IDs as values."""
    collections = {}
    try:
        # Open the CSV file in read mode
        with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            # Loop through each row and store collection name and ID in a dictionary
            for row in reader:
                collections[row["Collection Name"]] = row["Collection ID"]
    except FileNotFoundError:
        # Handle the case where the CSV file doesn't exist
        print(f"Error: The CSV collections details file {collections_csv_path} does not exist, or no collections have been created yet.")
        return None
    return collections


def list_folders(base_path):
    """List all subfolders in the specified base path."""
    # List all items in the directory at the base_path, filter only directories
    return [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]

def upload_documents_from_folder(collections_csv_path):
    """Upload documents from the specified folder to the selected collection."""
    # Retrieve collections from the CSV file
    collections = get_collections_from_csv(collections_csv_path)
    
    # If no collections are available, exit the function
    if not collections:
        return

    # Display available collections to the user and prompt them to select one
    print("Available collections:")
    for i, (collection_name, collection_id) in enumerate(collections.items(), start=1):
        print(f"{i}. {collection_name} (ID: {collection_id})")

    # Ask the user to select a collection by number
    choice = int(input("Select a collection by number: ")) - 1
    if choice < 0 or choice >= len(collections):
        print("Invalid selection. Exiting.")
        return

    # Get the collection details from the selected choice
    selected_collection_name, collection_id = list(collections.items())[choice]

    # List all available folders in the PDF files directory
    pdf_base_path = "D:/AI Test System/PDF Files"
    available_folders = list_folders(pdf_base_path)

    # If no folders are found, exit the function
    if not available_folders:
        print("No folders found in the PDF files directory.")
        return

    # Display available folders to the user and prompt them to select one
    print("Available folders for PDF documents:")
    for i, folder_name in enumerate(available_folders, start=1):
        print(f"{i}. {folder_name}")

    # Ask the user to select a folder by number
    folder_choice = int(input("Select a folder by number: ")) - 1
    if folder_choice < 0 or folder_choice >= len(available_folders):
        print("Invalid selection. Exiting.")
        return

    # Get the path for the selected folder
    selected_folder = available_folders[folder_choice]
    folder_path = os.path.join(pdf_base_path, selected_folder)

    # Check if the folder is empty or does not contain PDF files
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"The selected folder '{selected_folder}' is empty or does not contain any PDF files. Upload cancelled.")
        return

    # Define the path for logging document details in CSV format
    collection_csv_path = f"D:/AI Test System/csv details/documents/{selected_collection_name.replace(' ', '_')}_details.csv"

    # Ask the user if they want to check their quota before uploading
    check_quota = input("Do you want to check your quota before uploading documents? (yes/no): ").strip().lower()
    if check_quota == 'yes':
        get_quota()  # Call the function to display the quota

    # Confirm document upload with the user
    confirm_upload = input("Do you really want to add documents to the collection? (yes/no): ").strip().lower()
    if confirm_upload != 'yes':
        print("Document upload canceled.")
        return  # Exit if the user does not want to upload documents

    # Proceed with uploading each PDF file in the selected folder
    for filename in pdf_files:
        file_path = os.path.join(folder_path, filename)
        upload_document(collection_id, selected_collection_name, file_path, collection_csv_path)

    # Display a message indicating that document details have been logged in the CSV file
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
        

#################################################################################################################################
# =======================================
# Add PDF By Name To Collection
# =======================================
def upload_document_from_folder(collections_csv_path):
    """
    Upload a specific PDF document from a selected folder to a chosen collection.

    Parameters:
    collections_csv_path (str): The path to the CSV file containing collection details.

    Steps:
    1. Retrieve and display available collections from the CSV file.
    2. Prompt the user to select a collection.
    3. Display available folders containing PDF files.
    4. Prompt the user to select a folder.
    5. Ask the user to specify the PDF file to upload.
    6. Verify the file's existence in the selected folder.
    7. Optionally check the API quota before proceeding.
    8. Confirm the upload action with the user.
    9. Upload the specified document to the selected collection.
    10. Log the document's details in a corresponding CSV file.

    Notes:
    - Ensures user input is validated for proper selection.
    - Displays helpful messages in case of invalid input or errors.
    """
    collections = get_collections_from_csv(collections_csv_path)
    
    if not collections:
        return

    # Display collections and prompt the user to select one
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

    # Display available folders and prompt the user to select one
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

    # Ask the user for the specific document name to upload
    document_name = input("Enter the name of the PDF document to upload (with extension): ").strip()
    file_path = os.path.join(folder_path, document_name)

    # Check if the specified document exists in the selected folder
    if not os.path.isfile(file_path):
        print(f"The document '{document_name}' does not exist in the selected folder. Upload cancelled.")
        return

    collection_csv_path = f"D:/AI Test System/csv details/documents/{selected_collection_name.replace(' ', '_')}_details.csv"

    # Optionally check the API quota before uploading
    check_quota = input("Do you want to check your quota before uploading documents? (yes/no): ").strip().lower()
    if check_quota == 'yes':
        get_quota()  # Call the function to display the quota

    # Confirm the upload action
    confirm_upload = input("Do you really want to add this document to the collection? (yes/no): ").strip().lower()
    if confirm_upload != 'yes':
        print("Document upload canceled.")
        return

    # Proceed with uploading the specified document
    upload_document(collection_id, selected_collection_name, file_path, collection_csv_path)

    # Inform the user that the document details have been logged
    print(f"Document details logged in '{collection_csv_path}'.")


#################################################################################################################################
# ============================
# Get All Pdf Id From Csv
# ============================
def get_all_pdfs(collections_csv_path):
    """
    Retrieves a list of all PDF document names and IDs from the specified CSV file.

    Parameters:
    - collections_csv_path (str): Path to the CSV file containing document details.

    Returns:
    - A list of tuples containing document names and IDs if the file exists and contains data.
    - None if the file does not exist or is empty.

    Steps:
    1. Verify the existence of the CSV file.
    2. Open the CSV file and read its contents.
    3. Check if the file has rows; return None if empty.
    4. Extract and compile document names and IDs from the CSV rows.
    """
    if not os.path.isfile(collections_csv_path):
        print(f"The specified CSV file '{collections_csv_path}' does not exist.")
        return None
    
    documents = []
    
    with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Read all rows and check for content
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
    Displays a numbered list of PDF documents along with their IDs.

    Parameters:
    - documents (list): A list of tuples where each tuple contains:
        - document_name (str): The name of the PDF document.
        - document_id (str): The ID of the PDF document.

    Steps:
    1. Calculate and print the total number of PDF documents.
    2. Print each document name in a numbered format.
    """
    total_pdfs = len(documents)
    print(f"Total number of PDF documents: {total_pdfs}")
    
    print("List of PDF documents:")
    for index, (name, doc_id) in enumerate(documents, start=1):
        print(f"{index}. {name}")

        
#################################################################################################################################
# ============================
# Get Pdf By Id
# ============================
def get_all_pdfs_from_directory(documents_csv_path):
    """
    Retrieves all PDF document names and IDs from CSV files within a specified directory.

    Parameters:
    - documents_csv_path (str): Path to the directory containing CSV files with document details.

    Returns:
    - dict: A dictionary where:
        - Keys are collection names (derived from the CSV file names without extensions).
        - Values are lists of tuples containing (document_name, document_id).

    Workflow:
    1. Verify if the specified directory exists.
    2. Iterate over all `.csv` files in the directory.
    3. Extract document details (name and ID) from each CSV file.
    4. Skip empty files or files without valid document details.
    5. Store the results in a dictionary, keyed by collection names.

    Notes:
    - If the directory does not exist or contains no valid files, `None` is returned.
    - Empty CSV files are ignored, and a message is printed for each empty file.
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
    Displays the list of collections in a numbered format.

    Parameters:
    - collections (dict): 
      A dictionary where:
        - Keys are collection names.
        - Values are lists of tuples containing (document_name, document_id).

    Workflow:
    1. Check if the `collections` dictionary is not empty.
    2. Print each collection name with its corresponding index.
    3. If no collections are found, print an appropriate message.

    Notes:
    - An empty line is added after the list for better readability.
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
    Displays the list of PDF documents and their IDs for a specified collection.

    Parameters:
    - collection_name (str): The name of the collection to which the documents belong.
    - documents (list of tuples): 
      A list where each tuple contains:
        - document_name (str): The name of the document.
        - document_id (str): The unique identifier of the document.

    Workflow:
    1. Print the collection name as a header.
    2. Display the total number of documents within the collection.
    3. Iterate through the documents, printing their index, name, and ID in a formatted style.
    4. Add an empty line after the document list for better readability.

    Notes:
    - Provides a clear and organized structure to make it easier to identify documents.
    """
    print(f"Documents in '{collection_name}':")
    total_documents = len(documents)
    print(f"Total number of documents: {total_documents}")  # Display the total number of documents
    for index, (name, doc_id) in enumerate(documents, start=1):
        print(f"  {index}. {name} (ID: {doc_id})")
    print()  # Add an empty line for better readability


def get_document(api_key, document_id):
    """
    Fetches the details of a specific document from the ChatDoc API using its unique ID.

    Parameters:
    - api_key (str): The API key used for authentication with ChatDoc.
    - document_id (str): The unique identifier of the document to retrieve.

    Returns:
    - dict: The document details as a dictionary if the request is successful.
    - None: If the document is not found or an error occurs during the request.

    Workflow:
    1. Construct the API URL dynamically using the provided document ID.
    2. Set up the request headers to include the API key for authentication.
    3. Send a GET request to the ChatDoc API to retrieve document details.
    4. Handle API responses:
       - 200: Success, return the document details as JSON.
       - 404: Document not found, print an error message.
       - Other errors: Print the status code and error details for troubleshooting.

    Notes:
    - Ensure the `requests` library is installed in your environment to use this function.
    - Keep your API key secure to prevent unauthorized access.
    """
    # Define the API URL with the user-provided document ID
    get_document_url = f"{document_url}{document_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Send the request
    response = requests.get(get_document_url, headers=headers)

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
    Formats and displays the details of a document retrieved from the ChatDoc API.

    Parameters:
    - document_details (dict): A dictionary containing the document details returned by the API.

    Workflow:
    1. Check if the document details are available and contain the 'data' key.
    2. Extract relevant information such as ID, name, status, type, creation date, and OCR type.
    3. Format the creation date into a human-readable format if available.
    4. Print the extracted details in a structured format.
    5. Handle cases where document details are not available by displaying an appropriate message.

    Notes:
    - Ensure the document details passed to the function are in the expected format.
    - Use `datetime.fromtimestamp` for converting Unix timestamps into readable dates.
    """
    if document_details and 'data' in document_details:
        data = document_details['data']
        print("Document Details:")
        print(f"  ID: {data.get('id', 'N/A')}")
        print(f"  Name: {data.get('name', 'N/A')}")
        print(f"  Status: {data.get('status', 'N/A')}")
        print(f"  Type: {data.get('type', 'N/A')}")
        
        # Convert and format the creation date if available
        created_at = (
            datetime.fromtimestamp(data.get('created_at')).strftime('%Y-%m-%d %H:%M:%S')
            if data.get('created_at') else "N/A"
        )
        print(f"  Created at: {created_at}")
        print(f"  OCR Type: {data.get('ocr_type', 'N/A')}")
    else:
        print("No document details available.")
        
        

#################################################################################################################################    
# ===================================
# Delete All Pdfs In Give Collection
# =================================== 
def list_collection_files(documents_csv_path):
    """
    Lists all collection CSV files in the specified directory, excluding specific files like 'collections_details.csv'.

    Parameters:
    - documents_csv_path (str): Path to the directory containing collection CSV files.

    Returns:
    - dict: A dictionary where the keys are collection names (file names without '_details.csv') 
            and the values are the full file paths.

    Workflow:
    1. Verify if the specified directory exists.
    2. Iterate through files in the directory.
    3. Identify files ending with '_details.csv' and exclude specific ones (e.g., 'collections_details.csv').
    4. Format the collection name by removing '_details.csv' from the file name.
    5. Map the formatted name to its full file path in a dictionary.

    Notes:
    - If the directory does not exist, an empty dictionary is returned with a message.
    - Ensure the directory path is correct before calling this function.
    """
    collection_files = {}
    
    # Verify if the directory exists
    if not os.path.exists(documents_csv_path):
        print("The directory for collection files does not exist. Please check the path.")
        return collection_files
    
    # Iterate over files in the directory
    for filename in os.listdir(documents_csv_path):
        if filename.endswith("_details.csv"):
            # Format the collection name by removing '_details.csv'
            collection_name = filename.replace("_details.csv", "")
            collection_files[collection_name] = os.path.join(documents_csv_path, filename)
    
    return collection_files

def delete_all_documents_in_collection(api_key, csv_file_path):
    """
    Deletes all documents in a collection and removes the CSV file if all deletions are successful.

    Parameters:
    - api_key (str): The API key for authentication.
    - csv_file_path (str): Path to the CSV file storing document details.

    Workflow:
    1. Check if the specified CSV file exists.
    2. Confirm the deletion action with the user.
    3. Read document IDs from the CSV file.
    4. Delete each document using the `delete_document` function.
    5. If successful, remove the CSV file.
    """
    # Verify if the CSV file exists
    if not os.path.exists(csv_file_path):
        print("The CSV file does not exist. No deletions to perform.")
        return

    # Ask for confirmation
    confirm = input("Are you sure you want to delete all documents in the collection? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Deletion canceled.")
        return

    document_ids = []

    # Read document IDs from the CSV file
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)  # Skip the header row
            
            # Assuming 'Document ID' is in the 3rd column
            for row in reader:
                if len(row) >= 3:  # Ensure row has sufficient columns
                    document_ids.append(row[2])

        if not document_ids:
            print("No document IDs found in the CSV file.")
            return

        # Loop through document IDs and delete each
        for document_id in document_ids:
            response = delete_document(api_key, document_id)
            if response:
                print(f"Document with ID {document_id} deleted successfully.")
            else:
                print(f"Failed to delete document with ID {document_id}. Continuing with the next...")

        # Remove the CSV file if all documents are deleted
        os.remove(csv_file_path)
        print(f"All documents have been deleted, and the CSV file '{csv_file_path}' has been removed.")

    except Exception as e:
        print(f"An error occurred: {e}")

import requests

def delete_document(api_key, document_id):
    """
    Delete a single document using the ChatDoc API.

    Parameters:
    - api_key (str): The API key for authentication.
    - document_id (str): The ID of the document to delete.

    Returns:
    - bool: True if the document was successfully deleted, False otherwise.
    """
    delete_document_url = f"{document_url}{document_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(delete_document_url, headers=headers)
        
        # Check the response status code
        if response.status_code == 200:
            print(f"Document {document_id} deleted successfully.")
            return True
        else:
            print(f"Error deleting document {document_id}: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        # Handle network errors, invalid responses, etc.
        print(f"An error occurred while trying to delete document {document_id}: {e}")
        return False

 
#################################################################################################################################               
# ============================
# Delete Pdf By Id 
# ============================ 
def select_collection(documents_csv_path):
    """
    Display available collections and prompt the user to select one.
    Returns the path to the CSV file of the chosen collection.

    Parameters:
    - documents_csv_path (str): Path to the directory containing the collection CSV files.

    Returns:
    - str: Path to the CSV file of the chosen collection, or None if invalid input or no collection is found.
    """
    collection_files = list_collection_files(documents_csv_path)
    
    if not collection_files:
        print(f"Error: No collection files found in '{documents_csv_path}'. Please create collections first.")
        return None

    print("Available collections:")
    for idx, name in enumerate(collection_files, start=1):
        print(f"{idx}. {name}")
    
    while True:
        choice = input("Select the collection number from which you want to delete a document (or type 'exit' to quit): ").strip()
        
        # Allow user to exit gracefully
        if choice.lower() == 'exit':
            print("Exiting selection process.")
            return None

        try:
            choice = int(choice)
            if 1 <= choice <= len(collection_files):
                collection_name = list(collection_files.keys())[choice - 1]
                return collection_files[collection_name]
            else:
                print(f"Invalid selection. Please choose a number between 1 and {len(collection_files)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def delete_single_document(api_key, documents_csv_path):
    """
    Prompts the user to delete a document by ID with confirmation, checks for existence, and removes from CSV if found.

    Parameters:
    - api_key (str): The API key for authentication.
    - documents_csv_path (str): Path to the directory containing CSV files with document details.
    """
    # Select the collection CSV file
    csv_file_path = select_collection(documents_csv_path)
    if not csv_file_path:
        return  # Exit if no valid collection is chosen

    # Get all PDFs from the collection
    pdf_documents = get_all_pdfs(csv_file_path)
    if not pdf_documents:
        print("There are no PDF documents in the selected collection.")
        return

    # Print the list of documents for user to choose from
    print_pdf_list(pdf_documents)
    
    # Prompt user to select a document by number
    document_number = input("Please enter the number of the document to delete: ").strip()
    try:
        document_number = int(document_number)
        if document_number < 1 or document_number > len(pdf_documents):
            print("Invalid number. Please choose a valid document number.")
            return
        document_id = pdf_documents[document_number - 1][1]
        document_name = pdf_documents[document_number - 1][0]
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete the document '{document_name}' (ID: {document_id})? (yes/no): ").strip().lower()
    if confirm == "yes":
        # Attempt to delete the document via API
        delete_document_by_id(api_key, document_id)
        
        # If deletion is successful, remove document from the CSV
        update_csv_after_deletion(csv_file_path, document_id)
    else:
        print("Deletion canceled.")


def update_csv_after_deletion(csv_file_path, document_id):
    """
    Removes the document with the specified ID from the CSV file.

    Parameters:
    - csv_file_path (str): Path to the collection's CSV file.
    - document_id (str): The ID of the document to remove.
    """
    # Read the existing CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        rows = list(csv.DictReader(csv_file))
    
    # Remove the document from the list
    rows = [row for row in rows if row['Document ID'] != document_id]

    # Write the updated list back to the CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Document Name', 'Document ID', 'Collection Name']  # Adjust to your CSV format
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Document with ID {document_id} has been removed from the CSV file.")


def delete_document_by_id(api_key, document_id, csv_file_path):
    """
    Deletes a document via the API and removes its entry from the CSV file if successful.

    Parameters:
    - api_key (str): The API key for authentication.
    - document_id (str): The ID of the document to delete.
    - csv_file_path (str): Path to the CSV file storing document details.
    """
    delete_document_url = f"{document_url}{document_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.delete(delete_document_url, headers=headers)
    
    if response.status_code == 200:
        print("Document deleted from the collection successfully.")
        remove_document_from_csv(document_id, csv_file_path)
    else:
        print(f"Failed to delete the document from the collection. Status code: {response.status_code}, Message: {response.text}")

def remove_document_from_csv(document_id, csv_file_path):
    """
    Remove the entry of a document from the CSV file based on its document ID.
    
    This function:
    - Reads the CSV file and writes all rows to a temporary file except the row 
      corresponding to the provided document ID.
    - Replaces the original CSV file with the new temporary file.
    - If the CSV file becomes empty after the removal, it deletes the CSV file.
    
    Parameters:
    - document_id (str): The ID of the document to remove from the CSV file.
    - csv_file_path (str): The path to the CSV file containing document details.
    """
    # Define the path for the temporary file to store the modified data
    temp_file_path = "temp.csv"
    
    # Open the original CSV file in read mode and the temporary file in write mode
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file, \
         open(temp_file_path, mode='w', newline='', encoding='utf-8') as temp_file:
        
        reader = csv.reader(csv_file)
        writer = csv.writer(temp_file)
        
        # Write the header row to the temporary file
        headers = next(reader)
        writer.writerow(headers)
        
        # Initialize a counter for rows written to the temporary file
        rows_written = 0
        
        # Loop through each row in the original CSV file
        for row in reader:
            # If the document ID in the row doesn't match the document to remove, write the row to the temp file
            if row[2] != document_id:
                writer.writerow(row)
                rows_written += 1

    # Replace the original CSV file with the updated temporary file
    os.replace(temp_file_path, csv_file_path)
    
    # If no rows were written, the file is empty after the removal, so delete it
    if rows_written == 0:
        os.remove(csv_file_path)
        print("CSV file was empty after deletion and has been removed.")
    else:
        print("Document entry removed from CSV file.")


#################################################################################################################################
                                  # Send Question to ChatDOC and Receive Replies and Commit Files #
#################################################################################################################################

# ============================
# Check & Extract Collections
# ============================
def check_collections_in_csv(collection_names, document_folder):
    """
    Checks if collections exist in CSV files and gathers document IDs from them.

    Parameters:
    - collection_names (list): List of collection names to check.
    - document_folder (str): Path to the folder where collection CSV files are stored.

    Returns:
    - existing_collections (dict): A dictionary of existing collections with their file paths.
    - missing_collections (list): A list of collection names that are missing.
    - documents_id (list): A list of document IDs gathered from the collections.
    """
    existing_collections = {}  # Dictionary to store collections that exist
    missing_collections = []   # List to store collection names that are missing
    documents_id = []          # List to store document IDs from existing collections

    # Loop through each collection name
    for collection_name in collection_names:
        collection_file_path = os.path.join(document_folder, f"{collection_name}_details.csv")
        
        try:
            # Attempt to open the collection's CSV file
            with open(collection_file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)  # Read the CSV file as a dictionary
                collection_docs = [row["Document ID"].strip() for row in reader]  # Extract document IDs
                
                documents_id.extend(collection_docs)  # Add the document IDs to the list
                existing_collections[collection_name] = collection_file_path  # Add to the dictionary of existing collections

        except FileNotFoundError:
            missing_collections.append(collection_name)  # If file not found, add to missing list
        except IOError as e:
            print(f"Error reading CSV file {collection_file_path}: {e}")  # Handle other IO errors

    return existing_collections, missing_collections, documents_id  # Return the results

def extract_collections_from_response(question_file_path):
    """
    Extracts collection names from the response file associated with a given question file. 
    The function reads the response file, searches for the '## Test Configuration' section, 
    and collects all words ending with '_set' within that section. These words are treated as collection names.

    Parameters:
        question_file_path (str): The path to the question file, which is used to derive the response file.

    Returns:
        list: A list of collection names extracted from the response file.
    """
    
    # Extract the question number from the question file path by stripping 'prompt.md' from the filename
    question_number = os.path.basename(question_file_path).split('prompt.md')[0]
    
    # Construct the path to the corresponding response file using the question number
    response_file_path = os.path.join(os.path.dirname(question_file_path), f"{question_number}response.md")
    
    collections = []  # List to store collection names
    config_section = False  # Flag to indicate when we're in the 'Test Configuration' section

    try:
        # Open the response file and read it line by line
        with open(response_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Start extracting collection names once we reach the 'Test Configuration' section
                if '## Test Configuration' in line:
                    config_section = True
                # Stop extracting once we encounter another section header
                elif line.startswith('## ') and config_section:
                    break
                # If within the 'Test Configuration' section, find all words ending with '_set'
                elif config_section:
                    collections += re.findall(r'\b\w+_set\b', line)
    except FileNotFoundError:
        # Handle error if the response file does not exist
        print(f"File not found: {response_file_path}")
    except IOError as e:
        # Handle other IO errors
        print(f"Error reading file {response_file_path}: {e}")

    return collections  # Return the list of extracted collection names


#################################################################################################################################
# ============================
# Send Questions
# ============================
def send_request(payload):
    """
    Sends an HTTP POST request with the provided payload to the API.

    Parameters:
    - payload (dict): The data to be sent in the request body.

    Returns:
    - response: The API response object.
    """
    # Send a POST request to the API with the payload and the authorization header
    response = requests.post(
        question_url,  # The API endpoint URL
        json=payload,  # Convert the payload to JSON format
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}  # Include the API key in the request headers
    )
    return response

def process_response(response):
    """
    Processes the response from the API and extracts the relevant information.

    Parameters:
    - response: The response object returned from the API.

    Returns:
    - full_answer (str): The concatenated answer from the API response.
    - question_id (str or None): The ID of the question, if available.
    - pdf_upload_id (str or None): The PDF upload ID associated with the answer, if available.
    """
    # Split the response text by 'data: ' to separate each entry
    raw_data = response.text.split('data: ')
    
    answers = []  # List to store extracted answers
    question_id = None  # Variable to store question ID, initialized to None
    pdf_upload_id = None  # Variable to store PDF upload ID, renamed for clarity

    # Loop through each entry in the raw_data
    for entry in raw_data:
        if entry.strip():  # Skip empty entries
            try:
                # Try to parse the entry as JSON
                answer_data = json.loads(entry.strip())
                
                # Extract question ID if available
                if 'id' in answer_data:
                    question_id = answer_data['id']
                
                # Extract answer if available
                if 'answer' in answer_data:
                    answers.append(answer_data['answer'])
                
                # Extract source info and retrieve the upload ID if available
                if 'source_info' in answer_data:
                    source_info = answer_data['source_info']
                    if source_info and 'upload_id' in source_info[0]:
                        pdf_upload_id = source_info[0]['upload_id']
            except json.JSONDecodeError:
                # Handle any JSON decoding errors and print the erroneous entry
                print('JSON decoding error:', entry)

    # Concatenate all extracted answers into a single string
    full_answer = ''.join(answers)
    
    # Return the concatenated answer, the question ID, and the PDF upload ID
    return full_answer, question_id, pdf_upload_id

def create_question(question_text, document_ids):
    """
    Creates a question with the provided text and associated document IDs.

    Parameters:
    - question_text (str): The text of the question to be created.
    - document_ids (list): A list of document IDs to associate with the question.

    Returns:
    - full_answer (str): The full answer generated by the API.
    - question_id (str): The ID of the created question.
    - pdf_source_info_id (str): The ID of the PDF source info, if available.
    """
    # Check if document_ids is a valid list and is not empty
    if isinstance(document_ids, list) and document_ids:
        upload_ids = document_ids  # List of document IDs to associate with the question
    else:
        print("Invalid document IDs provided.")
        return

    # Prepare the payload for the API request
    payload = {
        'question': question_text,
        'upload_ids': upload_ids  # Include all document IDs associated with the question
    }

    # Send the request to create the question
    response = send_request(payload)

    # Handle the API response
    if response.status_code == 200:
        # Process the response to extract relevant data (answer, question ID, and PDF upload ID)
        full_answer, question_id, pdf_source_info_id = process_response(response)
        return full_answer, question_id, pdf_source_info_id
    else:
        # If the response indicates an error, print the error message
        try:
            print('Request error:', response.json())  # Attempt to parse the JSON error message
        except ValueError:
            print('Non-JSON request error:', response.text)  # If not JSON, print the raw response

def read_questions_in_file(md_file):
    """
    Reads the question from a markdown file.

    Parameters:
    - md_file (str): The path to the markdown file to read.

    Returns:
    - str: The extracted question, or None if not found.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use regex to search for the question within the markdown file
    match = re.search(r'## Prompt\s*(.*?)\s*## Prompt provided by', content, re.DOTALL)
    return match.group(1).strip() if match else None  # Return the question or None if not found

def read_questions_from_folder(folder, file_pattern):
    """
    Reads questions from all markdown files in a folder that match a specific pattern.

    Parameters:
    - folder (str): The folder containing the markdown files.
    - file_pattern (str): A regex pattern to match file names.

    Returns:
    - list: A list of tuples with file path and question text.
    """
    questions = []
    
    # Loop through all files in the folder
    for file_name in os.listdir(folder):
        # If the file matches the given pattern
        if re.match(file_pattern, file_name):
            file_path = os.path.join(folder, file_name)
            # Read the question from the file
            question = read_questions_in_file(file_path)
            if question:
                questions.append((file_path, question))  # Add the question and file path to the list

    return questions  # Return the list of questions


#################################################################################################################################
# ==================================
# Get PDF Response Source File Name
# ==================================
def find_pdf_name_by_upload_id(upload_id, document_folder):
    """
    Searches for a PDF file name by matching its upload ID in the CSV files within a given folder.
    The function iterates over all CSV files ending with '_details.csv' in the specified folder,
    checks for a matching upload ID in the 'Document ID' column, and returns the corresponding 
    PDF file name from the 'Document Name' column.

    Parameters:
        upload_id (str): The ID of the document to search for.
        document_folder (str): The folder containing the CSV files that list document details.

    Returns:
        str or None: The name of the PDF document if found, otherwise None.
    """
    
    # Loop through all files in the specified folder
    for csv_file in os.listdir(document_folder):
        # Check if the file is a CSV file containing document details
        if csv_file.endswith("_details.csv"):
            collection_file_path = os.path.join(document_folder, csv_file)
            try:
                # Open the CSV file and read its contents
                with open(collection_file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    # Iterate through each row in the CSV file
                    for row in reader:
                        # Check if the 'Document ID' matches the provided upload ID
                        if row["Document ID"].strip() == upload_id:
                            # Return the document name if a match is found
                            return row["Document Name"].strip()
            except Exception as e:
                # Handle any errors that occur while reading the CSV file
                print(f"Error reading file {collection_file_path}: {e}")

    # Return None if no matching document is found
    return None


#################################################################################################################################
# ==============================
# Store Response In Md Files
# ==============================
def store_response_in_file(question_num, question, response, pdf_name):
    """
    Writes the response, date, and relevant PDF information into a markdown file specific to the question.

    This function generates a markdown file with a specific name format based on the question number, and
    writes the following sections:
    - NotebookLM version (with the current date)
    - Response (the actual answer to the question)
    - Links (empty section for potential future use)
    - The name of the PDF file associated with the response.

    Parameters:
        question_num (int): The number of the question to create the file for. The file is named using this number.
        question (str): The question text (not used in the current implementation, but can be extended).
        response (str): The response to the question to be saved in the markdown file.
        pdf_name (str): The name of the PDF document related to the response, added under the "Links" section.

    Returns:
        None: The function writes to the file and does not return any value.
    """
    
    # Get the current date in the desired format (e.g., "Nov 18 2024")
    date_response = datetime.now().strftime("%b %d %Y")
    
    # Generate the file name using the question number, padded with leading zeros
    file_name = f"{str(question_num).zfill(4)}ra_notebooklm.md"  
    # Define the full file path where the markdown file will be saved
    file_path = os.path.join('D:/AI Test System/Source Files', file_name)
    
    # Open the file in write mode, clearing any existing content
    with open(file_path, 'w', encoding='utf-8') as f:
        # Write the notebook version and the current date to the file
        f.write(f"## NotebookLM Version\n")
        f.write(f"{date_response}\n")  # Include the date of the response
        # Write the header for the response section
        f.write(f"## Response\n")  
        f.write(f"{response}\n")  # Include the actual response text
        # Write the header for the links section (currently empty)
        f.write(f"## Links\n")  
        f.write(f"{pdf_name}\n\n")  # Add the name of the PDF related to the response


#################################################################################################################################
# =========================================
# Display Question And Details Of Response
# =========================================
def display_read_questions(questions):
    """
    Displays the list of question files that have been read.

    This function prints a header and iterates through the provided list of questions to display
    the file paths of the question files that were read. The list of questions is expected to
    be in the format of tuples where the first element is the file path of the question file.

    Parameters:
        questions (list): A list of tuples, where each tuple contains the file path of the question file
                          and the corresponding question text (though the text is not used in this function).
    
    Returns:
        None: The function prints the file paths to the console and does not return any value.
    """
    
    # Print a header for the output display
    print("\n--- Reading Questions ---\n")
    print("Reading questions from files:")
    
    # Iterate over the list of questions and display each file path
    for question_file, _ in questions:
        print(f"- {question_file}")


def display_details(questions_data):
    """
    Displays detailed information about the questions, including the question text, available collections,
    answers, and PDF file names.

    This function iterates through a list of dictionaries containing the details of each question and
    prints the relevant information for each question, including its number, associated file name,
    collections, answer, and PDF file name.

    Parameters:
        questions_data (list): A list of dictionaries, where each dictionary contains the details of a
                               question, including the file path, question number, question text,
                               available collections, the answer, and the associated PDF file name.
    
    Returns:
        None: The function prints detailed information to the console and does not return any value.
    """
    
    # Print a header to indicate the start of the question details display
    print("\n--- Question Details ---\n")
    
    # Iterate through each question data in the list and display the relevant details
    for question_data in questions_data:
        file_name = os.path.basename(question_data['file'])  # Get the base file name from the file path
        print(f"Question {question_data['number']} : File {file_name}")
        print(f"- Question : {question_data['text']}")
        print(f"- Available collections : {', '.join(question_data['collections'])}")
        print(f"- Answer : {question_data['answer']}")
        print(f"- PDF file name : {question_data['pdf_name']}")
        
        # Print a separator for readability between each question's details
        print("-" * 50 + "\n")
    
    # Print a footer indicating the end of the display
    print("\n--- End of display ---\n")


################################################################################################################################# 
# ===============================
# Commit Changes to Files in Git
# ===============================
def commit_and_push_changes(questions_folder, commit_message, remote_url, username, token, branch="main"):
    """
    Commits and pushes all modified files to a specified Git repository.
    Configures the remote URL if not already set and handles token-based authentication for pushing.
    
    This function performs the following steps:
    1. Changes the current working directory to the specified questions folder.
    2. Checks if the Git remote URL is configured. If not, it adds the remote URL.
    3. Checks for modified files. If no changes are found, it exits early.
    4. Adds all modified files to the staging area.
    5. Creates a commit with the provided commit message and the current date.
    6. Pushes the changes to the specified branch on the remote repository using the provided username and token.

    Parameters:
        questions_folder (str): The path to the folder containing the questions to commit and push.
        commit_message (str): The commit message to be used, which will include the current date.
        remote_url (str): The URL of the remote Git repository (e.g., https://github.com/username/repo.git).
        username (str): The Git username used for authentication.
        token (str): The personal access token to use for Git authentication.
        branch (str, optional): The branch to push to (default is "main").

    Returns:
        None: This function performs Git operations and prints the result to the console.
    """
    try:
        # Change to the directory containing the questions folder
        os.chdir(questions_folder)

        # Check if the remote URL is already configured
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

        # Add all changes (modified, new, and deleted files)
        subprocess.run(['git', 'add', '--all'], check=True)
        
        # Include the current date and time in the commit message
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_commit_message = f"{commit_message} - {current_date}"

        # Commit the changes
        subprocess.run(['git', 'commit', '-m', full_commit_message], check=True)

        # Format the push command with token-based authentication
        push_command = f'https://{username}:{token}@{remote_url[8:]}'

        # Push the changes to the remote repository
        subprocess.run(['git', 'push', '-u', push_command, branch], check=True)

        print(f"Changes committed and pushed successfully to branch '{branch}' with message: '{full_commit_message}'")
    
    except subprocess.CalledProcessError as e:
        # Catch errors related to subprocess (e.g., Git commands failing)
        print(f"Error during Git operations: {e}")
    except Exception as e:
        # Catch all other unexpected errors
        print(f"Unexpected error: {e}")
 
#################################################################################################################################         
# ============================
# Menu logic
# ============================
################################################################################################################################# 
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

################################################################################################################################# 
# ============================
# Main logic
# ============================
#################################################################################################################################
def main():
    # Main loop of the program, which remains active until the user chooses to exit
    while True:
        # Display the main menu to allow the user to choose an option
        display_main_menu()
        choice = input("Please select an option: ")  # Ask the user to select an option
        
        # Option 1: Create a new collection
        if choice == '1':
            create_new_collection()
        
        # Option 2: Manage existing collections
        elif choice == '2':
            while True:
                # Display the collection management menu
                display_collection_menu()
                collection_choice = input("Please choose a management option: ")
                
                # Option 2.1: View all created collections
                if collection_choice == '1':
                    get_all_created_collections(collections_csv_path)  # Call function to get all created collections
                    
                # Option 2.2: Check quota status
                elif collection_choice == '2':
                    get_quota()  # Call function to get quota information
                
                # Option 2.3: View documents within a collection
                elif collection_choice == "3":
                    collections = get_all_pdfs_from_directory(documents_csv_path)
                    if collections:
                        print_collections(collections)  # Display available collections
                        
                        # Ask the user to select a collection to view
                        collection_choice = input("Please enter the number of the collection you want to view: ")
                        
                        try:
                            # Validate the collection selection
                            collection_index = int(collection_choice) - 1
                            collection_name = list(collections.keys())[collection_index]
                            documents = collections[collection_name]
                            print_documents(collection_name, documents)  # Display documents in the selected collection

                        except (ValueError, IndexError):
                            print("Invalid input. Please enter a valid number.")
                    else:
                        print(f"Error: The CSV document details file in '{documents_csv_path}' does not exist, or no collections have been created yet.")
                
                # Option 2.4: View details of a specific document within a collection
                elif collection_choice == "4":
                    collections = get_all_pdfs_from_directory(documents_csv_path)
                    if collections:  # Only proceed if collections were found
                        print_collections(collections)  # Display available collections
                        
                        # Ask the user to select a collection
                        collection_choice = input("Please enter the number of the collection you want to view: ")
                        
                        try:
                            collection_index = int(collection_choice) - 1  # Convert to zero-based index
                            collection_name = list(collections.keys())[collection_index]
                            documents = collections[collection_name]
                            print_documents(collection_name, documents)  # Show documents in the selected collection
                            
                            # Ask the user to select a document to view details
                            document_choice = input("Please enter the number of the document you want to view details for: ")
                            
                            # Validate the document selection
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
                    
                # Option 2.5: Upload documents from a folder
                elif collection_choice == '5':
                    upload_documents_from_folder(collections_csv_path)
                
                # Option 2.6: Upload a document from a folder
                elif collection_choice == '6':
                    upload_document_from_folder(collections_csv_path)  # Call upload function with the selected collection
                
                # Option 2.7: Delete a single document
                elif collection_choice == '7':
                    delete_single_document(api_key, documents_csv_path)  # Call function to delete a document    
                
                # Option 2.8: Delete all documents from a collection
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
                        
                # Option 2.9: Exit collection management and return to the main menu
                elif collection_choice == '9':
                    break  # Go back to the main menu
                else:
                    print("Invalid choice. Please enter a valid option.")
                    
        # Option 3: Send questions to ChatDoc
        elif choice == '3':
            confirmation = input(
                "Are you sure you want to send the questions to ChatDoc? Type 'yes' to proceed or 'no' to return to the main menu: "
            ).strip().lower()

            if confirmation != 'yes':
                print("\nReturning to the main menu...\n")
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

        # Option 4: Exit the program
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()

    