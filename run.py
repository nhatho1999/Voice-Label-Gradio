import os

os.system(f"python app.py & streamlit run st_monitor.py --client.showSidebarNavigation=False --server.fileWatcherType none --browser.gatherUsageStats=False --server.port 7749")