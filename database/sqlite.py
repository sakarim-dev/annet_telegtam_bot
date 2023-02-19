import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('../database.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, name TEXT, phone INTEGER, email TEXT, "
        "description TEXT)")

    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", (user_id, '', '', '', ''))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            "UPDATE users SET name = '{}', phone = '{}', email = '{}', description = '{}' WHERE user_id == '{}'".format(
                data['name'], data['phone'], data['email'], data['description'], user_id))
        db.commit()


async def get_all_id():
    cur.execute("SELECT user_id FROM users")
    massive_big = cur.fetchall()

    return massive_big
