# Example of API URL and question ID
import requests

api_url = "https://api.chatdoc.com/api/v2/questions/{question_id}"
question_id = 8834653  # Replace with your question ID
auth_token = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Replace with your authentication token

response = requests.get(api_url.format(question_id=question_id), headers={
        "Authorization": f"Bearer {auth_token}"
    })

if response.status_code == 200:
    question_data = response.json()
    print("API Response:", question_data)  # Display API response for debugging
