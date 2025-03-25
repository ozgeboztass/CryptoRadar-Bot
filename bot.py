#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json
from dotenv import load_dotenv
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from pycoingecko import CoinGeckoAPI

# Loglama yapılandırması
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# .env dosyasından çevresel değişkenleri yükle
load_dotenv()

# CoinGecko API istemcisini başlat
cg = CoinGeckoAPI()

# Favori kripto paraları depolamak için dosya adı
FAVORITES_FILE = 'user_favorites.json'

def load_favorites():
    """Kullanıcıların favori kripto paralarını yükler"""
    try:
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Favorileri yüklerken hata: {e}")
        return {}

def save_favorites(favorites):
    """Kullanıcıların favori kripto paralarını kaydeder"""
    try:
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(favorites, f)
    except Exception as e:
        logger.error(f"Favorileri kaydederken hata: {e}")

# Favori kripto paraları yükle
user_favorites = load_favorites()

def start(update: Update, context: CallbackContext) -> None:
    """Başlangıç komutunu işler."""
    user = update.effective_user
    update.message.reply_text(
        f'Merhaba {user.first_name}! Ben Kripto Para Fiyat Botuyum.\n\n'
        f'Kullanılabilir komutlar:\n'
        f'/price [kripto_kodu] - Kripto fiyatlarını gösterir (örn: /price btc)\n'
        f'/top - En büyük 10 kriptoyu listeler\n'
        f'/add [kripto_kodu] - Kripto parayı favorilere ekler (örn: /add sol)\n'
        f'/favorites - Favori kripto paralarınızı listeler\n'
        f'/remove [kripto_kodu] - Kripto parayı favorilerden kaldırır (örn: /remove sol)\n'
        f'/help - Tüm komutları gösterir'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Yardım komutunu işler."""
    update.message.reply_text(
        '*Kullanılabilir Komutlar*\n\n'
        '/price [kripto_kodu] - Belirtilen kripto paranın fiyatını gösterir.\n'
        'Örnek: /price btc, /price eth veya /price btc eth\n\n'
        '/top - Piyasa değerine göre en büyük 10 kripto parayı listeler\n\n'
        '/add [kripto_kodu] - Kripto parayı favorilerinize ekler\n'
        'Örnek: /add sol\n\n'
        '/favorites - Favori kripto paralarınızın listesini gösterir\n\n'
        '/remove [kripto_kodu] - Kripto parayı favorilerinizden kaldırır\n'
        'Örnek: /remove sol\n\n'
        '/list - Popüler kripto paraların listesini gösterir',
        parse_mode=ParseMode.MARKDOWN
    )

def get_crypto_price(crypto_id: str) -> dict:
    """Belirtilen kripto paranın fiyat bilgisini döndürür."""
    try:
        # Kripto kodu kısaltmalarını tam adlara dönüştür
        if crypto_id.lower() == 'btc':
            crypto_id = 'bitcoin'
        elif crypto_id.lower() == 'eth':
            crypto_id = 'ethereum'
        elif crypto_id.lower() == 'sol':
            crypto_id = 'solana'
        elif crypto_id.lower() == 'doge':
            crypto_id = 'dogecoin'
        elif crypto_id.lower() == 'xrp':
            crypto_id = 'ripple'
        elif crypto_id.lower() == 'ada':
            crypto_id = 'cardano'
        elif crypto_id.lower() == 'dot':
            crypto_id = 'polkadot'
        elif crypto_id.lower() == 'ltc':
            crypto_id = 'litecoin'
        
        # CoinGecko API'den kripto para bilgilerini al
        price_data = cg.get_price(
            ids=crypto_id, 
            vs_currencies=['usd', 'eur', 'try'], 
            include_market_cap=True,
            include_24hr_change=True
        )
        
        if not price_data or crypto_id not in price_data:
            return {"error": f"{crypto_id} için veri bulunamadı."}
        
        return {
            "id": crypto_id,
            "data": price_data[crypto_id]
        }
    except Exception as e:
        logger.error(f"Kripto veri alırken hata: {e}")
        return {"error": f"Veri alınırken bir hata oluştu: {str(e)}"}

def format_price_message(crypto_data: dict) -> str:
    """Kripto para verilerini okunabilir bir mesaja dönüştürür."""
    if "error" in crypto_data:
        return crypto_data["error"]
    
    crypto_id = crypto_data["id"]
    data = crypto_data["data"]
    
    # İsmin ilk harfini büyük yap
    crypto_name = crypto_id.capitalize()
    
    message = f"*{crypto_name}* Fiyat Bilgisi:\n\n"
    
    # USD fiyatı
    if "usd" in data:
        usd_price = data["usd"]
        message += f"💵 *USD*: ${usd_price:,.2f}\n"
    
    # EUR fiyatı
    if "eur" in data:
        eur_price = data["eur"]
        message += f"💶 *EUR*: €{eur_price:,.2f}\n"
    
    # TRY fiyatı
    if "try" in data:
        try_price = data["try"]
        message += f"💷 *TRY*: ₺{try_price:,.2f}\n"
    
    # 24 saatlik değişim
    if "usd_24h_change" in data:
        change_24h = data["usd_24h_change"]
        emoji = "🟢" if change_24h > 0 else "🔴"
        message += f"{emoji} *24s Değişim*: %{change_24h:.2f}\n"
    
    # Piyasa değeri
    if "usd_market_cap" in data:
        market_cap = data["usd_market_cap"]
        message += f"📊 *Piyasa Değeri*: ${market_cap:,.0f}\n"
    
    return message

def price_command(update: Update, context: CallbackContext) -> None:
    """Kripto para fiyat komutunu işler."""
    if not context.args:
        update.message.reply_text(
            "Lütfen fiyatını öğrenmek istediğiniz kripto para kodunu belirtin. "
            "Örnek: /price btc"
        )
        return
    
    # Tüm argümanları al ve her biri için fiyat sorgulama yap
    crypto_ids = [arg.lower() for arg in context.args]
    
    for crypto_id in crypto_ids:
        crypto_data = get_crypto_price(crypto_id)
        message = format_price_message(crypto_data)
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def list_command(update: Update, context: CallbackContext) -> None:
    """Popüler kripto paraları listeler."""
    try:
        # CoinGecko API'den popüler kripto paraları al
        top_coins = cg.get_coins_markets(
            vs_currency='usd',
            order='market_cap_desc',
            per_page=10,
            page=1
        )
        
        message = "*Popüler Kripto Paralar:*\n\n"
        
        for i, coin in enumerate(top_coins, 1):
            price = coin['current_price']
            change_24h = coin['price_change_percentage_24h'] or 0
            emoji = "🟢" if change_24h > 0 else "🔴"
            
            message += f"{i}. *{coin['name']}* ({coin['symbol'].upper()})\n"
            message += f"   💵 ${price:,.2f} | {emoji} %{change_24h:.2f}\n"
            message += f"   `/price {coin['id']}`\n\n"
        
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Popüler kriptoları listelerken hata: {e}")
        update.message.reply_text(f"Popüler kripto paraları listelerken bir hata oluştu: {str(e)}")

def top_command(update: Update, context: CallbackContext) -> None:
    """En büyük 10 kriptoyu listeler. (list_command ile aynı işlevi görür)"""
    try:
        # CoinGecko API'den popüler kripto paraları al
        top_coins = cg.get_coins_markets(
            vs_currency='usd',
            order='market_cap_desc',
            per_page=10,
            page=1
        )
        
        message = "*En Büyük 10 Kripto Para:*\n\n"
        
        for i, coin in enumerate(top_coins, 1):
            price = coin['current_price']
            change_24h = coin['price_change_percentage_24h'] or 0
            emoji = "🟢" if change_24h > 0 else "🔴"
            market_cap = coin['market_cap']
            
            message += f"{i}. *{coin['name']}* ({coin['symbol'].upper()})\n"
            message += f"   💵 ${price:,.2f} | {emoji} %{change_24h:.2f}\n"
            message += f"   📊 Piyasa Değeri: ${market_cap:,.0f}\n"
            message += f"   Kod: `/price {coin['id']}`\n\n"
        
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"En büyük kriptoları listelerken hata: {e}")
        update.message.reply_text(f"En büyük kripto paraları listelerken bir hata oluştu: {str(e)}")

def add_favorite(update: Update, context: CallbackContext) -> None:
    """Kripto parayı kullanıcının favorilerine ekler."""
    if not context.args:
        update.message.reply_text(
            "Lütfen favorilerinize eklemek istediğiniz kripto para kodunu belirtin. "
            "Örnek: /add btc"
        )
        return
    
    crypto_id = context.args[0].lower()
    
    # Ortak kripto kodu kısaltmalarını tam adlara dönüştür
    if crypto_id == 'btc':
        crypto_id = 'bitcoin'
    elif crypto_id == 'eth':
        crypto_id = 'ethereum'
    elif crypto_id == 'sol':
        crypto_id = 'solana'
    elif crypto_id == 'doge':
        crypto_id = 'dogecoin'
    elif crypto_id == 'xrp':
        crypto_id = 'ripple'
    elif crypto_id == 'ada':
        crypto_id = 'cardano'
    elif crypto_id == 'dot':
        crypto_id = 'polkadot'
    elif crypto_id == 'ltc':
        crypto_id = 'litecoin'
    
    # Kripto para kodunun geçerli olup olmadığını kontrol et
    try:
        result = get_crypto_price(crypto_id)
        if "error" in result:
            update.message.reply_text(f"Hata: {result['error']}")
            return
        
        user_id = str(update.effective_user.id)
        
        # Kullanıcının favori listesini al veya oluştur
        if user_id not in user_favorites:
            user_favorites[user_id] = []
        
        # Zaten favorilerde var mı kontrol et
        if crypto_id in user_favorites[user_id]:
            update.message.reply_text(f"{crypto_id.capitalize()} zaten favorilerinizde!")
            return
        
        # Favorilere ekle
        user_favorites[user_id].append(crypto_id)
        save_favorites(user_favorites)
        
        update.message.reply_text(f"{crypto_id.capitalize()} favorilerinize eklendi! 📌")
    except Exception as e:
        logger.error(f"Favorilere eklerken hata: {e}")
        update.message.reply_text(f"İşlem sırasında bir hata oluştu: {str(e)}")

def remove_favorite(update: Update, context: CallbackContext) -> None:
    """Kripto parayı kullanıcının favorilerinden kaldırır."""
    if not context.args:
        update.message.reply_text(
            "Lütfen favorilerinizden kaldırmak istediğiniz kripto para kodunu belirtin. "
            "Örnek: /remove btc"
        )
        return

    crypto_id = context.args[0].lower()
    
    # Ortak kripto kodu kısaltmalarını tam adlara dönüştür
    if crypto_id == 'btc':
        crypto_id = 'bitcoin'
    elif crypto_id == 'eth':
        crypto_id = 'ethereum'
    elif crypto_id == 'sol':
        crypto_id = 'solana'
    elif crypto_id == 'doge':
        crypto_id = 'dogecoin'
    elif crypto_id == 'xrp':
        crypto_id = 'ripple'
    elif crypto_id == 'ada':
        crypto_id = 'cardano'
    elif crypto_id == 'dot':
        crypto_id = 'polkadot'
    elif crypto_id == 'ltc':
        crypto_id = 'litecoin'

    user_id = str(update.effective_user.id)
    
    # Kullanıcının favori listesini kontrol et
    if user_id not in user_favorites or crypto_id not in user_favorites[user_id]:
        update.message.reply_text(f"{crypto_id.capitalize()} favorilerinizde bulunamadı!")
        return
    
    # Favorilerden kaldır
    user_favorites[user_id].remove(crypto_id)
    save_favorites(user_favorites)
    
    update.message.reply_text(f"{crypto_id.capitalize()} favorilerinizden kaldırıldı! ✅")

def show_favorites(update: Update, context: CallbackContext) -> None:
    """Kullanıcının favori kripto paralarını gösterir."""
    user_id = str(update.effective_user.id)
    
    # Kullanıcının favori listesini kontrol et
    if user_id not in user_favorites or not user_favorites[user_id]:
        update.message.reply_text("Henüz favorilerinize kripto para eklemediniz! /add komutuyla ekleyebilirsiniz.")
        return
    
    message = "*Favori Kripto Paralarınız:*\n\n"
    
    for crypto_id in user_favorites[user_id]:
        result = get_crypto_price(crypto_id)
        if "error" not in result:
            price_usd = result["data"].get("usd", 0)
            change_24h = result["data"].get("usd_24h_change", 0)
            emoji = "🟢" if change_24h > 0 else "🔴"
            
            message += f"*{crypto_id.capitalize()}*\n"
            message += f"💵 ${price_usd:,.2f} | {emoji} %{change_24h:.2f}\n"
            message += f"Daha fazla bilgi: `/price {crypto_id}`\n\n"
        else:
            message += f"*{crypto_id.capitalize()}*: Veri alınamadı\n\n"
    
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def error_handler(update: Update, context: CallbackContext) -> None:
    """Bot hatalarını işler."""
    logger.error(f"Update {update} caused error {context.error}")
    try:
        update.message.reply_text("İşlem sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
    except:
        pass

def main() -> None:
    """Bot'u başlatır."""
    # Telegram API token'ını çevresel değişkenlerden al
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN çevresel değişkeni ayarlanmamış!")
        return
    
    # Updater'ı başlat
    updater = Updater(token)
    
    # Dispatcher'ı al
    dispatcher = updater.dispatcher
    
    # Komut işleyicilerini ekle
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("price", price_command))
    dispatcher.add_handler(CommandHandler("list", list_command))
    dispatcher.add_handler(CommandHandler("top", top_command))
    dispatcher.add_handler(CommandHandler("add", add_favorite))
    dispatcher.add_handler(CommandHandler("remove", remove_favorite))
    dispatcher.add_handler(CommandHandler("favorites", show_favorites))
    
    # Hata işleyicisini ekle
    dispatcher.add_error_handler(error_handler)
    
    # Bot'u başlat
    updater.start_polling()
    logger.info("Bot başlatıldı!")
    
    # Bot Ctrl+C ile durdurulana kadar çalışmaya devam et
    updater.idle()

if __name__ == '__main__':
    main() 