import cv2
from PIL import Image
import numpy as np
from skimage.restoration import denoise_nl_means, estimate_sigma
import SRCNN
from scipy import ndimage

视频地址 = r""
保存目录 = ""

背景颜色 = (29, 30, 32)  # 需要去除的颜色
容忍度 = 100

cap = cv2.VideoCapture(视频地址)

# 检查视频文件是否成功打开
if not cap.isOpened():
    print("无法打开视频文件")
    exit()

# 获取原始视频的帧率、宽度和高度
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 创建 VideoWriter 对象，用于写入新的视频文件

i = 1
# 循环读取视频帧
while True:
    print(f"{i} / {total_frames + 1}")
    # 读取一帧视频数据
    ret, frame = cap.read()
    # 如果视频读取完毕，退出循环
    if not ret:
        break

    ### 将BGR图像转换为RGBA图像
    # frame = frame[..., ::-1]  # 将 BGR 转换为 RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    ### 去除背景色
    image = Image.fromarray(frame)
    image.show()
    input()
    pixels = image.getdata()  # 获取图片的像素数据
    # 将蓝色色块变为透明
    new_pixels = []
    for pixel in pixels:
        当前颜色 = pixel[:3]
        # 判断是否为蓝色
        if abs(当前颜色[0] - 背景颜色[0]) <= 容忍度 and abs(当前颜色[1] - 背景颜色[1]) <= 容忍度 and abs(当前颜色[2] - 背景颜色[2]) <= 容忍度:
            # 将蓝色像素设置为完全透明
            new_pixels.append((0, 0, 0, 0))
        else:
            new_pixels.append(pixel)
    # 更新图片的像素数据
    image.putdata(new_pixels)
    image.save(f"{保存目录}/{i}.png")

    # ### 显示处理后的图像
    # cv2.imshow('RGBA图像', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    i += 1