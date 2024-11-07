import os
import re

def read_last_response_in_notebook(md_file):
    """Reads and extracts the last response from a ChatDoc notebook file."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Capture all responses
    matches = re.findall(r'## --- Response No. \d+ ---\s*## NotebookLM Version :.*?## Question :.*?## Response \d+ :\s*(.*?)\s*(?=## --- Response No. \d+ ---|$)', content, re.DOTALL)

    if matches:  # If there are any matches
        return matches[-1].strip()  # Return the last response
    else:
        return None

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

def extract_responses(folder, file_pattern_notebook, file_pattern_response):
    """Scans all files in a folder that match the specified patterns and extracts last responses and correct responses."""
    last_responses = {}
    correct_responses = {}

    # Iterate through the notebook files
    for file_name in os.listdir(folder):
        # Check if the file matches the pattern for ra_notebooklm files
        if re.match(file_pattern_notebook, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading responses from notebook: {file_path}")
            last_response = read_last_response_in_notebook(file_path)

            # Extract the file number from the file name
            file_number = file_name[:4]  # Get the first four characters as the file number
            if last_response:
                last_responses[file_number] = last_response  # Store the response

    # Iterate through the response files
    for file_name in os.listdir(folder):
        # Check if the file matches the pattern for response files
        if re.match(file_pattern_response, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading responses from response file: {file_path}")
            correct_response = read_responses_in_file(file_path)

            # Extract the file number from the file name
            file_number = file_name[:4]  # Get the first four characters as the file number
            if correct_response:
                correct_responses[file_number] = correct_response  # Store the response

    return last_responses, correct_responses

# Example usage
folder = 'D:/AI Test System/Source Files'  # Use normal slashes
file_pattern_notebook = r'^\d{4}ra_notebooklm\.md$'  # For notebook files
file_pattern_response = r'^\d{4}response\.md$'  # For response files

last_responses, correct_responses = extract_responses(folder, file_pattern_notebook, file_pattern_response)

# Display the last responses and the correct responses
print("\n--- Responses Summary ---")
for file_number in sorted(last_responses.keys()):
    last_response = last_responses.get(file_number, "No response found")
    correct_response = correct_responses.get(file_number, "No correct response found")
    
    print(f"Question {file_number}:")
    print(f"  Last ChatDoc Response:\n{last_response}\n")
    print(f"  Correct Response:\n{correct_response}\n")
    print("-" * 40)  # Separator line after each question
