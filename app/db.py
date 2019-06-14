import sqlite3

from app.domain import Product


def open_db(url):
    db = sqlite3.connect(url)
    db.row_factory = sqlite3.Row
    return db


def init_db(db):
    with db:
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            qty INTEGER NOT NULL DEFAULT 0 CHECK ( qty >= 0 )
        );
        ''')
        db.commit()


def get_products(db):
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, price, qty FROM products")
        items = []
        for row in cursor:
            items.append(
                Product(
                    row['id'],
                    row['name'],
                    row['price'],
                    row['qty']
                )
            )
        return items


def add(db, products):
    with db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO products(name, price, qty) VALUES (:name, :price, :qty)',
                       {'name': products.name, 'price': products.price, 'qty': products.qty})
        db.commit()


def get_by_id(db, id):
    with db:
        cursor = db.cursor()
        cursor.execute('SELECT id, name, price, qty FROM products WHERE id = :id', {'id': id})
        for row in cursor:
            return Product(
                row['id'],
                row['name'],
                row['price'],
                row['qty']
            )


def update(db, product):
    with db:
        cursor = db.cursor()
        cursor.execute('UPDATE products SET name = :name, price = :price, qty = :qty WHERE id = :id',
                       {'id': product.id, 'name': product.name, 'price': product.price, 'qty': product.qty})
        db.commit()


def remove(db, id):
    with db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM products WHERE id = :id', {'id': id})
        db.commit()


def sale(db, id, count):
    with db:
        cursor = db.cursor()
        cursor.execute('UPDATE products SET qty = qty - :count WHERE id = :id', {'id': id, 'count': count})
        db.commit()
