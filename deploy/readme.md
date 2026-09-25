# Деплой на сервер

Как поднять бота так, чтобы он работал круглосуточно и не зависел от твоего
компьютера. Подходит любой сервер на Ubuntu 22.04 / 24.04.

## Коротко

На сервере, в папке проекта:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip git

git clone https://github.com/666usr/tg-orders-bot.git
cd tg-orders-bot

nano .env          # впиши BOT_TOKEN и ADMIN_IDS (BOT_PROXY на сервере не нужен)
# сохранить: Ctrl+O, Enter, Ctrl+X

bash deploy/install.sh
```

Скрипт создаст виртуальное окружение, поставит зависимости и настроит
systemd-сервис `tg-orders-bot` с автозапуском и автоперезапуском.

## Полезные команды

```bash
sudo systemctl status tg-orders-bot     # текущий статус
sudo journalctl -u tg-orders-bot -f     # смотреть логи в реальном времени
sudo systemctl restart tg-orders-bot    # перезапустить
sudo systemctl stop tg-orders-bot       # остановить
```

## Обновление кода после изменений

```bash
git pull
sudo systemctl restart tg-orders-bot
```

## Важно

- **`.env` на сервере создаётся вручную** и в git не хранится. Токен не коммитить.
- **`BOT_PROXY` на сервере обычно не нужен** — у серверов, как правило, есть
  прямой доступ к Telegram. Если провайдер блокирует — добавь прокси как локально.
- **Порт открывать не нужно.** Бот работает через исходящие соединения
  (long polling), входящие порты ему не требуются.
- **Файл базы `orders.db`** создаётся рядом с ботом и живёт на диске сервера.
