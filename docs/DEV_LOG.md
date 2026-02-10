# DEV LOG

## 2026-02-10: Agency Research & Outreach Prep
- **Анализ рынка агентств:**
    - Составлен список из 10 агентств (US/Global + RU/CIS) с партнерскими программами.
    - Создан артефакт `docs/AGENCY_CONTACTS.md` с контактами.
- **Подготовка шаблонов:**
    - Разработаны 3 варианта писем (Research, Partnership, Seeking Advice).
    - Финализирован **Option 3** (Seeking Advice) с обезличенным обращением и конкретными цифрами (800+ клиник, ~130 проблемных).
    - Шаблоны сохранены в `docs/AGENCY_OUTREACH_TEMPLATES.md`.
- **Анализ данных:**
    - Проведен скрининг `dentists_results_final_v2.8.xlsx` для получения точных метрик (Geos/Issues Count).


## 2026-02-10: v2.8 Final Testing - ✅ SUCCESS
- **Результат:** Файл `data/dentists_results_final_v2.8.xlsx` сформирован (123KB).
- **Статус:** Аудит реального датасета прошел успешно.
- **Следующие шаги:** Переход к Data Collection (Google Places API).


## 2026-02-06: v2.8 Release - Финальная полировка и защита от WAF
- **Обход WAF и защита:**
    - Обновлен `audit_websites.py`: теперь сайты с кодами `403/405` или капчей помечаются как `⚠️ Protected` (Защищен), а не `❌ Offline`.
    - Восстановлено 7 ценных лидов, которые ранее отбрасывались.
- **Строгая фильтрация Email:**
    - Внедрен черный список для email-заглушек (`example@mysite.com`, `@domain.com`).
    - Добавлен умный фоллбэк на `info@domain.com` только в нужных случаях.
- **Восстановление отчета:**
    - Создан `scripts/apply_styles.py` для восстановления условного форматирования и ширины колонок в финальном Excel-отчете.
- **Вспомогательные утилиты:**
    - `scripts/recheck_offline.py`: Инструмент для глубокой перепроверки "оффлайн" сайтов без полного перезапуска аудита.

## 2026-02-05: v2.7 Release - Строгий поиск Email и HTTPS
- **Умный поиск Email (`audit_websites_helpers.py`):**
    - Парсинг страниц Contact/About через BeautifulSoup.
    - Фильтрация спама и заглушек.
    - Результат: ~80% восстановленных email'ов.
- **Принудительная проверка HTTPS:**
    - Исправлено ложное срабатывание "HTTP Only" для сайтов, блокирующих HTTP запросы.
    - Логика: Если HTTP недоступен, пробуем сразу HTTPS порт 443.
- **Обработка Offline сайтов:**
    - Колонки Mobile, Design, Security теперь показывают `N/A`, если сайт недоступен.

### **Tests**
- Ran integration test on 50 sites (`data/dentists_results_test_50.xlsx`).
- All systems functioning correctly.
 - BrokenSite Hunter

Все изменения записываются в **обратном хронологическом порядке** (новые сверху).

---

## 2026-02-05: v2.4 - Deduplication & Visual Enhancements

### Новые фичи
1. **Интеллектуальная Дедупликация (Deduplication)**
   - Создан модуль `audit_deduplication.py`
   - Логика: группировка по **Domain** (netloc), объединение конфликтующих значений через `\n`
   - Объединяет разные страницы одного бизнеса (напр., `/location1` и `/location2`)
   - Строки без Website сохраняются с warning
   - Интеграция перед началом аудита

   - Интеграция перед началом аудита
   
2. **Исправление SSL Audit (v2.5)**
   - **Problem:** Many sites flagged as "SSL Invalid" despite being accessible securely.
   - **Cause:** `requests` library uses a limited CA bundle; external APIs were timing out.
   - **Solution:** Implemented `check_ssl_local` using Python's `ssl` module to verify certificates against the **System Trust Store** (like a browser).
   - **Result:** Accurate SSL validation for 11/12 previously failed sites.

3. **Исправление Mobile Audit (Critical)**
   - Улучшена логика обнаружения `viewport` meta tag (regex)
   - Исправлена ошибка кодировки (Brotli), приводившая к ложноотрицательным результатам
   - Приоритет `viewport` тега как гарантии мобильной адаптивности
   
3. **SEO Audit (v2.6) - NEW!**
   - Добавлена проверка Title, Description, H1, OG Image
   - Новая колонка `🔍 SEO` (Optimized / Basic / Missing)
   - Интеграция деталей (например, "Missing Title") в Technical Notes
   - Цветовая подсветка для SEO статусов

4. **Цветовая Подсветка Technical Notes**
   - Реализована severity-based подсветка ячеек
   - 🔴 **CRITICAL:** HTTP only, Timeout, Flash
   - 🟠 **HIGH:** SSL issues, Mobile issues, Old jQuery
   - 🟡 **MEDIUM:** Slow loading, Outdated design
   - 🟢 **OK:** All checks passed

### Изменения в коде
- `scripts/audit_websites.py`: Интеграция `deduplicate_data` и `get_technical_notes_severity`
- `scripts/audit_deduplication.py`: Новый файл с логикой слияния строк

### Результат
- Тестовый файл: `data/dentists_test_20_results_v2.4_final.xlsx`
- Успешная проверка на 20 сайтах


## 2026-02-05: v2.3 FINAL - Concise English Technical Notes

### Изменения
1. **Technical Notes - краткий формат (3-5 строк)**
   - Полностью переписана функция `generate_technical_notes()`
   - Сокращено с 20-30 строк до максимум 5 строк
   - Приоритизация критичных проблем
   - Только ключевая информация

2. **Язык: Английский**
   - Все Technical Notes строго на английском языке
   - Примеры: "HTTP only (no encryption)", "Adobe Flash detected - broken since 2020"

3. **Директория результатов**
   - Возвращено сохранение в `data/` вместо `output/`
   - Файл: `data/dentists_test_20_results_v2.3.xlsx`

### Код
- Файл: `scripts/audit_websites.py:generate_technical_notes()` (строки 319-415)
- Размер функции: ~100 строк (было 200+)

### Примеры Technical Notes

**Timeout:**
```
⏱️ Site unreachable: Server timeout (>15s)
Check hosting or server overload
```

**HTTP + Mobile:**
```
❌ HTTP only (no encryption)
Google marks as 'Not Secure' - critical security issue
📱 No mobile version: missing viewport tag
```

**Flash:**
```
🎨 Adobe Flash detected - broken since 2020
```

**Outdated jQuery:**
```
🎨 Outdated: jQuery 1.8.3 (2006-2013)
📱 No mobile version: missing viewport tag
```

### Тестирование
- ✅ Аудит 20 сайтов успешно выполнен
- ✅ Technical Notes краткие и информативные
- ✅ Английский язык
- ✅ Excel форматирование работает (ширина 60, перенос текста)

### Результаты
- **Файл:** `data/dentists_test_20_results_v2.3.xlsx`
- **Статистика:** 17 CRITICAL, 3 HIGH, 4 HOT LEADS
- **Колонка 💬 Technical Notes:** Заполнение 2-5 строк на сайт

---

## 2026-02-05: v2.3 - Multi-Step Verification + Technical Notes

### Цель
Исправить багфикс для mintdds.com (Timeout → HTTP Only) и добавить персонализированные технические комментарии.

### Изменения
1. **Многоступенчатая проверка HTTPS/SSL**
   - Level 1: Локальные проверки (URL, HSTS, HTML canonical)
   - Level 2: External API (ssl-checker.io)
   - Level 3: Cross-validation
   - Код: `scripts/audit_websites_helpers.py`

2. **Многоступенчатая проверка Mobile**
   - Проверка viewport, media queries, responsive frameworks
   - Детализация причин (missing viewport, no media queries)

3. **Персонализированные Technical Notes**
   - Функция `generate_technical_notes()` (200+ строк)
   - Конкретные версии библиотек (jQuery 1.8.3)
   - Найденные теги (`<meta name="viewport">`)
   - Метрики времени (timeout >15s, load time)

4. **Excel Formatting**
   - Колонка `💬 Technical Notes`
   - Фиксированная ширина: 60 символов
   - Автоматический перенос текста
   - Top-left выравнивание

### Тестирование
- Протестировано на 20 сайтах
- mintdds.com теперь определяется как HTTPS ✅
- Методы проверки отображаются в консоли

### Файлы
- `scripts/audit_websites.py` - основной скрипт
- `scripts/audit_websites_helpers.py` - helper функции (NEW)
- `data/dentists_test_20_results_v2.3.xlsx` - результаты

---

## 2026-02-05: v2.2 - HTTP 403 Handling

### Изменения
1. HTTP 403 теперь обрабатывается как "Protected" (сайт работает)
2. Улучшен User-Agent для обхода WAF
3. Timeout увеличен до 15 секунд

### Тестирование
- Протестировано на 20 сайтах
- Сравнение v2.1 vs v2.2
- Создан скрипт `compare_results.py`

### Результаты
- ✅ 3 сайта с 403 корректно классифицируются
- ✅ Timeouts обрабатываются правильно
- ✅ Lead Quality классификация точнее

---

## 2026-02-04: v2.1 - Initial Release

### Функционал
- Проверка HTTPS/SSL
- Проверка мобильной версии
- Проверка устаревшего дизайна
- Excel форматирование
- Lead Quality классификация

### Файлы
- `scripts/audit_websites.py`
- `data/dentists_test_20.xlsx` (тестовые данные)
