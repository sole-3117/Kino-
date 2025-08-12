from aiogram.types import 
InlineKeyboardMarkup, InlineKeyboardButton def 
main_admin_kb():
    kb = InlineKeyboardMarkup(row_width=1) 
    kb.add(InlineKeyboardButton('Kanal 
    boshqaruvi', 
    callback_data='menu_channels')) 
    kb.add(InlineKeyboardButton('Kinolar', 
    callback_data='menu_movies')) 
    kb.add(InlineKeyboardButton('Reklama', 
    callback_data='menu_ads')) 
    kb.add(InlineKeyboardButton('Sozlamalar', 
    callback_data='menu_settings')) 
    kb.add(InlineKeyboardButton('Foydalanuvchilar', 
    callback_data='menu_users'))
    return kb
