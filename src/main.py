import os
import openai
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import markdown2

class Synth(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synth Browser and Chat")
        self.setGeometry(QRect(0, 0, 800, 600))

        # Set icon
        self.setWindowIcon(QIcon("assets/icon.png"))

        # Set custom font
        font = QFont("Roboto", 12)
        font.setWeight(20)
        self.setFont(font)

        # Browser view setup
        self.browser = QWebEngineView()

        # Stylish URL bar
        self.url_bar = QLineEdit(self)
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

        self.generated_image_url = "assets/placeholder.jpg"

        # Stylish Go button
        self.go_btn = QPushButton("Go", self)
        self.go_btn.setMinimumHeight(30)
        self.go_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #219d54;
            }
        """)
        self.go_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Stylish navigation buttons
        self.back_btn = QPushButton("👈", self)
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: #fff;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.forward_btn = QPushButton("👉", self)
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: #fff;
                padding: 10px 10px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #d68910;
            }
        """)
        self.forward_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Chat with AI button
        self.chat_btn = QPushButton("Chat with AI", self)
        self.chat_btn.setMinimumHeight(30)
        self.chat_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.chat_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Generate Image button
        self.generate_image_btn = QPushButton("Generate Image", self)
        self.generate_image_btn.setMinimumHeight(30)
        self.generate_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: #fff;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.generate_image_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Connect Generate Image button to the function
        self.generate_image_btn.clicked.connect(self.open_image_window)

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.horizontal_layout = QHBoxLayout()

        self._history = []

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

        # Set initial URL
        self.navigate("https://google.com")

    @property
    def url(self):
        return self.browser.url().toString()

    @url.setter
    def url(self, url):
        self.navigate(url)

    @property
    def history(self):
        return self._history

    @property
    def title(self):
        return self.browser.title()

    @title.setter
    def title(self, title):
        self.setWindowTitle(title)

    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

    def open_image_window(self):
        # Open a dialog to display the image
        image_dialog = QDialog(self)
        image_dialog.setMinimumSize(400, 400)
        image_dialog.setWindowTitle("🖼️ Generated Image")

        # Add input bar to dialog
        input_edit = QLineEdit(image_dialog)
        input_edit.setStyleSheet("""
            QLineEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                color: #2c3e50;
            }
        """)
        input_edit.setFont(QFont("Roboto", 12, 20))
        input_edit.setCursor(QCursor(Qt.IBeamCursor))

        # Add button to generate the image
        generate_btn = QPushButton("Generate", image_dialog)
        generate_btn.setFont(QFont("Roboto", 12, 20))
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: #fff;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        generate_btn.setCursor(QCursor(Qt.PointingHandCursor))
        generate_btn.clicked.connect(lambda: self.generate_image(input_edit, image_dialog))

        # Show <img> tag in dialog
        label = QLabel(image_dialog)
        path = "assets/placeholder.jpg"
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)

        # Add elements to dialog
        layout = QVBoxLayout(image_dialog)
        layout.addWidget(input_edit)
        layout.addWidget(generate_btn)
        layout.addWidget(label)

        image_dialog.exec_()

    def generate_image(self, input_edit, dialog):
        prompt = input_edit.text()

        # Replace this with OpenAI's DALL·E API call
        openai.api_key = ''  # Set your OpenAI API key here

        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"  # Adjust size as per your needs
            )
            image_url = response['data'][0]['url']

            # Save the image to assets/temp_img.png
            img_data = requests.get(image_url).content
            with open("assets/temp_img.png", "wb") as f:
                f.write(img_data)

            # Reload the image in the dialog
            pixmap = QPixmap("assets/temp_img.png")
            label = dialog.findChild(QLabel)
            label.setPixmap(pixmap)

        except Exception as e:
            print(f"Error generating image: {e}")

    def open_chat_window(self):
        chat_window = QDialog(self)
        chat_window.setMinimumSize(400, 500)
        chat_window.setWindowTitle("🗣️ Chat with AI")

        chat_output = QTextEdit(chat_window)
        chat_output.setReadOnly(True)
        chat_output.setLineWrapMode(QTextEdit.NoWrap)

        input_edit = QLineEdit(chat_window)
        input_edit.setStyleSheet("""
            QLineEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                color: #2c3e50;
            }
        """)
        input_edit.setCursor(QCursor(Qt.IBeamCursor))
        input_edit.setFont(QFont("Roboto", 12, 20))

        send_btn = QPushButton("✉️ Send", chat_window)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        send_btn.setCursor(QCursor(Qt.PointingHandCursor))
        send_btn.setFont(QFont("Roboto", 12, 20))

        send_btn.clicked.connect(lambda: self.send_message(input_edit, chat_output))

        layout = QVBoxLayout(chat_window)
        layout.addWidget(chat_output, 1)
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_edit, 1)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)

        # Add history to chat output
        for message in self.history:
            self.apply_styles(chat_output, message["content"], role=message["role"])

        chat_window.exec_()

    def send_message(self, input_edit, chat_output):
        prompt = input_edit.text()
        ai_response = self.generate_response(prompt)

        self.history.append({
            "role": "user",
            "content": prompt
        })

        self.history.append({
            "role": "bot",
            "content": ai_response
        })

        self.apply_styles(chat_output, prompt, role="user")
        self.apply_styles(chat_output, ai_response, role="bot")

        input_edit.clear()

    def apply_styles(self, chat_output, message, role):
        user_style = "color: #3498db;"
        bot_style = "color: #2ecc71; font-size: 12px;"
        
        message = markdown2.markdown(message)

        if role == "user":
            message_style = user_style
        elif role == "bot":
            message_style = bot_style
        else:
            message_style = ""

        chat_output.append(f"<span style='{message_style}'>{message}</span>")

    def generate_response(self, prompt):
        self.history.append({
            "role": "user",
            "content": prompt
        })
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
        )

        return response['choices'][0]['message']['content']

if __name__ == "__main__":
    app = QApplication([])
    window = Synth()
    window.show()
    app.exec_()
