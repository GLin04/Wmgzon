import sqlite3
from __init__ import create_app
from context_processors import delivery_info_context_processor, product_info_context_processor

app = create_app()
app.context_processor(delivery_info_context_processor)
app.context_processor(product_info_context_processor)

if __name__ == '__main__':

    # Closes the database if it was locked
    conn = sqlite3.connect('wmgzon.db')
    conn.close()
    app.run(host='0.0.0.0', port=int(3000), debug=True)