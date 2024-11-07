import os
import requests
import csv
import sys

# Add the 'Get PDF' folder to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Get PDF')))

# Import the function after updating the import path
from get_all_pdf_id_from_csv import get_all_pdfs, print_pdf_list

def list_collection_files(documents_csv_path):
    """
    Lists all CSV files in the specified directory, excluding 'collections_details.csv'.

    Parameters:
    - documents_csv_path: Path to the directory containing collection CSV files.

    Returns:
    - A dictionary with collection file names (without '_details.csv') as keys and full file paths as values.
    """
    collection_files = {}
    for filename in os.listdir(documents_csv_path):
        if filename.endswith("_details.csv") and filename != "collections_details.csv":
            collection_name = filename.replace("_details.csv", "")
            collection_files[collection_name] = os.path.join(documents_csv_path, filename)
    return collection_files

def select_collection(documents_csv_path):
    """
    Display available collections and prompt the user to select one.
    Returns the path to the CSV file of the chosen collection.
    """
    collection_files = list_collection_files(documents_csv_path)
    
    if not collection_files:
        print("No collections available.")
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

# Example usage
if __name__ == "__main__":
    api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Replace with your API key
    documents_csv_path = "D:/AI Test System/csv details/documents"
    delete_single_document(api_key, documents_csv_path)
