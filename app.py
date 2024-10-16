import os, json, glob

import gradio as gr
from gradio import *

from utils.auth import EraX_auth
from utils.paths import *

global state
state = {
    "text": "",
    "text_file_path": "",
    "message": "",
    "success": False,
    "saved_wav_file_path": None,
}


from moviepy.editor import concatenate_audioclips, AudioFileClip
import shutil

import numpy as np
import random

# Rule
audio_min_length =  1
audio_max_length =  30
audio_sample_rate =  16000
min_sec_word = 1/4

def get_Label_Studio__(username):
    print(f"{username} getting unlabeled TEXT ...")
    text, text_file_path = "", "" # biến cục bộ
    if username:
        user_texts_path = os.path.join(texts_path, username)
        unlabeled_text_files = glob.glob(f"{user_texts_path}/**/*.txt", recursive=True)
        if len(unlabeled_text_files):
            text_file_path = random.choice(unlabeled_text_files)
            with open(text_file_path, "r", encoding='utf-8') as fi:
                text = fi.read()
        else:
            text_file_path = None
            text = "Bạn đã hoàn thành, Không cần ghi âm thêm"
    # return text_file_path, text
    return text


with gr.Blocks() as Recorder:


    def authenticator(login_username, login_password):
        if (login_username, login_password) in set(EraX_auth):
            print(f"{login_username} đăng nhập thành công!")
            return True # --> connect user to Label Studio, keep user name as stateful
        else:
            return False
    

    def update_user_request(request: gr.Request, title):
        text = get_Label_Studio__(request.username)
        return gr.update(value=text), gr.update(value="Người dùng: " +  request.username)


    def start_recoding():
        global state
        state["saved_wav_file_path"] = None
        state["success"] = False
        return gr.update(interactive=False), gr.update(interactive=False), gr.update(label="Đang ghi âm...")
        

    def to_validate(filepath, msg):
        global state
        # Validation...        
        audio = AudioFileClip(filepath)
        audio = audio.set_fps(audio_sample_rate)
        audio_duration = audio.duration

        state["text"] = msg

        print ("Recoding stop, validating: ", audio.duration, audio.fps)
        
        if audio_min_length <= audio_duration <= audio_max_length and audio_duration >= min_sec_word*(state["text"].count(" ") + 1):
            print ("Can submit now !")
            state["success"] = True
            state["saved_wav_file_path"] = filepath
            state["message"] = "Ghi âm hợp lệ. Nghe kỹ lại và bấm Gửi-AAA hoăc Ghi âm lại."
            return gr.update(interactive=True), gr.update(interactive=True), gr.update(), gr.update(label=state["message"])
            
        else:
            state["success"] = False
            state["saved_wav_file_path"] = None

            if audio_duration < min_sec_word*(state["text"].count(" ") + 1):
                print ("Ghi âm QUÁ NGẮN !")
                state["message"] = "Ghi âm QUÁ NGẮN. Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."
            elif audio_duration > audio_max_length:
                print ("Ghi âm QUÁ DÀI !")
                state["message"] = "Ghi âm QÚA DÀI. Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."
            else:
                state["message"] = "Ghi âm KHÔNG HỢP LỆ. Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."
            return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(label=state["message"])
            

    def to_submit(user_markdown):
        global state
        username = user_markdown.split("Người dùng: ")[-1].strip()
        print ("Current username: ", username)
        
        if state["success"] and state["saved_wav_file_path"] is not None:
            print ("Saving success", state["saved_wav_file_path"])
            
            shutil.copy(state["saved_wav_file_path"], state["saved_wav_file_path"].split("/")[-1])
            state["success"] = False
            state["saved_wav_file_path"] = None

            text = get_Label_Studio__(username)

            msg_title = f"Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ - {gr.Request}"            
            # get another random text
            return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(value=text, label=msg_title)
            
        else:
            msg_title = f"Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ - {gr.Request}"            
            return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(value=text, label=msg_title)



    def redo():
        print ("Reset audio and record again...")
        global state
        state["success"] = False
        state["saved_wav_file_path"] = None
        state["message"] = "Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."            
        return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(label=state["message"])


    gr.Markdown("EraX & AAA - Dán nhãn âm thanh Việt")
    
    msg_title = "Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."    
    msg = gr.Textbox(value="Login xong sẽ có!", lines=5, label=msg_title, autoscroll=True, interactive=False, )
    user_markdown = gr.Markdown(value="Người dùng: Unknown")

    Recorder.load(update_user_request, outputs=[msg, user_markdown])

    wave_form =  gr.WaveformOptions(
        show_recording_waveform=True,
        waveform_color="green",
        waveform_progress_color="red",
        show_controls=True,
        sample_rate=audio_sample_rate,
    )
    
    audio_box = gr.Audio(label="Khu vực ghi âm",
                        streaming=False,
                        show_label=True,
                        sources="microphone", type="filepath",
                        show_download_button=True, 
                        interactive=True,
                        editable=True,
                        format="wav",
                        waveform_options=wave_form,
                        min_length=audio_min_length,
                        max_length=audio_max_length)

    with gr.Row():
        clear  = gr.Button('Ghi âm lại', interactive=False)
        submit = gr.Button("Gửi AAA", interactive=False)

    audio_box.start_recording(start_recoding, outputs=[clear, submit, msg])
    audio_box.stop_recording(to_validate, inputs=[audio_box, msg], outputs=[clear, submit, audio_box, msg])
        
    clear.click(redo, outputs=[clear, submit, audio_box, msg])
    submit.click(to_submit, inputs=user_markdown, outputs=[clear, submit, audio_box, msg], concurrency_limit=100, concurrency_id="submit_queue")


Recorder.queue(max_size=180)

Recorder.launch(auth=authenticator, ssl_verify=False, ssl_keyfile="key.pem", ssl_certfile="./cert.pem", 
               server_name="118.69.81.93", server_port=7794, share=False,
               inline=True,
               inbrowser=True, 
               show_error=True, debug=True, enable_monitoring=True)