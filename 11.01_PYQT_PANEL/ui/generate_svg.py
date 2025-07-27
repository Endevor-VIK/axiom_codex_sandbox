# === AXIOM_PY_HEADER ===
# FILE: generate_svg.py
# TITLE: AXIOM SVG GENERATOR — CORE MODULE
# VERSION: v1.0
# STATUS: ACTIVE / EXPANDABLE
# ZONE: [11_SYSTEM_INTERFACE/11.01_PYQT_PANEL/ui]
# COMMENT: Ядро SVG-генератора. Автоматизация создания sci-fi svg на основе шаблонов и параметров.
# AUTHOR: CREATOR & AXIOM
# DATE: 2025-07-26
# === CHANGELOG ===
# v1.0 — 2025-07-26 — Стартовая версия генератора (ядро, шаблоны, CLI, presets).
# =======================

"""
generate_svg.py — основной модуль генерации SVG для AXIOM SYSTEM.
— Использует svg-шаблоны (templates/*.svg.j2) и параметры (CLI/json) для создания визуальных элементов в style/.
— Ядро расширяемо, готово к интеграции в будущий GUI/панель.
"""

import os
import argparse
import json

class AxiomSVGGenerator:
    def __init__(self, templates_dir="templates", style_dir="style"):
        self.templates_dir = templates_dir
        self.style_dir = style_dir

    def render(self, template_name, params, output_name):
        # Загрузка шаблона
        tpl_path = os.path.join(self.templates_dir, template_name)
        if not os.path.exists(tpl_path):
            raise FileNotFoundError(f"Template {template_name} not found in {self.templates_dir}")
        with open(tpl_path, encoding="utf-8") as f:
            template = f.read()
        svg_code = template.format(**params)
        out_path = os.path.join(self.style_dir, output_name)
        with open(out_path, "w", encoding="utf-8") as out:
            out.write(svg_code)
        print(f"SVG создан: {out_path}")
        return out_path

    def list_templates(self):
        # Вывод доступных шаблонов
        return [f for f in os.listdir(self.templates_dir) if f.endswith('.svg.j2')]

    def load_presets(self, presets_file="svg_presets.json"):
        # (опционально) загрузка готовых профилей
        p_path = os.path.join(self.templates_dir, presets_file)
        if os.path.exists(p_path):
            with open(p_path, encoding="utf-8") as f:
                return json.load(f)
        return {}

# ==== CLI ====
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AXIOM SVG GENERATOR")
    parser.add_argument("--template", "-t", type=str, required=False, help="Название шаблона (пример: core.svg.j2)")
    parser.add_argument("--params", "-p", type=str, help="Параметры в формате JSON (пример: '{\"color\": \"#ae51ff\", \"size\": 56}')")
    parser.add_argument("--out", "-o", type=str, help="Имя svg-файла на выходе (например, axiom_core.svg)")
    parser.add_argument("--preset", type=str, help="Имя профиля из svg_presets.json (пример: VIKTOR_CORE)")
    parser.add_argument("--list", action="store_true", help="Показать все шаблоны")
    args = parser.parse_args()

    gen = AxiomSVGGenerator(
        templates_dir="templates",
        style_dir="style"
    )

    if args.list:
        print("Доступные шаблоны:")
        for t in gen.list_templates():
            print(f" - {t}")
        exit(0)

    # Параметры по preset'у (если выбран)
    params = {}
    if args.preset:
        presets = gen.load_presets()
        preset_data = presets.get("presets", {}).get(args.preset)
        if not preset_data:
            print(f"Профиль {args.preset} не найден в svg_presets.json")
            exit(1)
        params.update(preset_data)

    # Параметры через CLI (приоритетны)
    if args.params:
        params.update(json.loads(args.params))

    # Проверка обязательных
    if not args.template or not args.out or not params:
        print("❗ Укажи шаблон --template, выходной файл --out и параметры (через --params и/или --preset)!")
        exit(1)

    gen.render(args.template, params, args.out)
