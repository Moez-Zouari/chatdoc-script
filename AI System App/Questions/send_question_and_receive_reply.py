import os
import re
import json
import requests
import csv

# API Configuration
api_url = "https://api.chatdoc.com/api/v2/questions/multi-documents"
api_token = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"

def send_request(payload):
    response = requests.post(
        api_url,
        json=payload,
        headers={'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'}
    )
    return response

def process_response(response):
    raw_data = response.text.split('data: ')
    answers = []
    question_id = None

    for entry in raw_data:
        if entry.strip():
            try:
                answer_data = json.loads(entry.strip())
                if 'id' in answer_data:
                    question_id = answer_data['id']
                if 'answer' in answer_data:
                    answers.append(answer_data['answer'])
            except json.JSONDecodeError:
                print('Error decoding JSON:', entry)

    full_answer = ''.join(answers)
    return full_answer, question_id

def create_question(question_text, document_ids):
    if isinstance(document_ids, list) and document_ids:
        upload_ids = document_ids  # List of document IDs
    else:
        print("Invalid document IDs provided.")
        return

    # Create payload for request
    payload = {
        'question': question_text,
        'upload_ids': upload_ids  # Include all document IDs
    }

    response = send_request(payload)

    if response.status_code == 200:
        full_answer, question_id = process_response(response)
        return full_answer, question_id
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

def display_read_questions(questions):
    print("\n--- Reading Questions ---\n")
    print("Reading questions from files:")
    for question_file, _ in questions:
        print(f"- {question_file}")

def display_details(questions_data):
    print("\n--- Question Details ---\n")

    for question_data in questions_data:
        file_name = os.path.basename(question_data['fichier'])
        print(f"Question {question_data['numero']} : File {file_name}")
        print(f"- Question : {question_data['texte']}")
        print(f"- Available Collections : {', '.join(question_data['collections'])}")
        print(f"- Answer : {question_data['reponse']}")
        
        # Separator between questions
        print("-" * 50 + "\n")

        
    print("\n--- End of Display ---\n")

def main():
    questions_folder = 'D:/AI Test System/Source Files'
    file_pattern = r'^\d{4}prompt\.md$'
    document_folder = "D:/AI Test System/csv details/documents"
    
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
            'numero': question_number,
            'fichier': question_file_path,
            'texte': question_text,
            'collections': collection_names,
            'reponse': "Awaiting response..."  # Placeholder for the answer
        }

        questions_data.append(question_data)

        if documents_id:
            print(f"\nSending question: {question_text}")
            full_answer, question_id = create_question(question_text, documents_id)
            question_data['reponse'] = full_answer
            print(f"Question ID: {question_id}\n")
        else:
            print("No associated document for this question.\n")
    
    # Display details after processing all questions
    display_details(questions_data)

if __name__ == '__main__':
    main()
