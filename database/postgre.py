import psycopg2
from utils.config import PG_USER, PG_DATABASE, PG_PASSWORD, PG_IP

connection = psycopg2.connect(
    host=PG_IP,
    user=PG_USER,
    password=PG_PASSWORD,
    database=PG_DATABASE
)

cur = connection.cursor()


async def db_start():
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users2(users_id INTEGER PRIMARY KEY, name TEXT, phone INTEGER, email TEXT, description TEXT)""")


async def create_profile(users_id, username):
    user = cur.execute("""SELECT 1 FROM users WHERE users_id = '{key}'""".format(key=users_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", (users_id, '', username, '', '', '', ''))


async def edit_profile(state, users_id):
    async with state.proxy() as data:
        cur.execute(
            """UPDATE users SET name = '{}', phone = '{}', email = '{}', description = '{}' WHERE users_id == '{}'""".format(
                data['name'], data['phone'], data['email'], data['description'], users_id))


async def get_all_id():
    cur.execute("""SELECT users_id FROM users""")
    massive_big = cur.fetchall()
    print(massive_big)
    return massive_big


