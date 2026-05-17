import os

# ── Bot token from BotFather ─────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ── Admin Telegram user IDs ──────────────────────────────────────────
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "123456789").split(",")]

# ── Supported currencies ─────────────────────────────────────────────
CURRENCIES = {
    "USD": "🇺🇸 US Dollar",
    "ETB": "🇪🇹 Ethiopian Birr",
    "EUR": "🇪🇺 Euro",
    "GBP": "🇬🇧 British Pound",
    "AED": "🇦🇪 UAE Dirham",
    "SAR": "🇸🇦 Saudi Riyal",
}

# ── Escrow fee (%) ───────────────────────────────────────────────────
PLATFORM_FEE_PERCENT = 0.5   # 0.5% of trade amount

# ── Trade timeout (hours) ────────────────────────────────────────────
TRADE_TIMEOUT_HOURS = 2

# ── Database ─────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "p2p_bot.db")
