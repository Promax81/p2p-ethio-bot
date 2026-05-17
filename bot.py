"""
P2P Fiat Trading Telegram Bot
Supports: USD, ETB and other fiat currencies
Languages: English & Amharic
"""

import logging
import os
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters
)
from config import BOT_TOKEN
from database import init_db
from handlers import (
    start, language_select,
    main_menu, post_order_start, post_order_currency,
    post_order_type, post_order_amount, post_order_rate,
    post_order_payment, post_order_confirm,
    browse_orders, view_order, initiate_trade,
    my_orders, cancel_order_prompt, cancel_order_confirm,
    my_trades, trade_action, dispute_start, dispute_message,
    profile, admin_menu, admin_stats, admin_users,
    admin_disputes, admin_resolve_dispute,
    handle_text, cancel_conversation
)
from states import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    # ── Post Order Conversation ──────────────────────────────────────
    post_order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(post_order_start, pattern="^post_order$")],
        states={
            ORDER_CURRENCY:  [CallbackQueryHandler(post_order_currency, pattern="^cur_")],
            ORDER_TYPE:      [CallbackQueryHandler(post_order_type,     pattern="^type_")],
            ORDER_AMOUNT:    [MessageHandler(filters.TEXT & ~filters.COMMAND, post_order_amount)],
            ORDER_RATE:      [MessageHandler(filters.TEXT & ~filters.COMMAND, post_order_rate)],
            ORDER_PAYMENT:   [MessageHandler(filters.TEXT & ~filters.COMMAND, post_order_payment)],
            ORDER_CONFIRM:   [CallbackQueryHandler(post_order_confirm,  pattern="^order_confirm|order_cancel$")],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation),
                   CallbackQueryHandler(main_menu, pattern="^main_menu$")],
        allow_reentry=True,
    )

    # ── Dispute Conversation ─────────────────────────────────────────
    dispute_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(dispute_start, pattern="^dispute_")],
        states={
            DISPUTE_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, dispute_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
        allow_reentry=True,
    )

    # ── Register handlers ────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu",  main_menu))
    app.add_handler(CallbackQueryHandler(language_select,           pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(main_menu,                 pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(browse_orders,             pattern="^browse_orders"))
    app.add_handler(CallbackQueryHandler(view_order,                pattern="^view_order_"))
    app.add_handler(CallbackQueryHandler(initiate_trade,            pattern="^trade_"))
    app.add_handler(CallbackQueryHandler(my_orders,                 pattern="^my_orders$"))
    app.add_handler(CallbackQueryHandler(cancel_order_prompt,       pattern="^cancel_order_"))
    app.add_handler(CallbackQueryHandler(cancel_order_confirm,      pattern="^confirm_cancel_"))
    app.add_handler(CallbackQueryHandler(my_trades,                 pattern="^my_trades$"))
    app.add_handler(CallbackQueryHandler(trade_action,              pattern="^(release_|confirm_payment_|cancel_trade_)"))
    app.add_handler(CallbackQueryHandler(profile,                   pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(admin_menu,                pattern="^admin_menu$"))
    app.add_handler(CallbackQueryHandler(admin_stats,               pattern="^admin_stats$"))
    app.add_handler(CallbackQueryHandler(admin_users,               pattern="^admin_users$"))
    app.add_handler(CallbackQueryHandler(admin_disputes,            pattern="^admin_disputes$"))
    app.add_handler(CallbackQueryHandler(admin_resolve_dispute,     pattern="^resolve_"))
    app.add_handler(post_order_conv)
    app.add_handler(dispute_conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot started...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
