"""
Bilingual strings: English (en) & Amharic (am)
Usage:  t(lang, "key")   or   t(lang, "key", var=val)
"""

STRINGS = {
    # ── Welcome / Language ──────────────────────────────────────────
    "welcome": {
        "en": "👋 Welcome to *P2P Fiat Exchange Bot*!\n\nBuy and sell fiat currencies safely with escrow protection.\n\nPlease choose your language:",
        "am": "👋 እንኳን ወደ *P2P ምንዛሬ ቦት* በደህና መጡ!\n\nየምንዛሬ ግብይቶችን በደህና ያካሂዱ።\n\nቋንቋ ይምረጡ:",
    },
    "language_set": {
        "en": "✅ Language set to *English*.",
        "am": "✅ ቋንቋ *አማርኛ* ሆኗል።",
    },

    # ── Main Menu ───────────────────────────────────────────────────
    "main_menu": {
        "en": "🏠 *Main Menu*\n\nWhat would you like to do?",
        "am": "🏠 *ዋና ምናሌ*\n\nምን ማድረግ ይፈልጋሉ?",
    },
    "btn_post_order":   {"en": "📢 Post Order",      "am": "📢 ትዕዛዝ አስቀምጥ"},
    "btn_browse":       {"en": "🔍 Browse Orders",   "am": "🔍 ትዕዛዞችን ያስሱ"},
    "btn_my_orders":    {"en": "📋 My Orders",       "am": "📋 የእኔ ትዕዛዞች"},
    "btn_my_trades":    {"en": "🤝 My Trades",       "am": "🤝 የእኔ ግብይቶች"},
    "btn_profile":      {"en": "👤 Profile",         "am": "👤 መገለጫ"},
    "btn_admin":        {"en": "⚙️ Admin Panel",     "am": "⚙️ አስተዳዳሪ"},
    "btn_back":         {"en": "🔙 Back",            "am": "🔙 ተመለስ"},

    # ── Post Order ──────────────────────────────────────────────────
    "choose_currency": {
        "en": "💱 Which currency do you want to trade?",
        "am": "💱 የትኛውን ምንዛሬ መስራት ይፈልጋሉ?",
    },
    "choose_type": {
        "en": "📊 Are you *buying* or *selling* {currency}?",
        "am": "📊 {currency} *መግዛት* ወይም *መሸጥ* ይፈልጋሉ?",
    },
    "btn_buy":  {"en": "🟢 Buy",  "am": "🟢 ግዛ"},
    "btn_sell": {"en": "🔴 Sell", "am": "🔴 ሸጥ"},

    "enter_amount": {
        "en": "💰 Enter the amount of *{currency}* you want to {type}:",
        "am": "💰 ምን ያህል *{currency}* {type} ይፈልጋሉ? ቁጥሩን ያስገቡ:",
    },
    "enter_rate": {
        "en": "📈 Enter your exchange rate (how much ETB per 1 {currency})?",
        "am": "📈 የምንዛሬ ዋጋ ያስገቡ (1 {currency} ስንት ብር?):",
    },
    "enter_payment": {
        "en": "🏦 Enter your payment method and account details\n_(e.g. CBE: 1000123456789, TeleBirr: 0911223344)_:",
        "am": "🏦 የክፍያ ዘዴ እና መለያ ያስገቡ\n_(ለምሳሌ CBE: 1000123456789, ቴሌብር: 0911223344)_:",
    },
    "order_preview": {
        "en": "📋 *Order Preview*\n\n"
              "Type:    {order_type}\n"
              "Amount:  {amount} {currency}\n"
              "Rate:    {rate} ETB / {currency}\n"
              "Payment: {payment}\n\n"
              "Confirm?",
        "am": "📋 *ትዕዛዝ ቅድመ ዕይታ*\n\n"
              "አይነት:    {order_type}\n"
              "መጠን:  {amount} {currency}\n"
              "ዋጋ:    {rate} ብር / {currency}\n"
              "ክፍያ: {payment}\n\n"
              "ያረጋግጡ?",
    },
    "btn_confirm":      {"en": "✅ Confirm",  "am": "✅ አረጋግጥ"},
    "btn_cancel_order": {"en": "❌ Cancel",   "am": "❌ ሰርዝ"},
    "order_posted": {
        "en": "✅ Your order has been posted successfully!\nOrder ID: #{order_id}",
        "am": "✅ ትዕዛዝዎ ተልኳል!\nትዕዛዝ ቁጥር: #{order_id}",
    },
    "invalid_number": {
        "en": "⚠️ Please enter a valid number.",
        "am": "⚠️ እባክዎን ትክክለኛ ቁጥር ያስገቡ።",
    },

    # ── Browse Orders ───────────────────────────────────────────────
    "no_orders": {
        "en": "😔 No open orders found at the moment.",
        "am": "😔 አሁን ምንም ክፍት ትዕዛዝ የለም።",
    },
    "order_list_header": {
        "en": "📃 *Available Orders*\n\nTap an order to view details:",
        "am": "📃 *ያሉ ትዕዛዞች*\n\nዝርዝር ለማየት ትዕዛዙን ይንኩ:",
    },
    "order_detail": {
        "en": "📄 *Order #{order_id}*\n\n"
              "👤 Trader:    @{username}\n"
              "📊 Type:      {order_type}\n"
              "💰 Amount:    {amount} {currency}\n"
              "📈 Rate:      {rate} ETB / {currency}\n"
              "🏦 Payment:  {payment}\n"
              "⭐ Rating:   {rating}/5 ({trades} trades)\n\n"
              "Do you want to trade?",
        "am": "📄 *ትዕዛዝ #{order_id}*\n\n"
              "👤 ነጋዴ:      @{username}\n"
              "📊 አይነት:    {order_type}\n"
              "💰 መጠን:    {amount} {currency}\n"
              "📈 ዋጋ:      {rate} ብር / {currency}\n"
              "🏦 ክፍያ:   {payment}\n"
              "⭐ ደረጃ:   {rating}/5 ({trades} ግብይቶች)\n\n"
              "መስራት ይፈልጋሉ?",
    },
    "btn_trade": {"en": "🤝 Start Trade", "am": "🤝 ግብይት ጀምር"},
    "cannot_trade_own": {
        "en": "⛔ You cannot trade your own order.",
        "am": "⛔ የራስዎን ትዕዛዝ መሥራት አይችሉም።",
    },

    # ── Trade ───────────────────────────────────────────────────────
    "trade_started": {
        "en": "🤝 *Trade Started!*\n\n"
              "Trade ID: #{trade_id}\n"
              "Amount:   {amount} {currency}\n"
              "Rate:     {rate} ETB\n\n"
              "💡 *Next step (Buyer):* Send payment to the seller's account and tap *Payment Sent*.\n"
              "💡 *Next step (Seller):* Wait for buyer to send payment, then verify and tap *Release*.",
        "am": "🤝 *ግብይት ተጀምሯል!*\n\n"
              "ግብይት ቁጥር: #{trade_id}\n"
              "መጠን:   {amount} {currency}\n"
              "ዋጋ:     {rate} ብር\n\n"
              "💡 *ቀጣይ እርምጃ (ገዥ):* ለሻጩ ይክፈሉ፣ ከዚያ *ክፍያ ተልኳል* ይንኩ።\n"
              "💡 *ቀጣይ እርምጃ (ሻጭ):* ክፍያ ሲደርስ ያረጋግጡ ከዚያ *ፍቀድ* ይንኩ።",
    },
    "btn_payment_sent":  {"en": "💸 Payment Sent",    "am": "💸 ክፍያ ተልኳል"},
    "btn_release":       {"en": "✅ Release Funds",   "am": "✅ ፍቀድ"},
    "btn_dispute":       {"en": "⚠️ Raise Dispute",  "am": "⚠️ ቅሬታ አቅርብ"},
    "btn_cancel_trade":  {"en": "❌ Cancel Trade",    "am": "❌ ግብይት ሰርዝ"},

    "payment_marked": {
        "en": "✅ Payment marked as sent. Waiting for seller to confirm.",
        "am": "✅ ክፍያ እንደተላከ ምልክት ተደርጓል። ሻጩ ሲያረጋግጥ ይጠብቁ።",
    },
    "funds_released": {
        "en": "🎉 *Trade Complete!*\nFunds have been released. Please rate your partner.",
        "am": "🎉 *ግብይት ተጠናቋል!*\nክፍያ ፈቅዶ ተልኳል። አጋርዎን ይደምሩ።",
    },
    "trade_cancelled": {
        "en": "❌ Trade has been cancelled.",
        "am": "❌ ግብይቱ ተሰርዟል።",
    },
    "notify_seller_payment": {
        "en": "💸 Buyer has marked payment as sent for Trade #{trade_id}.\nPlease verify and release funds.",
        "am": "💸 ገዥው ለትዕዛዝ #{trade_id} ክፍያ ልኳል ብሏል።\nያረጋግጡ ከዚያ ፍቀዱ።",
    },
    "notify_buyer_released": {
        "en": "🎉 Seller has released funds for Trade #{trade_id}. Trade complete!",
        "am": "🎉 ሻጩ ለትዕዛዝ #{trade_id} ክፍያ ፈቅዷል። ግብይቱ ተጠናቋል!",
    },

    # ── Dispute ─────────────────────────────────────────────────────
    "dispute_reason": {
        "en": "⚠️ *Raise Dispute*\n\nPlease describe your issue briefly:",
        "am": "⚠️ *ቅሬታ አቅርብ*\n\nችግርዎን አጭር አድርገው ይግለጹ:",
    },
    "dispute_filed": {
        "en": "✅ Dispute filed. An admin will review shortly.\nDispute ID: #{dispute_id}",
        "am": "✅ ቅሬታ ቀርቧል። አስተዳዳሪ ብዙም ሳይቆይ ያየዋል።\nቅሬታ ቁጥር: #{dispute_id}",
    },
    "admin_dispute_notify": {
        "en": "🚨 *New Dispute #{dispute_id}*\nTrade: #{trade_id}\nRaised by: {username}\nReason: {reason}",
        "am": "🚨 *አዲስ ቅሬታ #{dispute_id}*\nግብይት: #{trade_id}\nያቀረበ: {username}\nምክንያት: {reason}",
    },

    # ── My Orders ───────────────────────────────────────────────────
    "my_orders_empty": {
        "en": "📭 You have no orders yet.",
        "am": "📭 ምንም ትዕዛዝ የለዎትም።",
    },
    "my_orders_header": {
        "en": "📋 *Your Orders:*",
        "am": "📋 *የእርስዎ ትዕዛዞች:*",
    },
    "btn_cancel_this": {"en": "🗑 Cancel Order #{id}", "am": "🗑 ትዕዛዝ #{id} ሰርዝ"},
    "cancel_order_confirm": {
        "en": "❓ Cancel Order #{order_id}?",
        "am": "❓ ትዕዛዝ #{order_id} ይሰረዝ?",
    },
    "order_cancelled": {
        "en": "✅ Order #{order_id} cancelled.",
        "am": "✅ ትዕዛዝ #{order_id} ተሰርዟል።",
    },

    # ── My Trades ───────────────────────────────────────────────────
    "my_trades_empty": {
        "en": "📭 You have no trades yet.",
        "am": "📭 ምንም ግብይት የለዎትም።",
    },
    "my_trades_header": {
        "en": "🤝 *Your Trades:*",
        "am": "🤝 *የእርስዎ ግብይቶች:*",
    },

    # ── Profile ─────────────────────────────────────────────────────
    "profile": {
        "en": "👤 *Your Profile*\n\n"
              "Name:        {full_name}\n"
              "Username:    @{username}\n"
              "Language:    {language}\n"
              "Rating:      ⭐ {rating}/5\n"
              "Total Trades:{trades}\n"
              "Joined:      {joined}",
        "am": "👤 *የእርስዎ መገለጫ*\n\n"
              "ስም:          {full_name}\n"
              "የተጠቃሚ ስም:   @{username}\n"
              "ቋንቋ:          {language}\n"
              "ደረጃ:         ⭐ {rating}/5\n"
              "ጠቅላላ ግብይቶች:{trades}\n"
              "የተቀላቀሉበት:  {joined}",
    },

    # ── Admin ───────────────────────────────────────────────────────
    "admin_menu": {
        "en": "⚙️ *Admin Panel*",
        "am": "⚙️ *አስተዳዳሪ ፓኔል*",
    },
    "btn_stats":        {"en": "📊 Statistics",    "am": "📊 ስታቲስቲክስ"},
    "btn_users":        {"en": "👥 Users",         "am": "👥 ተጠቃሚዎች"},
    "btn_disputes":     {"en": "⚠️ Disputes",     "am": "⚠️ ቅሬታዎች"},
    "admin_stats": {
        "en": "📊 *Bot Statistics*\n\n"
              "👥 Users:           {users}\n"
              "📋 Total Orders:    {orders}\n"
              "📂 Open Orders:     {open_orders}\n"
              "🤝 Total Trades:    {trades}\n"
              "✅ Completed:       {completed}\n"
              "⚠️ Open Disputes:  {disputes}",
        "am": "📊 *ቦት ስታቲስቲክስ*\n\n"
              "👥 ተጠቃሚዎች:        {users}\n"
              "📋 ጠቅላላ ትዕዛዞች:   {orders}\n"
              "📂 ክፍት ትዕዛዞች:    {open_orders}\n"
              "🤝 ጠቅላላ ግብይቶች:   {trades}\n"
              "✅ የተጠናቀቁ:        {completed}\n"
              "⚠️ ክፍት ቅሬታዎች:  {disputes}",
    },
    "no_disputes": {
        "en": "✅ No open disputes.",
        "am": "✅ ምንም ክፍት ቅሬታ የለም።",
    },
    "resolve_btn":  {"en": "✅ Resolve #{id}", "am": "✅ ፍታ #{id}"},

    # ── Generic ─────────────────────────────────────────────────────
    "cancelled": {
        "en": "Operation cancelled.",
        "am": "ሥራው ተሰርዟል።",
    },
    "not_authorized": {
        "en": "⛔ You are not authorized.",
        "am": "⛔ ፈቃድ የለዎትም።",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Return translated string, falling back to English."""
    lang = lang if lang in ("en", "am") else "en"
    template = STRINGS.get(key, {}).get(lang) or STRINGS.get(key, {}).get("en", key)
    try:
        return template.format(**kwargs)
    except KeyError:
        return template
