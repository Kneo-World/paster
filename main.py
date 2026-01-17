import os
import asyncio
import aiohttp
from aiogram import Bot

# Конфигурация из Secrets
TOKEN = os.environ['BOT_TOKEN']
ADMIN_ID = os.environ['MY_ID']
# Адрес коллекции подарков в TON (примерный, нужно уточнять актуальный)
GIFTS_COLLECTION = "EQCA14o1-VWhS29_Z9MHLz9fTz1_uByyO08unf89Xf0-f9f9" 

# Настройки фильтра
MIN_PRICE_TON = 50.0 # Находить подарки дороже 50 TON

bot = Bot(token=TOKEN)

async def check_new_gifts():
    last_lt = 0 # Индекс последней проверенной транзакции
    
    while True:
        try:
            # Используем TON API для получения транзакций коллекции
            url = f"https://toncenter.com/api/v2/getTransactions?address={GIFTS_COLLECTION}&limit=10"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    
                    if data.get('ok'):
                        transactions = data['result']
                        for tx in transactions:
                            # Логика фильтрации по цене и метаданным
                            # В реальности здесь нужно парсить поле 'value' или 'in_msg'
                            price = float(tx['out_msgs'][0]['value']) / 10**9 # Перевод из нано-TON
                            
                            if price >= MIN_PRICE_TON:
                                gift_id = tx['transaction_id']['hash']
                                await bot.send_message(
                                    ADMIN_ID, 
                                    f"🎁 Найден дорогой подарок!\n"
                                    f"💰 Цена: {price} TON\n"
                                    f"🔗 Ссылка: https://fragment.com/nft/{gift_id}"
                                )
                                
            # Пауза между проверками, чтобы не забанили API
            await asyncio.sleep(30) 
            
        except Exception as e:
            print(f"Ошибка мониторинга: {e}")
            await asyncio.sleep(10)

if __name__ == '__main__':
    print("Бот-мониторинг запущен...")
    loop = asyncio.get_event_loop()
    loop.create_task(check_new_gifts())
    # Здесь можно добавить запуск обычного aiogram бота для управления настройками
