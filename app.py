import waitress
from flask import Flask, render_template, request, redirect, url_for

import db
import os
from domain import Product


def start():
    app = Flask(__name__)
    db_url = 'db.sqlite'

    @app.route("/", methods=['GET'])
    def index():
        products = db.get_products(db.open_db(db_url))
        return render_template('index.html', products=products)

    @app.route("/add", methods=['GET'])
    def add_form():
        return render_template("add.html")

    @app.route("/add", methods=['POST'])
    def add():
        name = request.form['name']
        price = float(request.form['price'])
        qty = int(request.form['qty'])
        product = Product(0, name, price, qty)
        db.add(db.open_db(db_url), product)
        return redirect(url_for('index'))

    @app.route("/details/<id>", methods=['GET'])
    def details_by_id(id):
        product = db.get_by_id(db.open_db(db_url), id)
        return render_template('details.html', product=product)

    @app.route("/edit/<id>", methods=['GET'])
    def edit_form(id):
        product = db.get_by_id(db.open_db(db_url), id)
        return render_template('edit.html', product=product)

    @app.route("/edit/<id>", methods=['POST'])
    def edit(id):
        name = request.form['name']
        price = float(request.form['price'])
        qty = int(request.form['qty'])
        product = Product(id, name, price, qty)
        db.update(db.open_db(db_url), product)
        return redirect(url_for('details_by_id', id=id))

    @app.route('/remove/<id>', methods=['GET'])
    def remove_form(id):
        product = db.get_by_id(db.open_db(db_url), id)
        return render_template('remove.html', product=product)

    @app.route('/remove/<id>', methods=['POST'])
    def remove(id):
        db.remove(db.open_db(db_url), id)
        return redirect(url_for('index'))

    @app.route('/sale/<id>', methods=['GET'])
    def sale_form(id):
        product = db.get_by_id(db.open_db(db_url), id)
        return render_template('sale.html', product=product)

    @app.route('/sale/<id>', methods=['POST'])
    def sale(id):
        count = int(request.form['count'])
        db.sale(db.open_db(db_url), id, count)
        return redirect(url_for('index'))

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(debug=True)


if __name__ == '__main__':
    start()
