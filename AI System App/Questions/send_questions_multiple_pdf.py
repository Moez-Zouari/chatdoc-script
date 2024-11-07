import requests
import json

# Updated API URL for multiple documents
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

    # Create the payload for the request
    payload = {
        'question': question_text,
        'upload_ids': upload_ids  # Include all document IDs
    }

    response = send_request(payload)

    if response.status_code == 200:
        full_answer, question_id = process_response(response)
        print(f'Full answer: {full_answer}')
        print(f'Question ID: {question_id}')
        return question_id
    else:
        print('Request error:', response.json())

if __name__ == '__main__':
    question_text = "Combien le PIB nominal ?"
    document_ids = ["83e0973b-0778-4a6e-835a-cb22879b2912", "99581b0d-1952-4682-85e6-5d2c9565e17c"]  # List of document IDs
    create_question(question_text, document_ids)
