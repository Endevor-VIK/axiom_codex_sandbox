# === AXIOM_PY_HEADER ===
# FILE: main_window.py
# TITLE: AXIOM MAIN PANEL — SYSTEM WINDOW (WITH SVG GENERATOR)
# VERSION: v1.2
# STATUS: ACTIVE
# ZONE: [11_SYSTEM_INTERFACE/11.01_PYQT_PANEL/]
# COMMENT: Главное sci-fi окно с управлением и внешним QSS-дизайном.
# AUTHOR: CREATOR & AXIOM
# DATE: 2025-07-26
# === CHANGELOG ===
# v0.1 — 2025-07-26 — MVP окно.
# v0.2 — 2025-07-26 — Card-дизайн, objectName, поддержка QSS.
# v1.0 — 2025-07-26 — Первая sci-fi версия с GUI-интеграцией SVG Generator.
# v1.1 — 2025-07-26 — Красная sci-fi версия с меню управления.
# v1.2 — 2025-07-26 — Очистка, поддержка внешнего QSS, objectName для элементов.
# =======================

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from ui.panel_svg_generator import SVGGeneratorPanel

class AxiomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AXIOM PANEL — Main")
        self.setWindowIcon(QIcon("ui/style/axiom_core.svg"))
        self.resize(470, 440)
        self.svg_panel = None
        self.init_ui()

    def init_ui(self):
        # Центрируем карточку как в login_window
        central_widget = QWidget()
        vbox = QVBoxLayout(central_widget)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addStretch(1)

        # Карточка/панель
        card = QWidget(self)
        card.setObjectName("AxiomCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 38, 40, 35)
        card_layout.setSpacing(14)

        # SVG-лого или символ
        label_logo = QLabel("⦓Ξ⦔")
        label_logo.setAlignment(Qt.AlignCenter)
        label_logo.setStyleSheet("font-size:38px;color:#fd1a29;margin-bottom:6px;letter-spacing:0.2em;")
        card_layout.addWidget(label_logo)

        # Заголовок (title)
        label_title = QLabel("AXIOM SYSTEM PANEL")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setObjectName("AxiomTitle")
        card_layout.addWidget(label_title)

        # Subtitle
        label_subtitle = QLabel("SYSTEM CORE // PROTOCOL: RED")
        label_subtitle.setAlignment(Qt.AlignCenter)
        label_subtitle.setStyleSheet("color:#fd1a29;font-size:16px;font-weight:600;letter-spacing:0.09em;margin-bottom:10px;")
        card_layout.addWidget(label_subtitle)

        # Разделитель
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background:#fd1a29;max-height:2px;min-height:2px;border-radius:1px;margin:14px 0 14px 0;")
        card_layout.addWidget(line)

        # --- Sci-fi меню управления ---
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(12)
        menu_layout.setAlignment(Qt.AlignCenter)

        svg_gen_btn = QPushButton("⚡ SVG Generator")
        svg_gen_btn.setObjectName("svgGenBtn")
        svg_gen_btn.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
        svg_gen_btn.setCursor(Qt.PointingHandCursor)
        svg_gen_btn.clicked.connect(self.open_svg_generator)
        menu_layout.addWidget(svg_gen_btn)

        settings_btn = QPushButton("⚙ Настройки")
        settings_btn.setObjectName("settingsBtn")
        settings_btn.setFont(QFont("JetBrains Mono", 12))
        settings_btn.setCursor(Qt.PointingHandCursor)
        menu_layout.addWidget(settings_btn)

        modules_btn = QPushButton("📦 Модули")
        modules_btn.setObjectName("modulesBtn")
        modules_btn.setFont(QFont("JetBrains Mono", 12))
        modules_btn.setCursor(Qt.PointingHandCursor)
        menu_layout.addWidget(modules_btn)

        card_layout.addLayout(menu_layout)

        # Footer / статус
        label_footer = QLabel("AXIOM SYSTEM V2 • RED PROTOCOL • Build 2025-07-26")
        label_footer.setAlignment(Qt.AlignCenter)
        label_footer.setObjectName("AxiomFooter")
        card_layout.addWidget(label_footer)

        vbox.addWidget(card, alignment=Qt.AlignCenter)
        vbox.addStretch(1)
        self.setCentralWidget(central_widget)

    def open_svg_generator(self):
        if not self.svg_panel or not self.svg_panel.isVisible():
            self.svg_panel = SVGGeneratorPanel()
            self.svg_panel.show()
        else:
            self.svg_panel.raise_()
            self.svg_panel.activateWindow()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Используем твой axiom_red.qss (файл уже готов и лежит в ui/style)
    qss_path = os.path.join(os.path.dirname(__file__), "ui", "style", "axiom_red.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    window = AxiomMainWindow()
    window.show()
    sys.exit(app.exec_())


