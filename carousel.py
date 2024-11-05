import os
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
GROUP_ID = int(os.getenv("GROUP_IDS")) 
bot = Bot(token=os.getenv('CARSIMG_TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Определение состояний FSM
class PhotoCarouselStates(StatesGroup):
    uploading_photos = State()
    awaiting_caption = State()
    browsing_photos = State()

# Маршрутизатор
router = Router()

# Словарь для хранения фото и подписей по id пользователей
user_photos = {}

# Функции для создания клавиатур
class Keyboards:
    @staticmethod
    def control_keyboard():
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Завершить")]],
            resize_keyboard=True
        )

    @staticmethod
    def carousel_keyboard(user_id: int, group_id: int, index: int):
        builder = InlineKeyboardBuilder()
        builder.button(text="⬅️ Назад", callback_data=f"prev_{user_id}_{group_id}_{index}")
        builder.button(text="Вперед ➡️", callback_data=f"next_{user_id}_{group_id}_{index}")
        return builder.as_markup()

# Обработчики
@router.message(F.text == "/start")
async def start_handler(message: types.Message, state: FSMContext):
    # Очистка предыдущего состояния пользователя
    await state.clear()
    user_photos[message.from_user.id] = []

    await message.answer("Привет ✋ Давай создадим карусель из фотографий ⏬")
    await message.answer("1. Загрузи фото по 1шт не более 10, не забудь сжать их.")
    await message.answer("2. Описание для фото отправляй отдельным сообщением. \n⚠ Не используй встроенную Подпись.")
    await message.answer("Вперед к загрузке 📎 ")
    await state.set_state(PhotoCarouselStates.uploading_photos)

@router.message(PhotoCarouselStates.uploading_photos, F.photo)
async def photo_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]  # Берем фото в наилучшем качестве
    user_photos[user_id].append({"file_id": photo.file_id, "caption": ""})
    await message.answer("Фото загружено ✅ \nОтправь подпись к этому фото", reply_markup=Keyboards.control_keyboard())
    await state.set_state(PhotoCarouselStates.awaiting_caption)

@router.message(PhotoCarouselStates.awaiting_caption, F.text)
async def caption_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # Проверка на наличие фото перед добавлением подписи
    if user_photos.get(user_id):
        user_photos[user_id][-1]["caption"] = message.text
        await message.answer("Подпись сохранена ✅ \nМожешь загрузить еще фото или завершить ⏬", reply_markup=Keyboards.control_keyboard())
        await state.set_state(PhotoCarouselStates.uploading_photos)
    else:
        await message.answer("⚠ Ошибка: Сначала загрузите фото.")

@router.message(PhotoCarouselStates.uploading_photos, F.text == "Завершить")
async def finish_uploading_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not user_photos.get(user_id):
        await message.answer("⚠ Ты еще не загрузил ни одного фото ⚠")
        return

    await message.answer("Карусель отправлена ✅", reply_markup=types.ReplyKeyboardRemove())
    
    # Отправка карусели в группу с навигацией
    await send_carousel_to_group(user_id, GROUP_ID)

    # Переход к состоянию просмотра карусели
    await state.set_state(PhotoCarouselStates.browsing_photos)
    await state.update_data(current_index=0)

# Функция для отправки первого фото в виде карусели
async def send_carousel_to_group(user_id: int, group_id: int):
    if not user_photos.get(user_id):
        logger.warning(f"No photos found for user_id={user_id}")
        return

    # Начало с первого фото
    initial_index = 0
    await show_photo_in_group(user_id, group_id, initial_index)

# Функция для показа фото с кнопками навигации
async def show_photo_in_group(user_id: int, group_id: int, index: int):
    photo = user_photos[user_id][index]
    total_photos = len(user_photos[user_id])

    # Кнопки навигации и индикатор текущей позиции
    keyboard = Keyboards.carousel_keyboard(user_id, group_id, index)
    caption = f"{photo['caption']} \nФото {index + 1} из {total_photos}"

    try:
        await bot.send_photo(
            chat_id=group_id,
            photo=photo["file_id"],
            caption=caption,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Failed to send photo in group: {e}")

# Обработчик кнопок навигации в карусели
@router.callback_query(F.data.startswith(("next_", "prev_")))
async def carousel_navigation(call: types.CallbackQuery):
    data = call.data.split("_")
    direction, user_id, group_id, current_index = data[0], int(data[1]), int(data[2]), int(data[3])

    if user_photos.get(user_id):
        total_photos = len(user_photos[user_id])
        new_index = (current_index + 1) % total_photos if direction == "next" else (current_index - 1) % total_photos
        photo = user_photos[user_id][new_index]
        keyboard = Keyboards.carousel_keyboard(user_id, group_id, new_index)
        caption = f"{photo['caption']} \nФото {new_index + 1} из {total_photos}"

        try:
            await call.message.edit_media(
                types.InputMediaPhoto(media=photo["file_id"], caption=caption),
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Failed to edit media in group: {e}")

        await call.answer()
    else:
        logger.warning(f"Photos for user_id={user_id} are missing.")

# Включение маршрутизатора в диспетчер
dp.include_router(router)

if __name__ == "__main__":
    import asyncio

    async def main():  
        logger.info("Carousel bot запущен")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    asyncio.run(main())
