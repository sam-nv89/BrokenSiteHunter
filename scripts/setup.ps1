# ============================================
# Setup Script для Windows (PowerShell)
# Первоначальная настройка окружения
# ============================================

Write-Host "🚀 BrokenSite Hunter - Setup Script" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Проверка Python версии
Write-Host "`n📌 Проверка Python..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "3\.(11|12)") {
    Write-Host "✅ Python version: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "⚠️  Требуется Python 3.11+. Найдено: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Создание виртуального окружения
Write-Host "`n📌 Создание виртуального окружения..." -ForegroundColor Cyan
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✅ Виртуальное окружение создано" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Виртуальное окружение уже существует" -ForegroundColor Yellow
}

# Активация виртуального окружения
Write-Host "`n📌 Активация виртуального окружения..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Установка зависимостей
Write-Host "`n📌 Установка зависимостей..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install -r requirements.txt

# Копирование .env
Write-Host "`n📌 Настройка переменных окружения..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "✅ Создан .env файл из .env.example" -ForegroundColor Green
    Write-Host "⚠️  ВАЖНО: Отредактируйте .env и добавьте API ключи!" -ForegroundColor Yellow
} else {
    Write-Host "ℹ️  .env файл уже существует" -ForegroundColor Yellow
}

# Создание директорий
Write-Host "`n📌 Создание директорий для данных..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path exports, logs | Out-Null

# Инициализация базы данных
Write-Host "`n📌 Инициализация базы данных..." -ForegroundColor Cyan
python -c "from app.database import init_db; init_db()"
Write-Host "✅ База данных инициализирована (SQLite)" -ForegroundColor Green

Write-Host "`n✅ Установка завершена!" -ForegroundColor Green
Write-Host "`n📋 Следующие шаги:" -ForegroundColor Cyan
Write-Host "1. Отредактируйте .env и добавьте ваши API ключи (как минимум GOOGLE_PLACES_API_KEY)"
Write-Host "2. Запустите приложение: streamlit run app/main.py"
Write-Host "3. Откройте в браузере: http://localhost:8501"
Write-Host "`n📖 Документация: docs\README.md"
Write-Host "🗺️  Roadmap: docs\ROADMAP.md"
