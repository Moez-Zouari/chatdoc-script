import os
import re

def read_responses_in_file(md_file):
    """Reads and extracts responses starting from the second '## Response' in the file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use a regular expression to capture the text between the second '## Response' and the next '##'
    matches = re.findall(r'## Response\s*(.*?)\s*##', content, re.DOTALL)

    if len(matches) > 1:  # Check if there are at least two responses
        return matches[1].strip()  # Return the second response
    else:
        return None

def read_responses_from_folder(folder, file_pattern):
    """Scans all files in a folder that match the specified pattern and extracts the second responses."""
    total_responses = []

    # Iterate through the files in the folder
    for file_name in os.listdir(folder):
        # Check if the file matches the pattern (e.g., 0001response.md, 0002response.md, etc.)
        if re.match(file_pattern, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading responses from: {file_path}")
            response = read_responses_in_file(file_path)
            if response:  # If a second response is found
                total_responses.append(response)
             
    return total_responses
print(f"\n{'-'*40}")  # Separator line after each response
# Example usage
folder = 'D:/AI Test System/Source Files'  # Use normal slashes
file_pattern = r'^\d{4}response\.md$'  # For example, for files named 0001response.md, 0002response.md, etc.

responses = read_responses_from_folder(folder, file_pattern)
print(f"{'-'*40}\n")  # Separator line after each response

# Display the second responses with separation
for i, response in enumerate(responses, 1):
    print(f"Response {i}:\n\n {response}\n{'-'*40}\n")  # Separator line after each response
