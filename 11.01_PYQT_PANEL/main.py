# === AXIOM_PY_HEADER ===
# FILE: main.py
# TITLE: PYQT PANEL LAUNCHER
# VERSION: v0.2
# STATUS: DRAFT
# ZONE: [11_SYSTEM_INTERFACE]
# COMMENT: Точка входа для панели AXIOM SYSTEM V2. Подключает QSS-дизайн из ui/style/axiom_style.qss, запускает окна логина и основное окно.
# AUTHOR: CREATOR & AXIOM
# DATE: 2025-07-26
# === CHANGELOG ===
# v0.1 — 2025-07-26 — Инициализация файла, базовая структура и описание.
# v0.2 — 2025-07-26 — Подключение QSS-стиля, поддержка структуры ui/style/axiom_style.qss.
# =======================

"""
main.py — основной лаунчер панели AXIOM SYSTEM V2.
- Подключает дизайн-стиль (QSS) из ui/style/axiom_style.qss
- Стартует окно логина (login_window.py)
- При успехе запускает главное рабочее окно (main_window.py)
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

from login_window import LoginWindow   # Окно авторизации
from main_window import AxiomMainWindow     # Главное рабочее окно

# === Блок подключения QSS-стиля ===
def apply_axiom_style(app):
    """
    Загружает QSS-стиль AXIOM из ui/style/axiom_style.qss
    и применяет его ко всему приложению.
    """
    qss_path = os.path.join(
        os.path.dirname(__file__),
        "ui", "style", "axiom_style.qss"
    )
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            style = f.read()
            app.setStyleSheet(style)
            print(f"AXIOM QSS Style loaded from {qss_path}")
    else:
        print(f"⚠️ QSS файл не найден: {qss_path}")

def main():
    app = QApplication(sys.argv)
    apply_axiom_style(app)  # подключаем QSS до создания окон

    # === Запуск окна логина ===
    login = LoginWindow()
    if login.exec_() == login.Accepted:
        # === Успешный вход: открываем основное окно ===
        window = AxiomMainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()
