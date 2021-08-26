# -*- coding: utf-8 -*-
# @Time : 2021/8/25 13:07
# @Author : Odyssey Warsaw
# @File : mov2img.py


import cv2, os, time
from tools_main import *
from multiprocessing import Process
from multiprocessing import Pool

def sys_argv_var():
	parser = argparse.ArgumentParser(description="you should add those parameter")
	parser.add_argument("--filepath", default=None, help="--filepath videos/")
	parser.add_argument("--imgcutnum", default=3, help="--imgcutnum 3")
	parser.add_argument("--filetype", default="mp4", help="--filetype mp4")
	args = parser.parse_args()
	return args

def GetNameByEveryDir(file_dir, videoProperty):
    """[summary]

    Args:
        file_dir ([type]): [文件路径]
        videoProperty ([type]): [文件类型]

    Returns:
        [type]: [文件名列表，文件路径列表，文件夹列表]
    """
    FileNameWithPath = []
    FileName = []
    FileDir = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] in videoProperty:
                FileNameWithPath.append(os.path.join(root, file))  # 保存图片路径
                FileName.append(file)  # 保存图片名称
                FileDir.append(root[len(file_dir):])  # 保存图片所在文件夹

    return FileName, FileNameWithPath, FileDir


def video_to_omg(file_name, file_name_with_path, img_save_dir, count):
    """[summary]
    Args:
        file_name ([type]): 视频文件名
        file_name_with_path ([type]): 视频文件路径
        img_save_dir ([type]): 图片保存路径
        count ([int]): 1秒几张图片
    """
    print('Child process %s (%s)Running...' % (file_name, os.getpid()))
    videoLeftUp = cv2.VideoCapture(file_name_with_path)
    fps = videoLeftUp.get(cv2.CAP_PROP_FPS)
    # count = int(fps / count)  # 帧率，用于跳帧处理
    count = 3
    count_img = 0
    while (videoLeftUp.isOpened()):
        retLeftUp, frameLeftUp = videoLeftUp.read()
        if retLeftUp:
            count_img += 1
            if count_img % count == 0:
                # cv2.imshow(FileNameWithPath[j], frameLeftUp)
                dir_ornot(img_save_dir)
                img_name = img_save_dir + os.sep + file_name[:-4] + "0" + str(count_img).zfill(4) + ".jpg"
                # img_name = win_path_re(img_name)
                # print(img_name)
                cv2.imwrite(img_name, frameLeftUp)
        else:
            break
    count_img = 0
    videoLeftUp.release()
    print('Child process %s (%s)Stoping...' % (file_name, os.getpid()))


if __name__ == '__main__':
    args = sys_argv_var()
    time_time = time.time()
    root_dir = 'video_list/'
    save_dir = 'data_src/'
    FileName, FileNameWithPath, FileDir = GetNameByEveryDir(root_dir, '.mp4')
    # 设置进程池 最多10个进程
    p = Pool(6)
    # print(len(FileNameWithPath))
    # 20sec : 18378
    # 多线程写入图片
    for j in range(len(FileNameWithPath)):
        try:
            # 保存图片文件夹名  默认视频文件夹下的视频名文件夹
            img_save_dir = root_dir + FileName[j][:-4]
            if not os.path.exists(img_save_dir):
                os.makedirs(img_save_dir)
            # 多进程 未限制进程数
            # p=Process(target=video_to_omg,args=(FileName[j],FileNameWithPath[j],img_save_dir,5))
            # p.start()
            # 限制进程数
            # p.apply_async(video_to_omg, args=(FileName[j], FileNameWithPath[j], img_save_dir, 3))
            p.apply_async(video_to_omg, args=(FileName[j], FileNameWithPath[j], save_dir, 3))
        except Exception as e:
            print(e)
    p.close()
    p.join()
    print("inference time: {} s".format(round(time.time() - time_time, 4)))
