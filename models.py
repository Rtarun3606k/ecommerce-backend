from config import db,app
from datetime import datetime,timezone


# whwn ever you change data use this
# flask db init
# flask db migrate -m "Add new_column to Product"
# flask db upgrade



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    alternate_email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    Last_name = db.Column(db.String(80), unique=False, nullable=False)
    phone_number = db.Column(db.String(80), unique=True, nullable=False)
    alternate_phone_number = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    alterate_address = db.Column(db.Text(), unique=False, nullable=False)
    address = db.Column(db.Text(), unique=False, nullable=False)
    date_of_birth = db.Column(db.String(80), unique=False, nullable=False)
    zip_code = db.Column(db.String(80), unique=False, nullable=False)
    country = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.first_name

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image1 = db.Column(db.LargeBinary, nullable=False)
    mimetype1 = db.Column(db.String(100), nullable=False)
    image2 = db.Column(db.LargeBinary, nullable=False)
    mimetype2 = db.Column(db.String(100), nullable=False)
    image3 = db.Column(db.LargeBinary, nullable=False)
    mimetype3 = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100), nullable=True)
    colors = db.Column(db.String(200), nullable=True)  # Comma-separated string of available colors
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    orders = db.relationship('Order', backref='product', lazy=True)
    rating = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Product %r>' % self.name

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_status = db.Column(db.String(50), nullable=False, default='Pending')
    color = db.Column(db.String(50), nullable=False)  # Chosen color for the product
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Order %r>' % self.id

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), unique=True, nullable=False)
    store_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text(), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    zip_code = db.Column(db.String(80), nullable=False)
    products = db.relationship('Product', backref='seller', lazy=True)
    country = db.Column(db.String(80), default='Unknown') 

    def __repr__(self):
        return '<Seller %r>' % self.store_name

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('transactions', lazy=True))
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., Credit Card, PayPal, etc.
    status = db.Column(db.String(50), nullable=False, default='Completed')





class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()