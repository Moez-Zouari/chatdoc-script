import os
import re

def read_last_response_in_notebook(md_file):
    """Reads and extracts the last response from a ChatDoc notebook file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use a regular expression to capture all responses
    matches = re.findall(r'## --- Response No. \d+ ---\s*## NotebookLM Version :.*?## Question :.*?## Response \d+ :\s*(.*?)\s*(?=## --- Response No. \d+ ---|$)', content, re.DOTALL)

    if matches:  # If there are any matches
        return matches[-1].strip()  # Return the last response
    else:
        return None

def extract_responses(folder, file_pattern):
    """Scans all files in a folder that match the specified pattern and extracts the last responses."""
    responses = {}

    # Iterate through the files in the folder
    for file_name in os.listdir(folder):
        # Check if the file matches the pattern for ra_notebooklm files
        if re.match(file_pattern, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading responses from: {file_path}")
            last_response = read_last_response_in_notebook(file_path)

            # Extract the file number from the file name (assuming format is 0001ra_notebooklm.md)
            file_number = file_name[:4]  # Get the first four characters as the file number

            if last_response:  # If a last response is found
                responses[file_number] = last_response  # Store the response with the file number as key

    return responses

# Example usage
folder = 'D:/AI Test System/Source Files'  # Use normal slashes
file_pattern = r'^\d{4}ra_notebooklm\.md$'  # For example, for files named 0001ra_notebooklm.md, 0002ra_notebooklm.md, etc.

last_responses = extract_responses(folder, file_pattern)

# Display the last responses with the file number
for file_number, response in last_responses.items():
    print(f"Last ChatDoc Response For Question {file_number} : \n{response}")
