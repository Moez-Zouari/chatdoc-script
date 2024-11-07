import os
from datetime import datetime
import sys

# Add the 'read_questions' folder to the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'read_questions')))

# Import your modules
from read_question import read_questions_from_folder
from simulate_chatdoc import simulate_chatdoc_response

def store_response_in_file(question_num, question, response):
    """Adds the response to the output file specific to the question."""
    date_response = datetime.now().strftime("%b %d %Y - %H:%M:%S")
    
    file_name = f"{str(question_num).zfill(4)}ra_notebooklm.md"  # Create the file name with zfill
    file_path = os.path.join('D:/AI Test System/Source Files', file_name)
    
    # Count the number of responses already in the file
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Count the number of times "Response" appears to determine the new response number
        response_count = content.count("## Response") + 1
    else:
        response_count = 1
        
    # Create or open the file to add the response
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"## --- Response No. {response_count} ---\n")  # Separator line
        f.write(f"## NotebookLM Version :\n {date_response}\n")  # Write the version and date
        f.write(f"## Question : \n{question}\n")  # Write the question
        f.write(f"## Response {response_count} :  \n{response}\n")  # Write the response
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
