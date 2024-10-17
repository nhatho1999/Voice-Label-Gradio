import os

root_dir_path = "/mnt/data03/deployment/label/data/text2audio"
if not os.path.exists(root_dir_path):
    root_dir_path = "app"

label_studio_data_path = os.path.join(root_dir_path, "label_studio_data")
os.makedirs(label_studio_data_path, exist_ok=True)

storage_path = os.path.join(os.getcwd(), "storage")

label_studio_project_dir_name = "audios_jsons"
audios_path = os.path.join(storage_path, label_studio_project_dir_name)

os.environ["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"
os.environ["LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK"] = "true"
os.environ["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = audios_path
os.system("label-studio start --data-dir ./label_studio_data --port 7749")