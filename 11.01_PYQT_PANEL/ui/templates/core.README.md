# core.svg.j2 — Sci-Fi Core Node Template

---

### **Описание**
Шаблон SVG для генерации ядра (core node) AXIOM SYSTEM.  
Используется для оформления sci-fi узлов, глифов, энергетических центров, badge-элементов.

---

### **Параметры шаблона**

| Параметр      | Описание                               | Пример        |
|---------------|----------------------------------------|---------------|
| size          | Размер SVG-иконки (px)                 | 56            |
| color         | Основной цвет sci-fi ядра               | #ae51ff       |
| bg            | Цвет фона внутри кольца                 | #191726       |
| glow_color    | Цвет внешнего свечения                  | #efb6ff       |
| glow_opacity  | Прозрачность свечения                   | 0.18          |
| blade_opacity | Прозрачность “клинка”                   | 0.13          |
| ring_opacity  | Прозрачность внутреннего кольца         | 0.24          |
| core_color    | Цвет внутреннего ядра                   | #fff6ff       |
| core_opacity  | Прозрачность внутреннего ядра           | 0.88          |
| label         | Текст в центре (опционально)            | Ω             |
| label_color   | Цвет центрального текста                | #ae51ff       |

---

### **Пример вызова генератора**

```sh
python generate_svg.py -t core.svg.j2 -p "{\"size\":56,\"color\":\"#ae51ff\",\"bg\":\"#191726\",\"glow_color\":\"#efb6ff\",\"glow_opacity\":0.18,\"blade_opacity\":0.13,\"ring_opacity\":0.24,\"core_color\":\"#fff6ff\",\"core_opacity\":0.88,\"label\":\"Ω\",\"label_color\":\"#ae51ff\"}" -o axiom_viktor_core.svg
