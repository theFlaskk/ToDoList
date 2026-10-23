# TodoList

Учебный веб-проект на Python и Django: личный список задач с регистрацией, статусами, приоритетами, сроками и поиском.

## Требования
- Python 3.10+
- pip

## Локальный запуск

### Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ и зарегистрируйте аккаунт.

## Проверка тестов
```bash
python manage.py test
```

## Что уже реализовано
- Регистрация, вход и выход.
- Создание, просмотр, изменение и удаление задач.
- Статусы, приоритеты, срок и описание.
- Поиск и фильтр по статусу.
- Защита задач по владельцу.
- Django ORM, CSRF-токены в POST-формах и серверная валидация.

## Структура
- `tasks/models.py` — модели Task и Category.
- `tasks/forms.py` — формы и проверка пользовательского ввода.
- `tasks/services.py` — операции бизнес-уровня.
- `tasks/views.py` — обработчики веб-запросов.
- `tasks/tests.py` — базовые автоматические тесты.
- `templates/` — HTML-шаблоны.
- `static/css/style.css` — стили.

