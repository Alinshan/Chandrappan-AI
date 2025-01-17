import os
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import g4f  # Ensure you have installed this library or replace it with another library if needed.

class Waki(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Waki Browser and AI-Chat")
        self.setGeometry(QRect(100, 100, 800, 600))

        # Set icon
        icon_path = "assets/icon.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Set custom font
        font = QFont("Roboto", 12)
        self.setFont(font)

        # Browser view setup
        self.browser = QWebEngineView()

        # Stylish URL bar
        self.url_bar = QLineEdit(self)
        self.url_bar.setPlaceholderText("Enter URL...")
        self.url_bar.setMinimumHeight(30)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                color: #2c3e50;
            }
        """)
        self.url_bar.setCursor(QCursor(Qt.IBeamCursor))

        # Stylish buttons
        self.go_btn = QPushButton("Go", self)
        self.back_btn = QPushButton("👈", self)
        self.forward_btn = QPushButton("👉", self)
        self.chat_btn = QPushButton("Chat with AI", self)
        self.generate_image_btn = QPushButton("Generate Image", self)
        for btn in [self.go_btn, self.back_btn, self.forward_btn, self.chat_btn, self.generate_image_btn]:
            btn.setMinimumHeight(30)
            btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.go_btn)
        self.horizontal_layout.addWidget(self.back_btn)
        self.horizontal_layout.addWidget(self.forward_btn)
        self.layout.addLayout(self.horizontal_layout)
        self.layout.addWidget(self.browser)
        self.layout.addWidget(self.chat_btn)
        self.layout.addWidget(self.generate_image_btn)

        # Event connections
        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.text()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.chat_btn.clicked.connect(self.open_chat_window)
        self.generate_image_btn.clicked.connect(self.open_image_window)

        # Set initial URL
        self.navigate("https://google.com")

    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

    def open_image_window(self):
        image_dialog = QDialog(self)
        image_dialog.setWindowTitle("🖼 Generated Image")
        image_dialog.setMinimumSize(400, 400)

        input_edit = QLineEdit(image_dialog)
        input_edit.setPlaceholderText("Enter image description...")
        generate_btn = QPushButton("Generate", image_dialog)
        label = QLabel(image_dialog)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(image_dialog)
        layout.addWidget(input_edit)
        layout.addWidget(generate_btn)
        layout.addWidget(label)

        generate_btn.clicked.connect(lambda: self.generate_image(input_edit.text(), label))

        image_dialog.exec_()

    def generate_image(self, prompt, label):
        try:
            url = f"https://hercai.onrender.com/prodia/text2image?prompt={prompt}"
            response = requests.get(url)
            response.raise_for_status()
            image_url = response.json().get("url")

            if image_url:
                image_data = requests.get(image_url).content
                temp_image_path = "assets/temp_img.png"
                with open(temp_image_path, "wb") as f:
                    f.write(image_data)
                pixmap = QPixmap(temp_image_path)
                label.setPixmap(pixmap)
            else:
                label.setText("Failed to retrieve image URL.")
        except Exception as e:
            label.setText(f"Error: {str(e)}")

    def open_chat_window(self):
        chat_window = QDialog(self)
        chat_window.setWindowTitle("🗣 Chat with AI")
        chat_window.setMinimumSize(400, 500)

        chat_output = QTextEdit(chat_window)
        chat_output.setReadOnly(True)

        input_edit = QLineEdit(chat_window)
        send_btn = QPushButton("Send", chat_window)

        layout = QVBoxLayout(chat_window)
        layout.addWidget(chat_output)
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_edit)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)

        send_btn.clicked.connect(lambda: self.send_message(input_edit.text(), chat_output))

        chat_window.exec_()

    def send_message(self, prompt, chat_output):
        if not prompt.strip():
            return
        chat_output.append(f"User: {prompt}")
        ai_response = self.generate_response(prompt)
        chat_output.append(f"AI: {ai_response}")

    def generate_response(self, prompt):
        try:
            # Replace 'model' and 'provider' with actual values supported by g4f
            response = g4f.ChatCompletion.create(
                model='gpt-3.5-turbo',
                provider=g4f.Provider.Aichat,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"

if _name_ == "_main_":
    import sys
    app = QApplication(sys.argv)
    window = Waki()
    window.show()
    sys.exit(app.exec_())
