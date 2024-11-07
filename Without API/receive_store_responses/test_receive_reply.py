import os
from datetime import datetime
import sys

# Add the 'read_questions' folder to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'read_questions')))

# Import your modules
from read_question import read_questions_from_folder
from simulate_chatdoc import simulate_chatdoc_response

def store_response_in_file(question_num, question, response):
    """Rewrites the response and date in the output file specific to the question."""
    date_response = datetime.now().strftime("%b %d %Y")
    
    file_name = f"{str(question_num).zfill(4)}ra_notebooklm.md"  # Create the file name with zfill
    file_path = os.path.join('D:/AI Test System/Source Files', file_name)
    
    # Prepare the links part as empty
    links_section = "\n## Links\n"  # Keeping the Links section empty
    
    # Rewrite the file, clearing any previous content and storing the new data
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"## NotebookLM Version\n")
        f.write(f"{date_response}\n")  # Write the version and date
        f.write(f"## Response\n")  # Write the response header
        f.write(f"{response}\n")  # Write the response
        f.write(links_section)  # Write the empty links section
        f.write("---\n\n")  # Separator line

# Example usage
folder = 'D:/AI Test System/Source Files'
file_pattern = r'^\d{4}prompt\.md$'
questions = read_questions_from_folder(folder, file_pattern)

# Send each question (simulated) and store the response
for i, question in enumerate(questions, 1):
    print(f"Sending question {i}: {question}")
    response = simulate_chatdoc_response(question)
    
    if response:
        print(f"Simulated response for question {i}: {response}")
        store_response_in_file(i, question, response)   # Pass the question and response to the file
