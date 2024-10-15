import os, json

import gradio as gr
from gradio import *

from utils.auth import EraX_auth

global success, filepath_saved, text_to_reads, title_, text
success = False
filepath_saved = None

from moviepy.editor import concatenate_audioclips, AudioFileClip
import shutil

import numpy as np

# Rule
min_len =  1
max_len =  30
fps =  16000
min_sec_word = 1/4

with gr.Blocks() as Recoder:

    def authenticator(username, password):
        global success, filepath_saved, text_to_reads, title_, text
        # ---------------------------------------
        # TO DO: authenticated user
        if (username, password) in set(EraX_auth):
            print(f"{username} logged in Ok!")
            return True # --> connect user to Label Studio, keep user name as statèul
        else:
            return False
    
    def update_user_request(request: gr.Request, title):
        return title +  " *** " +  request.username
    
    # ---------------------------------------
    # TO DO: Get this text from Label Studio for each users that can be obtained as gr.Request.username
    text_to_reads = [
            "Check rule & pop-up yêu cầu ghi âm lại sau khi check nếu sai",
            "Con chiên ngoan đạo là người sẽ lên thiên đàng... Phải không? Nếu không nhất thiết như vậy thì khổ sở quá",
            "Chỉ khi đúng mới mở nút Submit",     
           ]
    
    text = text_to_reads[np.random.randint(0, len(text_to_reads)-1)]
    # ---------------------------------------
    
    title = gr.Markdown("EraX & AAA - Dán nhãn âm thanh Việt")
    
    Recoder.load(update_user_request, inputs=title, outputs=title)
    
    def start_recoding():
        global success, filepath_saved, text_to_reads, title_, text
        filepath = None
        success = False
        return gr.update(interactive=False), gr.update(interactive=False), gr.update(label="Đang ghi âm...")
        

    def to_validate(filepath):
        global success, filepath_saved, text_to_reads, title_, text
        # Validation...        
        audio = AudioFileClip(filepath)
        audio = audio.set_fps(16000)
        audio_length = audio.duration

        print ("Recoding stop, validating: ", audio.duration, audio.fps)
        
        if audio_length <= max_len and audio_length >= min_sec_word*len(text.split(" ")):
            print ("Can submit now !")
            success = True
            filepath_saved =  filepath

            title_ = "Ghi âm hợp lệ. Nghe kỹ lại và bấm Gửi-AAA hoăc Ghi âm lại."
            return gr.update(interactive=True), gr.update(interactive=True), gr.update(), gr.update(label=title_)
            
        else:
            success = False
            filepath_saved =  None

            if audio_length < min_sec_word*len(text.split(" ")):
                print ("Ghi âm QUÁ NGẮN !")
                title_ = "Ghi âm QUÁ NGẮN. Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."
            elif audio_length > max_len:
                print ("Ghi âm QUÁ DÀI !")
                title_ = "Ghi âm QÚA DÀI. Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."
            else:
                title_ = "Ghi âm KHÔNG HỢP LỆ. Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."
            return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(label=title_)
            

    def to_submit(title):
        global success, filepath_saved, text_to_reads, title_, text
        # submit...
        # Process audio to Label Studio

        print ("Current username: ", title.split("***")[-1].strip())
        
        if success and filepath_saved is not None:
            print ("Saving success", filepath_saved)

            # ---------------------------------------
            # TO DO: save to Label Studio
            # ---------------------------------------
            shutil.copy(filepath_saved, filepath_saved.split("/")[-1])
            success = False
            filepath_saved = None

            # ---------------------------------------
            # TO DO: Get next text from Label Studio
            text = text_to_reads[np.random.randint(0, len(text_to_reads))]
            # ---------------------------------------

            title_ = f"Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ - {gr.Request}"            
            # get another random text
            return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(value=text, label=title_)
            
        else:
            title_ = f"Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ - {gr.Request}"            
            return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(value=text, label=title_)


    def redo():
        print ("Reset audio and record again...")
        global success, filepath_saved, text_to_reads, title_, text
        filepath_saved = None
        success = False
        title_ = "Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."            
        return gr.update(interactive=False), gr.update(interactive=False), gr.update(value=None), gr.update(label=title_)



        

    title_ = "Xem kỹ đoạn văn và bấm Record để đọc hết toàn bộ."
    
    msg = gr.Textbox(value=text, lines=5, label=title_, autoscroll=True, interactive=False, )
    
    wave_form =  gr.WaveformOptions(
        show_recording_waveform=True,
        waveform_color="green",
        waveform_progress_color="red",
        show_controls=True,
        sample_rate=16000,
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
                         min_length=1,
                         max_length=30)

    with gr.Row():
        clear  = gr.Button('Ghi âm lại', interactive=False)
        submit = gr.Button("Gửi AAA", interactive=False)

    audio_box.start_recording(start_recoding, outputs=[clear, submit, msg])
    audio_box.stop_recording(to_validate, inputs=audio_box, outputs=[clear, submit, audio_box, msg])
        
    clear.click(redo, outputs=[clear, submit, audio_box, msg])
    submit.click(to_submit, inputs=title, outputs=[clear, submit, audio_box, msg], concurrency_limit=100, concurrency_id="submit_queue")


Recoder.queue(max_size=180)

Recoder.launch(auth=authenticator, ssl_verify=False, ssl_keyfile="key.pem", ssl_certfile="./cert.pem", 
               server_name="118.69.81.93", server_port=7794, share=False,
               inline=True,
               inbrowser=True, 
               show_error=True, debug=True, enable_monitoring=True) 