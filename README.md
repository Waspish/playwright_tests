# 🎭 Playwright_tests

Пакет автоматизированных UI-тестов на базе **Playwright** (Python) с интеграцией **Allure** и **GitHub Actions** (ручной запуск с выбором набора тестов).

## 📚 О проекте

Три набора тестов, покрывающих различные сценарии веб-тестирования:

- **`test_advanced.py`** – расширенные UI-сценарии (вкладки, ожидания, hover, drag‑and‑drop, алерты).
- **`test_network.py`** – тестирование сетевого слоя (перехват запросов, модификация ответов, статусы).
- **`test_trainings.py`** – базовые проверки локаторов (роли, текст, CSS, XPath).

Все тесты используют **pytest** и **Playwright**. Инфраструктура для запуска, отчётов и CI/CD уже настроена.

## 🛠 Технологический стек

- **Python** 3.11+
- **pytest** + `pytest-playwright`
- **Playwright** (браузеры Chromium, Firefox, WebKit)
- **Allure** (`allure-pytest`) – наглядные отчёты, скриншоты упавших тестов
- **GitHub Actions** – ручной запуск тестов через `workflow_dispatch`
- **pytest-xdist** – параллельный запуск (опционально)

## 🚀 Локальный запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Waspish/playwright_tests.git
cd playwright_tests
```

### 2. Создайте виртуальное окружение

```bash
python -m venv .venv
```

Активация:

- **Windows**: `.venv\Scripts\activate`
- **Linux/macOS**: `source .venv/bin/activate`

### 3. Установите зависимости

```bash
pip install -r requirements.txt
playwright install
```

### 4. Запустите тесты

```bash
pytest                     # все тесты
pytest -m smoke            # только smoke
pytest -m regression       # только regression
pytest -m extended         # только extended (сетевые сценарии)
```

## 🏷️ Маркеры (pytest.ini)

| Маркер       | Описание                                 |
|--------------|------------------------------------------|
| `smoke`      | Базовые smoke-тесты (основной функционал)|
| `regression` | Regression-тесты (расширенная проверка)  |
| `extended`   | Extended-тесты (сетевые перехваты, API)  |

## 📊 Allure-отчёт

```bash
# Запуск с сохранением данных для Allure
pytest --alluredir=./allure-results

# Генерация и открытие отчёта (требуется Allure Commandline)
allure serve ./allure-results
```

Скриншоты упавших тестов автоматически встраиваются в отчёт.

## ⚙️ GitHub Actions (ручной запуск)

Файл `.github/workflows/run_tests.yml` настроен на **ручной запуск** через интерфейс GitHub.

### Как запустить

1. Перейдите на вкладку **Actions** репозитория.
2. Выберите workflow **Python autotests**.
3. Нажмите **Run workflow** → выберите набор тестов (`smoke`, `regression`, `extended` или `all`).
4. Нажмите **Run workflow** – начнётся выполнение.

### Параметры выбора

| Опция         | Команда                              |
|---------------|--------------------------------------|
| `smoke`       | `pytest -m smoke --alluredir=...`    |
| `regression`  | `pytest -m regression --alluredir=...`|
| `extended`    | `pytest -m extended --alluredir=...` |
| `all`         | `pytest --alluredir=...`             |

### Что делает workflow?

- Устанавливает Python 3.11
- Кэширует зависимости
- Устанавливает `requirements.txt`
- Устанавливает браузеры Playwright (`playwright install --with-deps`)
- Запускает тесты с выбранным маркером
- Сохраняет папку `allure-results` как артефакт сборки (можно скачать)

## 📁 Структура проекта

```
.
├── .github/workflows/run_tests.yml   # CI/CD (ручной запуск)
├── conftest.py                       # Фикстуры (скриншоты при падении)
├── pytest.ini                        # Маркеры
├── requirements.txt                  # Зависимости
├── test_advanced.py                  # Расширенные UI-тесты
├── test_network.py                   # Сетевые тесты
└── test_trainings.py                 # Базовые тесты локаторов
```

## 📝 Примечания

- Скриншоты упавших тестов автоматически встраиваются в Allure-отчёт.
- Некоторые тесты могут быть временно пропущены (`@pytest.mark.skip`).