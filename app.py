from flask import Flask, render_template, request # type: ignore

app = Flask(__name__, template_folder='templates')

# Dictionary to store the count of orders for each type of pizza
pizza_orders = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    global pizza_orders

    if request.method == 'POST':
        sizes = ["small", "medium", "large"]
        extras = ["extra cheese", "gluten-free base"]

        size = request.form['size'].lower()
        toppings = [topping.strip() for topping in request.form['toppings'].split(',')]
        extra_choices = [extra.lower() for extra in request.form.getlist('extras')]

        if size not in sizes:
            return "Invalid size. Please go back and select small, medium, or large."
        elif not toppings:
            return "Toppings cannot be empty."
        elif any(extra not in extras for extra in extra_choices):
            return "Invalid extras. Please choose from 'extra cheese' or 'gluten-free base'."
        else:
            # Update pizza_orders dictionary
            pizza_key = (size, tuple(toppings), tuple(extra_choices))
            pizza_orders[pizza_key] = pizza_orders.get(pizza_key, 0) + 1

            order_details = {
                'size': size,
                'toppings': toppings,
                'extras': extra_choices
            }
            # Pass pizza_orders to the template
            return render_template('order_received.html', order_details=order_details, pizza_orders=pizza_orders)
    # Pass pizza_orders to the template
    return render_template('index.html', pizza_orders=pizza_orders)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
