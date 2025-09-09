from .db import db


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<categories {self.id}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float(50))
    stock = db.Column(db.Integer)
    image = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship("Categories", backref=db.backref('product', lazy='dynamic'))

    def __init__(self, name, price, stock, image, category_id=None):
        self.name = name
        self.price = price
        self.stock = stock
        self.image = image
        self.category_id = category_id

    def __repr__(self):
        return f"<Product {self.id}>"

    def get(self, id):
        if id == self.id:
            return f"{self.name} {self.price}"
