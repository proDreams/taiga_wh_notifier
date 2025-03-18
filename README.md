# Napkin Tools: Taigram (Taiga Telegram Notifier)

![GitHub License](https://img.shields.io/github/license/proDreams/reback)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/proDreams/reback/build-release.yml)
[![Code on a Napkin](https://img.shields.io/badge/Telegram-Code_on_a_Napkin-blue)](https://t.me/press_any_button)
[![Notes on a Napkin](https://img.shields.io/badge/Telegram-Notes_on_a_Napkin-blue)](https://t.me/writeanynotes)

## [Русская версия](README-RU.md)

<p align="center">
  <img src=".github/images/logo.png" width="560" alt="Taigram">
</p>

## Table of Contents

1. [About the Project](#about-the-project)
2. [Requirements](#requirements)
3. [Quick Start](#quick-start)
4. [Features](#features)
5. [Technologies](#technologies)
6. [Development](#development)
7. [Code Style](#code-style)
8. [Authors](#authors)
9. [License](#license)
10. [Troubleshooting](#troubleshooting)

## About the Project

*To be added later*

## Requirements

To ensure the project works correctly, you need:

- **Domain Name.** Telegram does not support WebHook connections via an IP address or without an SSL certificate.
- **Telegram Bot Token.** You can create one using [BotFather](https://t.me/BotFather).
- **Telegram Chat ID**:
    - For personal messages from the bot: `1234567`.
    - For a small group: `-1234567`.
    - For a large group/supergroup: `-1001234567`.
    - **Important:**
        - To receive personal messages, you must start a chat with the bot.
        - For groups, you need to add the bot to the group and grant it minimal admin rights to send messages.
- **(Optional) Telegram Chat Thread ID.** Required for sending messages to a specific topic in a supergroup.

## Quick Start

To launch the project, follow these steps:

1. Connect to your server via SSH and create a directory for the project in a convenient location:
    ```bash
    mkdir taigram && cd taigram
    ```
2. Download the configuration file and set up the settings:
    1. Download the file:
        ```bash
        mkdir -p config && wget -O config/settings.yaml https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/config/settings.prod_example.yaml
        ```
    2. Open the file for editing:
       ```bash
       nano config/settings.yaml
       ```
    3. Update the following parameters:
        - `ADMIN_IDS` – specify the main bot administrators as a list using `-`.
        - `ERRORS_CHAT_ID` – enter the chat ID where error messages will be sent.
        - _(Optional)_ `ERRORS_THREAD_ID` – specify the thread ID in a supergroup. Leave it empty if not needed.
        - `WEBHOOK_DOMAIN` – enter your domain name.
        - _(Optional)_ `DEFAULT_LANGUAGE` – set the bot's default interface language.
        - _(Optional/Important)_`TIME_ZONE` - specify your desired time zone. By default, it is `Europe/Moscow`.
        - `TELEGRAM_BOT_TOKEN` – enter the Telegram bot token.
        - `DB_URL` – replace:
            - `twhn_user` with your database username.
            - `twhn_password` with your database password.
        - _(optional)_ `DB_NAME` - specify the database name. By default, it is `taigram`.

        You can find other available configuration parameters in the documentation (coming soon).
    4. Save and exit by pressing `CTRL+S`, then `CTRL+X`.
3. Create a `.env` file, replacing `MONGO_USERNAME` and `MONGO_PASSWORD` with the values set in `settings.yaml`:
    ```bash
    cat <<EOF > .env
    MONGO_USERNAME=twhn_user
    MONGO_PASSWORD=twhn_password
    EOF
    ```
4. Download the `docker-compose` file:
    1. **If you have your own web server (Caddy/NGINX/etc.)**:
        1. Download `docker-compose.yaml`:
            ```bash
            wget -O docker-compose.yaml https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/docker-compose.yaml
            ```
        2. Open the file for editing:
            ```bash
            nano docker-compose.yaml
            ```
        3. Uncomment the `networks` block at the bottom, replacing `<network_name>` with your web server’s network name,
           e.g.:
            ```yaml
             networks:
               default:
                 name: caddy-network
                 external: true
            ```
        4. Save and exit by pressing `CTRL+S`, then `CTRL+X`.
        5. Configure proxying in your web server to `taigram:8000`.
    2. **If you don't have a web server on your server**:
        1. Download `docker-compose.yaml`:
            ```bash
            wget -O docker-compose.yaml https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/docker-compose.caddy.yaml
            ```
        2. Download `Caddyfile`:
            ```bash
            mkdir -p caddy && wget -O Caddyfile https://raw.githubusercontent.com/proDreams/taiga_wh_notifier/refs/heads/main/caddy/Caddyfile
            ```
        3. Open the file for editing:
            ```bash
            nano caddy/Caddyfile
            ```
        4. Replace `example.example.com` with your actual domain name.
        5. Save and exit by pressing `CTRL+S`, then `CTRL+X`.
5. Start the project:
    ```bash
    sudo docker compose up -d
    ```
6. Once the bot starts, you will receive a notification in Telegram:
    ```plaintext
    Service Notification: Bot started. /start
    ```

## Features

*To be added later*

## Technologies

*To be added later*

## Development

See detailed guidelines in [CONTRIBUTING.md](.github/CONTRIBUTING.md).
*Additional sections to be added later*

## Code Style

Refer to [STYLEGUIDE.md](.github/STYLEGUIDE.md).
*Updates to be added later*

## Authors

- **Development**:
    - [Ivan Ashikhmin](https://t.me/proDreams)
    - [Viktor Vangeli](https://t.me/VictorVangeli)
    - [Viktor Korolev](https://t.me/wiltort)
    - [Roman Shabrov](https://t.me/Rororoqadhehrbfn)
- **Design**:
    - [Evgenij Akopyan](https://t.me/SBTesla)

Developed as part of the **"Code on a Napkin"** project.

Website: https://pressanybutton.ru/
Telegram channel: https://t.me/press_any_button

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## **Troubleshooting**

__Will be moved to the documentation later.__

### **Issue:**

MongoDB fails to start with the error: *"Processor without AVX instructions is not supported."*

### **Solution:**

1. Open `docker-compose.yaml` for editing:
    ```bash
    nano docker-compose.yaml
    ```
2. Find and replace the following lines:
    - Change `image: mongo` to `image: ghcr.io/flakybitnet/mongodb-server:7.0.16-fb2`
    - Change `MONGO_INITDB_ROOT_USERNAME: ${MONGO_USERNAME}` to `MONGODB_ROOT_USER: ${MONGO_USERNAME}`
    - Change `MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}` to `MONGODB_ROOT_PASSWORD: ${MONGO_PASSWORD}`

   The final `mongo` service should look like this:
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
3. Save and exit by pressing `CTRL+S`, then `CTRL+X`.
4. Start the project:
    ```bash
    sudo docker compose up -d
    ```
