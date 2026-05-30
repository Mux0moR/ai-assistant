# GoogyAIPro - Local RAG AI Assistant

GoogyAIPro — это локальный ИИ-ассистент с веб-интерфейсом, работающий по технологии RAG (Retrieval-Augmented Generation). Он позволяет искать информацию в ваших собственных документах (PDF, TXT, MD) и отвечать на вопросы, используя мощь локальных моделей через Ollama.

![GoogyAIPro Landing](https://cdni.iconscout.com/illustration/premium/thumb/robot-assistant-illustration-download-in-svg-png-gif-file-formats--artificial-intelligence-chatbot-pack-science-technology-illustrations-4131561.png)

## Особенности
- **Полная локальность:** Ваши данные не покидают ваш компьютер.
- **RAG (Retrieval-Augmented Generation):** Ответы строятся на основе ваших документов.
- **Веб-виджет:** Удобный интерфейс "капли", который раскрывается в полноценный чат.
- **Быстрая разработка:** Построен на FastAPI и uv.
- **Векторная база данных:** Использует ChromaDB для эффективного поиска по смыслам.

## Стек технологий
- **Backend:** Python, FastAPI
- **LLM Engine:** [Ollama](https://ollama.com/) (Gemma, Llama)
- **Vector DB:** [ChromaDB](https://www.trychroma.com/)
- **Embeddings:** `nomic-embed-text`
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Package Manager:** [uv](https://github.com/astral-sh/uv)

## Установка и запуск

### 1. Предварительные требования
Установите [Ollama](https://ollama.com/) и загрузите необходимые модели:
```bash
ollama pull gemma4:e4b
ollama pull nomic-embed-text
```

### 2. Клонирование репозитория
```bash
git clone https://github.com/ваш-аккаунт/googy-ai-pro.git
cd googy-ai-pro
```

### 3. Установка зависимостей
Используйте `uv` для быстрой установки:
```bash
uv sync
```

### 4. Настройка окружения
Создайте файл `.env` в корневой директории:
```env
MODEL_NAME=gemma4:e4b
EMBED_MODEL=nomic-embed-text
KNOWLEDGE_DIR=knowledge
DB_DIR=data
```

### 5. Добавление знаний
Поместите ваши документы (PDF, TXT или MD) в папку `knowledge/`.

### 6. Запуск
```bash
uv run main.py
```
Откройте [http://localhost:8000](http://localhost:8000) в вашем браузере.

## Структура проекта
- `src/main.py` — основной сервер FastAPI и логика RAG.
- `static/` — фронтенд (HTML, CSS, JS).
- `knowledge/` — папка для ваших документов.
- `data/` — локальное хранилище ChromaDB.

## Лицензия
Этот проект распространяется под лицензией MIT.
