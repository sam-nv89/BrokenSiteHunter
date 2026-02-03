# BrokenSite Hunter 🎯

**Автономная DaaS-платформа для поиска SME с техническими проблемами на сайтах**

## 🚀 Что это?

BrokenSite Hunter — система для автоматического поиска, анализа и обогащения лидов среди малого и среднего бизнеса в Tier-1 и CIS рынках. Платформа находит компании с критическими техническими проблемами (просроченный SSL, низкая скорость сайта, отсутствие мобильной адаптации) и предоставляет полные контактные данные ЛПР.

## 💡 Основные возможности

- ✅ **Автоматический сбор** бизнес-данных через Google Places API
- ✅ **Email enrichment** через multi-layer стратегию (парсинг сайтов, WHOIS, pattern guessing)
- ✅ **Технический аудит** (SSL, PageSpeed, Mobile responsiveness)
- ✅ **Web GUI** для управления без кода
- ✅ **Экспорт в CSV/Excel** для продажи агентствам

## 🎯 Целевые метрики

- **Доход:** $2000+/месяц
- **Операционные расходы:** $5-10/месяц (VPS)
- **Email покрытие:** 50-70%
- **Автономность:** 24/7 работа

## 🛠️ Технологический стек

- **Backend:** Python 3.11+, Scrapy, Selenium
- **Database:** PostgreSQL / SQLite
- **Web UI:** Streamlit
- **Orchestration:** n8n (self-hosted)
- **Audit Tools:** Google Lighthouse API, SSL Labs API
- **Deploy:** Docker, Docker Compose

## 📦 Установка

### Требования

- Python 3.11 или выше
- PostgreSQL 14+ (или SQLite для разработки)
- Node.js 18+ (для n8n, опционально)
- Docker & Docker Compose (для production)

### Быстрый старт

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Project_5
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте API ключи
```

5. Запустите приложение:
```bash
streamlit run app/main.py
```

## 🔑 Конфигурация

Создайте файл `.env` на основе `.env.example`:

```env
# Google Places API
GOOGLE_PLACES_API_KEY=your_api_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/brokensitehunter
# Или для SQLite:
# DATABASE_URL=sqlite:///./database.db

# Scraping Settings
MAX_REQUESTS_PER_MINUTE=30
USER_AGENT_ROTATION=true

# Email Enrichment
HUNTER_IO_API_KEY=optional_for_premium_features
```

## 📖 Использование

1. Откройте веб-интерфейс (по умолчанию: http://localhost:8501)
2. Введите параметры поиска:
   - **Страна:** например, "Russia"
   - **Город:** например, "Москва"
   - **Ниша:** например, "restaurant"
3. Нажмите "Start" и дождитесь завершения
4. Скачайте CSV-файл с результатами

## 🗂️ Структура проекта

```
Project_5/
├── app/
│   ├── main.py                 # Streamlit GUI
│   ├── config.py               # Конфигурация
│   ├── scrapers/               # Модули скрапинга
│   ├── audit/                  # Модули аудита
│   ├── database/               # ORM модели
│   └── export/                 # Экспорт данных
├── n8n/                        # Workflows для автоматизации
├── scripts/                    # Вспомогательные скрипты
├── docs/                       # Документация
├── tests/                      # Тесты
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 📊 Roadmap

- [x] **Неделя 1-2:** MVP на локальном ПК
- [ ] **Неделя 3-4:** Тестирование и первые продажи
- [ ] **Неделя 5-6:** Деплой на VPS и автоматизация
- [ ] **Неделя 7-8:** Достижение $2000/мес

Подробный roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)

## 📝 Документация

- [Архитектура](docs/ARCHITECTURE.md) — детальное описание системы
- [Журнал разработки](docs/DEV_LOG.md) — история изменений
- [AI Memo](docs/AI_MEMO.md) — переписка с AI, вопросы и решения
- [API Reference](docs/API.md) — документация API (TBD)

## 🤝 Вклад

Проект в стадии MVP. Вклад приветствуется после стабилизации основного функционала.

## 📄 Лицензия

Proprietary — все права защищены.

## 🆘 Поддержка

Для вопросов и предложений создавайте issues в репозитории.

---

**Версия:** 0.1.0-alpha  
**Статус:** MVP в разработке  
**Последнее обновление:** 2026-02-03
