FROM 3.11.8-windowsservercore-ltsc2022
WORKDIR /FACE
COPY . .
RUN pip install tk opencv-python face_recognition Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
CMD [ "python","main.py" ]