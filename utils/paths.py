import os

LABEL_STUDIO_ADMIN_TOKEN = "969bb00b2b2bf1876b04fa64a7502ab7af8a6d45"

label_studio_URL = 'http://localhost:7749'


label_studio_headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Token {LABEL_STUDIO_ADMIN_TOKEN}'
}

storage_path = "/mnt/data03/deployment/label/data/text2audio/storage"
if not os.path.exists(storage_path):
    storage_path = "app/storage"

texts_path = os.path.join(storage_path, "texts")
os.makedirs(texts_path, exist_ok=True)

labeled_texts_path = os.path.join(storage_path, "labeled_texts")
os.makedirs(labeled_texts_path, exist_ok=True)

label_studio_project_dir_name = "audios_jsons"
audios_path = os.path.join(storage_path, label_studio_project_dir_name)
jsons_path = os.path.join(storage_path, label_studio_project_dir_name)
os.makedirs(audios_path, exist_ok=True)
os.makedirs(jsons_path, exist_ok=True)