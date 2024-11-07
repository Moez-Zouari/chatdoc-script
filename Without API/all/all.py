import os
import re
import random
from datetime import datetime

def print_separator(text):
    """
    Prints a separator line with centered text.
    Used to structure and organize the display of different sections.
    """
    # Calculate the total length of the separator
    total_length = 60
    text_length = len(text)
    # Calculate padding on each side
    padding_length = (total_length - text_length - 2) // 2  # -2 for the spaces around the text
    # Construct the separator
    separator = "-" * padding_length + " " + text + " " + "-" * padding_length
    # Adjust if the total length is odd
    if len(separator) < total_length:
        separator += "-"
    print(separator)

def read_questions_in_file(md_file):
    """
    Reads and extracts a question located between the sections '## Prompt' and
    '## Prompt provided by' in a specific Markdown file.
    
    Arguments:
    - md_file: path to the Markdown file containing the question.

    Returns:
    - The question as a string, or None if not found.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'## Prompt\s*(.*?)\s*## Prompt provided by', content, re.DOTALL)
    return match.group(1).strip() if match else None

def read_questions_from_folder(folder, file_pattern):
    """
    Scans all files in a folder that match the specified pattern and extracts questions.
    
    Arguments:
    - folder: the directory containing the files.
    - file_pattern: the pattern to match specific filenames.

    Returns:
    - A list of questions found within matching files.
    """
    total_questions = []
    
    for file_name in os.listdir(folder):
        if re.match(file_pattern, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading questions from: {file_path}")
            question = read_questions_in_file(file_path)
            if question:
                total_questions.append(question)

    return total_questions

def simulate_chatdoc_response(question):
    """
    Simulates a ChatDoc response based on a question.
    
    Arguments:
    - question: the question string to generate a response for.

    Returns:
    - A simulated response string.
    """
    possible_responses = [
        "This is a simulated response for the question ",
        "I cannot answer that at the moment, but here's a suggestion",
        "The answer might be related to the following documentation",
        "I recommend checking the following resources for more information"
    ]
    return random.choice(possible_responses) 

def store_response_in_file(question_num, question, response):
    """
    Stores the simulated response in a file specific to the question number.
    
    Arguments:
    - question_num: unique number of the question file.
    - question: the question text.
    - response: the generated response to be stored.
    """
    date_response = datetime.now().strftime("%b %d %Y - %H:%M:%S")
    
    file_name = f"{str(question_num).zfill(4)}ra_notebooklm.md"
    file_path = os.path.join('D:/AI Test System/Source Files', file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        response_count = content.count("## Response") + 1
    else:
        response_count = 1
        
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"## --- Response No. {response_count} ---\n")
        f.write(f"## NotebookLM Version :\n {date_response}\n")
        f.write(f"## Question : \n{question}\n")
        f.write(f"## Response {response_count} :  \n{response}\n")

def read_last_response_in_notebook(md_file):
    """
    Reads and extracts the last response from a ChatDoc notebook file.
    
    Arguments:
    - md_file: path to the Markdown file.

    Returns:
    - The last response as a string, or None if not found.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = re.findall(r'## --- Response No. \d+ ---\s*## NotebookLM Version :.*?## Question :.*?## Response \d+ :\s*(.*?)\s*(?=## --- Response No. \d+ ---|$)', content, re.DOTALL)
    return matches[-1].strip() if matches else None

def read_responses_in_file(md_file):
    """
    Reads and extracts the correct response starting from the second '## Response' in the file.
    
    Arguments:
    - md_file: path to the Markdown file.

    Returns:
    - The second response as a string, or None if not found.
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = re.findall(r'## Response\s*(.*?)\s*##', content, re.DOTALL)
    return matches[1].strip() if len(matches) > 1 else None

def extract_responses(folder, file_pattern_notebook, file_pattern_response):
    """
    Scans all files in a folder that match the specified patterns, extracting
    the last responses and correct responses.
    
    Arguments:
    - folder: the directory containing the files.
    - file_pattern_notebook: pattern to match notebook files.
    - file_pattern_response: pattern to match response files.

    Returns:
    - Two dictionaries containing last responses and correct responses, indexed by file number.
    """
    last_responses = {}
    correct_responses = {}

    for file_name in os.listdir(folder):
        if re.match(file_pattern_notebook, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading responses from notebook: {file_path}")
            last_response = read_last_response_in_notebook(file_path)
            file_number = file_name[:4]  # Get the first four characters as the file number
            if last_response:
                last_responses[file_number] = last_response

    for file_name in os.listdir(folder):
        if re.match(file_pattern_response, file_name):
            file_path = os.path.join(folder, file_name)
            print(f"Reading responses from response file: {file_path}")
            correct_response = read_responses_in_file(file_path)
            file_number = file_name[:4]
            if correct_response:
                correct_responses[file_number] = correct_response

    return last_responses, correct_responses

# Example usage
folder = 'D:/AI Test System/Source Files'
file_pattern_prompt = r'^\d{4}prompt\.md$'
file_pattern_notebook = r'^\d{4}ra_notebooklm\.md$'
file_pattern_response = r'^\d{4}response\.md$'
print("\n")
print_separator("Read Questions From Prompt File")
questions = read_questions_from_folder(folder, file_pattern_prompt)
print("\n")
print_separator("Sending Question and Receive Response")
for i, question in enumerate(questions, 1):
    print(f"Sending question {i}: {question}")
    response = simulate_chatdoc_response(question)
    if response:
        print(f"Simulated response for question {i}: {response}")
        store_response_in_file(i, question, response)
print("\n")
print_separator("Extract Last ChatDoc Response and Correct Response")
last_responses, correct_responses = extract_responses(folder, file_pattern_notebook, file_pattern_response)
print("\n")
print_separator("")
print_separator("Display Last ChatDoc Response and Correct Response")
print_separator("")
for file_number in sorted(last_responses.keys()):
    last_response = last_responses.get(file_number, "No response found")
    correct_response = correct_responses.get(file_number, "No correct response found")
    
    print("\n") 
    print_separator(f"Question {file_number}:")
    print("\n") 
    print_separator("Last ChatDoc Response")
    print(last_response)
    print("\n") 
    print_separator("Correct Response")
    print(correct_response)
