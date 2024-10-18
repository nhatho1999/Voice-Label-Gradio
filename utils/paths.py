import os

app_server_root_dir_path = "/mnt/data03/deployment/label/data/text2audio"
if not os.path.exists(app_server_root_dir_path):
    app_server_root_dir_path = "app"

storage_path = os.path.join(app_server_root_dir_path, "storage")

texts_path = os.path.join(storage_path, "texts")
os.makedirs(texts_path, exist_ok=True)

labeled_texts_path = os.path.join(storage_path, "labeled_texts")
os.makedirs(labeled_texts_path, exist_ok=True)

label_studio_project_dir_name = "audios_jsons"
audios_path = os.path.join(storage_path, label_studio_project_dir_name)
jsons_path = os.path.join(storage_path, label_studio_project_dir_name)
os.makedirs(audios_path, exist_ok=True)