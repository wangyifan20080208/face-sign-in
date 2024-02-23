# face sign in

声明：本项目已基于Apache 2.0协议开源,github链接“https://github.com/wangyifan20080208/face-sign-in”

## 运行环境搭建

### python

基于tk opencv-python face_recognition Pillow库开发
安装依赖`pip install tk opencv-python face_recognition Pillow`

如失败，请运行`pip install tk opencv-python face_recognition Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple some-package`

安装后在程序目录内使用shell(linux)或cmd(windows)运行

`python main.py`

### docker

开发中

***

以下是所使用的python库

**Tkinter (tk):**

Tkinter 是 Python 的标准 GUI（图形用户界面）工具包。
它提供了一组模块，用于创建简单和复杂的图形用户界面。
Tkinter 允许开发人员创建窗口、按钮、标签、输入字段等，并以用户友好的方式进行排列。

**OpenCV (opencv-python):**

OpenCV（Open Source Computer Vision Library）是一个流行的开源库，用于计算机视觉和图像处理任务。
它提供了广泛的功能，用于图像和视频处理、对象检测、特征提取、运动跟踪等任务。
OpenCV 支持多种编程语言，包括 Python、C++ 和 Java。
其主要功能包括图像/视频输入输出、图像滤波、特征检测、对象识别和摄像机校准等。

**face_recognition:**

face_recognition 是一个基于 dlib 和 OpenCV 构建的 Python 库，用于人脸识别任务。
它提供了简单的 API 用于人脸检测、人脸识别和人脸关键点检测。
该库可用于识别图像或视频中的人脸、人脸属性识别（如年龄和性别估计）以及人脸相似性比较等任务。

**Pillow:**

Pillow（Python Imaging Library，PIL）是一个强大的库，用于打开、操作和保存许多不同的图像文件格式。
它提供了基本图像处理任务的功能，如调整大小、裁剪、旋转和过滤图像。
Pillow 支持各种图像文件格式，包括 JPEG、PNG、GIF、BMP 和 TIFF。
它被广泛用于图像编辑、图像增强、生成缩略图以及在不同图像格式之间进行转换等任务。
