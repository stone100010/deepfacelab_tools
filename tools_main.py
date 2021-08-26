# -*- coding: utf-8 -*-
# @Time : 2021/8/25 12:38
# @Author : Odyssey Warsaw
# @File : tools_main.py


# -*- coding: cp936 -*-
import os

def win_path_re(path):
    path_new = path.replace("\\", "/")
    return path_new

def dir_ornot(path):
    if not os.path.exists(path):
        os.mkdir(path)

def file_list(root_path, filetype):
    file_arr = []
    i = 1
    # root_path = 'video_list/'
    for root, dirs, files in os.walk(root_path):
        for file in files:
            file_tyle = file.split(".")[-1]
            if file_tyle == filetype:
                file_path = os.path.join(root, file)
                file_new = str(i).zfill(4)+ "." + file_tyle
                file_path_new = os.path.join(root, file_new)
                file_path_new = win_path_re(file_path_new)
                # print(file_path, file_path_new)
                i+=1
                try:
                    os.rename(file_path, file_path_new)
                except Exception as e:
                    print(file_path, "rename error")
    #         file_arr.append(file_path)
    # return file_arr


if __name__ == "__main__":
    root_path = "video_list"
    # file_list(root_path, filetype="mp4")
