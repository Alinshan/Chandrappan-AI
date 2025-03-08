import os
import openai
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import markdown2

# Ensure OpenAI API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

class Synth(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synth Browser and Chat")
        self.setGeometry(QRect(0, 0, 800, 600))
        self.setWindowIcon(QIcon("assets/icon.png"))

        font = QFont("Roboto", 12)
        self.setFont(font)

        # Browser view setup
        self.browser = QWebEngineView()

        # URL bar
        self.url_bar = QLineEdit(self)
        self.url_bar.setPlaceholderText("Enter URL...")

        # Navigation Buttons
        self.go_btn = QPushButton("Go", self)
        self.back_btn = QPushButton("👈", self)
        self.forward_btn = QPushButton("👉", self)
        self.chat_btn = QPushButton("Chat with AI", self)
        self.generate_image_btn = QPushButton("Generate Image", self)

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

        self.navigate("https://google.com")

    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def open_image_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Generate Image")
        dialog.setMinimumSize(400, 400)

        input_edit = QLineEdit(dialog)
        input_edit.setPlaceholderText("Enter image description")
        generate_btn = QPushButton("Generate", dialog)
        label = QLabel(dialog)

        layout = QVBoxLayout(dialog)
        layout.addWidget(input_edit)
        layout.addWidget(generate_btn)
        layout.addWidget(label)

        generate_btn.clicked.connect(lambda: self.generate_image(input_edit.text(), label))
        dialog.exec_()

    def generate_image(self, prompt, label):
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url

            img_data = requests.get(image_url).content
            with open("assets/generated_image.png", "wb") as f:
                f.write(img_data)

            pixmap = QPixmap("assets/generated_image.png")
            label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate image: {e}")

    def open_chat_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Chat with AI")
        dialog.setMinimumSize(400, 500)

        chat_output = QTextEdit(dialog)
        chat_output.setReadOnly(True)
        input_edit = QLineEdit(dialog)
        send_btn = QPushButton("Send", dialog)

        layout = QVBoxLayout(dialog)
        layout.addWidget(chat_output)
        layout.addWidget(input_edit)
        layout.addWidget(send_btn)

        send_btn.clicked.connect(lambda: self.send_message(input_edit, chat_output))
        dialog.exec_()

    def send_message(self, input_edit, chat_output):
        user_message = input_edit.text().strip()
        if not user_message:
            return

        chat_output.append(f"<b>You:</b> {user_message}")
        input_edit.clear()

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            ai_response = response.choices[0].message.content
            chat_output.append(f"<b>AI:</b> {ai_response}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get AI response: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = Synth()
    window.show()
    app.exec_()
