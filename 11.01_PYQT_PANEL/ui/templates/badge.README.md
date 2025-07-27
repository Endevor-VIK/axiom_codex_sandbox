# badge.svg.j2 — Sci-Fi Badge Template

---

### **Описание**
SVG-шаблон для sci-fi badge (лейблов, статусных маркеров) AXIOM SYSTEM.  
Идеален для оформления статусов, узлов, протоколов, меток и уровней.

---

### **Параметры шаблона**

| Параметр      | Описание                               | Пример        |
|---------------|----------------------------------------|---------------|
| size          | Размер SVG-badge (px)                  | 56            |
| bg            | Цвет фона                              | #181a26       |
| bg_opacity    | Прозрачность фона                      | 0.95          |
| color         | Цвет рамки/акцентов                    | #ae51ff       |
| border_width  | Толщина рамки                          | 2.2           |
| border_opacity| Прозрачность рамки                     | 1             |
| decor_color   | Цвет декоративного shape               | #ae51ff       |
| decor_opacity | Прозрачность shape                     | 0.13          |
| label         | Текст внутри badge                     | Ω             |
| label_color   | Цвет текста                            | #ae51ff       |
| label_size    | Размер шрифта                          | 18            |

---

### **Пример вызова генератора**

```sh
python generate_svg.py -t badge.svg.j2 -p "{\"size\":56,\"bg\":\"#181a26\",\"bg_opacity\":0.95,\"color\":\"#ae51ff\",\"border_width\":2.2,\"border_opacity\":1,\"decor_color\":\"#ae51ff\",\"decor_opacity\":0.13,\"label\":\"Ω\",\"label_color\":\"#ae51ff\",\"label_size\":18}" -o badge_viktor.svg