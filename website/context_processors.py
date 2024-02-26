from flask import session
import sqlite3

def delivery_info_context_processor():
    conn = sqlite3.connect('wmgzon.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_postcode
        FROM delivery_info
        WHERE user_email = ?
    ''', (session.get('user_email'),))
    session['postcode'] = cursor.fetchone()

    if session['postcode']:
        return {'postcode': session['postcode'][0]}
    else:
        return {'postcode': 'No delivery info'}

