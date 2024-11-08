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
    pdf_source_info_id = None

    for entry in raw_data:
        if entry.strip():
            try:
                answer_data = json.loads(entry.strip())
                if 'id' in answer_data:
                    question_id = answer_data['id']
                if 'answer' in answer_data:
                    answers.append(answer_data['answer'])
                if 'source_info' in answer_data:  # Check for source_info in the response
                    source_info = answer_data['source_info']
                    print (source_info)
                    # Get the upload_id from the source_info
                    if source_info and 'upload_id' in source_info[0]:
                        pdf_source_info_id = source_info[0]['upload_id']
                        print(pdf_source_info_id)
            except json.JSONDecodeError:
                print('Error decoding JSON:', entry)

    full_answer = ''.join(answers)
    
    # Adding a line to print the data received
    print(f"Data received: {raw_data}")  # This will print the raw data before processing

    return full_answer, question_id, pdf_source_info_id

def create_question(question_text, document_ids):
    if isinstance(document_ids, list) and document_ids:
        upload_ids = document_ids  # List of document IDs
    else:
        print("Invalid document IDs provided.")
        return

    # Create the payload for the request
    payload = {
        'question': question_text,
        'upload_ids': upload_ids,  # Include all document IDs
    }

    response = send_request(payload)

    if response.status_code == 200:
        full_answer, question_id, pdf_source_info_id = process_response(response)
        print(f'Full answer: {full_answer}')
        print(f'Question ID: {question_id}')
        print(f'Pdf Source Info Id: {pdf_source_info_id}')  # Print the upload_id from source_info
        return question_id
    else:
        print('Request error:', response.json())

if __name__ == '__main__':
    question_text = "Il s'appelle quoi l'ecrivains ?"
    document_ids = ["32af8457-b591-4f63-8467-2d0f422b975a", "d5dc7e7f-2e8c-4a06-ad8c-6ce44830cb2a"]  # List of document IDs
    create_question(question_text, document_ids)
 