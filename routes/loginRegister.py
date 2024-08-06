from flask import Blueprint,jsonify,request,current_app
import bcrypt
from config import db
from models import User
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,create_refresh_token
from datetime import timedelta
import re

loginRegister = Blueprint('loginRegister', __name__)

@loginRegister.route('/register',methods=['POST'])
def index():
    print("Received JSON data:")
    password = request.json.get('Password')
    first_name = request.json.get('First_Name')
    last_name = request.json.get('Last_Name')
    address = request.json.get('Address')
    alternate_address = request.json.get('Alternate_Address')
    phone_number = request.json.get('Phone_Number')
    alternate_phone_number = request.json.get('Alternate_Phone_Number')
    email = request.json.get('Email')
    alternate_email = request.json.get('Alternate_Email')
    gender = request.json.get('Gender')
    city = request.json.get('City')
    state = request.json.get('State')
    zip_code = request.json.get('Zip_Code')
    country = request.json.get('Country')
    date_of_birth = request.json.get('Date_of_Birth')

    # converting password to array of bytes 
    bytes = password.encode('utf-8') 
    # generating the salt 
    salt = bcrypt.gensalt() 
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    save_data = User(password=hash,first_name=first_name,Last_name=last_name,address=address,alterate_address=alternate_address,phone_number=phone_number,alternate_phone_number=alternate_phone_number,email=email,gender=gender, city=city, state=state, zip_code=zip_code, country=country, date_of_birth=date_of_birth, alternate_email=alternate_email)
    try:
        db.session.add(save_data)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': "User already exists"+str(e)}), 400
    



@loginRegister.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    phone_number = request.json.get("phone_number", "")
    password = request.json.get("password", "")

    if len(password) < 5:
        return jsonify({"msg": "Password must be at least 5 characters long"}), 400

    if email:
        if len(email) < 5:
            return jsonify({"msg": "Invalid email"}), 400

        check_user = User.query.filter_by(email=email).first()
    elif phone_number:
        if len(phone_number) < 5:
            return jsonify({"msg": "Invalid phone number"}), 400

        check_user = User.query.filter_by(phone_number=phone_number).first()
    else:
        return jsonify({"msg": "Email or phone number required"}), 400

    if check_user and bcrypt.checkpw(password.encode('utf-8'), check_user.password):
        access_token = create_access_token(identity=check_user.id, expires_delta=timedelta(minutes=10),additional_claims={"token_type": "access_token"})
        refresh_token = create_refresh_token(identity=check_user.id, expires_delta=timedelta(minutes=30) ,additional_claims={"token_type": "refresh_token"})
        return jsonify(access_token=access_token, refresh_token=refresh_token, msg="Login successful"), 200

    return jsonify({"msg": "Invalid credentials"}), 401
    


@loginRegister.route('/get_users',methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_dict = {
            "id":user.id,
            "first_name":user.first_name,
            "last_name":user.Last_name,
            "gender":user.gender,
            "phone_number":user.phone_number,
            "alternate_phone_number":user.alternate_phone_number,
            "address":user.address,
            "alternate_address":user.alterate_address,
            "email":user.email
        }
        user_list.append(user_dict)
    return jsonify(user_list), 200



@loginRegister.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    check_user = User.query.filter_by(id=user_id).first()
    
    if check_user:
        user_dict = {
            "id": check_user.id,
            "first_name": check_user.first_name,
            "last_name": check_user.Last_name,
            "email": check_user.email,
            "alternate_email":check_user.alternate_email,
            "phone_number":check_user.phone_number,
            "alternate_phone_number":check_user.alternate_phone_number,
            "gender":check_user.gender,
            "alterate_address":check_user.alterate_address,
            "address":check_user.address, 
            "date_of_birth":check_user.date_of_birth,
            "zip_code":check_user.zip_code, 
            "country":check_user.country,
            "city":check_user.city,
            "state":check_user.state, 
            # Add more fields as needed
        }
        return jsonify({"msg": "User found", "user_data": user_dict}), 200
    else:
        return jsonify({"msg": "User not found"}), 404
    




@loginRegister.route('/update_user', methods=['POST'])
@jwt_required()
def update():
    check_user = User.query.filter_by(id=get_jwt_identity()).first()
    if not check_user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    current_app.logger.debug(f"Received JSON data: {data}")  # Log the received JSON data
    print("Received JSON data:", data) 
    

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')
    alternate_address = data.get('alternate_address')
    phone_number = data.get('phone_number')
    alternate_phone_number = data.get('alternate_phone_number')
    email = data.get('email')
    alternate_email = data.get('alternate_email')
    gender = data.get('gender')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')
    country = data.get('country')
    date_of_birth = data.get('date_of_birth')

    # Ensure required fields are not None
    if not all([first_name, last_name, email, phone_number]):
        return jsonify({'error': 'Missing required fields'}), 400

    print("Updating user with:")
    print(f"first_name={first_name}, last_name={last_name}, email={email}, "
              f"phone_number={phone_number}, alternate_email={alternate_email}, "
              f"address={address}, alternate_address={alternate_address}, "
              f"gender={gender}, city={city}, state={state}, zip_code={zip_code}, "
              f"country={country}, date_of_birth={date_of_birth}")

    # Check if any other user has the same phone number
    if phone_number != check_user.phone_number:
        check_user_ph = User.query.filter_by(phone_number=phone_number).first()
        if check_user_ph:
            return jsonify({'error': 'Phone number already exists'}), 400

    # Check if any other user has the same email
    if email != check_user.email:
        check_user_email = User.query.filter_by(email=email).first()
        if check_user_email:
            return jsonify({'error': 'Email already exists'}), 400

    # Check if any other user has the same alternate email, if provided
    if alternate_email and alternate_email != check_user.alternate_email:
        check_user_al_email = User.query.filter_by(alternate_email=alternate_email).first()
        if check_user_al_email:
            return jsonify({'error': 'Alternate email already exists'}), 400

    # Check if any other user has the same alternate phone number, if provided
    if alternate_phone_number and alternate_phone_number != check_user.alternate_phone_number:
        check_user_al_ph = User.query.filter_by(alternate_phone_number=alternate_phone_number).first()
        if check_user_al_ph:
            return jsonify({'error': 'Alternate phone number already exists'}), 400

    # Update user details
    check_user.first_name = first_name
    check_user.Last_name = last_name
    check_user.address = address
    check_user.alterate_address = alternate_address
    check_user.gender = gender
    check_user.city = city
    check_user.state = state
    check_user.zip_code = zip_code
    check_user.country = country
    check_user.date_of_birth = date_of_birth
    check_user.phone_number = phone_number
    check_user.alternate_phone_number = alternate_phone_number
    check_user.email = email
    check_user.alternate_email = alternate_email

    try:
        db.session.commit()
        return jsonify({'msg': 'User updated successfully'}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"User update failed: {str(e)}")  # Log the error message
        return jsonify({'msg': "User update failed: " + str(e)}), 400

    return jsonify({'error': 'User not found'}), 404


@loginRegister.route('/get_orders', methods=['GET'])
def get_orders():
    orders = User.query.all()
    order_list = []
    for order in orders:
        order_dict = {
            "id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "order_status": order.order_status,
            "color": order.color,
            "created_at": order.created_at,
            "updated_at": order.updated_at
        }
        order_list.append(order_dict)
    return jsonify(order_list), 200