"""
Database layer – SQLite via Python's built-in sqlite3.
Tables: users, orders, trades, disputes, messages
"""

import sqlite3
import datetime
from config import DATABASE_URL

# ── Connection helper ────────────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ── Schema ───────────────────────────────────────────────────────────
def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id           INTEGER PRIMARY KEY,
            telegram_id  INTEGER UNIQUE NOT NULL,
            username     TEXT,
            full_name    TEXT,
            language     TEXT DEFAULT 'en',
            rating       REAL DEFAULT 5.0,
            total_trades INTEGER DEFAULT 0,
            is_banned    INTEGER DEFAULT 0,
            created_at   TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS orders (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            order_type   TEXT NOT NULL,   -- 'buy' | 'sell'
            currency     TEXT NOT NULL,
            amount       REAL NOT NULL,
            rate         REAL NOT NULL,
            payment_info TEXT NOT NULL,
            status       TEXT DEFAULT 'open',  -- open | trading | closed | cancelled
            created_at   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(telegram_id)
        );

        CREATE TABLE IF NOT EXISTS trades (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id       INTEGER NOT NULL,
            buyer_id       INTEGER NOT NULL,
            seller_id      INTEGER NOT NULL,
            amount         REAL NOT NULL,
            rate           REAL NOT NULL,
            currency       TEXT NOT NULL,
            status         TEXT DEFAULT 'pending',
            -- pending | payment_sent | released | cancelled | disputed
            created_at     TEXT DEFAULT (datetime('now')),
            updated_at     TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (order_id)   REFERENCES orders(id),
            FOREIGN KEY (buyer_id)   REFERENCES users(telegram_id),
            FOREIGN KEY (seller_id)  REFERENCES users(telegram_id)
        );

        CREATE TABLE IF NOT EXISTS disputes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_id    INTEGER NOT NULL,
            raised_by   INTEGER NOT NULL,
            reason      TEXT,
            status      TEXT DEFAULT 'open',  -- open | resolved
            resolution  TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (trade_id)  REFERENCES trades(id),
            FOREIGN KEY (raised_by) REFERENCES users(telegram_id)
        );
        """)
    print("✅ Database initialized")


# ────────────────────────────────────────────────────────────────────
# USER helpers
# ────────────────────────────────────────────────────────────────────
def upsert_user(telegram_id: int, username: str, full_name: str):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO users (telegram_id, username, full_name)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                username  = excluded.username,
                full_name = excluded.full_name
        """, (telegram_id, username, full_name))


def get_user(telegram_id: int):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE telegram_id=?", (telegram_id,)
        ).fetchone()


def set_language(telegram_id: int, lang: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET language=? WHERE telegram_id=?", (lang, telegram_id)
        )


def get_user_language(telegram_id: int) -> str:
    user = get_user(telegram_id)
    return user["language"] if user else "en"


def get_all_users():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()


def ban_user(telegram_id: int, ban: bool = True):
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET is_banned=? WHERE telegram_id=?", (int(ban), telegram_id)
        )


# ────────────────────────────────────────────────────────────────────
# ORDER helpers
# ────────────────────────────────────────────────────────────────────
def create_order(user_id, order_type, currency, amount, rate, payment_info):
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO orders (user_id, order_type, currency, amount, rate, payment_info)
            VALUES (?,?,?,?,?,?)
        """, (user_id, order_type, currency, amount, rate, payment_info))
        return cur.lastrowid


def get_open_orders(order_type=None, currency=None):
    query = "SELECT * FROM orders WHERE status='open'"
    params = []
    if order_type:
        query += " AND order_type=?"
        params.append(order_type)
    if currency:
        query += " AND currency=?"
        params.append(currency)
    query += " ORDER BY created_at DESC LIMIT 50"
    with get_conn() as conn:
        return conn.execute(query, params).fetchall()


def get_order(order_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()


def get_user_orders(user_id: int):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()


def update_order_status(order_id: int, status: str):
    with get_conn() as conn:
        conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))


# ────────────────────────────────────────────────────────────────────
# TRADE helpers
# ────────────────────────────────────────────────────────────────────
def create_trade(order_id, buyer_id, seller_id, amount, rate, currency):
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO trades (order_id, buyer_id, seller_id, amount, rate, currency)
            VALUES (?,?,?,?,?,?)
        """, (order_id, buyer_id, seller_id, amount, rate, currency))
        return cur.lastrowid


def get_trade(trade_id: int):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM trades WHERE id=?", (trade_id,)).fetchone()


def get_user_trades(user_id: int):
    with get_conn() as conn:
        return conn.execute("""
            SELECT * FROM trades
            WHERE buyer_id=? OR seller_id=?
            ORDER BY created_at DESC
        """, (user_id, user_id)).fetchall()


def update_trade_status(trade_id: int, status: str):
    now = datetime.datetime.utcnow().isoformat()
    with get_conn() as conn:
        conn.execute(
            "UPDATE trades SET status=?, updated_at=? WHERE id=?",
            (status, now, trade_id)
        )


def increment_trade_count(user_id: int):
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET total_trades=total_trades+1 WHERE telegram_id=?",
            (user_id,)
        )


# ────────────────────────────────────────────────────────────────────
# DISPUTE helpers
# ────────────────────────────────────────────────────────────────────
def create_dispute(trade_id, raised_by, reason):
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO disputes (trade_id, raised_by, reason)
            VALUES (?,?,?)
        """, (trade_id, raised_by, reason))
        return cur.lastrowid


def get_open_disputes():
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM disputes WHERE status='open' ORDER BY created_at"
        ).fetchall()


def resolve_dispute(dispute_id: int, resolution: str):
    with get_conn() as conn:
        conn.execute("""
            UPDATE disputes SET status='resolved', resolution=? WHERE id=?
        """, (resolution, dispute_id))


# ────────────────────────────────────────────────────────────────────
# STATS helpers
# ────────────────────────────────────────────────────────────────────
def get_stats():
    with get_conn() as conn:
        users       = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        orders      = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        open_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status='open'").fetchone()[0]
        trades      = conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0]
        completed   = conn.execute("SELECT COUNT(*) FROM trades WHERE status='released'").fetchone()[0]
        disputes    = conn.execute("SELECT COUNT(*) FROM disputes WHERE status='open'").fetchone()[0]
        return {
            "users": users, "orders": orders, "open_orders": open_orders,
            "trades": trades, "completed": completed, "disputes": disputes
        }
