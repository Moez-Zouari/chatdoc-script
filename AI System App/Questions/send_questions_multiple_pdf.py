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
    question_text = "Quel pourcentage de la surface totale de la planète est recouvert d'eau ?"
    document_ids = ["32af8457-b591-4f63-8467-2d0f422b975a", "d5dc7e7f-2e8c-4a06-ad8c-6ce44830cb2a"]  # List of document IDs
    create_question(question_text, document_ids)
