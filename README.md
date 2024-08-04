# ArtifactMMO Game Bot

## Установка
1. Склонируйте репозиторий:

```bash
git clone https://github.com/ваше_имя_пользователя/artifactsmmo-bot.git
cd artifactsmmo-bot
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте файл .env в корневой директории и добавьте следующие переменные:

```
TOKEN="ваш_api_ключ"
CHARACTER_NAME="имя_вашего_персонажа"
```

## Использование

1. Поместите сценарии команд в файл input.txt или другой текстовый файл. Пример сценария:

```txt
repeat 2
    move 0 0
    move 1 1
end
move 0 1
```
2. Запустите бота:

```bash
python main.py
```

3. Бот выполнит команды, описанные в сценарии.
