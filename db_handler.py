import sqlite3
import json


def update(user_id, **user_data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    # Convert stage to a JSON string if it is present in user_data
    if 'stage' in user_data and isinstance(user_data['stage'], list):
        user_data['stage'] = json.dumps(user_data['stage'])

    if existing_user:
        # Update existing user
        for key, value in user_data.items():
            cursor.execute(f'UPDATE users SET {key} = ? WHERE user_id = ?', (value, user_id))
    else:
        # Insert new user
        default_user = {
            'user_id': user_id, 'mail': None, 'password': None, 'verified': None,
            'stage': json.dumps([None, 0]), 'affiliate': None, 'earnings': 0
        }
        default_user.update(user_data)
        cursor.execute('''
            INSERT INTO users (user_id, mail, password, verified, stage, affiliate, earnings)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (default_user['user_id'], default_user['mail'], default_user['password'], default_user['verified'],
              default_user['stage'], default_user['affiliate'], default_user['earnings']))

    conn.commit()
    conn.close()


def check_user_existence(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_exists = cursor.fetchone() is not None
    conn.close()
    return user_exists


def get_user_data(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_data = {
            'user_id': user[0], 'mail': user[1], 'password': user[2],
            'verified': bool(user[3]), 'stage': json.loads(user[4]),
            'affiliate': user[5], 'earnings': user[6]
        }
        return user_data
    return None
