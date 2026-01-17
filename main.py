import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest

# Извлекаем данные из Secrets
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']

# Создаем клиент
client = TelegramClient('my_parser_session', API_ID, API_HASH)

async def check_user_gifts(user_id):
    try:
        # Запрашиваем полную информацию о пользователе
        full_info = await client(GetFullUserRequest(user_id))
        
        # Проверка наличия NFT/Звездных подарков
        # В новых версиях API поле называется 'star_gifts'
        if hasattr(full_info, 'star_gifts') and full_info.star_gifts:
            return len(full_info.star_gifts.gifts) # Возвращаем кол-во подарков
        return 0
    except Exception:
        return 0

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Парсер запущен. Отправь /scan в любом чате, чтобы найти владельцев NFT.")

@client.on(events.NewMessage(pattern='/scan'))
async def scan(event):
    chat = await event.get_chat()
    await event.respond("🔍 Начинаю сканирование участников...")
    
    found_count = 0
    # iter_participants проходит по всем людям в группе
    async for user in client.iter_participants(chat, limit=200): # Лимит 200 для теста
        if user.bot: continue
        
        gifts_count = await check_user_gifts(user.id)
        if gifts_count > 0:
            found_count += 1
            username = f"@{user.username}" if user.username else "Скрыт"
            await event.respond(f"🎁 Нашел! {username} | Подарков: {gifts_count}")
        
        # Небольшая пауза, чтобы Telegram не забанил за спам запросами
        await asyncio.sleep(1)

    await event.respond(f"✅ Сканирование завершено. Найдено: {found_count}")

print("Бот успешно запущен!")
client.start()
client.run_until_disconnected()
