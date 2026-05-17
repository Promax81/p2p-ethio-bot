"""
All Telegram handlers for the P2P bot.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode

import database as db
from strings import t
from config import CURRENCIES, ADMIN_IDS
from states import *

# ── Helpers ──────────────────────────────────────────────────────────

def lang(update: Update) -> str:
    uid = update.effective_user.id
    return db.get_user_language(uid)


def kb(buttons: list) -> InlineKeyboardMarkup:
    """Build InlineKeyboardMarkup from list of (text, callback_data) rows."""
    return InlineKeyboardMarkup(buttons)


async def send(update: Update, text: str, reply_markup=None, edit=False):
    md = ParseMode.MARKDOWN
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=md, reply_markup=reply_markup)
    else:
        target = update.message or update.callback_query.message
        await target.reply_text(text, parse_mode=md, reply_markup=reply_markup)


# ── /start ────────────────────────────────────────────────────────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.upsert_user(user.id, user.username or "", user.full_name or "")
    buttons = [[
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇪🇹 አማርኛ",  callback_data="lang_am"),
    ]]
    await update.message.reply_text(
        "👋 Welcome / እንኳን ደህና መጡ!\n\nChoose language / ቋንቋ ይምረጡ:",
        reply_markup=kb(buttons)
    )


async def language_select(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chosen = query.data.split("_")[1]   # 'en' or 'am'
    db.set_language(update.effective_user.id, chosen)
    await send(update, t(chosen, "language_set"), edit=True)
    await main_menu(update, ctx)


# ── Main Menu ────────────────────────────────────────────────────────

async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = lang(update)
    uid = update.effective_user.id
    buttons = [
        [InlineKeyboardButton(t(lg, "btn_post_order"), callback_data="post_order"),
         InlineKeyboardButton(t(lg, "btn_browse"),     callback_data="browse_orders")],
        [InlineKeyboardButton(t(lg, "btn_my_orders"),  callback_data="my_orders"),
         InlineKeyboardButton(t(lg, "btn_my_trades"),  callback_data="my_trades")],
        [InlineKeyboardButton(t(lg, "btn_profile"),    callback_data="profile")],
    ]
    if uid in ADMIN_IDS:
        buttons.append([InlineKeyboardButton(t(lg, "btn_admin"), callback_data="admin_menu")])
    await send(update, t(lg, "main_menu"), kb(buttons), edit=bool(update.callback_query))


# ── Post Order ───────────────────────────────────────────────────────

async def post_order_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    buttons = [[InlineKeyboardButton(f"{v}", callback_data=f"cur_{k}")] for k, v in CURRENCIES.items()]
    buttons.append([InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")])
    await send(update, t(lg, "choose_currency"), kb(buttons), edit=True)
    return ORDER_CURRENCY


async def post_order_currency(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    ctx.user_data["currency"] = update.callback_query.data.split("_")[1]
    lg = lang(update)
    cur = ctx.user_data["currency"]
    buttons = [
        [InlineKeyboardButton(t(lg, "btn_buy"),  callback_data="type_buy"),
         InlineKeyboardButton(t(lg, "btn_sell"), callback_data="type_sell")],
    ]
    await send(update, t(lg, "choose_type", currency=cur), kb(buttons), edit=True)
    return ORDER_TYPE


async def post_order_type(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    ctx.user_data["order_type"] = update.callback_query.data.split("_")[1]
    lg = lang(update)
    cur = ctx.user_data["currency"]
    otype = ctx.user_data["order_type"]
    await send(update, t(lg, "enter_amount", currency=cur, type=otype), edit=True)
    return ORDER_AMOUNT


async def post_order_amount(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = lang(update)
    try:
        ctx.user_data["amount"] = float(update.message.text.replace(",", ""))
    except ValueError:
        await update.message.reply_text(t(lg, "invalid_number"))
        return ORDER_AMOUNT
    cur = ctx.user_data["currency"]
    await update.message.reply_text(t(lg, "enter_rate", currency=cur))
    return ORDER_RATE


async def post_order_rate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = lang(update)
    try:
        ctx.user_data["rate"] = float(update.message.text.replace(",", ""))
    except ValueError:
        await update.message.reply_text(t(lg, "invalid_number"))
        return ORDER_RATE
    await update.message.reply_text(t(lg, "enter_payment"))
    return ORDER_PAYMENT


async def post_order_payment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = lang(update)
    ctx.user_data["payment"] = update.message.text
    ud = ctx.user_data
    otype_label = "BUY 🟢" if ud["order_type"] == "buy" else "SELL 🔴"
    preview = t(lg, "order_preview",
                order_type=otype_label,
                amount=ud["amount"],
                currency=ud["currency"],
                rate=ud["rate"],
                payment=ud["payment"])
    buttons = [[
        InlineKeyboardButton(t(lg, "btn_confirm"),      callback_data="order_confirm"),
        InlineKeyboardButton(t(lg, "btn_cancel_order"), callback_data="order_cancel"),
    ]]
    await update.message.reply_text(preview, parse_mode=ParseMode.MARKDOWN, reply_markup=kb(buttons))
    return ORDER_CONFIRM


async def post_order_confirm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    if update.callback_query.data == "order_cancel":
        await send(update, t(lg, "cancelled"), edit=True)
        await main_menu(update, ctx)
        return ConversationHandler.END
    ud = ctx.user_data
    uid = update.effective_user.id
    order_id = db.create_order(uid, ud["order_type"], ud["currency"],
                               ud["amount"], ud["rate"], ud["payment"])
    await send(update, t(lg, "order_posted", order_id=order_id), edit=True)
    await main_menu(update, ctx)
    return ConversationHandler.END


# ── Browse Orders ─────────────────────────────────────────────────────

async def browse_orders(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer()
    lg = lang(update)
    orders = db.get_open_orders()
    if not orders:
        buttons = [[InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")]]
        await send(update, t(lg, "no_orders"), kb(buttons), edit=bool(update.callback_query))
        return
    buttons = []
    for o in orders:
        label = f"{'🟢 BUY' if o['order_type']=='buy' else '🔴 SELL'} {o['amount']} {o['currency']} @ {o['rate']} ETB"
        buttons.append([InlineKeyboardButton(label, callback_data=f"view_order_{o['id']}")])
    buttons.append([InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")])
    await send(update, t(lg, "order_list_header"), kb(buttons), edit=bool(update.callback_query))


async def view_order(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    order_id = int(update.callback_query.data.split("_")[-1])
    o = db.get_order(order_id)
    if not o:
        await browse_orders(update, ctx)
        return
    owner = db.get_user(o["user_id"])
    text = t(lg, "order_detail",
             order_id=o["id"],
             username=owner["username"] or "N/A",
             order_type=o["order_type"].upper(),
             amount=o["amount"],
             currency=o["currency"],
             rate=o["rate"],
             payment=o["payment_info"],
             rating=owner["rating"],
             trades=owner["total_trades"])
    buttons = []
    if o["user_id"] != update.effective_user.id:
        buttons.append([InlineKeyboardButton(t(lg, "btn_trade"), callback_data=f"trade_{order_id}")])
    buttons.append([InlineKeyboardButton(t(lg, "btn_back"), callback_data="browse_orders")])
    await send(update, text, kb(buttons), edit=True)


# ── Initiate Trade ────────────────────────────────────────────────────

async def initiate_trade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    order_id = int(update.callback_query.data.split("_")[1])
    o = db.get_order(order_id)
    uid = update.effective_user.id

    if o["user_id"] == uid:
        await send(update, t(lg, "cannot_trade_own"), edit=True)
        return

    # Determine buyer/seller
    if o["order_type"] == "sell":
        buyer_id, seller_id = uid, o["user_id"]
    else:
        buyer_id, seller_id = o["user_id"], uid

    trade_id = db.create_trade(order_id, buyer_id, seller_id,
                               o["amount"], o["rate"], o["currency"])
    db.update_order_status(order_id, "trading")

    text = t(lg, "trade_started",
             trade_id=trade_id,
             amount=o["amount"],
             currency=o["currency"],
             rate=o["rate"])

    trade_buttons = _trade_buttons(lg, trade_id, uid, buyer_id, seller_id, "pending")
    await send(update, text, trade_buttons, edit=True)

    # Notify the order owner
    partner_id = o["user_id"]
    partner_lang = db.get_user_language(partner_id)
    partner_text = t(partner_lang, "trade_started",
                     trade_id=trade_id,
                     amount=o["amount"],
                     currency=o["currency"],
                     rate=o["rate"])
    partner_buttons = _trade_buttons(partner_lang, trade_id, partner_id, buyer_id, seller_id, "pending")
    try:
        await ctx.bot.send_message(partner_id, partner_text,
                                   parse_mode=ParseMode.MARKDOWN,
                                   reply_markup=partner_buttons)
    except Exception:
        pass


def _trade_buttons(lg, trade_id, viewer_id, buyer_id, seller_id, status):
    buttons = []
    if status == "pending" and viewer_id == buyer_id:
        buttons.append([InlineKeyboardButton(t(lg, "btn_payment_sent"),
                                             callback_data=f"confirm_payment_{trade_id}")])
    if status == "payment_sent" and viewer_id == seller_id:
        buttons.append([InlineKeyboardButton(t(lg, "btn_release"),
                                             callback_data=f"release_{trade_id}")])
    buttons.append([InlineKeyboardButton(t(lg, "btn_dispute"),
                                         callback_data=f"dispute_{trade_id}")])
    buttons.append([InlineKeyboardButton(t(lg, "btn_cancel_trade"),
                                         callback_data=f"cancel_trade_{trade_id}")])
    return kb(buttons)


# ── Trade Actions ─────────────────────────────────────────────────────

async def trade_action(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    data = update.callback_query.data
    uid = update.effective_user.id

    if data.startswith("confirm_payment_"):
        trade_id = int(data.split("_")[-1])
        trade = db.get_trade(trade_id)
        db.update_trade_status(trade_id, "payment_sent")
        await send(update, t(lg, "payment_marked"), edit=True)
        # Notify seller
        seller_lang = db.get_user_language(trade["seller_id"])
        try:
            await ctx.bot.send_message(
                trade["seller_id"],
                t(seller_lang, "notify_seller_payment", trade_id=trade_id),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=_trade_buttons(seller_lang, trade_id,
                                            trade["seller_id"],
                                            trade["buyer_id"],
                                            trade["seller_id"], "payment_sent")
            )
        except Exception:
            pass

    elif data.startswith("release_"):
        trade_id = int(data.split("_")[-1])
        trade = db.get_trade(trade_id)
        db.update_trade_status(trade_id, "released")
        db.update_order_status(trade["order_id"], "closed")
        db.increment_trade_count(trade["buyer_id"])
        db.increment_trade_count(trade["seller_id"])
        await send(update, t(lg, "funds_released"), edit=True)
        # Notify buyer
        buyer_lang = db.get_user_language(trade["buyer_id"])
        try:
            await ctx.bot.send_message(
                trade["buyer_id"],
                t(buyer_lang, "notify_buyer_released", trade_id=trade_id),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            pass

    elif data.startswith("cancel_trade_"):
        trade_id = int(data.split("_")[-1])
        trade = db.get_trade(trade_id)
        db.update_trade_status(trade_id, "cancelled")
        db.update_order_status(trade["order_id"], "open")  # re-open order
        await send(update, t(lg, "trade_cancelled"), edit=True)


# ── Dispute ───────────────────────────────────────────────────────────

async def dispute_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    trade_id = int(update.callback_query.data.split("_")[-1])
    ctx.user_data["dispute_trade_id"] = trade_id
    await send(update, t(lg, "dispute_reason"), edit=True)
    return DISPUTE_MSG


async def dispute_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = lang(update)
    uid = update.effective_user.id
    trade_id = ctx.user_data.get("dispute_trade_id")
    reason = update.message.text
    dispute_id = db.create_dispute(trade_id, uid, reason)
    db.update_trade_status(trade_id, "disputed")
    await update.message.reply_text(t(lg, "dispute_filed", dispute_id=dispute_id),
                                    parse_mode=ParseMode.MARKDOWN)
    # Notify admins
    user = db.get_user(uid)
    for admin_id in ADMIN_IDS:
        admin_lang = db.get_user_language(admin_id)
        try:
            await ctx.bot.send_message(
                admin_id,
                t(admin_lang, "admin_dispute_notify",
                  dispute_id=dispute_id, trade_id=trade_id,
                  username=user["username"] or str(uid), reason=reason),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            pass
    return ConversationHandler.END


# ── My Orders ─────────────────────────────────────────────────────────

async def my_orders(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    uid = update.effective_user.id
    orders = db.get_user_orders(uid)
    if not orders:
        buttons = [[InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")]]
        await send(update, t(lg, "my_orders_empty"), kb(buttons), edit=True)
        return
    text = t(lg, "my_orders_header") + "\n\n"
    buttons = []
    for o in orders:
        text += f"#{o['id']} | {o['order_type'].upper()} {o['amount']} {o['currency']} @ {o['rate']} — *{o['status']}*\n"
        if o["status"] == "open":
            buttons.append([InlineKeyboardButton(
                t(lg, "btn_cancel_this", id=o["id"]),
                callback_data=f"cancel_order_{o['id']}"
            )])
    buttons.append([InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")])
    await send(update, text, kb(buttons), edit=True)


async def cancel_order_prompt(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    order_id = int(update.callback_query.data.split("_")[-1])
    buttons = [[
        InlineKeyboardButton(t(lg, "btn_confirm"),      callback_data=f"confirm_cancel_{order_id}"),
        InlineKeyboardButton(t(lg, "btn_cancel_order"), callback_data="my_orders"),
    ]]
    await send(update, t(lg, "cancel_order_confirm", order_id=order_id), kb(buttons), edit=True)


async def cancel_order_confirm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    order_id = int(update.callback_query.data.split("_")[-1])
    db.update_order_status(order_id, "cancelled")
    await send(update, t(lg, "order_cancelled", order_id=order_id), edit=True)
    await main_menu(update, ctx)


# ── My Trades ─────────────────────────────────────────────────────────

async def my_trades(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    uid = update.effective_user.id
    trades = db.get_user_trades(uid)
    if not trades:
        buttons = [[InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")]]
        await send(update, t(lg, "my_trades_empty"), kb(buttons), edit=True)
        return
    text = t(lg, "my_trades_header") + "\n\n"
    buttons = []
    for tr in trades:
        role = "🛒 Buyer" if tr["buyer_id"] == uid else "💰 Seller"
        text += (f"#{tr['id']} | {role} | {tr['amount']} {tr['currency']} "
                 f"@ {tr['rate']} — *{tr['status']}*\n")
        if tr["status"] in ("pending", "payment_sent"):
            other = tr["seller_id"] if tr["buyer_id"] == uid else tr["buyer_id"]
            buttons.append([InlineKeyboardButton(
                f"📋 Trade #{tr['id']}",
                callback_data=f"trade_{tr['order_id']}"
            )])
    buttons.append([InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")])
    await send(update, text, kb(buttons), edit=True)


# ── Profile ───────────────────────────────────────────────────────────

async def profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    uid = update.effective_user.id
    user = db.get_user(uid)
    lang_label = "English 🇬🇧" if user["language"] == "en" else "አማርኛ 🇪🇹"
    text = t(lg, "profile",
             full_name=user["full_name"] or "N/A",
             username=user["username"] or "N/A",
             language=lang_label,
             rating=user["rating"],
             trades=user["total_trades"],
             joined=user["created_at"][:10])
    buttons = [
        [InlineKeyboardButton("🌐 Change Language", callback_data="lang_switch")],
        [InlineKeyboardButton(t(lg, "btn_back"), callback_data="main_menu")],
    ]
    await send(update, text, kb(buttons), edit=True)


# ── Admin ─────────────────────────────────────────────────────────────

def _require_admin(uid):
    return uid in ADMIN_IDS


async def admin_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    uid = update.effective_user.id
    if not _require_admin(uid):
        await send(update, t(lang(update), "not_authorized"), edit=True)
        return
    lg = lang(update)
    buttons = [
        [InlineKeyboardButton(t(lg, "btn_stats"),    callback_data="admin_stats"),
         InlineKeyboardButton(t(lg, "btn_users"),    callback_data="admin_users")],
        [InlineKeyboardButton(t(lg, "btn_disputes"), callback_data="admin_disputes")],
        [InlineKeyboardButton(t(lg, "btn_back"),     callback_data="main_menu")],
    ]
    await send(update, t(lg, "admin_menu"), kb(buttons), edit=True)


async def admin_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    s = db.get_stats()
    text = t(lg, "admin_stats", **s)
    buttons = [[InlineKeyboardButton(t(lg, "btn_back"), callback_data="admin_menu")]]
    await send(update, text, kb(buttons), edit=True)


async def admin_users(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    users = db.get_all_users()
    text = f"👥 *Users ({len(users)})*\n\n"
    for u in users[:20]:
        status = "🚫" if u["is_banned"] else "✅"
        text += f"{status} @{u['username'] or 'N/A'} — {u['total_trades']} trades — ⭐{u['rating']}\n"
    buttons = [[InlineKeyboardButton(t(lg, "btn_back"), callback_data="admin_menu")]]
    await send(update, text, kb(buttons), edit=True)


async def admin_disputes(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    disputes = db.get_open_disputes()
    if not disputes:
        buttons = [[InlineKeyboardButton(t(lg, "btn_back"), callback_data="admin_menu")]]
        await send(update, t(lg, "no_disputes"), kb(buttons), edit=True)
        return
    text = "⚠️ *Open Disputes*\n\n"
    buttons = []
    for d in disputes:
        text += f"#{d['id']} | Trade #{d['trade_id']} — {d['reason'][:60]}\n"
        buttons.append([InlineKeyboardButton(
            t(lg, "resolve_btn", id=d["id"]),
            callback_data=f"resolve_{d['id']}_buyer"
        )])
    buttons.append([InlineKeyboardButton(t(lg, "btn_back"), callback_data="admin_menu")])
    await send(update, text, kb(buttons), edit=True)


async def admin_resolve_dispute(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lg = lang(update)
    parts = update.callback_query.data.split("_")
    dispute_id = int(parts[1])
    resolution = parts[2] if len(parts) > 2 else "resolved by admin"
    db.resolve_dispute(dispute_id, resolution)
    await send(update, f"✅ Dispute #{dispute_id} resolved.", edit=True)
    await admin_disputes(update, ctx)


# ── Fallbacks ─────────────────────────────────────────────────────────

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await main_menu(update, ctx)


async def cancel_conversation(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = lang(update)
    await update.message.reply_text(t(lg, "cancelled"))
    return ConversationHandler.END
