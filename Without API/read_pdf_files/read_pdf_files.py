# import os

# def list_pdf_files(folder):
#     """Lists all PDF files in the specified folder."""
#     pdf_files = [file for file in os.listdir(folder) if file.endswith('.pdf')]
#     return pdf_files

# # Spécifiez le chemin d'accès au dossier
# pdf_folder = 'D:/AI Test System/PDF Files'
# pdf_files = list_pdf_files(pdf_folder)

# print("Fichiers PDF trouvés dans le dossier :")
# for pdf_file in pdf_files:
#     print(pdf_file)
    
# import requests

# # URL de l'API pour récupérer le quota
# api_url = "https://api.chatdoc.com/api/v2/users/quota"
# headers = {
#     "Authorization": "Bearer ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc",  # Remplacez par votre clé API
#     "Content-Type": "application/json"
# }

# # Envoyer la requête GET pour obtenir le quota
# response = requests.get(api_url, headers=headers)

# # Vérification de la réponse
# if response.status_code == 200:
#     quota_info = response.json()
#     print("Informations de Quota :")
#     print(quota_info)
# else:
#     print("Erreur :", response.status_code, response.text)
    

## Création d'une nouvelle collection

# import requests

# # URL de l'API pour créer une nouvelle collection
# api_url = "https://api.chatdoc.com/api/v2/collections"

# # Remplacer par votre clé d'API réelle
# headers = {
#     "Authorization": "Bearer ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc",
#     "Content-Type": "application/json"
# }

# # Détails de la collection à créer
# data = {
#     "name": "Nouvelle Collection PDF"  # Remplacez par le nom de votre choix
# }

# # Effectuer la requête POST pour créer la collection
# response = requests.post(api_url, headers=headers, json=data)

# # Vérifier la réponse de l'API
# if response.status_code == 200:
#     collection = response.json()
#     print("Nouvelle collection créée avec succès :")
#     print(f"Nom : {collection['data']['name']}, ID : {collection['data']['id']}")
# else:
#     print("Erreur :", response.status_code, response.text)
#     print("Erreur :", response.status_code, response.text)






    
## Ajout des document dans une collection
    
# import requests

# # Remplacer par votre clé d'API et l'ID de la collection
# api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Clé d'API réelle
# collection_id = "e2bb82fe-16c7-4c4c-bead-361e395263ac"  # ID de la collection
# pdf_file_path = "D:/AI Test System/PDF Files/pays.pdf"  # Chemin vers votre fichier PDF

# # URL de l'API pour uploader un document
# upload_url = f"https://api.chatdoc.com/api/v2/documents/upload"

# headers = {
#     "Authorization": f"Bearer {api_key}"
# }

# # Ouvrir le fichier PDF et effectuer la requête POST
# with open(pdf_file_path, 'rb') as file:
#     files = {
#         "file": (pdf_file_path, file, "application/pdf")
#     }
#     data = {
#         "collection_id": collection_id  # ID de la collection cible
#     }
#     response = requests.post(upload_url, headers=headers, files=files, data=data)

# # Vérifier la réponse de l'API
# if response.status_code == 200:
#     document = response.json()
#     print("Document uploadé avec succès dans la collection.")
#     print(f"Nom du document : {document['data']['name']}, ID du document : {document['data']['id']}")
# else:
#     print("Erreur lors de l'upload :", response.status_code, response.text)



import requests

# Remplacer par l'ID de la collection que vous souhaitez supprimer
collection_id = "e2bb82fe-16c7-4c4c-bead-361e395263ac"
# URL de l'API pour supprimer la collection
api_url = f"https://api.chatdoc.com/api/v2/collections/{collection_id}"
api_key = "ak-VStt1ft_v9Rfun_D2zXcmYpeZ8V76Mm1Ck1JOMxSGjc"  # Clé d'API réelle

# En-têtes de la requête, avec votre clé API
headers = {
    "Authorization": f"Bearer {api_key}",  # Remplacez par votre clé API
    "Content-Type": "application/json"
}

# Effectuer la requête DELETE
response = requests.delete(api_url, headers=headers)

# Vérifier la réponse de l'API
if response.status_code == 200:
    print("Collection supprimée avec succès.")
else:
    print("Erreur lors de la suppression :", response.status_code, response.text)
