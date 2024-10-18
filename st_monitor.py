import os
import random
import json
import streamlit as st

from utils.paths import audios_path

# Đặt cấu hình trang
st.set_page_config(layout="centered")

# Tạo tiêu đề cho ứng dụng ở cột đầu tiên
with st.container():
    st.title("EraX - GHI ÂM GIỌNG NÓI VIỆT")

# Biến để lưu trữ kết quả
random_files_output = ""
selected_files_output = ""
file_count = 0  # Biến đếm số lượng file trong selectbox2

# Kiểm tra nếu đường dẫn không rỗng và tồn tại
if audios_path and os.path.exists(audios_path):
    # Lấy danh sách các thư mục con
    folder_names = [f for f in os.listdir(audios_path) if os.path.isdir(os.path.join(audios_path, f))]
    default_ix = 0
    if "nhat.ph" in set(folder_names):
        default_ix = folder_names.index("nhat.ph")

    # Tạo 4 cột cho 4 thành phần với kích thước bằng nhau
    # col1, col2, col3, col4 = st.layout(4)

    # Selectbox đầu tiên (Chọn thư mục)
    with st.container():
        selected_folder = st.selectbox("Chọn người dùng", folder_names, index=default_ix)

    # Nếu đã chọn thư mục, hiển thị selectbox thứ hai với danh sách file
    if selected_folder:

        selected_folder_path = os.path.join(audios_path, selected_folder)
        wav_file_names = [file for file in os.listdir(selected_folder_path) if file.lower().endswith((".wav"))]
        len_wav_file_names = len(wav_file_names)

        with st.container():
            st.title(f"Số lượng GHI ÂM đã thực hiện: {len_wav_file_names}")

        idx_wav_file_name = 0

        if len(wav_file_names):
            with st.container():
                if st.button("Lấy mẫu ngẫu nhiên", key="random_button"):
                    idx_wav_file_name = random.randint(0, len(wav_file_names)-1)


            # Selectbox thứ hai (Chọn file)
            with st.container():
                selected_file_name = st.selectbox("Chọn GHI ÂM:", wav_file_names, index=idx_wav_file_name)
            
            if selected_file_name:
                if st.button("Nghe GHI ÂM và xem NỘI DUNG", key="select_button"):
                    
                    file_name_without_ext = selected_file_name[:-4] # - ".wav"
                    json_file_name = f"{file_name_without_ext}.json"
                    wav_file_path = os.path.join(selected_folder_path, selected_file_name)
                    json_file_path = os.path.join(selected_folder_path, json_file_name)
                    with open(json_file_path, "r", encoding='utf-8') as fi:
                        json_data = json.load(fi)
                    
                    result_output = json_data["predictions"][0]["result"][0]["value"]["text"][0]

                    st.subheader("Kết quả:")
                    st.audio(data=wav_file_path, format="audio/wav")
                    # st.text_area(label="Đây là nội dung tương ứng", value=result_output, 
                    st.markdown(f':green[{result_output}]')

        else:
            st.warning(f"{selected_folder} chưa có ghi âm nào.")