import os
import requests
import markdown2

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


class Waki(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waki Browser and AI-Chat")
        self.setGeometry(QRect(0, 0, 800, 600))
        self.setWindowIcon(QIcon("assets/icon.png"))

        font = QFont("Roboto", 12)
        font.setWeight(20)
        self.setFont(font)

        self.browser = QWebEngineView()

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
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            QPushButton:active {
                animation: pulse 0.3s ease;
            }
        """)
        self.go_btn.setCursor(QCursor(Qt.PointingHandCursor))

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
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            QPushButton:active {
                animation: pulse 0.3s ease;
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
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            QPushButton:active {
                animation: pulse 0.3s ease;
            }
        """)
        self.forward_btn.setCursor(QCursor(Qt.PointingHandCursor))

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
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            QPushButton:active {
                animation: pulse 0.3s ease;
            }
        """)
        self.chat_btn.setCursor(QCursor(Qt.PointingHandCursor))

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
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            QPushButton:active {
                animation: pulse 0.3s ease;
            }
        """)
        self.generate_image_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.generate_image_btn.clicked.connect(self.open_image_window)

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

        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.text()))
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.chat_btn.clicked.connect(self.open_chat_window)

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
        image_dialog = QDialog(self)
        image_dialog.setMinimumSize(400, 400)
        image_dialog.setWindowTitle("🖼️ Generated Image")

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
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            QPushButton:active {
                animation: pulse 0.3s ease;
            }
        """)
        generate_btn.setCursor(QCursor(Qt.PointingHandCursor))
        generate_btn.clicked.connect(lambda: self.generate_image_llama3(input_edit, image_dialog))

        label = QLabel(image
