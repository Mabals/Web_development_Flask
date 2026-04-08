from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'disebo_secret_key'  # For sessions

# Menu data
bunny_chows = [
    {"id": 1, "name": "Basic Bunny Chow", "price": 22, "ingredients": "chips, atchaar, polony, smoked vienna"},
    {"id": 2, "name": "Cheese Bunny Chow", "price": 25, "ingredients": "chips, atchaar, polony, smoked vienna, cheese"},
    {"id": 3, "name": "Russian Bunny Chow", "price": 28,
     "ingredients": "chips, atchaar, polony, smoked vienna, cheese, russian"},
    {"id": 4, "name": "Quarter Bunny Chow", "price": 33,
     "ingredients": "chips, atchaar, polony, smoked vienna, cheese, russian, egg"}
]
drinks = [
    {"id": 1, "name": "Coke 500ml", "price": 15},
    {"id": 2, "name": "Coke 1.5L", "price": 25},
    {"id": 3, "name": "Sprite 500ml", "price": 15},
    {"id": 4, "name": "Sprite 1.5L", "price": 25},
    {"id": 5, "name": "Fanta Orange 500ml", "price": 15},
    {"id": 6, "name": "Fanta Orange 1.5L", "price": 25},
    {"id": 7, "name": "Stoney 500ml", "price": 15},
    {"id": 8, "name": "Stoney 1.5L", "price": 25}
]


@app.route('/')
def index():
    return render_template('index.html', bunny_chows=bunny_chows, drinks=drinks)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = int(request.form['id'])
    qty = int(request.form.get('qty', 1))
    item_type = request.form['type']

    if 'cart' not in session:
        session['cart'] = []

    # Find item
    if item_type == 'bunny':
        item = next((i for i in bunny_chows if i['id'] == item_id), None)
    else:
        item = next((i for i in drinks if i['id'] == item_id), None)

    if item:
        session['cart'].append({'item': item, 'qty': qty})
        session.modified = True
        flash(f'Added {item["name"]} x{qty} to cart!')

    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    if 'cart' not in session:
        return render_template('cart.html', cart=[], total=0)

    total = sum(c['item']['price'] * c['qty'] for c in session['cart'])
    return render_template('cart.html', cart=session['cart'], total=total)


@app.route('/checkout')
def checkout():
    if 'cart' in session:
        # Simulate order (print to console)
        print("New order:", session['cart'])
        session.pop('cart', None)
        flash('Order placed! Thanks for ordering from Disebo\'s.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)