from flask import Blueprint, render_template, request, redirect, jsonify, url_for, flash, json, typing as ft
from .models import Product, Categories
from flask.views import View
from .db import db
from redis import Redis
from werkzeug.utils import secure_filename
import os

redis = Redis(host='localhost', port=6379, db=2)

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@routes.route('/')
def index():
    return render_template("index.html")


@routes.route('category', methods=['post', 'get'])
def category():
    if request.method == "POST":
        name = request.form.get('name')
        category = Categories(name)
        db.session.add(category)
        db.session.commit()
        print(category)
        return redirect('/')
    return render_template("categories.html")


@routes.route('/contact', methods=['GET'])
def contact_us():
    categories = Categories.query.all()
    return render_template('add_product.html', categories=categories)


@routes.route("/submit", methods=['get', 'post'])
def submit():
    # categories = Categories.query.all()

    if request.method == "POST":
        name = request.form.get('name')
        price = request.form.get('price')
        category_id = request.form.get('category')
        stock = request.form.get('stock')
        image_file = request.files.get('image')

        if not all([name, price, category_id, stock, image_file]):
            # flash("All fields are required.")
            return redirect(url_for('routes.home'))

        filename = secure_filename(image_file.filename)
        filepath = os.path.join("src/templates/assets/image/", filename)
        image_file.save(filepath)

        new_product = Product(
            name=name,
            price=float(price),
            stock=int(stock),
            image=filepath,
            category_id=int(category_id)
        )
        db.session.add(new_product)
        db.session.commit()

        # Save name and image to Redis
        redis_data = {'name': name, 'image': filepath}
        redis.set(f'product:{new_product.id}', json.dumps(redis_data))

        flash("Product submitted successfully.")
    return redirect(url_for('routes.contact_us'))


@routes.route('/products', methods=["GET", "POST"])
def products():
    # keys = redis.keys('products:*')
    # products = [json.loads(redis.get(product).decode('utf-8')) for product in keys]
    # return render_template('product.html', products=products)

    product_keys = [key for key in redis.scan_iter("product:*")]
    products = []

    for key in product_keys:
        data = json.loads(redis.get(key))
        product_id = f"{key}".split(':')[1]
        print(product_id)
        product_id = int("".join(filter(str.isdigit, product_id)))
        products.append({
            'id': product_id,
            'name': data['name'],
            'image': data['image']
        })

    return render_template('product.html', products=products)


@routes.route('/product/<int:product_id>', methods=["GET"])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


class OrderView(View):
    def dispatch_request(self, product_id=1):
        if request.method == "GET":
            product = Product.query.get_or_404(product_id)
            return render_template('order.html', product=product)
        if request.method == "POST":
            name = request.form.get('name')
            email = request.form.get('email')
            quantity = request.form.get('quantity')
            address = request.form.get('address')

            if not all([name, email, quantity, address]):
                flash("Please fill in all fields")
                return redirect(url_for('routes.order', product_id=product_id))

            flash("Order received (not saved to database).")
            return redirect(url_for('routes.home'))
