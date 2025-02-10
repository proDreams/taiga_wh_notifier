# Руководство для участников проекта

## Начало работы

### Требования
- Python 3.12+
- uv (менеджер зависимостей)

### Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/proDreams/taiga_wh_notifier.git && cd taiga_wh_notifier
```
2. Установите зависимости:
```bash
uv sync
```
3. Настройте pre-commit:
```bash
uv run pre-commit install
```

## Процесс разработки

### Выбор задачи
- Выберите задачу из [списка Issues](https://github.com/proDreams/taiga_wh_notifier/issues)  или из [списка задач проекта](https://tasks.pressanybutton.ru/project/taiga-webhook-telegram-notifier/timeline)
- Убедитесь, что задача не назначена другому разработчику

### Ветвление
Создайте ветку по шаблону:
`фамилия/краткое_описание_задачи` или `фамилия/номер_задачи`

Примеры:
```bash
git checkout -b ivanov/add_payment_webhook

git checkout -b ivanov/task_42
```

### Коммиты
Используйте [Conventional Commits](https://www.conventionalcommits.org/):
```bash
git commit -m "feat: add payment webhook handler"
```

Допустимые типы коммитов:
- `feat`: Новая функциональность
- `fix`: Исправление ошибки
- `docs`: Изменения документации
- `refactor`: Рефакторинг кода
- `test`: Тесты
- `chore`: Обновление зависимостей

## Code Review

### Требования к Pull Request
1. Ссылка на связанную задачу в описании
2. Полное описание изменений
3. Успешное прохождение CI/CD
4. Соответствие стилю кода (проверено pre-commit)

Пример оформления PR:
```markdown
## Описание изменений- Добавлен обработчик вебхука для платежей
- Обновлена документация API

Связанная задача: #123
```

### Процесс ревью
1. Назначьте ревьюверов из команды
2. Отвечайте на комментарии прямо в PR
3. Исправления вносите в ту же ветку
4. После 2 аппрувов - мердж в main

## Стиль кода

Следуйте [РУКОВОДСТВУ ПО СТИЛЮ КОДА](STYLEGUIDE-RU.md).

Основные правила:
- Типизация для всех публичных методов
- Документация в формате Google-style docstrings
- Форматирование через ruff и isort

Перед коммитом:
```bash
uv run pre-commit run -a
```

## Помощь

Если вы застряли:
1. Поищите в закрытых Issues
2. Напишите в [Telegram-чат проекта](https://t.me/+Li2vbxfWo0Q4ZDk6)
3. Создайте Issue с меткой `question`

---

Благодарим за ваш вклад! Каждая ваша правка помогает сделать проект лучше.
