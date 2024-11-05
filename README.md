# Photo-Carousel-Telegram-Bot
Это проект бота Telegram, который позволяет пользователям создавать фотокарусели и делиться ими в группе. Бот позволяет загружать фото, добавлять подписи и просматривать фото с навигацией "Назад" и "Вперед" прямо в группе.

This project is a Telegram bot that allows users to create photo carousels and share them in a group. The bot enables photo uploads, adding captions, and browsing photos with "Back" and "Next" navigation directly in the group.
Оглавление (Table of Contents)

    Описание (Description)
    Функции (Features)
    Установка (Installation)
    Использование (Usage)
    Переменные окружения (Environment Variables)
    Автор (Author)

Описание (Description)

Этот бот позволяет пользователям Telegram создавать и отправлять фотокарусели в группах. Фотокарусель включает в себя фото с подписями и кнопками для навигации. Этот бот написан на Python с использованием библиотеки Aiogram.

This bot allows Telegram users to create and share photo carousels in groups. The carousel includes photos with captions and navigation buttons. The bot is written in Python using the Aiogram library.
Функции (Features)

    Поддержка загрузки до 10 фотографий с подписями.
    Навигация по карусели с кнопками "Назад" и "Вперед".
    Возможность завершить загрузку фото и отправить карусель в группу.
    Хранение фото и подписей по пользователю.
    Логирование для отслеживания ошибок и состояния работы.

    Supports uploading up to 10 photos with captions.
    Carousel navigation with "Back" and "Next" buttons.
    Ability to finish photo uploads and send the carousel to a group.
    Storage of photos and captions by user.
    Logging to monitor errors and work status.

Установка (Installation)

    Клонируйте репозиторий:

    bash

git clone https://github.com/semenovstyle/Photo-Carousel-Telegram-Bot.git
cd photo-carousel-bot

Установите зависимости:

bash

    pip install -r requirements.txt

    Создайте файл .env и добавьте переменные окружения (см. Переменные окружения).

    Clone the repository:

    bash

git clone https://github.com/semenovstyle/Photo-Carousel-Telegram-Bot.git
cd photo-carousel-bot

Install dependencies:

bash

    pip install -r requirements.txt

    Create a .env file and add environment variables (see Environment Variables).

Использование (Usage)

Запустите бота:

bash

python3 carousel.py

Добавьте бота в группу, где требуется создание каруселей. Начните с командой /start и следуйте инструкциям для загрузки фотографий и подписей.

Run the bot:

bash

python3 carousel.py

Add the bot to the group where carousel creation is needed. Start with the /start command and follow the instructions to upload photos and captions.
Переменные окружения (Environment Variables)

Бот использует следующие переменные окружения, которые должны быть заданы в файле .env:

    CARSIMG_TOKEN — токен Telegram API для вашего бота.
    GROUP_IDS — ID группы Telegram, куда будет отправлена карусель.

The bot uses the following environment variables, which should be set in a .env file:

    CARSIMG_TOKEN — Telegram API token for your bot.
    GROUP_IDS — Telegram group ID where the carousel will be sent.

Автор (Author)

   Semenov Sergey
