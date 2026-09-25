# Образ для запуска бота на платформе (Railway, Koyeb, Render и др.)
# или в обычном Docker.
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала зависимости - так слой кэшируется и сборка быстрее.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем код проекта.
COPY . .

# Токен и id администратора задаются переменными окружения платформы
# (BOT_TOKEN, ADMIN_IDS). Файл .env в образ не попадает.
CMD ["python", "bot.py"]
