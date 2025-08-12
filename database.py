import aiosqlite import asyncio from datetime 
import datetime class Database:
    def __init__(self, path='bot.db'): 
        self.path = path self._lock = 
        asyncio.Lock()
    async def init(self): async with 
        aiosqlite.connect(self.path) as db:
            await db.executescript(\"\"\"\ 
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, username TEXT, 
    fullname TEXT, joined_date TEXT
); CREATE TABLE IF NOT EXISTS movies ( code 
    INTEGER PRIMARY KEY, title TEXT, format 
    TEXT, language TEXT, file_id TEXT, views 
    INTEGER DEFAULT 0, is_deleted INTEGER 
    DEFAULT 0
); CREATE TABLE IF NOT EXISTS channels ( 
    username TEXT PRIMARY KEY
); CREATE TABLE IF NOT EXISTS ads ( id INTEGER 
    PRIMARY KEY AUTOINCREMENT, image_file_id 
    TEXT, text TEXT, button_text TEXT, 
    button_url TEXT, schedule_time TEXT, 
    repeat_count INTEGER DEFAULT 0
); CREATE TABLE IF NOT EXISTS admins ( user_id 
    INTEGER PRIMARY KEY
); CREATE TABLE IF NOT EXISTS settings ( key 
    TEXT PRIMARY KEY, value TEXT
); \"\"\") await db.commit() async def 
    execute(self, query, params=(), 
    fetch=False, fetchone=False):
        async with self._lock: async with 
            aiosqlite.connect(self.path) as 
            db:
                cur = await db.execute(query, 
                params) if fetch:
                    rows = await 
                    cur.fetchall() await 
                    cur.close() return rows
                if fetchone: row = await 
                    cur.fetchone() await 
                    cur.close() return row
                await db.commit() return None
    # Users
    async def add_user(self, user_id, 
    username, fullname):
        await self.execute( "INSERT OR IGNORE 
            INTO users (id, username, 
            fullname, joined_date) VALUES (?, 
            ?, ?, ?)", (user_id, username or 
            '', fullname or '', 
            datetime.utcnow().isoformat())
        ) async def count_users(self): row = 
        await self.execute("SELECT COUNT(*) 
        FROM users", fetchone=True) return 
        row[0] if row else 0
    async def get_all_user_ids(self): rows = 
        await self.execute("SELECT id FROM 
        users", fetch=True) return [r[0] for r 
        in rows]
    # Movies
    async def add_movie(self, title, fmt, 
    lang, file_id):
        rows = await self.execute("SELECT code 
        FROM movies ORDER BY code", 
        fetch=True) codes = [r[0] for r in 
        rows] code = 1 for c in codes:
            if c == code: code += 1 else: 
                break
        await self.execute( "INSERT INTO 
            movies (code, title, format, 
            language, file_id, views, 
            is_deleted) VALUES (?, ?, ?, ?, ?, 
            0, 0)", (code, title, fmt, lang, 
            file_id)
        ) return code async def 
    get_movie(self, code):
        return await self.execute("SELECT 
        code, title, format, language, 
        file_id, views, is_deleted FROM movies 
        WHERE code = ?", (code,), 
        fetchone=True)
    async def soft_delete_movie(self, code): 
        await self.execute("UPDATE movies SET 
        is_deleted = 1 WHERE code = ?", 
        (code,))
    async def increment_views(self, code): 
        await self.execute("UPDATE movies SET 
        views = views + 1 WHERE code = ?", 
        (code,))
    async def count_movies(self): row = await 
        self.execute("SELECT COUNT(*) FROM 
        movies WHERE is_deleted = 0", 
        fetchone=True) return row[0] if row 
        else 0
    async def get_total_views(self): row = 
        await self.execute("SELECT SUM(views) 
        FROM movies", fetchone=True) return 
        row[0] if row and row[0] is not None 
        else 0
    # Channels
    async def add_channel(self, username): 
        username = username.lstrip('@') await 
        self.execute("INSERT OR IGNORE INTO 
        channels (username) VALUES (?)", 
        (username,))
    async def remove_channel(self, username): 
        username = username.lstrip('@') await 
        self.execute("DELETE FROM channels 
        WHERE username = ?", (username,))
    async def list_channels(self): rows = 
        await self.execute("SELECT username 
        FROM channels", fetch=True) return 
        [r[0] for r in rows]
    # Ads
    async def add_ad(self, image_file_id, 
    text, button_text, button_url, 
    schedule_time, repeat_count):
        await self.execute("INSERT INTO ads 
        (image_file_id, text, button_text, 
        button_url, schedule_time, 
        repeat_count) VALUES (?, ?, ?, ?, ?, 
        ?)", (image_file_id, text, 
        button_text, button_url, 
        schedule_time, repeat_count))
    async def list_ads(self): return await 
        self.execute("SELECT id, 
        image_file_id, text, button_text, 
        button_url, schedule_time, 
        repeat_count FROM ads", fetch=True)
    async def delete_ad(self, ad_id): await 
        self.execute("DELETE FROM ads WHERE id 
        = ?", (ad_id,))
    # Admins
    async def add_admin(self, user_id): await 
        self.execute("INSERT OR IGNORE INTO 
        admins (user_id) VALUES (?)", 
        (user_id,))
    async def remove_admin(self, user_id):
        await self.execute("DELETE FROM admins WHE
