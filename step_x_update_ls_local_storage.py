

import os, requests

LABEL_STUDIO_ADMIN_TOKEN = "969bb00b2b2bf1876b04fa64a7502ab7af8a6d45"

label_studio_URL = 'http://localhost:7749'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Token {LABEL_STUDIO_ADMIN_TOKEN}',
    # 'X-CSRFToken': 'm53vS36OJbpp5WCVOotPHzrlg3tK1iOtXI6X96vKjTKivQWoG6NmN2FdNJtdJJtw'
}


def create_local_storage_for(username, proj_id):
    data = {
        "title": f"EraX Ghi âm project_id #{proj_id}",
        "description": f"Ghi âm của project_id #{proj_id}",
        "project": proj_id,
        "path": f"/app/storage/audios_jsons/{username}",
        "regex_filter": ".*json",
        "use_blob_urls": False
    }
    session = requests.Session()
    session.get(label_studio_URL)
    
    if 'csrftoken' in session.cookies:
        # Django 1.6 and up
        csrftoken = session.cookies['csrftoken']
    else:
        # older versions
        csrftoken = session.cookies['csrf']
        
    resp = session.post(
        f'{label_studio_URL}/api/storages/localfiles/',
        headers=headers,
        json=data
    )

    return resp

from utils.auth import EraX_auth

username_list = [_[0] for _ in EraX_auth]


resp = create_local_storage_for(username="nhat.ph", proj_id=202)
print(resp)

# from tqdm import tqdm

# for proj_id_s1, username in tqdm(enumerate(username_list)):
#     proj_id = proj_id_s1 + 1
#     resp = create_local_storage_for(username, proj_id)