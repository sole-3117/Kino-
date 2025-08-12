import logging, traceback, asyncio from 
aiogram import Bot, Dispatcher, types from 
aiogram.utils import executor from 
aiogram.types import ParseMode, 
InlineKeyboardButton, InlineKeyboardMarkup 
from aiogram.contrib.middlewares.logging 
import LoggingMiddleware from 
aiogram.dispatcher import FSMContext from 
aiogram.contrib.fsm_storage.memory import 
MemoryStorage from 
aiogram.dispatcher.filters.state import State, 
StatesGroup from datetime import datetime from 
apscheduler.schedulers.asyncio import 
AsyncIOScheduler from config import BOT_TOKEN, 
MAIN_ADMIN, DATABASE_PATH from database import 
Database from admin_panel import main_admin_kb 
logging.basicConfig(level=logging.INFO) logger 
= logging.getLogger(__name__) bot = 
Bot(token=BOT_TOKEN) storage = MemoryStorage() 
dp = Dispatcher(bot, storage=storage) 
dp.middleware.setup(LoggingMiddleware()) db = 
Database(DATABASE_PATH) scheduler = 
AsyncIOScheduler() class 
AddMovieStates(StatesGroup):
    waiting_for_video = State() 
    waiting_for_title = State() 
    waiting_for_format = State() 
    waiting_for_language = State()
async def on_startup(dp): await db.init() 
    await db.add_admin(MAIN_ADMIN)
    # default setting mandatory_subscribe = 
    # False if not set
    cur = await 
    db.get_setting('mandatory_subscribe') if 
    cur is None:
        await 
        db.set_setting('mandatory_subscribe', 
        'False')
    scheduler.start() logger.info('Bot 
    started')
def admin_check(func): async def 
    wrapper(message, *args, **kwargs):
        is_admin = await 
        db.is_admin(message.from_user.id) if 
        not is_admin:
            await message.reply('Siz admin 
            emassiz.') return
        return await func(message, *args, 
        **kwargs)
    return wrapper
# Start
@dp.message_handler(commands=['start']) async 
def cmd_start(message: types.Message):
    await db.add_user(message.from_user.id, 
    message.from_user.username or '', 
    message.from_user.full_name or '') await 
    bot.send_message(MAIN_ADMIN, f'Yangi user: 
    {message.from_user.full_name} 
    (@{message.from_user.username}) 
    id={message.from_user.id}') await 
    message.reply('Assalomu alaykum! Kinoni 
    olish uchun kod yuboring yoki /help ni 
    bosing.')
@dp.message_handler(commands=['help']) async 
def cmd_help(message: types.Message):
    await message.reply('/admin - admin panel 
    (admins only)\nKodni yuboring: kod raqam 
    bilan')
@dp.message_handler(commands=['admin']) async 
def cmd_admin(message: types.Message):
    if not await 
    db.is_admin(message.from_user.id):
        return await message.reply('Siz admin 
        emassiz.')
    users = await db.count_users() movies = 
    await db.count_movies() views = await 
    db.get_total_views() kb = main_admin_kb() 
    txt = f'Admin panel\nUsers: 
    {users}\nMovies: {movies}\nViews: {views}' 
    await message.reply(txt, reply_markup=kb)
# setchannels add/remove via command
@dp.message_handler(commands=['setchannels']) 
@admin_check async def 
cmd_setchannels(message: types.Message):
    parts = message.get_args().split() if 
    len(parts) < 2:
        return await 
        message.reply('Foydalanish: 
        /setchannels add @channel yoki 
        /setchannels remove @channel')
    action = parts[0].lower() ch = parts[1] if 
    action == 'add':
        await db.add_channel(ch) await 
        message.reply(f'Kanal qo\'shildi: 
        {ch}')
    elif action == 'remove': await 
        db.remove_channel(ch) await 
        message.reply(f'Kanal o\'chirildi: 
        {ch}')
    else: await message.reply('Noto\'g\'ri 
        foydalanish.')
# addmovie flow
@dp.message_handler(commands=['addmovie']) 
@admin_check async def cmd_addmovie(message: 
types.Message):
    await message.reply('Yuboring video faylni 
    (video yoki document).') await 
    AddMovieStates.waiting_for_video.set()
@dp.message_handler(content_types=['video','document'], 
state=AddMovieStates.waiting_for_video) async 
def proc_video(message: types.Message, state: 
FSMContext):
    file_id = message.video.file_id if 
    message.video else 
    message.document.file_id await 
    state.update_data(file_id=file_id) await 
    AddMovieStates.next() await 
    message.reply('Kino nomini kiriting:')
@dp.message_handler(state=AddMovieStates.waiting_for_title) 
async def proc_title(message: types.Message, 
state: FSMContext):
    await 
    state.update_data(title=message.text.strip()) 
    await AddMovieStates.next() await 
    message.reply('Formatni kiriting 
    (mp4/mkv):')
@dp.message_handler(state=AddMovieStates.waiting_for_format) 
async def proc_format(message: types.Message, 
state: FSMContext):
    await 
    state.update_data(format=message.text.strip()) 
    await AddMovieStates.next() await 
    message.reply('Tilni kiriting:')
@dp.message_handler(state=AddMovieStates.waiting_for_language) 
async def proc_lang(message: types.Message, 
state: FSMContext):
    data = await state.get_data() title = 
    data.get('title') fmt = data.get('format') 
    lang = message.text.strip() file_id = 
    data.get('file_id') code = await 
    db.add_movie(title, fmt, lang, file_id)
    await message.reply(f'Kino qo\'shildi. Kod: {cod
