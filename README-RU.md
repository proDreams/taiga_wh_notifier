# Napkin Tools: Taigram (Taiga Telegram Notifier)

![GitHub License](https://img.shields.io/github/license/proDreams/reback)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/proDreams/reback/build-release.yml)
[![Код на салфетке](https://img.shields.io/badge/Telegram-Код_на_салфетке-blue)](https://t.me/press_any_button)
[![Заметки на салфетке](https://img.shields.io/badge/Telegram-Заметки_на_салфетке-blue)](https://t.me/writeanynotes)

<p align="center">
  <img src=".github/images/logo.png" width="560" alt="Taigram">
</p>

## Оглавление

1. [О проекте](#о-проекте)
2. [Требования](#требования)
3. [Быстрый старт](#быстрый-старт)
4. [Функционал](#функционал)
5. [Технологии](#технологии)
6. [Разработка](#разработка)
7. [Стиль кода](#стиль-кода)
8. [Авторы](#авторы)
9. [Лицензия](#лицензия)
10. [Решение проблем](#решение-проблем)

## О проекте

*Будет добавлено позже*

## Требования

Для корректной работы проекта, необходимо:

- **Доменное имя.** Telegram не поддерживает подключение WebHook по IP-адресу и без SSL-сертификата.
- **Telegram Bot Token.** Его можно создать с помощью [BotFather](https://t.me/BotFather).
- **Telegram Chat ID**:
    - Для личных сообщений от бота: `1234567`.
    - Для небольшой группы: `-1234567`
    - Для большой группы/супергруппы: `-1001234567`
    - **Важно:**
        - Для личных сообщений необходимо начать диалог с ботом.
        - Для групп необходимо добавить бота в группу и дать ему минимальные права администратора, чтобы он смог
          отправлять сообщения.
- **(Необязательно) Telegram Chat Thread ID**. Необходим для отправки сообщений в определённую тему в супергруппе.

## Быстрый старт

Для того чтобы запустить проект, достаточно выполнить несколько шагов:

1. Подключитесь по SSH к серверу и в удобном месте создайте директорию для проекта:
    ```bash
    mkdir taigram && cd taigram
    ```
2. Скачайте конфигурационный файл и пропишите настройки:
    1. Скачайте файл:
        ```bash
        mkdir -p config && wget -O config/settings.yaml https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/config/settings.prod_example.yaml
        ```
    2. Откройте файл для редактирования:
       ```bash
       nano config/settings.yaml
       ```
    3. Замените следующие параметры:
        - `ADMIN_IDS` - пропишите через `-` список главных администраторов бота.
        - `ERRORS_CHAT_ID` - пропишите идентификатор чата, в который будут отправляться сообщения об ошибках.
        - _(необязательно)_ `ERRORS_THREAD_ID` - пропишите идентификатор темы в супергруппе, если не требуется, оставьте
          пустым.
        - `WEBHOOK_DOMAIN` - пропишите доменное имя.
        - _(необязательно)_ `DEFAULT_LANGUAGE` - измените язык интерфейса бота по умолчанию.
       - _(необязательно/Важно)_`TIME_ZONE` - пропишите желаемую временную зону. По умолчанию `Europe/Moscow`.
        - `TELEGRAM_BOT_TOKEN` - пропишите токен Telegram-бота.
        - `DB_URL` - замените:
            - `twhn_user` - на собственное имя пользователя БД.
            - `twhn_password` - на собственный пароль БД.
        - _(необязательно)_ `DB_NAME` - пропишите имя базы данных. По умолчанию `taigram`.

        С другими доступными параметрами конфигурации, можно ознакомиться в документации (скоро будет).
    4. Сохраните и выйдите, нажав `CTRL+S`, затем `CTRL+X`.
3. Создайте `.env-файл`, заменив значения `MONGO_USERNAME` и `MONGO_PASSWORD` на прописанные ранее в `settings.yaml`:
    ```bash
    cat <<EOF > .env
    MONGO_USERNAME=twhn_user
    MONGO_PASSWORD=twhn_password
    EOF
    ```
4. Скачайте `docker-compose-файл`:
    1. Если у вас настроен **свой веб-сервер (Caddy/NGINX/etc..)**:
        1. Скачайте `docker-compose.yaml`:
            ```bash
            wget -O docker-compose.yaml https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/docker-compose.yaml
            ```
        2. Откройте файл для редактирования:
            ```bash
            nano docker-compose.yaml
            ```
        3. Раскомментируйте в самом конце блок `networks`, заменив `<network_name>` на имя сети вашего веб-сервера,
           например:
            ```yaml
             networks:
               default:
                 name: caddy-network
                 external: true
            ```
        4. Сохраните и выйдите, нажав `CTRL+S`, затем `CTRL+X`.
    2. Если на сервере нет своего веб-сервера:
        1. Скачайте `docker-compose.yaml`:
            ```bash
            wget -O docker-compose.yaml https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/docker-compose.caddy.yaml
            ```
        2. Скачайте `Caddyfile`:
            ```bash
            mkdir -p caddy && wget -O Caddyfile https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/caddy/Caddyfile
            ```
        3. Откройте файл для редактирования
            ```bash
            nano caddy/Caddyfile
            ```
        4. Замените `example.example.com` на ваше доменное имя.
        5. Сохраните и выйдите, нажав `CTRL+S`, затем `CTRL+X`.
5. Запустите проект:
    ```bash
    sudo docker compose up -d
    ```
6. Когда бот запустится, вы получите уведомление в Telegram:
    ```plaintext
    Service Notification: Bot started. /start
    ```

## Функционал

*Будет добавлено позже*

## Технологии

*Будет добавлено позже*

## Разработка

Смотри подробное руководство в [CONTRIBUTING-RU.md](.github/CONTRIBUTING-RU.md).
*Дополнения будут добавлены позже*

## Стиль кода

Смотри [STYLEGUIDE-RU.md](.github/STYLEGUIDE-RU.md)
*Дополнения будут добавлены позже*

## Авторы

- **Разработка**:
    - [Иван Ашихмин](https://t.me/proDreams)
    - [Виктор Вангели](https://t.me/VictorVangeli)
    - [Виктор Королев](https://t.me/wiltort)
    - [Роман Шабров](https://t.me/Rororoqadhehrbfn)
- **Дизайн**:
    - [Евгений Акопян](https://t.me/SBTesla)

Программа написана в рамках проекта "Код на салфетке":

- Сайт: https://pressanybutton.ru/
- Telegram-канал: https://t.me/press_any_button

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности можно найти в файле [LICENSE](LICENSE).

## Решение проблем

__Позже будет перенесено в документацию__

**Проблема:**
Не запускается MongoDB с ошибкой "не поддерживается процессор без AVX-инструкций"

**Решение:**

1. Открыть `docker-compose.yaml` для редактирования:
    ```bash
    nano docker-compose.yaml
    ```
2. Найти и заменить следующие строки:
    - `image: mongo` на `image: ghcr.io/flakybitnet/mongodb-server:7.0.16-fb2`
    - `MONGO_INITDB_ROOT_USERNAME: ${MONGO_USERNAME}` на `MONGODB_ROOT_USER: ${MONGO_USERNAME}`
    - `MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}` на `MONGODB_ROOT_PASSWORD: ${MONGO_PASSWORD}`

   Итоговый вид сервиса `mongo`:
    ```yaml
    mongo:
      image: ghcr.io/flakybitnet/mongodb-server:7.0.16-fb2
      container_name: taigram_mongo
      restart: always
      environment:
        MONGODB_ROOT_USER: ${MONGO_USERNAME}
        MONGODB_ROOT_PASSWORD: ${MONGO_PASSWORD}
      volumes:
        - taigram_mongo_db:/data/db
      healthcheck:
        test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
        interval: 10s
        timeout: 10s
        retries: 5
    ```
3. Сохраните и выйдите, нажав `CTRL+S`, затем `CTRL+X`.
4. Запустите проект:
    ```bash
    sudo docker compose up -d
    ```
