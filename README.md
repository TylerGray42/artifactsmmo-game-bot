# ArtifactMMO Game Bot

## Установка
1. Склонируйте репозиторий:

```bash
git clone https://github.com/TylerGray42/artifactsmmo-game-bot.git
cd artifactsmmo-game-bot
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

## Поддерживаемые команды
### Основные действия
- `move x y`: Перемещает персонажа к координатам `(x, y)`.
- `fight`: Начинает сражение с монстром, если он находится на текущей позиции персонажа.
- `gathering`: Начинает добычу ресуров, если они находится на текущей позиции персонажа.
- `equip code slot`: Экипирует предмет с кодом `code` на слот `slot`.
- `unequip slot`: Снимает предмет из слота `slot`.
- `crafting code n`: Создаёт `n` предметов с кодом `code`, персонаж должен находиться на карте с мастерской.

### Информация о пресонаже
- `character info`: Основная информация о персонаже (имя, уровень, здоровье, золото, координаты).
- `character skills`: Информация о навыках персонажа.
- `character stats`: Характеристика персонажа (атрибуты и элементы).
- `character equipment`: Экипировка персонажа.
- `character task`: Текущая задача персонажа.
- `character inventory`: Инвентарь персонажа.

### Управление скриптом
- `#` в начале строки - комментарий.
- `repeat n`: Повторяет вложенные команды `n` раз.
- `end`: Завершает блок команд для повторения.

## TODO
- При получении предмета выводить его количество в инвентаре
- Выбор: чтение из файла / чтение из консоли
- Цикл while, для проверки количества предметов в инвентаре
- Добавление другого функционала, присутствующего в API
