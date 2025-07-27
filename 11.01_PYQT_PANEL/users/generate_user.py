# === AXIOM_PY_HEADER ===
# FILE: generate_user.py
# TITLE: USER HASH GENERATOR
# VERSION: v0.1
# STATUS: DRAFT
# ZONE: [11_SYSTEM_INTERFACE/11.01_PYQT_PANEL/users]
# COMMENT: Утилита для генерации SHA256-хеша пароля и добавления пользователя в auth.json.
# AUTHOR: CREATOR & AXIOM
# DATE: 2025-07-26
# === CHANGELOG ===
# v0.1 — 2025-07-26 — Инициализация файла, генерация хеша, создание auth.json, добавление пользователя.
# =======================

"""
generate_user.py — консольный скрипт для добавления нового пользователя в систему авторизации AXIOM PANEL.
- Запрашивает логин и пароль (скрыто)
- Генерирует SHA256-хеш пароля
- Добавляет пользователя в users/auth.json (создаёт файл, если не существует)
- Безопасно работает только внутри users/ (и не должен уходить в git!)
"""

import hashlib
import json
import os
import getpass

AUTH_FILE = os.path.join(os.path.dirname(__file__), "auth.json")

def main():
    print("=== AXIOM USER GENERATOR ===")
    login = input("Введите логин: ").strip()
    password = getpass.getpass("Введите пароль: ").strip()
    hash_pw = hashlib.sha256(password.encode()).hexdigest()
    print(f"\nSHA256-хеш пароля: {hash_pw}\n")

    # Загружаем или создаём файл auth.json
    users = []
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            try:
                data = json.load(f)
                users = data.get("users", [])
            except Exception:
                print("Ошибка чтения auth.json. Перезаписываем файл.")
                users = []
    # Проверяем, есть ли уже такой пользователь
    for user in users:
        if user["login"] == login:
            print("Пользователь с таким логином уже существует! Обновляем пароль...")
            user["password_hash"] = hash_pw
            break
    else:
        users.append({"login": login, "password_hash": hash_pw})

    with open(AUTH_FILE, "w") as f:
        json.dump({"users": users}, f, indent=2, ensure_ascii=False)

    print(f"Пользователь '{login}' успешно добавлен/обновлён в auth.json.")

if __name__ == "__main__":
    main()
