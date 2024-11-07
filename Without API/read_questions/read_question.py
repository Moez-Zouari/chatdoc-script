import os
import re

def read_questions_in_file(md_file):
    """Reads and extracts questions between '## Prompt' and '## Prompt provided by'."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use a regular expression to capture the text between '## Prompt' and '## Prompt provided by'
    match = re.search(r'## Prompt\s*(.*?)\s*## Prompt provided by', content, re.DOTALL)

    if match:
        # Extract and clean the found text
        question = match.group(1).strip()
        return question
    else:
        return None

def read_questions_from_folder(folder, file_pattern):
    """Scans all files in a folder that match the specified pattern and extracts the questions."""
    total_questions = []
    
    # Iterate through the files in the folder
    for file_name in os.listdir(folder):
        # Check if the file matches the pattern (e.g., 0001prompt.md, 0002prompt.md, etc.)
        if re.match(file_pattern, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading questions from: {file_path}")
            question = read_questions_in_file(file_path)
            
            if question:  # If a question is found
                total_questions.append(question)

    return total_questions

# Example usage
folder = 'D:/AI Test System/Source Files'  # Use normal slashes
file_pattern = r'^\d{4}prompt\.md$'  # For example, for files named 0001prompt.md, 0002prompt.md, etc.

questions = read_questions_from_folder(folder, file_pattern)

# Display the questions
for i, question in enumerate(questions, 1):
    print(f"Question {i}: {question}")
