# Kripto Para Telegram Botu

Bu bot, kullanıcıların Telegram üzerinden kripto para fiyatlarını sorgulamasını ve portföylerini takip etmesini sağlayan bir Python uygulamasıdır.

## Özellikler

### Fiyat Sorgulama
- `/price [kripto_kodu]` komutu ile belirtilen kripto paranın anlık fiyatını gösterme (örn: `/price btc`)
- Çoklu kripto para sorgulama (örn: `/price btc eth`)
- `/top` komutu ile en büyük 10 kripto parayı listeleme
- `/list` komutu ile popüler kripto paraların listesini gösterme

### Favori Kripto Paraları Yönetme
- `/add [kripto_kodu]` komutu ile kripto paraları favorilere ekleme (örn: `/add sol`)
- `/favorites` komutu ile favori kripto paraların listesini gösterme
- `/remove [kripto_kodu]` komutu ile kripto parayı favorilerden kaldırma (örn: `/remove sol`)

### Portföy Takibi
- `/portfolio` komutu ile portföyünüzü görüntüleme
- `/add_transaction [kripto_kodu] [işlem_tipi] [miktar] [fiyat] [tarih] [komisyon]` komutu ile portföyünüze işlem ekleme
- `/performance` komutu ile portföyünüzün performansını ve kar/zarar durumunu görüntüleme
- `/list_transactions` komutu ile tüm işlemlerinizi listeleme
- `/delete_transaction [kripto_kodu] [işlem_no]` komutu ile belirtilen işlemi silme

## Teknik Gereksinimler

- Python 3.7+
- python-telegram-bot kütüphanesi
- Kripto para verileri için CoinGecko API'si

## Planlama

1. **Proje Yapısı Oluşturma**
   - Gerekli dizinler ve dosyalar
   - requirements.txt dosyası

2. **Bot Temel Yapısının Kurulması**
   - Telegram API bağlantısı
   - Komut işleyicilerinin tanımlanması

3. **CoinGecko API Entegrasyonu**
   - Kripto para verilerini çekme
   - Veri dönüşümü ve sunumu

4. **Komutların Uygulanması**
   - `/price` komutunun uygulanması
   - `/top` komutunun uygulanması
   - `/add`, `/remove` ve `/favorites` komutlarının uygulanması
   - Portföy takibi komutlarının uygulanması
   - Hata yönetimi

5. **Test ve Hata Ayıklama**
   - Farklı senaryoların test edilmesi
   - Hata ayıklama ve düzeltme

## Kurulum

1. Repoyu klonlayın:
   ```
   git clone https://github.com/kullaniciadi/telegrambot.git
   cd telegrambot
   ```

2. Sanal ortam oluşturun ve gerekli paketleri yükleyin:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. `.env` dosyası oluşturup Telegram Bot Token'ınızı ekleyin:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

4. Botu çalıştırın:
   ```
   python bot.py
   ```

## Bot Nasıl Kullanılır

### Temel Komutlar
- `/start` - Botu başlatır ve kullanım bilgilerini gösterir
- `/help` - Komutlar hakkında yardım bilgisi verir

### Fiyat Komutları
- `/price btc` - Bitcoin'in anlık fiyatını gösterir
- `/price btc eth` - Belirtilen kripto paraların fiyatlarını gösterir
- `/top` - En büyük 10 kripto parayı listeler
- `/list` - Popüler kripto paraların listesini gösterir

### Favori Komutları
- `/add sol` - Solana'yı favorilere ekler
- `/favorites` - Favori kripto paralarınızı listeler
- `/remove sol` - Solana'yı favorilerden kaldırır

### Portföy Komutları
- `/portfolio` - Portföyünüzü gösterir
- `/add_transaction btc buy 0.05 35000 2023-11-20 10` - Bitcoin alım işlemi ekler
  - Format: `/add_transaction [kripto_kodu] [buy/sell] [miktar] [fiyat] [tarih] [komisyon]`
  - Tarih ve komisyon opsiyoneldir
- `/performance` - Portföyünüzün performansını ve kar/zarar durumunu gösterir
- `/list_transactions` - Tüm işlemlerinizi listeler
- `/delete_transaction btc 1` - Bitcoin'in 1 numaralı işlemini siler

## Kısaltmalar

Bot aşağıdaki yaygın kripto para kısaltmalarını tanır:

- btc - Bitcoin
- eth - Ethereum
- sol - Solana
- doge - Dogecoin
- xrp - Ripple
- ada - Cardano
- dot - Polkadot
- ltc - Litecoin

## İletişim

Herhangi bir sorunuz veya öneriniz varsa, lütfen GitHub üzerinden issue açın. 