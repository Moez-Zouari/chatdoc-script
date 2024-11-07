import os
import requests
import csv

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
        if filename.endswith("_details.csv"):
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

# Example usage
if __name__ == "__main__":
    api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"
    documents_csv_path = "D:/AI Test System/csv details/documents"
    
    # List available collections
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
        print("No collections found or the collections CSV file does not exist.")