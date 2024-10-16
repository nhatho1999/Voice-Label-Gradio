

import os, requests

LABEL_STUDIO_ADMIN_TOKEN = "969bb00b2b2bf1876b04fa64a7502ab7af8a6d45"

label_studio_URL = 'http://localhost:7749'

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Token {LABEL_STUDIO_ADMIN_TOKEN}',
    # 'X-CSRFToken': 'm53vS36OJbpp5WCVOotPHzrlg3tK1iOtXI6X96vKjTKivQWoG6NmN2FdNJtdJJtw'
}

label_interface = """<View>
  <Audio name="audio" value="$audio" zoom="true" hotkey="ctrl+enter" />
  <Header value="Provide Transcription" />
  <TextArea name="transcription" toName="audio"
            rows="4" editable="true" maxSubmissions="1" />
</View>"""


def create_project(username):

    # Tạo project với Interface
    data = {
        "title": f"Ghi âm của #{username}",
        "description": f"Ghi âm giọng nói Việt #{username}",
        "label_config": label_interface,
        "expert_instruction": "Ghi âm",
        "show_instruction": True,
        "show_skip_button": True,
        "enable_empty_annotation": True,
        "show_annotation_history": True,
        "reveal_preannotations_interactively": True,
        "show_collab_predictions": True,
        "maximum_annotations": 5,
        "color": "#FFFFFF",
        # "control_weights": {
        #     "my_bbox": {
        #       "type": "RectangleLabels",
        #       "labels": {
        #         "Car": 1,
        #         "Airplaine": 0.5
        #       },
        #       "overall": 0.33
        #     }
        # }
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
        f'{label_studio_URL}/api/projects/',
        headers=headers,
        json=data
    )

    return resp

from utils.auth import EraX_auth

username_list = [_[0] for _ in EraX_auth]

from tqdm import tqdm

for username in tqdm(username_list):
    resp = create_project(username)