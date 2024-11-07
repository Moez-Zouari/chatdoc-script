import requests

def get_quota():
    # API URL to retrieve the quota
    api_url = "https://api.chatdoc.com/api/v2/users/quota"
    headers = {
        "Authorization": "Bearer ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc",  # Remplacez par votre clé API
        "Content-Type": "application/json"
    }

    # Send the GET request to obtain the quota
    response = requests.get(api_url, headers=headers)

    # Check the response
    if response.status_code == 200:
        quota_info = response.json()
        
        # Extract relevant information
        package_info = quota_info.get('data', {}).get('package', {})
        question_info = package_info.get('question', {})
        elite_page_info = package_info.get('elite_page', {})
        
        # Formatted display
        print("Quota Information:")
        print(f"- Max Questions: {question_info.get('max_count', 0)}")
        print(f"- Questions Used: {question_info.get('used_count', 0)}")
        print(f"- Max Elite Pages: {elite_page_info.get('max_count', 0)}")
        print(f"- Elite Pages Used: {elite_page_info.get('used_count', 0)}")
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    get_quota()