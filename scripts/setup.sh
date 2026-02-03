#!/bin/bash

# ============================================
# Setup Script для BrokenSite Hunter
# Первоначальная настройка окружения
# ============================================

echo "🚀 BrokenSite Hunter - Setup Script"
echo "===================================="

# Проверка Python версии
echo "📌 Проверка Python..."
python_version=$(python --version 2>&1)
if [[ $python_version == *"3.11"* ]] || [[ $python_version == *"3.12"* ]]; then
    echo "✅ Python version: $python_version"
else
    echo "⚠️  Требуется Python 3.11+. Найдено: $python_version"
    exit 1
fi

# Создание виртуального окружения
echo ""
echo "📌 Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "ℹ️  Виртуальное окружение уже существует"
fi

# Активация виртуального окружения
echo ""
echo "📌 Активация виртуального окружения..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Установка зависимостей
echo ""
echo "📌 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Копирование .env
echo ""
echo "📌 Настройка переменных окружения..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Создан .env файл из .env.example"
    echo "⚠️  ВАЖНО: Отредактируйте .env и добавьте API ключи!"
else
    echo "ℹ️  .env файл уже существует"
fi

# Создание директорий
echo ""
echo "📌 Создание директорий для данных..."
mkdir -p exports logs

# Инициализация базы данных
echo ""
echo "📌 Инициализация базы данных..."
python -c "from app.database import init_db; init_db()"
echo "✅ База данных инициализирована (SQLite)"

echo ""
echo "✅ Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте .env и добавьте ваши API ключи (как минимум GOOGLE_PLACES_API_KEY)"
echo "2. Запустите приложение: streamlit run app/main.py"
echo "3. Откройте в браузере: http://localhost:8501"
echo ""
echo "📖 Документация: docs/README.md"
echo "🗺️  Roadmap: docs/ROADMAP.md"
