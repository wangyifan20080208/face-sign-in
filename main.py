import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
from PIL import Image, ImageTk
import pickle
import datetime
import pandas as pd

#定义变量通知启动子功能
class FaceRecognitionApp:

    def __init__(self, root):

        self.root = root
        self.root.title("人脸识别提交")
        self.root.configure(bg="#ffffff")  # 设置背景色

        # 初始化摄像头
        self.video_capture = cv2.VideoCapture(0)

        # 创建登录界面
        self.label = tk.Label(root, text="请输入用户名：", font=('Segoe UI', 14), bg="#ffffff")
        self.label.pack(pady=20)

        self.entry = tk.Entry(root, font=('Segoe UI', 12))
        self.entry.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

        self.login_button = tk.Button(root, text="提交", command=self.login, font=('Segoe UI', 12), bg="#4caf50", fg="white", relief=tk.FLAT)
        self.login_button.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
        self.login_button.bind("<Enter>", self.on_enter)
        self.login_button.bind("<Leave>", self.on_leave)

        self.register_button = tk.Button(root, text="录入人脸", command=self.register_face, font=('Segoe UI', 12), bg="#2196f3", fg="white", relief=tk.FLAT)
        self.register_button.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
        self.register_button.bind("<Enter>", self.on_enter)
        self.register_button.bind("<Leave>", self.on_leave)

        # 用户名和人脸图像的字典
        self.user_faces = self.load_faces()

        # 开始捕获摄像头图像
        self.start_capture()


    def on_enter(self, event):
        event.widget.config(bg="#64b5f6")


    def on_leave(self, event):
        event.widget.config(bg="#2196f3")


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
                messagebox.showinfo("提交成功", f"恭喜{username}已完成。")#，相似度：{similarity:.2f}
                self.video_capture.release()
                self.root.destroy()

                # 获取当前时间
                current_time = datetime.datetime.now()

                # 创建一个名为"统计.xlsx"的文件，如果文件已存在，则打开该文件
                try:
                    df = pd.read_excel('统计.xlsx')
                except FileNotFoundError:
                    df = pd.DataFrame(columns=['用户名', '提交时间'])

                # 创建一个新的数据行，包含用户名和登录时间
                new_row = {'用户名': username, '提交时间': current_time}

                # 将新的数据行添加到xlsx文件中
                df = df._append(new_row, ignore_index=True)

                # 保存xlsx文件
                df.to_excel('统计.xlsx', index=False)

                break
            else:
                messagebox.showerror("提交失败", f"相似度不足，无提交录，相似度：{similarity:.2f}")
                break
        else:
            messagebox.showerror("提交失败", "未能识别出您的人脸，请重试")

    def register_face(self):
        username = self.entry.get()

        # 创建录入人脸的界面
        register_window = tk.Toplevel(self.root)
        register_window.title("录入人脸")
        register_window.configure(bg="#ffffff")

        # 创建提示标签
        info_label = tk.Label(register_window, text="请调整姿势，然后点击按钮录入人脸", font=('Segoe UI', 12), bg="#ffffff")
        info_label.pack(pady=20)

        # 创建按钮
        register_button = tk.Button(register_window, text="录入人脸", command=lambda: self.capture_and_register(username), font=('Segoe UI', 12), bg="#4caf50", fg="white", relief=tk.FLAT)
        register_button.pack(pady=10)

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
    while True:
        root = tk.Tk()
        app = FaceRecognitionApp(root)
        root.mainloop()
    