# === AXIOM_PY_HEADER ===
# FILE: login_window.py
# TITLE: LOGIN WINDOW MODULE
# VERSION: v0.3
# STATUS: DRAFT
# ZONE: [11_SYSTEM_INTERFACE]
# COMMENT: Окно авторизации с фирменной "карточкой" и поддержкой QSS-стиля из axiom_style.qss.
# AUTHOR: CREATOR & AXIOM
# DATE: 2025-07-26
# === CHANGELOG ===
# v0.1 — 2025-07-26 — MVP: базовая форма логина.
# v0.2 — 2025-07-26 — Вынесена авторизация в users/auth.json, SHA256-хеш.
# v0.3 — 2025-07-26 — Дизайн-карточка, objectName, центрирование, поддержка QSS.
# =======================

"""
login_window.py — окно авторизации AXIOM PANEL.
- Фирменная карточка (card-компоновка) с QSS-стилем.
- Логины и хеши паролей хранятся в users/auth.json.
- Можно расширять под любой будущий UI и модули.
"""

from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
import hashlib
import json
import os

# === Путь к auth.json ===
AUTH_FILE = os.path.join(
    os.path.dirname(__file__), "users", "auth.json"
)

def check_credentials(login, password):
    if not os.path.exists(AUTH_FILE):
        return False
    try:
        with open(AUTH_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return False
    hash_pw = hashlib.sha256(password.encode()).hexdigest()
    for user in data.get("users", []):
        if user["login"] == login and user["password_hash"] == hash_pw:
            return True
    return False

class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setWindowTitle("AXIOM PANEL — Login")
        self.setMinimumSize(470, 440)
        self.setMaximumSize(700, 680)

        # === Apply QSS style ===
        qss_path = os.path.join(
            os.path.dirname(__file__),
            "ui", "style", "axiom_red.qss"
        )
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

        # === Карточка (обёртка) ===
        card = QWidget(self)
        card.setObjectName("AxiomCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 38, 40, 35)
        card_layout.setSpacing(12)

        # SVG-лого — можешь заменить на свой QPixmap/QSvgWidget
        label_logo = QLabel("⦓Ξ⦔")
        label_logo.setAlignment(Qt.AlignCenter)
        label_logo.setStyleSheet("font-size:38px;color:#fd1a29;margin-bottom:6px;letter-spacing:0.2em;")
        card_layout.addWidget(label_logo)

        # Заголовок (title)
        label_title = QLabel("ВХОД В AXIOM PANEL")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setObjectName("AxiomTitle")
        card_layout.addWidget(label_title)

        # Subtitle
        label_subtitle = QLabel("ACCESS TO SYSTEM CORE // PROTOCOL: RED")
        label_subtitle.setAlignment(Qt.AlignCenter)
        label_subtitle.setStyleSheet("color:#fd1a29;font-size:16px;font-weight:600;letter-spacing:0.09em;margin-bottom:10px;")
        card_layout.addWidget(label_subtitle)

        # Разделитель
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background:#fd1a29;max-height:2px;min-height:2px;border-radius:1px;margin:14px 0 14px 0;")
        card_layout.addWidget(line)

        # Логин
        label_user = QLabel("Логин:")
        label_user.setStyleSheet("color:#fd1a29;font-size:15px;font-weight:600;")
        input_user = QLineEdit()
        input_user.setPlaceholderText("Введите логин")

        # Пароль
        label_pass = QLabel("Пароль:")
        label_pass.setStyleSheet("color:#fd1a29;font-size:15px;font-weight:600;")
        input_pass = QLineEdit()
        input_pass.setPlaceholderText("Введите пароль")
        input_pass.setEchoMode(QLineEdit.Password)

        card_layout.addWidget(label_user)
        card_layout.addWidget(input_user)
        card_layout.addWidget(label_pass)
        card_layout.addWidget(input_pass)

        # Кнопка входа
        button_login = QPushButton("ВОЙТИ")
        button_login.setCursor(Qt.PointingHandCursor)
        button_login.setDefault(True)
        card_layout.addWidget(button_login)

        # Footer
        label_footer = QLabel("AXIOM SYSTEM V2 • RED PROTOCOL • Build 2025-07-26")
        label_footer.setAlignment(Qt.AlignCenter)
        label_footer.setObjectName("AxiomFooter")
        card_layout.addWidget(label_footer)

        # Внешний layout
        outer_layout = QVBoxLayout(self)
        outer_layout.addStretch(1)
        outer_layout.addWidget(card, alignment=Qt.AlignCenter)
        outer_layout.addStretch(1)

        self.input_user = input_user
        self.input_pass = input_pass
        button_login.clicked.connect(self.check_login)

    def check_login(self):
        user = self.input_user.text()
        pwd = self.input_pass.text()
        if check_credentials(user, pwd):
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка входа", "Неверный логин или пароль.")

