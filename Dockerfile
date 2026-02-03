FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Chrome для Selenium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Создание директорий для данных
RUN mkdir -p /app/exports /app/logs

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_PORT=8501

# Expose порт для Streamlit
EXPOSE 8501

# Запуск приложения
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
