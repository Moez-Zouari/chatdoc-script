import os
import subprocess
import re
import json
import requests
import csv
from datetime import datetime

# API configuration
api_url = "https://api.chatdoc.com/api/v2/questions/multi-documents"
api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"

def commit_and_push_changes(questions_folder, commit_message, remote_url, username, token, branch="main"):
    """
    Commits and pushes all modified files to a specified Git repository.
    Configures the remote URL if not already set.
    """
    try:
        os.chdir(questions_folder)

        # Check if a remote is already configured
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        remotes = result.stdout.strip()
        if remote_url not in remotes:
            print(f"Remote not configured. Adding remote URL: {remote_url}")
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        else:
            print(f"Remote URL already configured: {remote_url}")

        # Check for modified files
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        modified_files = result.stdout.strip()

        if not modified_files:
            print("No changes detected. Nothing to commit.")
            return

        # Add all changes
        subprocess.run(['git', 'add', '--all'], check=True)
        
        # Include the current date in the commit message
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_commit_message = f"{commit_message} - {current_date}"

        # Commit the changes
        subprocess.run(['git', 'commit', '-m', full_commit_message], check=True)

        # Format the push command with token authentication
        push_command = f'https://{username}:{token}@{remote_url[8:]}'

        # Push to the remote repository
        subprocess.run(['git', 'push', '-u', push_command, branch], check=True)

        print(f"Changes committed and pushed successfully to branch '{branch}' with message: '{full_commit_message}'")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def send_request(payload):
    response = requests.post(
        api_url,
        json=payload,
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    )
    return response

def process_response(response):
    raw_data = response.text.split('data: ')
    answers = []
    question_id = None
    pdf_upload_id = None  # Renamed for clarity

    for entry in raw_data:
        if entry.strip():
            try:
                answer_data = json.loads(entry.strip())
                if 'id' in answer_data:
                    question_id = answer_data['id']
                if 'answer' in answer_data:
                    answers.append(answer_data['answer'])
                if 'source_info' in answer_data:
                    source_info = answer_data['source_info']
                    # Retrieve the upload_id from source_info
                    if source_info and 'upload_id' in source_info[0]:
                        pdf_upload_id = source_info[0]['upload_id']
            except json.JSONDecodeError:
                print('JSON decoding error:', entry)

    full_answer = ''.join(answers)
    return full_answer, question_id, pdf_upload_id  # Return pdf_upload_id

def create_question(question_text, document_ids):
    if isinstance(document_ids, list) and document_ids:
        upload_ids = document_ids  # List of document IDs
    else:
        print("Invalid document IDs provided.")
        return

    # Create the payload for the request
    payload = {
        'question': question_text,
        'upload_ids': upload_ids  # Include all document IDs
    }

    response = send_request(payload)

    if response.status_code == 200:
        full_answer, question_id, pdf_source_info_id = process_response(response)
        return full_answer, question_id, pdf_source_info_id
    else:
        try:
            print('Request error:', response.json())
        except ValueError:
            print('Non-JSON request error:', response.text)

def read_questions_in_file(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'## Prompt\s*(.*?)\s*## Prompt provided by', content, re.DOTALL)
    return match.group(1).strip() if match else None

def read_questions_from_folder(folder, file_pattern):
    questions = []
    
    for file_name in os.listdir(folder):
        if re.match(file_pattern, file_name):
            file_path = os.path.join(folder, file_name)
            question = read_questions_in_file(file_path)
            if question:
                questions.append((file_path, question))

    return questions

def check_collections_in_csv(collection_names, document_folder):
    existing_collections = {}
    missing_collections = []
    documents_id = []

    for collection_name in collection_names:
        collection_file_path = os.path.join(document_folder, f"{collection_name}_details.csv")
        
        try:
            with open(collection_file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                collection_docs = [row["Document ID"].strip() for row in reader]
                
                documents_id.extend(collection_docs)
                existing_collections[collection_name] = collection_file_path

        except FileNotFoundError:
            missing_collections.append(collection_name)
        except IOError as e:
            print(f"Error reading CSV file {collection_file_path}: {e}")

    return existing_collections, missing_collections, documents_id

def extract_collections_from_response(question_file_path):
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
                    break
                elif config_section:
                    collections += re.findall(r'\b\w+_set\b', line)
    except FileNotFoundError:
        print(f"File not found: {response_file_path}")
    except IOError as e:
        print(f"Error reading file {response_file_path}: {e}")

    return collections

def find_pdf_name_by_upload_id(upload_id, document_folder):
    for csv_file in os.listdir(document_folder):
        if csv_file.endswith("_details.csv"):
            collection_file_path = os.path.join(document_folder, csv_file)
            try:
                with open(collection_file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Document ID"].strip() == upload_id:
                            return row["Document Name"].strip()  # Returns the PDF file name
            except Exception as e:
                print(f"Error reading file {collection_file_path}: {e}")
    return None  # If file name is not found

def store_response_in_file(question_num, question, response, pdf_name):
    """Rewrites the response and date in the output file specific to the question."""
    date_response = datetime.now().strftime("%b %d %Y")
    
    file_name = f"{str(question_num).zfill(4)}ra_notebooklm.md"  # Create the file name with zfill
    file_path = os.path.join('D:/AI Test System/Source Files', file_name)
    
    # Rewrite the file, clearing any previous content and storing the new data
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"## NotebookLM Version\n")
        f.write(f"{date_response}\n")  # Write the version and date
        f.write(f"## Response\n")  # Write the response header
        f.write(f"{response}\n")  # Write the response
        f.write(f"## Links\n")  # Write the empty links section
        f.write(f"{pdf_name}\n\n")  # Separator line

def display_read_questions(questions):
    print("\n--- Reading Questions ---\n")
    print("Reading questions from files:")
    for question_file, _ in questions:
        print(f"- {question_file}")

def display_details(questions_data):
    print("\n--- Question Details ---\n")
    for question_data in questions_data:
        file_name = os.path.basename(question_data['file'])
        print(f"Question {question_data['number']} : File {file_name}")
        print(f"- Question : {question_data['text']}")
        print(f"- Available collections : {', '.join(question_data['collections'])}")
        print(f"- Answer : {question_data['answer']}")
        print(f"- PDF file name : {question_data['pdf_name']}")
        print("-" * 50 + "\n")
    print("\n--- End of display ---\n")

def main():
    questions_folder = 'D:/AI Test System/Source Files'
    file_pattern = r'^\d{4}prompt\.md$'
    document_folder = "D:/AI Test System/csv details/documents"
    # Parameters
    commit_message = "Update files"        # Commit message
    remote_url = "https://git.intern.lauterbach.com/mzouari/AIPromptManagementSystem.git"  # Remote repository URL
    username = "mzouari"  # Git username
    token = "36b00d788950edf7f2ac01360595c3ed1875b9b0"  # Your Git authentication token
    branch = "main"  # Branch (default "main")
    
    questions = read_questions_from_folder(questions_folder, file_pattern)
    questions_data = []

    # Display read questions
    display_read_questions(questions)
    
    print("\n--- Sending Questions ---\n")
    for question_file_path, question_text in questions:
        question_number = os.path.basename(question_file_path).split('prompt.md')[0]
        
        collection_names = extract_collections_from_response(question_file_path)
        
        existing_collections, missing_collections, documents_id = check_collections_in_csv(collection_names, document_folder)
        
        # Prepare data for detailed display
        question_data = {
            'number': question_number,
            'file': question_file_path,
            'text': question_text,
            'collections': collection_names,
            'answer': "Awaiting response...",  # Placeholder for the answer
            'pdf_upload_id': None,  # Key for PDF upload ID
            'pdf_name': None  # PDF file name
        }

        questions_data.append(question_data)
        
        if documents_id:
            print(f"\nSending question: {question_text}")
            full_answer, question_id, pdf_upload_id = create_question(question_text, documents_id)
            question_data['answer'] = full_answer
            print(f"Question ID: {question_id}\n")
            if full_answer:
                question_data['answer'] = full_answer
                question_data['pdf_upload_id'] = pdf_upload_id
                
                # Find the PDF file name
                pdf_name = find_pdf_name_by_upload_id(pdf_upload_id, document_folder)
                question_data['pdf_name'] = pdf_name

        store_response_in_file(question_number, question_text, full_answer, pdf_name)

    # Display details of processed questions
    display_details(questions_data)
    # Commit the changes in Git
    # Call the function
    commit_and_push_changes(questions_folder, commit_message, remote_url, username, token, branch)

if __name__ == "__main__":
    main()
