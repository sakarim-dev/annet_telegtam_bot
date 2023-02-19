from itertools import chain
from utils.config import TOKEN_BOT_TEST, ADMIN_ID
from utils.keyboards import *
from aiogram import types, executor, Bot, Dispatcher
from asyncio import sleep
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.sqlite import *


async def on_startup(_):
    await db_start()


storage = MemoryStorage()
bot = Bot(TOKEN_BOT_TEST)
dp = Dispatcher(bot, storage=storage)


class User(StatesGroup):
    name = State()
    phone = State()
    email = State()
    description = State()


class Admin(StatesGroup):
    ads = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Добро пожаловать, Admin',
                             reply_markup=get_admin_keyboard())

    else:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать к Аннет!',
                             reply_markup=get_main_keyboard())
        await message.answer('Выберите действие')
    await create_profile(user_id=message.from_user.id)


@dp.chat_join_request_handler()
async def channel_sub(update: types.ChatJoinRequest):
    print(update.from_user)
    await update.approve()
    await bot.send_message(chat_id=update.from_user.id, text="Ты подписался на канал - спасибо!")


@dp.message_handler(content_types=['text'])
async def answers(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        if message.text == "Запись на тет-а-тет с Аннет":
            await message.answer('TODO - Добавить описание', reply_markup=get_record_keyboard())
            await bot.send_message(chat_id=ADMIN_ID, text="Кто-то записывается к Аннет!")
        elif message.text == "Контакты":
            await message.answer('Ссылки на социальные сети', reply_markup=get_links_keyboard())
        elif message.text == "Предварительная запись на Практикум «Энергия жизни»":
            await message.answer('Заполните анкету для предварительной записи', reply_markup=get_form_one_keyboard())
        elif message.text == "Пройти отбор на Наставничество от Аннет":
            await message.answer('Заполните анкету для отбора на Наставничество', reply_markup=get_form_two_keyboard())
        else:
            await message.answer('Выберите, пожалуйста, действие, которое указано на кнопках',
                                 reply_markup=get_main_keyboard())
    else:
        if message.text == "Количество пользователей":
            await message.answer(f'Количество пользователей бота - <b>{str(len(await get_all_id()))}</b>',
                                 parse_mode='html')
        elif "/ads" in message.text:
            words = message.text.split(' ')
            fragment = '/ads'
            new_words = []
            for word in words:
                if fragment not in word:
                    new_words.append(word)

            massive = await get_all_id()
            massive = list(chain(*massive))
            check_error = False
            for i in massive:
                try:

                    await bot.send_message(chat_id=i, text=' '.join(new_words))
                    await sleep(0.3)
                except Exception as e:
                    check_error = True
                    print(e)
                    pass

            if check_error:
                await bot.send_message(chat_id=ADMIN_ID, text="<b>Info</b>: Ряд пользователей из базы данных не "
                                                              "получили рассылку из-за того что бот был заблокирован"
                                                              " с их стороны", parse_mode='html')
            await bot.send_message(chat_id=ADMIN_ID, text="Рассылка отправлена")


@dp.callback_query_handler(text='record', state=None)
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, "Для записи нам нужны ваши данные")
    await User.name.set()
    await bot.send_message(query.from_user.id, "Укажите Ваше имя")


@dp.message_handler(state=User.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await User.next()
    await message.answer('Укажите Ваш номер телефона')


@dp.message_handler(state=User.phone)
async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.answer('Укажите Ваш email')
    await User.next()


@dp.message_handler(state=User.email)
async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await message.answer('Твой запрос на тет-а-тет')
    await User.next()


@dp.message_handler(state=User.description)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_message(chat_id=ADMIN_ID,
                               text=f"Пользователь @{message.from_user.username} оставил запрос на тет-а-тет с Аннет \n"
                                    f"<b>1. Имя:</b> {data['name']}\n"
                                    f"<b>2. Номер телефона:</b> {data['phone']}\n"
                                    f"<b>3. Email:</b> {data['email']}\n"
                                    f"<b>4. Запрос на тет-а-тет:</b> {data['description']}", parse_mode='html')

        await message.answer(text=f"Ваш запрос на тет-а-тет с Аннет. Пожалуйста, проверьте данные \n"
                                  f"<b>1. Имя:</b> {data['name']}\n"
                                  f"<b>2. Номер телефона:</b> {data['phone']}\n"
                                  f"<b>3. Email:</b> {data['email']}\n"
                                  f"<b>4. Запрос на тет-а-тет:</b> {data['description']}", parse_mode='html')

    await edit_profile(state, user_id=message.from_user.id)
    await message.answer('Если вы нашли ошибку в запросе, то Вы можете заполнить их заново нажав на кнопку',
                         reply_markup=get_record_repeat_keyboard())
    await state.finish()


@dp.callback_query_handler(text='all_right')
async def all_right(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, 'Вы успешно зарегистрированы, мы с вами свяжемся в ближайшее время')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
