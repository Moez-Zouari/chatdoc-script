import csv
import os

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

# Example usage
if __name__ == "__main__":
    documents_csv_path = "D:/AI Test System/csv details/documents"  # Path to the directory containing collection CSV files
    
    # List available collection files
    collection_files = list_collection_files(documents_csv_path)
    
    if not collection_files:
        print("No collections available in the specified directory.")
    else:
        print("Available collections:")
        for i, collection_name in enumerate(collection_files.keys(), start=1):
            print(f"{i}. {collection_name}")
        
        # Let the user choose a collection
        choice = input("Please enter the number of the collection you want to view: ")
        
        try:
            selected_index = int(choice) - 1  # Convert to zero-based index
            if 0 <= selected_index < len(collection_files):
                collection_name = list(collection_files.keys())[selected_index]
                collections_csv_path = collection_files[collection_name]
                
                # Get and display PDFs in the selected collection
                documents = get_all_pdfs(collections_csv_path)
                if documents:  # Only print if documents were found
                    print_pdf_list(documents)
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
