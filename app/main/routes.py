import os
from flask import Blueprint, app, request, jsonify
from app.main.product_services import create_product, delete_product_info, get_all_products, get_product_items, get_unique_product_item
from app.main.s3_photo import upload_file_s3

api = Blueprint('api', __name__, url_prefix='/api')

# 商品情報_登録 API
@api.route('/products', methods=['POST'])
def add_product():
    data = request.json

    result, status_code = create_product(data)
    return jsonify(result), status_code


# 画像_S3_アップロード API
@api.route('upload-images', methods=['POST'])
def upload_image():
    if 'photo' not in request.files:
        return jsonify({'error': 'ファイルが見つかりませんでした'}), 400

    file = request.files['photo']

    s3_bucket_name = os.getenv('AWS_BUCKET_NAME')
    s3_file_key = f"upload/{file.filename}"
    
    s3_url = upload_file_s3(file, s3_bucket_name, s3_file_key)

    if s3_url:
        return jsonify({'s3Url': s3_url}), 200
    else:
        return jsonify({'error': 'S3へのアップロードに失敗しました'}), 500


# 商品情報_取得 API
@api.route('/fetch-products', methods=['GET', 'OPTIONS'])
def fetch_all_products():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    return get_all_products()
    

# 商品項目_取得 API
@api.route('/product-items', methods=['GET', 'OPTIONS'])
def fetch_product_items():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    return get_product_items()


# 商品情報_個別取得 API
@api.route('/product-detail/<int:id>', methods=['GET', 'OPTIONS'])
def fetch_unique_product_item(id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    return get_unique_product_item(id)

# 商品情報_更新 API

# 商品情報_削除 API
@api.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    return delete_product_info(id)


# from flask import Blueprint, app, request, jsonify
# from app.main.services import create_product

# api = Blueprint('api', __name__, url_prefix='/api')

# @api.route('/products', methods=['POST'])
# def add_product():
#     data = request.get_json()
#     result, status_code = create_product(data)
#     return jsonify(result), status_code
#     # print("test")