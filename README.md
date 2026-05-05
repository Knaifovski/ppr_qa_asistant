# 📦 Python GUI App (Message Generator)

Это небольшое приложение на Python с графическим интерфейсом.

## 🧠 Что делает приложение

Окно разделено на 2 части:

### 📌 Левая часть — поля ввода

```python
fields = [
    ("packages", "Идентификаторы посылок (через запятую)"),
    ("reception_act_id", "ID акта приемки"),
    ("store_id", "ID ЦФЗ"),
    ("delivery_id", "ID доставки"),
    ("refund_act_id", "ID акта возврата"),
    ("count_of_packages", "Количество посылок (для PICKED_UP) (default = 1)")
]
```

### 🔘 Правая часть — кнопки действий

```python
buttons = [
    ButtonConfig("btn_reception", "NOT_RECEIVED -> PLACEMENT", self.copy_reception),
    ButtonConfig("btn_sorting", "PLACEMENT -> READY", self.copy_placement),
    ButtonConfig("btn_in_delivery", "PICKING -> IN_DELIVERY", self.copy_in_delivery),
    ButtonConfig("btn_delivered", "IN_DELIVERY -> DELIVERED", self.copy_delivered),
    ButtonConfig("btn_picked_up", "READY_FOR_PICKUP -> PICKED_UP", self.copy_picked_up),
    ButtonConfig("btn_return_processing", "PICKED_UP -> PROCESSING", self.copy_processing),
    ButtonConfig("btn_return_ready_for_refund", "PROCESSING -> READY_FOR_REFUND", self.copy_return_ready_for_refund),
    ButtonConfig("btn_return_refunded", "READY_FOR_REFUND -> REFUNDED", self.copy_return_refunded),
]
```

### ⚙️ Как работает логика

* Пользователь заполняет поля слева
* Кнопки справа становятся **активными только при выполнении условий**
* При нажатии кнопки:

  * формируется сообщение
  * оно копируется в буфер обмена
  * готово для вставки в нужный message topic

---

# 🐍 Установка Python

## 🪟 Windows

1. Скачать Python:
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. При установке ОБЯЗАТЕЛЬНО поставить галочку:

```
✔ Add Python to PATH
```

3. Проверка:

```bash
python --version
pip --version
```

---

## 🍎 macOS

Через Homebrew:

```bash
brew install python
```

Проверка:

```bash
python3 --version
pip3 --version
```

---

## 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

Проверка:

```bash
python3 --version
pip3 --version
```

---

# 🧪 Создание виртуального окружения

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

После активации должно появиться:

```
(venv)
```

---

# 📦 Установка зависимостей

```bash
pip install -r requirements.txt
```

---

# 🚀 Запуск приложения

## Вариант 1 — напрямую

```bash
python main.py
```

или

```bash
python3 main.py
```

---

## Вариант 2 — Создать файлик

```bash
pyinstaller --onefile --windowed main.py
```
После исполнения команды создастся папка dist, в которой будет файл для вашей ОС

---

# ❗ Частые ошибки

## ❌ python is not recognized

👉 Python не добавлен в PATH

Решение: переустановить Python и поставить галочку "Add to PATH"

---

## ❌ pip: command not found

```bash
python -m ensurepip --upgrade
```

---

## ❌ ModuleNotFoundError

```bash
pip install -r requirements.txt
```

---

## ❌ venv не активируется (Windows)

```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```
