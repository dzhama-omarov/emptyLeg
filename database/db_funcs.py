from sqlite3 import connect, IntegrityError


def get_allowed_fields(table_name):
    conn = connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return set(columns)


def init_db():
    conn = connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            fullName TEXT UNIQUE NOT NULL,
            company TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )'''
    )

    conn.commit()
    conn.close()


def register_user(email, fullName, company, password):
    conn = connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT *
        FROM users
        WHERE email = ?''',
        (email,)
    )
    if cursor.fetchone():
        return 'This email is already registered'
    else:
        cursor.execute(
            '''INSERT INTO users (email, fullName, company, password)
            VALUES (?,?,?,?)''',
            (email, fullName, company, password)
        )
        conn.commit()
        conn.close()
        return "Registration successful"


def add_user(username, password):
    conn = connect('database/users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, password)
        )
        conn.commit()
    except IntegrityError:
        return False  # username уже есть
    finally:
        conn.close()
    return True


def logIn_success(login, password):
    conn = connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT id, email, password
        FROM users
        WHERE email = ?''',
        (login,)
    )
    logIn_data = cursor.fetchone()
    conn.close()
    if logIn_data[1] == login and logIn_data[2] == password:
        return logIn_data[0]
    return None


def get_from_db(user_id, *fields):
    allowed_fields = get_allowed_fields('users')

    if not fields:
        fields = ('*',)
    else:
        fields = tuple(f for f in fields if f in allowed_fields)
        if not fields:
            fields = ('*',)

    columns = ', '.join(fields)
    query = f'SELECT {columns} FROM users WHERE id = ?'

    conn = connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result