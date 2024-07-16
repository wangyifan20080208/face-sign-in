import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
from PIL import Image, ImageTk
import pickle
import datetime
import pandas as pd
import pandas as pd
from datetime import datetime

#定义变量通知启动子功能
class FaceRecognitionApp:

    def __init__(self, root):

        self.root = root
        self.setup_gui()
        self.video_capture = cv2.VideoCapture(0)
        self.user_faces = self.load_faces()
        self.current_frame = None
        self.start_capture()

    def setup_gui(self):
        self.root.title("人脸识别提交")
        self.root.configure(bg="#ffffff")

        self.label = tk.Label(self.root, text="请输入用户名：", font=('Segoe UI', 14), bg="#ffffff")
        self.label.pack(pady=20)

        self.entry = tk.Entry(self.root, font=('Segoe UI', 12))
        self.entry.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

        self.login_button = tk.Button(self.root, text="提交", command=self.login, font=('Segoe UI', 12), bg="#4caf50", fg="white", relief=tk.FLAT)
        self.login_button.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
        self.login_button.bind("<Enter>", self.on_enter)
        self.login_button.bind("<Leave>", self.on_leave)

        self.register_button = tk.Button(self.root, text="录入人脸", command=self.register_face, font=('Segoe UI', 12), bg="#2196f3", fg="white", relief=tk.FLAT)
        self.register_button.pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)
        self.register_button.bind("<Enter>", self.on_enter)
        self.register_button.bind("<Leave>", self.on_leave)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)


    def on_enter(self, event):
        event.widget.config(bg="#64b5f6")


    def on_leave(self, event):
        event.widget.config(bg="#2196f3")

    def load_faces(self):
        try:
            with open("faces.pkl", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def save_faces(self):
        with open("faces.pkl", "wb") as file:
            pickle.dump(self.user_faces, file)

    def start_capture(self):
        self.update_frame()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.current_frame = frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.config(image=imgtk)
        self.root.after(10, self.update_frame)

    def get_face_encoding(self, frame):
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            return face_recognition.face_encodings(frame, face_locations)[0]
        return None

    def login(self):
        username = self.entry.get()
        if username in self.user_faces:
            user_encoding = self.user_faces[username]["encoding"]
            current_encoding = self.get_face_encoding(self.current_frame)

            if current_encoding is not None and face_recognition.compare_faces([user_encoding], current_encoding)[0]:
                messagebox.showinfo("成功", "登录成功")
                self.record_login(username)
            else:
                messagebox.showerror("错误", "人脸不匹配")
        else:
            messagebox.showerror("错误", "用户名不存在")

    def record_login(self, username):
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 创建数据框
        new_entry = pd.DataFrame([[username, current_time]], columns=['用户名', '提交时间'])

        # 读取现有的 Excel 文件或创建一个新的
        try:
            df = pd.read_excel("统计.xlsx")
            df = pd.concat([df, new_entry], ignore_index=True)
        except FileNotFoundError:
            df = new_entry

        # 保存到 Excel 文件
        df.to_excel("统计.xlsx", index=False)

    def register_face(self):
        username = self.entry.get()
        if username:
            current_encoding = self.get_face_encoding(self.current_frame)
            if current_encoding is not None:
                self.user_faces[username] = {"encoding": current_encoding}
                self.save_faces()
                messagebox.showinfo("成功", "人脸录入成功")
            else:
                messagebox.showerror("错误", "无法检测到人脸")
        else:
            messagebox.showerror("错误", "请输入用户名")

    def close_app(self):
        self.video_capture.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
