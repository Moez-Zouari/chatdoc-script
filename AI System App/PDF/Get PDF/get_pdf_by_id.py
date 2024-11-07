import requests
from datetime import datetime
import csv
import os

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

# Example usage
if __name__ == "__main__":
    api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Replace with your actual API key
    documents_csv_path = "D:/AI Test System/csv details/documents"  # Path to the directory containing CSV files

    collections = get_all_pdfs_from_directory(documents_csv_path)
    if collections:  # Proceed if collections are found
        print_collections(collections)  # Display collections
        
        # Ask the user to select a collection by number
        collection_choice = input("Please enter the number of the collection you want to view: ")
        
        # Validate the input
        try:
            collection_index = int(collection_choice) - 1  # Convert to zero-based index
            collection_name = list(collections.keys())[collection_index]
            documents = collections[collection_name]
            print_documents(collection_name, documents)  # Display documents in the selected collection
            
            # Ask the user to select a document by number
            document_choice = input("Please enter the number of the document you want to view the details for: ")
            
            # Validate the input
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
        print("No collections available.")
