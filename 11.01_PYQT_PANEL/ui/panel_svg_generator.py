# === AXIOM_PY_HEADER ===
# FILE: panel_svg_generator.py
# TITLE: AXIOM SVG GENERATOR — GUI PANEL
# VERSION: v0.1
# STATUS: DRAFT / WORKING
# ZONE: [11_SYSTEM_INTERFACE/11.01_PYQT_PANEL/ui]
# COMMENT: Визуальный модуль для генерации и предпросмотра SVG (интеграция ядра генератора).
# AUTHOR: CREATOR & AXIOM
# DATE: 2025-07-26
# === CHANGELOG ===
# v0.1 — 2025-07-26 — Рабочая версия панели, поддержка шаблонов, параметров, предпросмотра и экспорта.
# =======================

"""
panel_svg_generator.py — GUI для генерации и предпросмотра SVG-шаблонов AXIOM SYSTEM.
Позволяет выбрать шаблон, заполнить параметры, просмотреть результат, экспортировать SVG.
"""

import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QFileDialog, QSpinBox, QScrollArea, QMessageBox
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt

from .generate_svg import AxiomSVGGenerator

class SVGGeneratorPanel(QWidget):
    def __init__(self, templates_dir="templates", style_dir="style"):
        super().__init__()
        self.setWindowTitle("AXIOM PANEL — SVG GENERATOR")
        self.templates_dir = templates_dir
        self.style_dir = style_dir
        self.generator = AxiomSVGGenerator(templates_dir, style_dir)
        self.presets = self.load_presets()
        self.svg_widget = QSvgWidget()
        self.param_widgets = {}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- 1. Шаблон ---
        self.template_combo = QComboBox()
        self.template_combo.addItems(self.generator.list_templates())
        self.template_combo.currentIndexChanged.connect(self.template_changed)
        layout.addWidget(QLabel("Шаблон SVG:"))
        layout.addWidget(self.template_combo)

        # --- 2. Пресеты (если есть) ---
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("(Без пресета)")
        for key in self.presets:
            self.preset_combo.addItem(key)
        self.preset_combo.currentIndexChanged.connect(self.preset_selected)
        layout.addWidget(QLabel("Профиль/Пресет:"))
        layout.addWidget(self.preset_combo)

        # --- 3. Параметры шаблона ---
        self.param_area = QScrollArea()
        self.param_area.setWidgetResizable(True)
        self.param_widget = QWidget()
        self.param_layout = QVBoxLayout(self.param_widget)
        self.param_area.setWidget(self.param_widget)
        layout.addWidget(QLabel("Параметры SVG:"))
        layout.addWidget(self.param_area)

        # --- 4. Preview & Export ---
        btn_layout = QHBoxLayout()
        self.preview_btn = QPushButton("Предпросмотр")
        self.preview_btn.clicked.connect(self.preview_svg)
        self.save_btn = QPushButton("Экспорт SVG")
        self.save_btn.clicked.connect(self.save_svg)
        btn_layout.addWidget(self.preview_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("SVG Preview:"))
        layout.addWidget(self.svg_widget, stretch=1)

        self.setLayout(layout)
        self.resize(480, 650)
        self.template_changed()  # инициализация параметров

    def load_presets(self):
        # Поиск svg_presets.json в templates
        p_path = os.path.join(self.templates_dir, "svg_presets.json")
        if os.path.exists(p_path):
            with open(p_path, encoding="utf-8") as f:
                data = json.load(f)
            return data.get("presets", {})
        return {}

    def template_changed(self):
        # При смене шаблона — обновить поля параметров
        tpl = self.template_combo.currentText()
        # По умолчанию: params = список параметров из шаблона или стандарт
        # Для MVP: выводим поля вручную (расширь под свои параметры!)
        self.clear_param_fields()
        # Минимальный набор, можешь расширять под любые шаблоны
        param_names = [
            "size", "color", "bg", "glow_color", "glow_opacity", "blade_opacity", "ring_opacity",
            "core_color", "core_opacity", "label", "label_color", "label_size", "bg_opacity", "border_width",
            "border_opacity", "decor_color", "decor_opacity"
        ]
        for pname in param_names:
            hl = QHBoxLayout()
            lbl = QLabel(pname + ":")
            edit = QLineEdit()
            hl.addWidget(lbl)
            hl.addWidget(edit)
            self.param_layout.addLayout(hl)
            self.param_widgets[pname] = edit
        self.param_widget.setLayout(self.param_layout)

    def clear_param_fields(self):
        # Очистить все поля параметров
        for i in reversed(range(self.param_layout.count())):
            item = self.param_layout.itemAt(i)
            if item:
                w = item.widget()
                if w:
                    w.deleteLater()
                else:
                    # это layout, удаляем его элементы
                    l = item.layout()
                    if l:
                        for j in reversed(range(l.count())):
                            lw = l.itemAt(j).widget()
                            if lw:
                                lw.deleteLater()
                        l.deleteLater()
                    self.param_layout.removeItem(item)
        self.param_widgets = {}

    def preset_selected(self):
        # Если выбран профиль — подгрузить параметры
        preset_name = self.preset_combo.currentText()
        if preset_name and preset_name in self.presets:
            params = self.presets[preset_name]["params"]
            for k, v in params.items():
                if k in self.param_widgets:
                    self.param_widgets[k].setText(str(v))
        else:
            # Если выбрано "Без пресета" — очистить все поля
            for w in self.param_widgets.values():
                w.clear()

    def get_params(self):
        params = {}
        for k, w in self.param_widgets.items():
            v = w.text().strip()
            if v != "":
                # Попробуем автоматически привести к float/int если число
                if v.replace('.', '', 1).isdigit():
                    params[k] = float(v) if '.' in v else int(v)
                else:
                    params[k] = v
        return params

    def preview_svg(self):
        tpl = self.template_combo.currentText()
        params = self.get_params()
        tmp_svg = "_tmp_preview.svg"
        try:
            self.generator.render(tpl, params, tmp_svg)
            self.svg_widget.load(tmp_svg)
            if os.path.exists(tmp_svg):
                os.remove(tmp_svg)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка генерации", str(e))

    def save_svg(self):
        tpl = self.template_combo.currentText()
        params = self.get_params()
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить SVG", self.style_dir, "SVG Files (*.svg)")
        if file_path:
            try:
                self.generator.render(tpl, params, os.path.basename(file_path))
                self.svg_widget.load(file_path)
                QMessageBox.information(self, "Успех", f"SVG успешно сохранён:\n{file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка экспорта", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SVGGeneratorPanel()
    window.show()
    sys.exit(app.exec_())
