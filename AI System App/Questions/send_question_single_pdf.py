import requests
import json

api_url = "https://api.chatdoc.com/api/v2/questions"
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
    if isinstance(document_ids, list):
        upload_id = ','.join(document_ids)
    else:
        upload_id = document_ids

    payload = {'question': question_text, 'upload_id': upload_id}
    response = send_request(payload)

    if response.status_code == 200:
        full_answer, question_id = process_response(response)
        print(f'Full answer: {full_answer}')
        print(f'Question ID: {question_id}')
        return question_id
    else:
        print('Request error:', response.json())

if __name__ == '__main__':
    question_text = "What is the name of the writer?"
    document_ids = ["32af8457-b591-4f63-8467-2d0f422b975a"]
    create_question(question_text, document_ids)
