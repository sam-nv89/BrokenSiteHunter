# 🚀 Инструкция: Как Запустить Audit Скрипт

## ✅ Что Вам Нужно

1. **Python 3.7+** (у вас уже должен быть установлен)
2. **Ваш CSV файл** с дантистами
3. **5-10 минут** времени

---

## 📋 Шаг 1: Установка Зависимостей

Откройте PowerShell в папке проекта и выполните:

```powershell
cd d:\AppDevelopment\Project7
pip install requests pandas openpyxl urllib3
```

**Что это делает:**
- `requests` - для HTTP запросов (проверка сайтов)
- `pandas` - для работы с CSV/Excel файлами
- `openpyxl` - для работы с XLSX (Excel) файлами
- `urllib3` - для SSL проверок

**Время**: 1-2 минуты

---

## 📋 Шаг 2: Подготовка XLSX Файла

1. Скопируйте ваш XLSX файл с дантистами в папку `d:\AppDevelopment\Project7\data\`
2. Переименуйте его в `dentists_raw.xlsx` (или запомните имя файла)

**Пример структуры** (по вашему скриншоту):
```
business_name | address | phone | website | rating | ...
Boston Dental | 123 Main | 617-555 | bostondental.com | 4.5 | ...
```

**Важно:** Скрипт автоматически найдет колонку с website/URL!

---

## 📋 Шаг 3: Запуск Скрипта

### Базовая Проверка (Все включено!)

```powershell
    cd d:\AppDevelopment\Project7
    python scripts\audit_websites.py data\dentists_raw.xlsx data\dentists_audited.xlsx
```

**Что проверяется (автоматически):**
- ✅ **SSL/HTTPS**: Безопасность
- ✅ **Доступность**: Работает ли сайт
- ✅ **⚡ Скорость**: Реальное время загрузки (без API ключа!)
- ✅ **📱 Mobile Friendly**: Адаптивен ли сайт (viewport check)
- ✅ **🎨 Outdated Design**: Устаревшие технологии (Flash, old jQuery, tables)

**Время выполнения**: ~8-10 секунд на сайт (включая паузы для безопасности)
- 10 сайтов = ~1.5 минуты
- 600 сайтов = ~1.5 часа

---

## 📊 Результаты (Новые Колонки)

Файл `dentists_audited.xlsx` будет автоматически отформатирован:

| Колонка | Описание | Особенности |
|---------|----------|-------------|
| **#** | Номер п/п | По центру (USA standard) |
| **Website** | Ссылка | Кликабельная (www.domain.com) |
| **⭐ Customer Rating** | Рейтинг | Цветовое кодирование (🟢>4.5) |
| **🌐 Website Status** | Статус | Online/Offline |
| **🔒 Security** | HTTPS | Valid/Invalid/HTTP Only |
| **⚡ Speed** | Время (сек) | Fast/Average/Slow (реальный замер) |
| **📱 Mobile** | Мобильная версия | ✅ Yes / ❌ No |
| **🎨 Design** | Дизайн | ✅ Modern / ⚠️ Outdated |
| **🎯 Lead Quality** | Качество лида | 🔥 HOT LEAD / 🟠 QUALIFIED |

---

## 🎯 Lead Quality Логика

Скрипт автоматически определяет качество лида:

### 🔥 HOT LEAD
- **Критическая проблема**: Сайт не работает ИЛИ HTTP (небезопасен)
- **Рейтинг**: Хороший (≥ 4.0) -> У бизнеса есть деньги и репутация, но сайт губит продажи.

### 🟠 QUALIFIED
- **Проблемы**:
  - Нет мобильной версии (❌ No)
  - Устаревший дизайн (⚠️ Outdated)
  - Медленная скорость (🔴 Slow)
- **Рейтинг**: Любой

### ⚪ SKIP
- Сайт работает идеально, современный, быстрый.

---

## ⚡ Быстрый Старт (TL;DR)

```powershell
    # 1. Установить зависимости (один раз)
    pip install requests pandas openpyxl urllib3

    # 2. Запустить скрипт
    cd d:\AppDevelopment\Project7
    python scripts\audit_websites.py data\dentists.xlsx data\final_audit.xlsx

    # 3. Открыть результат
    start data\final_audit.xlsx
```

---

## ⚡ Быстрый Старт (TL;DR)

```powershell
# 1. Установить зависимости
pip install requests pandas openpyxl urllib3

# 2. Запустить скрипт
cd d:\AppDevelopment\Project7
python scripts\audit_websites.py data\ваш_файл.xlsx data\результат.xlsx

# 3. Открыть результат в Excel
start data\результат.xlsx
```

---

## ❓ Troubleshooting

### Ошибка: "Module not found"
```powershell
pip install requests pandas urllib3
```

### Ошибка: "File not found"
Проверьте путь к файлу:
```powershell
dir data\dentists_raw.xlsx  # Должен показать файл
```

### Ошибка: "No website column found"
Скрипт автоматически ищет колонки: website, url, site.
Если ваша колонка называется иначе - напишите мне, я адаптирую скрипт.

### Скрипт работает слишком долго
Это нормально! ~2 секунды на сайт (чтобы не заблокировали).
150 сайтов = ~5 минут.

---

## 🎉 Готово!

После выполнения всех шагов у вас будет:
- ✅ CSV с результатами проверки
- ✅ ~100 qualified leads (CRITICAL + HIGH + MEDIUM)
- ✅ Готовность к следующему этапу: Email Enrichment

**Следующий шаг:** Найти email контакты для этих 100 сайтов!
