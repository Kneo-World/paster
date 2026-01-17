import os
from pyrogram import Client, filters

# Данные берем из переменных окружения Render
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING") # Для работы на хостинге

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Ключевые слова для поиска
KEYWORDS = ["nft", "gift", "подарок", "раздача", "t.me/nft_gift"]

@app.on_message(filters.text & ~filters.me)
async def check_nft_gifts(client, message):
    text = message.text.lower()
    
    # Проверяем наличие ключевых слов или ссылок на подарки
    if any(word in text for word in KEYWORDS):
        # Пересылаем сообщение тебе в "Избранное"
        await message.forward("me")
        print(f"✅ Нашел потенциальный NFT подарок в чате: {message.chat.title}")

if __name__ == "__main__":
    print("Юзербот запущен и ищет NFT подарки...")
    app.run()
