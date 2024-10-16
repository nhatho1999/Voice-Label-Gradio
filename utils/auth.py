import os
import pandas as pd

utils_path = os.path.dirname(__file__)
df = pd.read_excel(os.path.join(utils_path, "200_tai_khoan_ghi_am.xlsx"))

username_lst = df["uname"].tolist()
password_lst = df["password"].tolist()

admin_lst = [
    ("nguyen", "Nguyen@1969"),
    ("nhat.ph", "Nhat@123"),
    ("thuc.pd", "Thuc@234"),
    ("dung.ht", "Dung@345")
]

EraX_auth = [(un, pw) for un, pw in zip(username_lst, password_lst)] + admin_lst

username_2_lsStorageID = dict()
for ls_storage_id_1, tuple_un_pw in enumerate(EraX_auth):
    un, pw = tuple_un_pw
    username_2_lsStorageID[un] = ls_storage_id_1 + 1