#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json
from datetime import datetime
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
# Portföy verilerini saklamak için dosya adı
PORTFOLIO_FILE = 'user_portfolios.json'

# Kripto kısaltmaları için sözlük - daha dinamik bir çözüm
CRYPTO_SYMBOLS = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'sol': 'solana',
    'doge': 'dogecoin',
    'xrp': 'ripple',
    'ada': 'cardano',
    'dot': 'polkadot',
    'ltc': 'litecoin',
    'bnb': 'binancecoin',
    'usdt': 'tether',
    'usdc': 'usd-coin',
    'matic': 'polygon',
    'link': 'chainlink',
    'uni': 'uniswap',
    'avax': 'avalanche-2'
}

def convert_crypto_symbol(symbol: str) -> str:
    """Kripto para sembollerini tam adlara dönüştürür."""
    symbol = symbol.lower()
    return CRYPTO_SYMBOLS.get(symbol, symbol)  # Eğer sözlükte yoksa kendisini döndür

def validate_date(date_str: str) -> bool:
    """Tarih formatının geçerli olup olmadığını kontrol eder (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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

def load_portfolios():
    """Kullanıcıların portföy verilerini yükler"""
    try:
        if os.path.exists(PORTFOLIO_FILE):
            with open(PORTFOLIO_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Portföyleri yüklerken hata: {e}")
        return {}

def save_portfolios(portfolios):
    """Kullanıcıların portföy verilerini kaydeder"""
    try:
        with open(PORTFOLIO_FILE, 'w') as f:
            json.dump(portfolios, f, indent=4)
    except Exception as e:
        logger.error(f"Portföyleri kaydederken hata: {e}")

# Favori kripto paraları ve portföyleri yükle
user_favorites = load_favorites()
user_portfolios = load_portfolios()

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
        f'/portfolio - Portföyünüzü gösterir\n'
        f'/add_transaction - Portföyünüze işlem eklemenizi sağlar\n'
        f'/performance - Portföyünüzün performansını gösterir\n'
        f'/list_transactions - Tüm işlemlerinizi listeler\n'
        f'/help - Tüm komutları gösterir'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Yardım komutunu işler."""
    update.message.reply_text(
        '*Kullanılabilir Komutlar*\n\n'
        '*Kripto Fiyat Komutları:*\n'
        '/price [kripto_kodu] - Belirtilen kripto paranın fiyatını gösterir.\n'
        'Örnek: /price btc, /price eth veya /price btc eth\n\n'
        '/top - Piyasa değerine göre en büyük 10 kripto parayı listeler\n\n'
        '/list - Popüler kripto paraların listesini gösterir\n\n'
        '*Favori Komutları:*\n'
        '/add [kripto_kodu] - Kripto parayı favorilerinize ekler\n'
        'Örnek: /add sol\n\n'
        '/favorites - Favori kripto paralarınızın listesini gösterir\n\n'
        '/remove [kripto_kodu] - Kripto parayı favorilerinizden kaldırır\n'
        'Örnek: /remove sol\n\n'
        '*Portföy Takip Komutları:*\n'
        '/portfolio - Portföyünüzü görüntüler\n\n'
        '/add_transaction - Portföyünüze işlem eklemenizi sağlar\n'
        'Örnek: /add_transaction btc buy 0.05 35000 2023-11-20 10\n\n'
        '/performance - Portföyünüzün performansını ve kar/zarar durumunu gösterir\n\n'
        '/list_transactions - Tüm işlemlerinizi listeler\n\n'
        '/delete_transaction [kripto_kodu] [işlem_no] - Belirtilen işlemi siler\n'
        'Örnek: /delete_transaction btc 1',
        parse_mode=ParseMode.MARKDOWN
    )

def get_crypto_price(crypto_id: str) -> dict:
    """Belirtilen kripto paranın fiyat bilgisini döndürür."""
    try:
        # Kripto kodu kısaltmasını tam ada dönüştür
        crypto_id = convert_crypto_symbol(crypto_id)
        
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
    
    # Kripto kodu kısaltmasını tam ada dönüştür
    crypto_id = convert_crypto_symbol(crypto_id)
    
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
    
    # Kripto kodu kısaltmasını tam ada dönüştür
    crypto_id = convert_crypto_symbol(crypto_id)

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

def portfolio_command(update: Update, context: CallbackContext) -> None:
    """Kullanıcının portföyünü gösterir."""
    user_id = str(update.effective_user.id)
    
    if user_id not in user_portfolios or "portfolio" not in user_portfolios[user_id]:
        update.message.reply_text(
            "Henüz portföyünüzde kripto para bulunmuyor.\n"
            "İşlem eklemek için /add_transaction komutunu kullanabilirsiniz."
        )
        return
    
    user_portfolio = user_portfolios[user_id]["portfolio"]
    
    if not user_portfolio:
        update.message.reply_text("Portföyünüz boş.")
        return
    
    message = "*📊 Portföyünüz:*\n\n"
    total_portfolio_value = 0
    
    for crypto_id, data in user_portfolio.items():
        amount = data["amount"]
        if amount <= 0:
            continue
            
        # Güncel fiyat bilgisini al
        price_data = get_crypto_price(crypto_id)
        
        if "error" not in price_data:
            price_usd = price_data["data"].get("usd", 0)
            price_try = price_data["data"].get("try", 0)
            
            value_usd = amount * price_usd
            value_try = amount * price_try
            total_portfolio_value += value_usd
            
            # İsmin ilk harfini büyük yap
            crypto_name = crypto_id.capitalize()
            
            message += f"*{crypto_name}*\n"
            message += f"💰 Miktar: {amount:.8f}\n"
            message += f"💵 Değer: ${value_usd:.2f} (₺{value_try:.2f})\n"
            message += f"🏷️ Güncel Fiyat: ${price_usd:.2f}\n\n"
        else:
            message += f"*{crypto_id.capitalize()}*: Fiyat verisi alınamadı\n\n"
    
    message += f"*Toplam Portföy Değeri:* ${total_portfolio_value:.2f}\n"
    message += "\nDetaylı kar/zarar analizi için /performance komutunu kullanabilirsiniz."
    
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def add_transaction(update: Update, context: CallbackContext) -> None:
    """Kullanıcının portföyüne yeni bir işlem ekler."""
    if not context.args or len(context.args) < 4:
        update.message.reply_text(
            "Lütfen işlem bilgilerini doğru formatta girin:\n\n"
            "/add_transaction <crypto_kodu> <işlem_tipi> <miktar> <fiyat> <tarih> <komisyon>\n\n"
            "Örnek:\n"
            "/add_transaction btc buy 0.05 35000 2023-11-20 10\n\n"
            "İşlem tipleri: buy (alım) veya sell (satım)\n"
            "Tarih formatı: YYYY-MM-DD (boş bırakılırsa bugünün tarihi kullanılır)\n"
            "Komisyon: İşlem ücreti (boş bırakılabilir, varsayılan: 0)"
        )
        return
    
    user_id = str(update.effective_user.id)
    
    try:
        # Argümanları parse et
        crypto_id = context.args[0].lower()
        transaction_type = context.args[1].lower()
        
        # Miktar ve fiyat doğrulaması
        try:
            amount = float(context.args[2])
            if amount <= 0:
                update.message.reply_text("Miktar sıfırdan büyük olmalıdır.")
                return
        except ValueError:
            update.message.reply_text("Geçersiz miktar. Lütfen sayısal bir değer girin.")
            return
            
        try:
            price = float(context.args[3])
            if price <= 0:
                update.message.reply_text("Fiyat sıfırdan büyük olmalıdır.")
                return
        except ValueError:
            update.message.reply_text("Geçersiz fiyat. Lütfen sayısal bir değer girin.")
            return
        
        # Tarih doğrulaması (opsiyonel)
        today = datetime.now().strftime("%Y-%m-%d")
        date = today  # Varsayılan: bugün
        
        if len(context.args) > 4:
            date_str = context.args[4]
            if validate_date(date_str):
                date = date_str
            else:
                update.message.reply_text(
                    f"Geçersiz tarih formatı: {date_str}\n"
                    f"Lütfen YYYY-MM-DD formatında bir tarih girin. "
                    f"Varsayılan olarak bugünün tarihi ({today}) kullanılacak."
                )
        
        # Komisyon doğrulaması (opsiyonel)
        fee = 0  # Varsayılan: 0
        if len(context.args) > 5:
            try:
                fee = float(context.args[5])
                if fee < 0:
                    update.message.reply_text("Komisyon negatif olamaz. Varsayılan olarak 0 kullanılacak.")
                    fee = 0
            except ValueError:
                update.message.reply_text("Geçersiz komisyon. Varsayılan olarak 0 kullanılacak.")
        
        # Kripto kodu kısaltmasını tam ada dönüştür
        crypto_id = convert_crypto_symbol(crypto_id)
        
        # İşlem tipi kontrolü
        if transaction_type not in ["buy", "sell"]:
            update.message.reply_text("Geçersiz işlem tipi. 'buy' veya 'sell' kullanın.")
            return
        
        # Kullanıcının portföyünü oluştur (yoksa)
        if user_id not in user_portfolios:
            user_portfolios[user_id] = {"portfolio": {}}
        
        if "portfolio" not in user_portfolios[user_id]:
            user_portfolios[user_id]["portfolio"] = {}
        
        # Kripto para portföyde var mı kontrol et
        if crypto_id not in user_portfolios[user_id]["portfolio"]:
            user_portfolios[user_id]["portfolio"][crypto_id] = {
                "amount": 0,
                "transactions": []
            }
        
        # Satış yapılıyorsa, yeterli miktar var mı kontrol et
        if transaction_type == "sell":
            current_amount = user_portfolios[user_id]["portfolio"][crypto_id]["amount"]
            if amount > current_amount:
                update.message.reply_text(
                    f"Yeterli miktarda {crypto_id.capitalize()} yok. "
                    f"Mevcut miktar: {current_amount}"
                )
                return
        
        # İşlemi portföye ekle
        transaction = {
            "date": date,
            "type": transaction_type,
            "amount": amount,
            "price": price,
            "fee": fee
        }
        
        user_portfolios[user_id]["portfolio"][crypto_id]["transactions"].append(transaction)
        
        # Toplam miktarı güncelle
        if transaction_type == "buy":
            user_portfolios[user_id]["portfolio"][crypto_id]["amount"] += amount
        else:  # sell
            user_portfolios[user_id]["portfolio"][crypto_id]["amount"] -= amount
        
        # Değişiklikleri kaydet
        save_portfolios(user_portfolios)
        
        update.message.reply_text(
            f"{transaction_type.capitalize()} işlemi başarıyla eklendi!\n"
            f"Kripto: {crypto_id.capitalize()}\n"
            f"Miktar: {amount}\n"
            f"Fiyat: ${price}\n"
            f"Tarih: {date}"
        )
    except Exception as e:
        logger.error(f"İşlem eklenirken hata: {e}")
        update.message.reply_text(f"İşlem eklenirken bir hata oluştu: {str(e)}")

def performance_command(update: Update, context: CallbackContext) -> None:
    """Portföyün performansını ve kar/zarar durumunu gösterir."""
    user_id = str(update.effective_user.id)
    
    if user_id not in user_portfolios or "portfolio" not in user_portfolios[user_id]:
        update.message.reply_text(
            "Henüz portföyünüzde kripto para bulunmuyor.\n"
            "İşlem eklemek için /add_transaction komutunu kullanabilirsiniz."
        )
        return
    
    user_portfolio = user_portfolios[user_id]["portfolio"]
    
    if not user_portfolio:
        update.message.reply_text("Portföyünüz boş.")
        return
    
    message = "*📈 Portföy Performansı:*\n\n"
    total_investment = 0
    total_current_value = 0
    
    for crypto_id, data in user_portfolio.items():
        if not data["transactions"]:
            continue
            
        # Güncel fiyat bilgisini al
        price_data = get_crypto_price(crypto_id)
        
        if "error" not in price_data:
            current_price = price_data["data"].get("usd", 0)
            current_amount = data["amount"]
            
            # Yatırım miktarını ve kar/zararı hesapla
            invested = 0
            proceeds = 0
            
            for transaction in data["transactions"]:
                if transaction["type"] == "buy":
                    invested += transaction["amount"] * transaction["price"] + transaction["fee"]
                else:  # sell
                    proceeds += transaction["amount"] * transaction["price"] - transaction["fee"]
            
            # Güncel değer
            current_value = current_amount * current_price
            
            # Toplam kar/zarar
            if current_amount > 0:
                total_buy_amount = sum(t["amount"] for t in data["transactions"] if t["type"] == "buy")
                
                # Sıfıra bölme kontrolü
                if total_buy_amount > 0:
                    realized_pl = proceeds - (invested * (1 - current_amount / total_buy_amount))
                else:
                    realized_pl = proceeds
                
                unrealized_pl = current_value - invested + proceeds
                total_pl = unrealized_pl + realized_pl
                
                # Yüzde değişim - sıfıra bölme kontrolü
                if invested > 0:
                    percent_change = (total_pl / invested) * 100
                else:
                    percent_change = 0
                
                # İsmin ilk harfini büyük yap
                crypto_name = crypto_id.capitalize()
                
                message += f"*{crypto_name}*\n"
                message += f"💰 Mevcut Miktar: {current_amount:.8f}\n"
                message += f"💵 Güncel Değer: ${current_value:.2f}\n"
                message += f"💲 Toplam Yatırım: ${invested:.2f}\n"
                
                emoji = "🟢" if total_pl >= 0 else "🔴"
                message += f"{emoji} Kar/Zarar: ${total_pl:.2f} (%{percent_change:.2f})\n\n"
                
                total_investment += invested
                total_current_value += current_value
            else:
                # Tümü satılmış
                realized_pl = proceeds - invested
                
                # Yüzde değişim - sıfıra bölme kontrolü
                if invested > 0:
                    percent_change = (realized_pl / invested) * 100
                else:
                    percent_change = 0
                
                message += f"*{crypto_id.capitalize()}* (Tümü Satıldı)\n"
                emoji = "🟢" if realized_pl >= 0 else "🔴"
                message += f"{emoji} Gerçekleşen Kar/Zarar: ${realized_pl:.2f} (%{percent_change:.2f})\n\n"
        else:
            message += f"*{crypto_id.capitalize()}*: Fiyat verisi alınamadı\n\n"
    
    # Toplam portföy performansı - sıfıra bölme kontrolü
    if total_investment > 0:
        total_pl = total_current_value - total_investment
        total_percent = (total_pl / total_investment) * 100
        
        message += f"*Toplam Portföy:*\n"
        message += f"💲 Toplam Yatırım: ${total_investment:.2f}\n"
        message += f"💵 Güncel Değer: ${total_current_value:.2f}\n"
        
        emoji = "🟢" if total_pl >= 0 else "🔴"
        message += f"{emoji} Toplam Kar/Zarar: ${total_pl:.2f} (%{total_percent:.2f})"
    elif total_current_value > 0:
        # Toplam yatırım sıfırsa ancak portföyde değer varsa
        message += f"*Toplam Portföy:*\n"
        message += f"💵 Güncel Değer: ${total_current_value:.2f}\n"
        message += "💲 Yatırım miktarı hesaplanamadı"
    
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def list_transactions(update: Update, context: CallbackContext) -> None:
    """Kullanıcının tüm işlemlerini listeler."""
    user_id = str(update.effective_user.id)
    
    if user_id not in user_portfolios or "portfolio" not in user_portfolios[user_id]:
        update.message.reply_text("Henüz hiç işleminiz bulunmuyor.")
        return
    
    message = "*📜 İşlem Geçmişiniz:*\n\n"
    transaction_count = 0
    
    for crypto_id, data in user_portfolios[user_id]["portfolio"].items():
        if not data["transactions"]:
            continue
            
        message += f"*{crypto_id.capitalize()}*:\n"
        
        for i, transaction in enumerate(data["transactions"]):
            transaction_type = "Alım" if transaction["type"] == "buy" else "Satım"
            transaction_count += 1
            
            message += f"{i+1}. {transaction_type}: {transaction['amount']} adet\n"
            message += f"   Fiyat: ${transaction['price']}\n"
            message += f"   Tarih: {transaction['date']}\n"
        
        message += "\n"
    
    if transaction_count == 0:
        update.message.reply_text("Henüz hiç işleminiz bulunmuyor.")
        return
    
    message += "İşlem silmek için /delete_transaction [kripto_kodu] [işlem_no] komutunu kullanabilirsiniz."
    
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def delete_transaction(update: Update, context: CallbackContext) -> None:
    """Belirtilen işlemi siler."""
    if len(context.args) < 2:
        update.message.reply_text(
            "Silmek istediğiniz işlemi belirtin:\n"
            "/delete_transaction [kripto_kodu] [işlem_no]\n\n"
            "İşlemlerinizi görmek için /list_transactions komutunu kullanabilirsiniz."
        )
        return
    
    user_id = str(update.effective_user.id)
    
    try:
        crypto_id = context.args[0].lower()
        
        # İşlem numarası doğrulaması
        try:
            transaction_index = int(context.args[1]) - 1  # Kullanıcı 1'den başlayarak sayar
            if transaction_index < 0:
                update.message.reply_text("İşlem numarası 1'den küçük olamaz.")
                return
        except ValueError:
            update.message.reply_text("İşlem numarası bir sayı olmalıdır.")
            return
        
        # Kripto kodu kısaltmasını tam ada dönüştür
        crypto_id = convert_crypto_symbol(crypto_id)
        
        # Portföy ve işlem kontrolü
        if (user_id not in user_portfolios or 
            "portfolio" not in user_portfolios[user_id] or 
            crypto_id not in user_portfolios[user_id]["portfolio"] or 
            "transactions" not in user_portfolios[user_id]["portfolio"][crypto_id] or 
            transaction_index >= len(user_portfolios[user_id]["portfolio"][crypto_id]["transactions"])):
            
            update.message.reply_text("Geçersiz kripto para veya işlem numarası.")
            return
        
        # İşlemi al
        transaction = user_portfolios[user_id]["portfolio"][crypto_id]["transactions"][transaction_index]
        
        # Toplam miktarı güncelle
        if transaction["type"] == "buy":
            user_portfolios[user_id]["portfolio"][crypto_id]["amount"] -= transaction["amount"]
        else:  # sell
            user_portfolios[user_id]["portfolio"][crypto_id]["amount"] += transaction["amount"]
        
        # İşlemi sil
        del user_portfolios[user_id]["portfolio"][crypto_id]["transactions"][transaction_index]
        
        # Değişiklikleri kaydet
        save_portfolios(user_portfolios)
        
        update.message.reply_text(
            f"İşlem başarıyla silindi!\n"
            f"Kripto: {crypto_id.capitalize()}\n"
            f"İşlem Tipi: {transaction['type']}\n"
            f"Miktar: {transaction['amount']}\n"
            f"Fiyat: ${transaction['price']}"
        )
    except Exception as e:
        logger.error(f"İşlem silinirken hata: {e}")
        update.message.reply_text(f"İşlem silinirken bir hata oluştu: {str(e)}")

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
    
    # Portföy komutlarını ekle
    dispatcher.add_handler(CommandHandler("portfolio", portfolio_command))
    dispatcher.add_handler(CommandHandler("add_transaction", add_transaction))
    dispatcher.add_handler(CommandHandler("performance", performance_command))
    dispatcher.add_handler(CommandHandler("list_transactions", list_transactions))
    dispatcher.add_handler(CommandHandler("delete_transaction", delete_transaction))
    
    # Hata işleyicisini ekle
    dispatcher.add_error_handler(error_handler)
    
    # Bot'u başlat
    updater.start_polling()
    logger.info("Bot başlatıldı!")
    
    # Bot Ctrl+C ile durdurulana kadar çalışmaya devam et
    updater.idle()

if __name__ == '__main__':
    main() 