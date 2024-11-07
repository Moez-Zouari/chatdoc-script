import os
import requests
import csv
from datetime import datetime

# API URL for creating a new collection
collection_url = "https://api.chatdoc.com/api/v2/collections"

# Real API Key
api_key = "aaz"

# Headers for the API request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

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


create_new_collection()

