from flask import request, jsonify, send_file,Blueprint
from config import app ,db
from models import User,Image,Product,Order
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from io import BytesIO
from flask_jwt_extended import verify_jwt_in_request, create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from routes.loginRegister import loginRegister
from routes.check_session_token import check_session_token
from routes.seller import seller
from routes.Products import Products


app.register_blueprint(loginRegister, url_prefix='/loginRegister')
app.register_blueprint(check_session_token, url_prefix='/check_session_token')
app.register_blueprint(seller, url_prefix='/seller')
app.register_blueprint(Products, url_prefix='/products')


@app.route('/check_token', methods=['POST'])
def check_token():
    try:
        verify_jwt_in_request()
        return jsonify({"msg": "Token is valid"}), 200
    except ExpiredSignatureError:
        return jsonify({"msg": "Token is expired"}), 401
    except InvalidTokenError:
        return jsonify({"msg": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"msg": str(e)}), 401


# @app.route('/')
# def index():
#     return jsonify({'message': 'Hello World'})




# # @app.route('/',)
# def index():
#     return jsonify({'message':'Hello World'})

# @app.route('/upload', methods=['POST'])
# def upload_images():
#     if 'images' not in request.files:
#         return jsonify({'error': 'No images part'}), 400

#     files = request.files.getlist('images')
#     saved_files = []

#     for file in files:
#         if file:
#             filename = secure_filename(file.filename)
#             mimetype = file.mimetype

#             new_image = Image(
#                 name=filename,
#                 img=file.read(),
#                 mimetype=mimetype
#             )
#             db.session.add(new_image)
#             db.session.commit()

#             saved_files.append(filename)

#     return jsonify({'saved_files': saved_files}), 201


# @app.route('/images', methods=['GET'])
# def get_images():
#     images = Image.query.all()
#     image_list = [
#         {
#             'id': image.id,
#             'name': image.name,
#             'mimetype': image.mimetype
#         } for image in images
#     ]
#     return jsonify(image_list)

# @app.route('/images/<int:image_id>', methods=['GET'])
# def get_image(image_id):
#     image = Image.query.get_or_404(image_id)
#     return send_file(
#         BytesIO(image.img),
#         mimetype=image.mimetype,
#         as_attachment=False,
#         download_name=image.name
#     )

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(port=5000, debug=True)



