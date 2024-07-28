import os
import g4f
import requests
import markdown2

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class Chandrappan(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chandrappan An AI Browser and AI-Chat Bot")
        self.setGeometry(QRect(0, 0, 800, 600))

        self.setWindowIcon(QIcon("assets/icon.png"))

        self.light_theme = {
            "background-color": "#ffffff",
            "text-color": "#000000",
            "input-bg-color": "#ecf0f1",
            "input-border-color": "#bdc3c7",
            "button-bg-color": "#3498db",
            "button-text-color": "#fff",
            "button-hover-bg-color": "#2980b9"
        }

        self.dark_theme = {
            "background-color": "#2c3e50",
            "text-color": "#ecf0f1",
            "input-bg-color": "#34495e",
            "input-border-color": "#2c3e50",
            "button-bg-color": "#e74c3c",
            "button-text-color": "#fff",
            "button-hover-bg-color": "#c0392b"
        }

        self.current_theme = self.light_theme

        self.apply_stylesheet()

        font = QFont("Roboto", 12)
        font.setWeight(20)
        self.setFont(font)

        # Browser view setup
        self.browser = QWebEngineView()

        # Dropdown menu for browser selection
        self.browser_select = QComboBox(self)
        self.browser_select.addItems(["QWebEngineView", "QTextBrowser"])  # Add more browsers as needed
        self.browser_select.setStyleSheet(self.generate_stylesheet("combobox"))
        self.browser_select.currentIndexChanged.connect(self.switch_browser)

        # Stylish URL bar
        self.url_bar = QLineEdit(self)
        self.url_bar.setMinimumHeight(30)
        self.url_bar.setStyleSheet(self.generate_stylesheet("lineedit"))
        self.url_bar.setCursor(QCursor(Qt.IBeamCursor))

        self.generated_image_url = "assets/placeholder.jpg"

        # Stylish Go button
        self.go_btn = QPushButton("Go", self)
        self.go_btn.setMinimumHeight(30)
        self.go_btn.setStyleSheet(self.generate_stylesheet("button"))
        self.go_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Stylish navigation buttons
        self.back_btn = QPushButton("👈", self)
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setStyleSheet(self.generate_stylesheet("button"))
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.forward_btn = QPushButton("👉", self)
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setStyleSheet(self.generate_stylesheet("button"))
        self.forward_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Chat with AI button
        self.chat_btn = QPushButton("Chat with AI", self)
        self.chat_btn.setMinimumHeight(30)
        self.chat_btn.setStyleSheet(self.generate_stylesheet("button"))
        self.chat_btn.setCursor(QCursor(Qt.PointingHandCursor))

        # Generate Image button
        self.generate_image_btn = QPushButton("Generate Image", self)
        self.generate_image_btn.setMinimumHeight(30)
        self.generate_image_btn.setStyleSheet(self.generate_stylesheet("button"))
        self.generate_image_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.generate_image_btn.clicked.connect(self.open_image_window)

        # Theme toggle button
        self.theme_btn = QPushButton("Toggle Theme", self)
        self.theme_btn.setMinimumHeight(30)
        self.theme_btn.setStyleSheet(self.generate_stylesheet("button"))
        self.theme_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.theme_btn.clicked.connect(self.toggle_theme)

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.horizontal_layout = QHBoxLayout()

        self._history = []

        self.horizontal_layout.addWidget(self.browser_select)  # Add browser selection dropdown
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.go_btn)
        self.horizontal_layout.addWidget(self.back_btn)
        self.horizontal_layout.addWidget(self.forward_btn)
        self.horizontal_layout.addWidget(self.theme_btn)

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

    def switch_browser(self):
        browser_type = self.browser_select.currentText()

        # Remove the current browser view from the layout
        self.layout.removeWidget(self.browser)
        self.browser.deleteLater()

        # Create a new browser view based on the selection
        if (browser_type == "QWebEngineView"):
            self.browser = QWebEngineView()
        elif (browser_type == "QTextBrowser"):
            self.browser = QTextBrowser()

        # Add the new browser view to the layout
        self.layout.insertWidget(1, self.browser)
        self.navigate(self.url_bar.text())

    def open_image_window(self):
        image_dialog = QDialog(self)
        image_dialog.setMinimumSize(400, 400)
        image_dialog.setWindowTitle("🖼️ Generated Image")

        input_edit = QLineEdit(image_dialog)
        input_edit.setStyleSheet(self.generate_stylesheet("lineedit"))
        input_edit.setFont(QFont("Roboto", 12, 20))
        input_edit.setCursor(QCursor(Qt.IBeamCursor))

        generate_btn = QPushButton("Generate", image_dialog)
        generate_btn.setFont(QFont("Roboto", 12, 20))
        generate_btn.setStyleSheet(self.generate_stylesheet("button"))
        generate_btn.setCursor(QCursor(Qt.PointingHandCursor))
        generate_btn.clicked.connect(lambda: self.generate_image(input_edit, image_dialog))

        label = QLabel(image_dialog)
        path = "assets/placeholder.jpg" if not os.path.exists("assets/temp_img.png") else "assets/temp_img.png"
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)

        layout = QVBoxLayout(image_dialog)
        layout.addWidget(input_edit)
        layout.addWidget(generate_btn)
        layout.addWidget(label)

        image_dialog.exec_()

    def generate_image(self, input_edit, dialog):
        prompt = input_edit.text()
        url = "https://hercai.onrender.com/prodia/text2image?prompt=" + prompt

        response = requests.get(url)
        image_url = response.json()["url"]

        with open("assets/temp_img.png", "wb") as f:
            f.write(requests.get(image_url).content)

        pixmap = QPixmap("assets/temp_img.png")
        label = dialog.findChild(QLabel)
        label.setPixmap(pixmap)

    def open_chat_window(self):
        chat_window = QDialog(self)
        chat_window.setMinimumSize(400, 500)
        chat_window.setWindowTitle("🗣️ Chat with AI")

        chat_output = QTextEdit(chat_window)
        chat_output.setReadOnly(True)
        chat_output.setLineWrapMode(QTextEdit.NoWrap)

        input_edit = QLineEdit(chat_window)
        input_edit.setStyleSheet(self.generate_stylesheet("lineedit"))
        input_edit.setCursor(QCursor(Qt.IBeamCursor))
        input_edit.setFont(QFont("Roboto", 12, 20))

        send_btn = QPushButton("✉️ Send", chat_window)
        send_btn.setStyleSheet(self.generate_stylesheet("button"))
        send_btn.setCursor(QCursor(Qt.PointingHandCursor))
        send_btn.setFont(QFont("Roboto", 12, 20))

        send_btn.clicked.connect(lambda: self.send_message(input_edit, chat_output))

        layout = QVBoxLayout(chat_window)
        layout.addWidget(chat_output, 1)
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_edit, 1)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)

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
        user_style = """
            color: #3498db;
        """

        bot_style = """
            color: #2ecc71;
            font-size: 12px;
        """
        
        message = markdown2.markdown(message)

        message_style = user_style if role == "user" else bot_style if role == "bot" else ""

        chat_output.append(f"<span style='{message_style}'>{message}</span>")

    def generate_response(self, prompt):
        self.history.append({
                "role": "user",
                "content": prompt
            })
        response = g4f.ChatCompletion.create(
            model=g4f.models.llama3_70b,
            messages=self.history,
        )

        return response

    def toggle_theme(self):
        self.current_theme = self.dark_theme if self.current_theme == self.light_theme else self.light_theme
        self.apply_stylesheet()

    def apply_stylesheet(self):
        stylesheet = f"""
            QWidget {{
                background-color: {self.current_theme["background-color"]};
                color: {self.current_theme["text-color"]};
            }}
            QLineEdit {{
                background-color: {self.current_theme["input-bg-color"]};
                border: 1px solid {self.current_theme["input-border-color"]};
                border-radius: 5px;
                padding: 5px;
                color: {self.current_theme["text-color"]};
            }}
            QPushButton {{
                background-color: {self.current_theme["button-bg-color"]};
                color: {self.current_theme["button-text-color"]};
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme["button-hover-bg-color"]};
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
            QPushButton:active {{
                animation: pulse 0.3s ease;
            }}
            QComboBox {{
                background-color: {self.current_theme["input-bg-color"]};
                border: 1px solid {self.current_theme["input-border-color"]};
                border-radius: 5px;
                padding: 5px;
                color: {self.current_theme["text-color"]};
            }}
        """
        self.setStyleSheet(stylesheet)

    def generate_stylesheet(self, widget_type):
        if widget_type == "lineedit":
            return f"""
                background-color: {self.current_theme["input-bg-color"]};
                border: 1px solid {self.current_theme["input-border-color"]};
                border-radius: 5px;
                padding: 5px;
                color: {self.current_theme["text-color"]};
            """
        elif widget_type == "button":
            return f"""
                background-color: {self.current_theme["button-bg-color"]};
                color: {self.current_theme["button-text-color"]};
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            """
        elif widget_type == "combobox":
            return f"""
                background-color: {self.current_theme["input-bg-color"]};
                border: 1px solid {self.current_theme["input-border-color"]};
                border-radius: 5px;
                padding: 5px;
                color: {self.current_theme["text-color"]};
            """
        else:
            return ""

if __name__ == "__main__":
    app = QApplication([])
    window = Chandrappan()
    window.show()
    app.exec_()
