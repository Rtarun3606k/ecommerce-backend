from flask import Blueprint,jsonify,request,current_app,send_file
import bcrypt
from config import db
from models import User,Seller,Product,db
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,create_refresh_token
from datetime import timedelta
import re
import base64
from sqlalchemy.exc import IntegrityError
from io import BytesIO


seller = Blueprint('seller', __name__)

@seller.route('/register',methods=['POST'])
def register():
    print("Received JSON data:")
    password = request.json.get('Password')
    first_name = request.json.get('First_Name')
    last_name = request.json.get('Last_Name')
    address = request.json.get('Address')
    phone_number = request.json.get('Phone_Number')
    email = request.json.get('Email')
    store_name = request.json.get('Store_Name')
    city = request.json.get('City')
    state = request.json.get('State')
    zip_code = request.json.get('Zip_Code')


    bytes = password.encode('utf-8') 
    # generating the salt 
    salt = bcrypt.gensalt() 
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt)
    save_data = Seller(password=hash,first_name=first_name,last_name=last_name,address=address,phone_number=phone_number,email=email,store_name=store_name,zip_code=zip_code,city=city,state=state)
    try:
        db.session.add(save_data)
        db.session.commit()
        return jsonify({'message': 'Seller created successfully'}), 201
    except Exception as e:
        return jsonify({'error': "Seller already exists"+str(e)}), 400
    return jsonify({'message': 'Seller created successfully'}), 201

@seller.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    phone_number = request.json.get("phone_number", "")
    password = request.json.get("password", "")
    print(email, phone_number, password)

    if len(password) < 5:
        return jsonify({"msg": "Password must be at least 5 characters long"}), 400

    check_user = None

    if email:
        if len(email) < 5:
            return jsonify({"msg": "Invalid email"}), 400

        check_user = Seller.query.filter_by(email=email).first()
        if not check_user:
            return jsonify({"msg": "Invalid email"}), 400

    elif phone_number:
        if len(phone_number) < 5:
            return jsonify({"msg": "Invalid phone number"}), 400

        check_user = Seller.query.filter_by(phone_number=phone_number).first()
        if not check_user:
            return jsonify({"msg": "Invalid phone number"}), 400

    else:
        return jsonify({"msg": "Email or phone number required"}), 400

    if check_user and bcrypt.checkpw(password.encode('utf-8'), check_user.password):
        print("Login successful")
        access_token = create_access_token(identity=check_user.id, expires_delta=timedelta(minutes=10), additional_claims={"token_type": "access_token", "role": "seller"})
        refresh_token = create_refresh_token(identity=check_user.id, expires_delta=timedelta(minutes=30), additional_claims={"token_type": "refresh_token", "role": "seller"})
        return jsonify(access_token=access_token, refresh_token=refresh_token, msg="Login successful"), 200

    print("Login unsuccessful")
    return jsonify({"msg": "Invalid credentials"}), 401



@seller.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    check_user = Seller.query.filter_by(id=user_id).first()
    
    if check_user:
        user_dict = {
            "id": check_user.id,
            "first_name": check_user.first_name,
            "last_name": check_user.last_name,
            "email": check_user.email,
            "store_name":check_user.store_name,
            "phone_number":check_user.phone_number,
            "country":check_user.country,
            "address":check_user.address, 
           
            "zip_code":check_user.zip_code, 
            # "country":check_user.country,
            "city":check_user.city,
            "state":check_user.state, 
            # Add more fields as needed
        }
        print(user_dict)
        return jsonify({"msg": "User found", "user_data": user_dict}), 200
    else:
        return jsonify({"msg": "User not found"}), 404
    


@seller.route('/upload_product', methods=['POST'])
@jwt_required()
def upload_products():
    check_user = Seller.query.filter_by(id=get_jwt_identity()).first()
    if check_user:
        name = request.json.get('name')
        price = request.json.get('price')
        description = request.json.get('description')
        
        # Fetch and decode image1
        image1 = request.json.get('image1')
        mimetype1 = request.json.get('mimetype1')
        if image1:
            image1 = base64.b64decode(image1)
        
        # Fetch and decode image2
        image2 = request.json.get('image2')
        mimetype2 = request.json.get('mimetype2')
        if image2:
            image2 = base64.b64decode(image2)
        
        # Fetch and decode image3
        image3 = request.json.get('image3')
        mimetype3 = request.json.get('mimetype3')
        if image3:
            image3 = base64.b64decode(image3)
        
        stock = request.json.get('stock')
        category = request.json.get('category')
        colors = request.json.get('colors')
        seller_id = check_user.id
        
        save_data = Product(
            name=name,
            price=price,
            description=description,
            image1=image1,
            mimetype1=mimetype1,
            image2=image2,
            mimetype2=mimetype2,
            image3=image3,
            mimetype3=mimetype3,
            stock=stock,
            category=category,
            colors=colors,
            seller_id=seller_id
        )
        
        try:
            db.session.add(save_data)
            db.session.commit()
            return jsonify({"msg": "Product created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Product already exists"+str(e)}), 400
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": "Product already exists"+str(e)}), 400
        



@seller.route('/get_image/<int:product_id>/<int:image_number>', methods=['GET'])
def get_image(product_id, image_number):
    product = Product.query.get_or_404(product_id)
    
    image_data = None
    mimetype = None
    if image_number == 1:
        image_data = product.image1
        mimetype = product.mimetype1
    elif image_number == 2:
        image_data = product.image2
        mimetype = product.mimetype2
    elif image_number == 3:
        image_data = product.image3
        mimetype = product.mimetype3
    else:
        return jsonify({"msg": "Invalid image number"}), 400

    if not image_data:
        return jsonify({"msg": "Image not found"}), 404

    return send_file(BytesIO(image_data), mimetype=mimetype)


@seller.route('/get_products', methods=['GET'])
@jwt_required()
def get_products():
    check_user = Seller.query.filter_by(id=get_jwt_identity()).first()
    if check_user:
        products = Product.query.filter_by(seller_id=check_user.id).all()
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
                "seller_id": product.seller_id
            }
            product_list.append(product_dict)
        return jsonify({"msg":"data sent sucessfully","products":product_list}), 200

