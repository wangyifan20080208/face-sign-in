import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
from PIL import Image, ImageTk
import pickle

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("人脸识别登录")

        # 初始化摄像头
        self.video_capture = cv2.VideoCapture(0)

        # 创建登录界面
        self.label = tk.Label(root, text="请输入用户名：")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.login_button = tk.Button(root, text="登录", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(root, text="录入人脸", command=self.register_face)
        self.register_button.pack()

        # 用户名和人脸图像的字典
        self.user_faces = self.load_faces()

        # 开始捕获摄像头图像
        self.start_capture()

    def login(self):
        username = self.entry.get()

        if username in self.user_faces:
            user_encoding = self.user_faces[username]["encoding"]

            # 读取摄像头图像
            ret, frame = self.video_capture.read()

            # 检测摄像头中的人脸
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            # 比对人脸
            for face_encoding in face_encodings:
                # 计算欧氏距离
                distance = face_recognition.face_distance([user_encoding], face_encoding)
                similarity = 1 - distance[0]  # 相似度越大越相似

                if similarity > 0.6:  
                    messagebox.showinfo("登录成功", f"欢迎回来，{username}，相似度：{similarity:.2f}")
                    self.video_capture.release()
                    self.root.destroy()
                    print("ok")
                    break
                else:
                    messagebox.showerror("登录失败", f"相似度不足，无法登录，相似度：{similarity:.2f}")
                    break
            else:
                messagebox.showerror("登录失败", "未能识别出您的人脸，请重试")
        else:
            messagebox.showerror("用户不存在", "请先录入人脸")

    def register_face(self):
        username = self.entry.get()

        # 创建录入人脸的界面
        register_window = tk.Toplevel(self.root)
        register_window.title("录入人脸")

        # 创建提示标签
        info_label = tk.Label(register_window, text="请调整姿势，然后点击按钮录入人脸")
        info_label.pack()

        # 创建按钮
        register_button = tk.Button(register_window, text="录入人脸", command=lambda: self.capture_and_register(username))
        register_button.pack()

    def capture_and_register(self, username):
        # 读取摄像头图像
        ret, frame = self.video_capture.read()

        # 检测摄像头中的人脸
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if len(face_encodings) == 1:
            # 保存用户人脸图像和编码
            self.user_faces[username] = {"image": cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
                                          "encoding": face_encodings[0]}
            messagebox.showinfo("录入成功", f"{username}的人脸已成功录入")

            # 保存人脸信息到文件
            self.save_faces()
        else:
            messagebox.showerror("录入失败", "未能识别出您的人脸，请重试")

    def start_capture(self):
        ret, frame = self.video_capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)

            self.label.config(image=photo)
            self.label.image = photo
            self.root.after(10, self.start_capture)
        else:
            messagebox.showerror("错误", "无法启动摄像头")

    def load_faces(self):
        try:
            with open("faces.pkl", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def save_faces(self):
        with open("faces.pkl", "wb") as file:
            pickle.dump(self.user_faces, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
