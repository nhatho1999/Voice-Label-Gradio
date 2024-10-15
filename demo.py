import gradio as gr

from utils.auth import EraX_auth

def create_greeting(request: gr.Request):
    return gr.Markdown(value=f"Thanks for connecting from: {request.client}")

with gr.Blocks() as demo:
    user_ip = gr.Markdown(value="Not logged in")

    demo.load(create_greeting, inputs=None, outputs=user_ip)

demo.launch(auth=EraX_auth, share=False, server_port=9910)