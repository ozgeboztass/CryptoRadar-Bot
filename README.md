# 🚀 Kripto Para Telegram Botu

Gelişmiş kripto para takibi ve portföy yönetimi sağlayan Telegram botu.

## 📋 İçindekiler
- [Özellikler](#özellikler)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Desteklenen Kripto Paralar](#desteklenen-kripto-paralar)
- [Katkıda Bulunma](#katkıda-bulunma)
- [İletişim](#iletişim)

## ✨ Özellikler

### 💹 Fiyat Sorgulama
- `/price [kripto_kodu]` ile anlık fiyat görüntüleme
  ```
  Örnek: /price btc
  ```
- Çoklu kripto para sorgulama
  ```
  Örnek: /price btc eth sol
  ```
- `/top` komutu ile en büyük 10 kripto parayı listeleme
- `/list` komutu ile popüler kripto paraları görüntüleme

### ⭐ Favori Yönetimi
- `/add [kripto_kodu]` ile favorilere ekleme
- `/favorites` ile favori listesini görüntüleme
- `/remove [kripto_kodu]` ile favorilerden çıkarma

### 📊 Portföy Takibi
- `/portfolio` ile portföy görüntüleme
- `/add_transaction` ile işlem ekleme
  ```
  Format: /add_transaction [kripto_kodu] [alım/satım] [miktar] [fiyat] [tarih] [komisyon]
  Örnek: /add_transaction btc buy 0.05 35000 2023-11-20 10
  ```
- `/performance` ile kar/zarar analizi
- `/list_transactions` ile işlem geçmişi
- `/delete_transaction` ile işlem silme

## 🛠️ Gereksinimler

- Python 3.7+
- python-telegram-bot
- pycoingecko
- python-dotenv
- requests

## ⚙️ Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/username/telegrambot.git
cd telegrambot
```

2. Sanal ortam oluşturun:
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyası oluşturun:
```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

5. Botu çalıştırın:
```bash
python bot.py
```

## 📱 Kullanım

### 🔰 Temel Komutlar
| Komut | Açıklama |
|-------|-----------|
| `/start` | Botu başlatır ve kullanım bilgilerini gösterir |
| `/help` | Tüm komutların detaylı açıklamalarını gösterir |

### 💰 Fiyat Komutları
| Komut | Açıklama |
|-------|-----------|
| `/price btc` | Bitcoin fiyatını gösterir |
| `/price btc eth` | Belirtilen kripto paraların fiyatlarını gösterir |
| `/top` | En büyük 10 kripto parayı listeler |
| `/list` | Popüler kripto paraları listeler |

### ⭐ Favori Komutları
| Komut | Açıklama |
|-------|-----------|
| `/add sol` | Solana'yı favorilere ekler |
| `/favorites` | Favori kripto paraları listeler |
| `/remove sol` | Solana'yı favorilerden kaldırır |

### 📈 Portföy Komutları
| Komut | Açıklama |
|-------|-----------|
| `/portfolio` | Portföy durumunu gösterir |
| `/add_transaction` | Yeni işlem ekler |
| `/performance` | Portföy performansını gösterir |
| `/list_transactions` | Tüm işlemleri listeler |
| `/delete_transaction` | İşlem siler |

## 🪙 Desteklenen Kripto Paralar

| Kısaltma | Kripto Para |
|----------|-------------|
| BTC | Bitcoin |
| ETH | Ethereum |
| SOL | Solana |
| DOGE | Dogecoin |
| XRP | Ripple |
| ADA | Cardano |
| DOT | Polkadot |
| LTC | Litecoin |
| BNB | Binance Coin |
| USDT | Tether |
| USDC | USD Coin |
| MATIC | Polygon |
| LINK | Chainlink |
| UNI | Uniswap |
| AVAX | Avalanche |

## 🤝 Katkıda Bulunma

1. Bu repoyu forklayın
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Sorularınız veya önerileriniz için:
- GitHub Issues üzerinden bildirim oluşturabilirsiniz
- [Telegram Grubumuza](https://t.me/your_support_group) katılabilirsiniz

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

---
⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
