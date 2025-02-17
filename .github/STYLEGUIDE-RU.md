# Руководство по стилю разработки

## 1. Структура проекта
### 1.1 Организация модулей и пакетов
- Каждый самостоятельный элемент выделяется в отдельный модуль (`.py` файл)
- Группы связанных модулей объединяются в пакеты (директории с `__init__.py`)
- Примеры пакетов: `database`, `payment_system`, `utils`

## 2. Система именования
### 2.1 Пакеты
Формат: `[подсистема]_[контекст]` (опционально через нижнее подчеркивание)
Примеры:
```plaintext
menu_general  # с указанием подсистемы
s3
database
payment_system
```

### 2.2 Модули
Формат: `[функциональное_назначение].py`
Примеры:
```python
handlers.py
schemas.py
services.py
```

### 2.3 Компоненты
Формат: `[контекст]_[тип_компонента]`
Примеры:
```python
# Роутеры
@menu_general_router.message()

# Обработчики
def send_welcome_handler()

# Клавиатуры
welcome_inline_kb
general_menu_reply_kb
```

## 3. Документирование кода
### 3.1 Однострочные комментарии
- Размещаются над комментируемым кодом
- Используются для кратких пояснений и TODO-заметок

Пример:
```python
# Инициализация кэша с TTL 300 секунд
cache = LRUCache(ttl=300)

# TODO: Добавить обработку исключений
```

### 3.2 Многострочная документация (Docstrings)
- Оформляется в тройных кавычках
- Размещается сразу после объявления объекта
- Поддерживает автодокументирование и IDE-подсказки

Структура:
1. Краткое назначение
2. Логика работы
3. Параметры
4. Возвращаемые значения

Пример:
```python
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Вычисляет евклидово расстояние между двумя точками.

    :param x1: Координата X первой точки
    :param y1: Координата Y первой точки
    :param x2: Координата X второй точки
    :param y2: Координата Y второй точки
    :return: Расстояние между точками с точностью до 2 знаков
    """
    return round(((x2-x1)**2 + (y2-y1)**2)**0.5, 2)
```

## 4. Работа с Pydantic-схемами
### 4.1 Организация
- Модули именуются как `[контекст]_schemas.py`
- Схемы группируются по направлениям данных

### 4.2 Конвенции именования
- CamelCase с суффиксом направления данных
- Примеры:
  - `UserCreateInput`
  - `PaymentDetailsOutput`
  - `ProfileUpdateRequest`

### 4.3 Типизация и связи
- Обязательное указание типов полей
- Для связей схем используется отложенный импорт

Пример:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .payment_schemas import PaymentSchemaOutput

class OrderSchemaOutput(BaseModel):
    total: float
    payment_details: "PaymentSchemaOutput"
```

## 5. Стилистика кода
### 5.1 Автоматизированные проверки
Используется pre-commit с набором линтеров:
```bash
# Установка
uv run pre-commit install

# Запуск проверок
uv run pre-commit run -a
```

### 5.2 Основные правила
- Соответствие PEP8
- Максимальная длина строки 120 символов
- Использование type hints для всех публичных методов
- Автоматическое форматирование через ruff и isort

## 6. Работа с Git
### 6.1 Ветвление
Формат имени ветки: `фамилия/название_задачи`  или `фамилия/номер_задачи`
Пример: `ivanov/payment_integration` или `ivanov/task_42`

### 6.2 Коммиты
Формат: `тип: описание` (Conventional Commits)

| Тип      | Назначение                                     |
|----------|------------------------------------------------|
| feat     | Новая функциональность                        |
| fix      | Исправление ошибок                            |
| docs     | Изменения документации                        |
| style    | Форматирование кода                           |
| refactor | Рефакторинг без изменения функционала         |
| test     | Изменения в тестах                            |
| chore    | Обновление зависимостей/конфигураций          |

Пример: `feat: add user registration endpoint`

### 6.3 Процесс Code Review
1. Создать ветку от `main`
2. Выполнить задачу и запушить изменения
3. Создать Pull Request
4. Пройти ревью кода
5. Внести правки (при необходимости)
6. Выполнить мердж после аппрува

---

Данное руководство обязательно к соблюдению всеми участниками проекта. Предложения по улучшению приветствуются через Issue в репозитории.
