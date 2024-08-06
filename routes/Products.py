from flask import Blueprint,jsonify,request,current_app
import bcrypt
from config import db
from models import User,Product
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,create_refresh_token
from datetime import timedelta
import re


Products = Blueprint('Products', __name__)


@Products.route('/get_products', methods=['GET'])
def get_products():
    # check_user = Seller.query.filter_by(id=get_jwt_identity()).first()
    # if check_user:
        products = Product.query.all()
        product_list = []
        for product in products:
            product_dict = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "stock": product.stock,
                "category": product.category,
                "colors": product.colors,
                "seller_id": product.seller_id,
                "rating": product.rating
            }
            product_list.append(product_dict)
        return jsonify({"msg":"data sent sucessfully","products":product_list}), 200