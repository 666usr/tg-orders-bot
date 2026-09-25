#!/usr/bin/env bash
# Установка Telegram-бота на сервер (Ubuntu / Debian).
#
# Запуск (из корня проекта, где лежит bot.py):
#     bash deploy/install.sh
#
# Скрипт:
#   1. ставит Python и системные пакеты;
#   2. создаёт виртуальное окружение и ставит зависимости;
#   3. создаёт systemd-сервис, чтобы бот работал круглосуточно
#      и сам перезапускался после сбоев или перезагрузки сервера.

set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SERVICE_NAME="tg-orders-bot"
RUN_USER="$(whoami)"

echo "Папка проекта: $APP_DIR"
echo "Пользователь:  $RUN_USER"

# 1. Системные пакеты
echo "==> Устанавливаю системные пакеты"
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

# 2. Виртуальное окружение и зависимости
echo "==> Создаю виртуальное окружение"
python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install --upgrade pip
"$APP_DIR/.venv/bin/pip" install -r "$APP_DIR/requirements.txt"

# 3. Проверка файла .env
if [ ! -f "$APP_DIR/.env" ]; then
  echo "ОШИБКА: нет файла .env."
  echo "Создайте его из .env.example и впишите BOT_TOKEN и ADMIN_IDS."
  exit 1
fi

# 4. systemd-сервис
echo "==> Создаю systemd-сервис"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Telegram orders bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${RUN_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/.venv/bin/python ${APP_DIR}/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "==> Готово. Статус сервиса:"
sudo systemctl --no-pager --full status "$SERVICE_NAME" | head -n 15
