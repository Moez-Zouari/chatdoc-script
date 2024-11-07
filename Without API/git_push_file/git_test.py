import subprocess
import os

def set_remote_url(remote_name, url):
    """Définir l'URL du dépôt distant si elle n'est pas déjà définie."""
    try:
        # Vérifier l'URL actuelle du dépôt distant
        result = subprocess.run(["git", "remote", "get-url", remote_name], capture_output=True, text=True)
        
        # Si l'URL n'est pas définie ou incorrecte, mettre à jour l'URL
        if result.returncode != 0 or result.stdout.strip() != url:
            subprocess.run(["git", "remote", "set-url", remote_name, url], check=True)
            print(f"L'URL du dépôt distant '{remote_name}' a été définie sur {url}.")
        else:
            print(f"L'URL du dépôt distant '{remote_name}' est déjà définie sur {url}.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la configuration de l'URL du dépôt distant : {e}")

def commit_to_git(file_path, commit_message, remote_name='origin', branch='main'):
    """Effectuer un commit et un push dans un dépôt Git spécifique pour le fichier donné."""
    
    # Définir l'URL du dépôt distant automatiquement (si ce n'est pas déjà fait)
    remote_url = "https://github.com/Moez-Zouari/AIPromptManagementSystem.git"
    set_remote_url(remote_name, remote_url)
    
    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return

    try:
        # Ajout du fichier au suivi de git
        subprocess.run(["git", "add", file_path], check=True)
        
        # Effectuer le commit
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Pousser les modifications vers le dépôt distant et la branche spécifiée
        subprocess.run(["git", "push", remote_name, branch], check=True)
        
        print(f"Le fichier {file_path} a été commité et poussé avec succès vers {remote_name}/{branch}.")
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du commit ou du push : {e}")

# Exemple d'utilisation
commit_to_git('D:/AI Test System/Source Files/0001ra_notebooklm.md', 'Ajout de la réponse au fichier notebook', remote_name='origin', branch='main')
