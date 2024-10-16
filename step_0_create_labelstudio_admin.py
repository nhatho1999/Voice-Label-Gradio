# CHỈ CHẠY 1 LẦN DUY NHẤT, TẠO 1 TÀI KHOẢN BẤT KỲ XONG LƯU LẠI TOKEN.
# LƯU Ý: PHẢI CHẠY XONG step_1 RỒI MỚI TẮT CẢ 2 KERNEL NHÉ

# import os

# root_dir_path = os.getcwd()
# label_studio_data_path = os.path.join(root_dir_path, "label_studio_data")
# os.makedirs(label_studio_data_path, exist_ok=True)

# storage_path = os.path.join(os.getcwd(), "storage")

# label_studio_project_dir_name = "audios_jsons"
# audios_path = os.path.join(storage_path, label_studio_project_dir_name)

# os.environ["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"
# # os.environ["LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK"] = "true"
# os.environ["LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT"] = audios_path
# os.system("label-studio start --data-dir ./label_studio_data --port 7749")

LABEL_STUDIO_ADMIN_TOKEN = "969bb00b2b2bf1876b04fa64a7502ab7af8a6d45"