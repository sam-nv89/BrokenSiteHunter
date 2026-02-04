# 🚀 Инструкция: Публикация на GitHub

## Шаг 1: Создание Репозитория на GitHub

### Вариант A: Через Веб-Интерфейс (Рекомендуется)

1. **Откройте GitHub:**
   - Перейдите на https://github.com
   - Войдите в свой аккаунт

2. **Создайте новый репозиторий:**
   - Нажмите зеленую кнопку **"New"** (или **"+"** → **"New repository"**)
   
3. **Заполните форму:**
   ```
   Repository name: brokensitehunter
   Description: DaaS platform for finding SMEs with technical website issues
   Visibility: ✅ Private (рекомендуется на старте)
   
   ⚠️ НЕ инициализируйте с:
   ❌ README (у нас уже есть)
   ❌ .gitignore (у нас уже есть)
   ❌ License (добавим позже при необходимости)
   ```

4. **Нажмите "Create repository"**

5. **Скопируйте URL репозитория:**
   - Формат: `https://github.com/ваш-username/brokensitehunter.git`
   - Или SSH: `git@github.com:ваш-username/brokensitehunter.git`

---

### Вариант B: Через GitHub CLI (Быстрее, но требует установки)

Если у вас установлен GitHub CLI (`gh`):

```powershell
# Создание приватного репозитория
gh repo create brokensitehunter --private --source=. --remote=origin --push

# Всё готово! Репозиторий создан и код загружен
```

---

## Шаг 2: Связывание Локального Проекта с GitHub

### Команды для PowerShell (Windows)

Откройте PowerShell в директории проекта и выполните:

```powershell
# 1. Перейти в директорию проекта (если не там)
cd d:\Projects\Project_5

# 2. Добавить remote (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/brokensitehunter.git

# 3. Переименовать ветку в main (если используется master)
git branch -M main

# 4. Отправить код на GitHub
git push -u origin main
```

### Если Попросит Авторизацию

#### Вариант 1: HTTPS (Проще)
При первом push Windows запросит авторизацию:
- **Username:** ваш GitHub username
- **Password:** **НЕ пароль от аккаунта**, а **Personal Access Token**

**Как создать токен:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Выберите scopes: `repo` (полный доступ)
4. Скопируйте токен (он показывается только раз!)
5. Используйте его вместо пароля

#### Вариант 2: SSH (Безопаснее)
Если настроен SSH ключ:
```powershell
git remote set-url origin git@github.com:YOUR_USERNAME/brokensitehunter.git
git push -u origin main
```

---

## Шаг 3: Проверка

После успешного push:

1. **Откройте ваш репозиторий:**
   ```
   https://github.com/YOUR_USERNAME/brokensitehunter
   ```

2. **Должны увидеть:**
   - ✅ README.md с описанием проекта
   - ✅ Структуру папок (app/, docs/, scripts/, etc.)
   - ✅ Все файлы из проекта

3. **Проверьте README:**
   - Markdown должен отображаться корректно
   - Ссылки на документацию работают

---

## Шаг 4: Настройка .env (Важно!)

⚠️ **Файл `.env` НЕ загружен на GitHub** (он в `.gitignore`) — это правильно!

**Для других разработчиков:**
1. Клонируют репозиторий
2. Копируют `.env.example` в `.env`
3. Заполняют своими API ключами

---

## Дальнейшая Работа с Git

### Базовые Команды

```powershell
# Проверить статус (какие файлы изменены)
git status

# Добавить все изменения
git add .

# Создать коммит
git commit -m "Описание изменений"

# Отправить на GitHub
git push

# Получить изменения с GitHub
git pull
```

### Workflow для Разработки

```powershell
# 1. Внесли изменения в код
# 2. Проверили что изменилось
git status

# 3. Добавили файлы
git add .

# 4. Коммит с понятным сообщением
git commit -m "feat: реализован Google Maps scraper"

# 5. Отправка на GitHub
git push
```

### Рекомендации по Commit Messages

Используйте **Conventional Commits** формат:

```
feat: новая функция
fix: исправление бага
docs: изменения в документации
refactor: рефакторинг кода
test: добавление тестов
chore: технические изменения (зависимости, конфиг)
```

**Примеры:**
```
feat: добавлен Google Places API scraper
fix: исправлена ошибка SMTP verification
docs: обновлен ROADMAP с новыми метриками
refactor: оптимизирован email enrichment pipeline
```

---

## Готовые Команды (Copy-Paste)

### После Создания Репозитория на GitHub

```powershell
# Замените YOUR_USERNAME на ваш GitHub username
$GITHUB_USERNAME = "YOUR_USERNAME"

git remote add origin "https://github.com/$GITHUB_USERNAME/brokensitehunter.git"
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### Ошибка: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/brokensitehunter.git
```

### Ошибка: "Authentication failed"
- Используйте Personal Access Token вместо пароля
- Или настройте SSH ключ

### Ошибка: "Updates were rejected"
```powershell
# Принудительная отправка (ОСТОРОЖНО: перезаписывает remote)
git push -u origin main --force
```

---

## Следующие Шаги

После загрузки на GitHub:

1. **Настройте GitHub Actions** (опционально):
   - Автоматическое тестирование при push
   - Деплой на VPS

2. **Добавьте Badges в README:**
   ```markdown
   ![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
   ![License](https://img.shields.io/badge/license-Proprietary-red.svg)
   ```

3. **Создайте Issues** для трекинга задач:
   - "Реализовать Google Maps scraper"
   - "Добавить email enrichment"
   - etc.

4. **Branch Protection** (для production):
   - Settings → Branches → Add rule
   - Require pull request reviews
   - Require status checks

---

## Резюме

✅ Локальный Git репозиторий инициализирован  
✅ Первый коммит создан  
⏳ Создайте репозиторий на GitHub (вручную)  
⏳ Выполните команды для push  

**Время до публикации:** 2-3 минуты

---

**Автор:** BrokenSite Hunter Team  
**Дата:** 2026-02-04
