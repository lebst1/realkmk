from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import bold, italic, code

API_TOKEN = "7525450620:AAGNu2ZHVWQbXN0i49zTB18dMsQE6Tzm1iI"
CHANNEL_ID = -1002469247122
SPECIAL_CHAT_ID = -4531452660

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Функция для создания клавиатуры
def create_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Одобрить', callback_data='approve'),
                  InlineKeyboardButton('Отклонить', callback_data='decline'))
    return keyboard

# Обработчик входящих сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    # Проверка на команду /start
    if message.text == '/start':
        await message.answer('👋Привет! 📨Напишите сообщение и после проверки модератором, оно отправиться в канал!')
        return

    # Получаем username и ID пользователя
    username = message.from_user.username
    user_id = message.from_user.id

    # Добавляем @ к username, если он не пустой
    if username:
        username = f'@{username}'

        # Отправляем сообщение в спец чат с кнопками и информацией о пользователе
    await bot.send_message(SPECIAL_CHAT_ID, f'Сообщение от {username} (ID: {user_id}):\n\n{message.text}',
                      reply_markup=create_keyboard())
    

    # Сообщение пользователю о том, что сообщение на проверке
    await message.answer('⏳ Ваше сообщение отправлено на проверку.')

# Обработчик нажатий на кнопки
@dp.callback_query_handler(text=['approve', 'decline'])
async def handle_callback_query(call: types.CallbackQuery):
    # Получаем текст сообщения
    message_text = call.message.text

    if call.data == 'approve':
        # Извлекаем только текст из сообщения
        text_to_send = message_text.split('\n\n')[1] 
        # Отправляем только текст в канал
        await bot.send_message(CHANNEL_ID, text_to_send)
        await call.answer('✅ Сообщение одобрено и отправлено в канал')

        # Получаем ID пользователя, отправившего сообщение
        user_id = int(call.message.text.split(' (ID: ')[1].split(')')[0])

        # Отправляем сообщение пользователю о том, что его сообщение одобрено
        await bot.send_message(user_id, '✅ Ваше сообщение одобрено и отправлено в канал.')
    else:
        await call.answer('❌ Сообщение отклонено')

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('👋Привет! 📨Напишите сообщение и после проверки модератором, оно отправиться в канал!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
