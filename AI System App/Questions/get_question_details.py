# Exemple d'URL de l'API et ID de question
import requests


api_url = "https://api.chatdoc.com/api/v2/questions/{question_id}"
question_id = 8834653  # Remplacer par votre ID de question
auth_token = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Remplacer par votre token d'authentification

response = requests.get(api_url.format(question_id=question_id), headers={
        "Authorization": f"Bearer {auth_token}"
    })

if response.status_code == 200:
    question_data = response.json()
    print("Réponse de l'API :", question_data)  # Afficher la réponse de l'API pour débogage