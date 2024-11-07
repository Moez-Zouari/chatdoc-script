import csv

def get_all_created_collections(collections_csv_path):
    """Retrieve collections from the CSV file and display them, including duplicates and creation dates."""
    collections = []

    try:
        with open(collections_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            # Read collections into a list of tuples (name, id, creation date)
            for row in reader:
                collections.append((row["Collection Name"], row["Collection ID"], row["Creation Date"]))

    except FileNotFoundError:
        print(f"Error: The file '{collections_csv_path}' was not found.")
        return collections
    except Exception as e:
        print(f"An error occurred: {e}")
        return collections

    # Display the collections in a presentable format
    if collections:
        print("\n=== List of Collections ===")
        for name, collection_id, creation_date in collections:
            print(f"Collection Name: {name} | Collection ID: {collection_id} | Creation Date: {creation_date}")
        print("===========================")
    else:
        print("No collections found.")

    return collections

# Example usage
collections_csv_path = 'D:/AI Test System/csv details/collections/collections_details.csv'
get_all_created_collections(collections_csv_path)
