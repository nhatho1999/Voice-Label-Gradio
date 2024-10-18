import os
from utils.prod_config import SERVER_GRADIO_PORT, SERVER_STREAMLIT_PORT

os.system(f"fuser -k {SERVER_GRADIO_PORT}/tcp")
os.system(f"fuser -k {SERVER_STREAMLIT_PORT}/tcp")
os.system(f"python app.py & streamlit run st_monitor.py --client.showSidebarNavigation=False --server.fileWatcherType none --browser.gatherUsageStats=False --server.port {SERVER_STREAMLIT_PORT}")