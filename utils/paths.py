import os

storage_path = os.path.join(os.getcwd(), "storage")

texts_path = os.path.join(storage_path, "texts")
os.makedirs(texts_path, exist_ok=True)

labeled_texts_path = os.path.join(storage_path, "labeled_texts")
os.makedirs(labeled_texts_path, exist_ok=True)

label_studio_project_dir_name = "audios_jsons"
audios_path = os.path.join(storage_path, label_studio_project_dir_name)
jsons_path = os.path.join(storage_path, label_studio_project_dir_name)
os.makedirs(audios_path, exist_ok=True)
os.makedirs(jsons_path, exist_ok=True)

temp_path = os.path.join(storage_path, "temp")
os.makedirs(temp_path, exist_ok=True)