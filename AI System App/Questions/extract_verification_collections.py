import re
import os
import csv

def extract_collections_from_response(question_file_path):
    """Extract collection names from the response file associated with the question file."""
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
                    break  # Stop once we leave the 'Test Configuration' section
                elif config_section:
                    collections += re.findall(r'\b\w+_set\b', line)
    except FileNotFoundError:
        print(f"File not found: {response_file_path}")
    except IOError as e:
        print(f"Error reading file {response_file_path}: {e}")

    return collections

def check_collections_in_csv(collection_names, csv_file_path):
    """Check if extracted collection names exist in the CSV file."""
    existing_collections = {}
    missing_collections = []

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = list(csv.DictReader(csv_file))  # Convert reader to a list for re-use
            csv_collections = [row.get("Collection Name").strip() for row in reader]  # Strip spaces

            for collection_name in collection_names:
                if collection_name in csv_collections:
                    collection_id = next(row["Collection ID"] for row in reader if row["Collection Name"].strip() == collection_name)
                    existing_collections[collection_name] = collection_id
                else:
                    missing_collections.append(collection_name)

    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except IOError as e:
        print(f"Error reading CSV file {csv_file_path}: {e}")

    return existing_collections, missing_collections

# Example usage
if __name__ == '__main__':
    question_file = r"D:\AI Test System\Source Files\0001prompt.md"
    csv_file_path = r"D:\AI Test System\csv details\collections\collections_details.csv"

    # Extract collection names from the response file
    collection_names = extract_collections_from_response(question_file)
    print("Extracted collection names:", collection_names)

    # Check if the extracted collections exist in the CSV file
    existing_collections, missing_collections = check_collections_in_csv(collection_names, csv_file_path)

    if existing_collections:
        print("Collections found in the CSV with their IDs:", existing_collections)
    else:
        print("None of the extracted collections were found in the CSV file.")
    
    if missing_collections:
        print(f"The following collections were not found in the CSV and need to be created: {missing_collections}")
    else:
        print("All extracted collections are already present in the CSV.")
