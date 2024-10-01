from datetime import datetime
import os
from flask import jsonify, request
from app import db
from app.main.models import Product, ExhibitInfo, ExhibitProduct, Photo, ProductTag, Work, Character, Category, StorageSpace, ExhibitorPlatform, MoneyCurrency
from app.main.s3_photo import upload_file_s3

# 商品情報_登録
def create_product(data):
    try:
        # JSONデータから値を取得
        product_name = data.get('product_name')
        product_code = data.get('product_code')
        price = data.get('price')
        description = data.get('description')
        quantity_in_stock = data.get('quantity_in_stock')
        product_url = data.get('product_url')
        work_id = data.get('work_id')
        character_id = data.get('character_id')
        category_id = data.get('category_id')
        storage_space_id = data.get('storage_space_id')
        product_tags = data.get('product_tags', [])
        photo_urls = data.get('photo_urls', [])

        # 商品情報の登録
        new_product = Product(
            product_name=product_name,
            product_code=product_code,
            price=price,
            description=description,
            quantity_in_stock=quantity_in_stock,
            product_url=product_url,
            work_id=work_id,
            character_id=character_id,
            category_id=category_id,
            storage_space_id=storage_space_id,
        )
        db.session.add(new_product)
        db.session.flush()  # Product IDを取得するためにflush

        # 商品画像の登録
        for url in photo_urls:
            new_photo = Photo(
                product_id=new_product.product_id,
                image_path=url
            )
            db.session.add(new_photo)

        # Tagsの処理
        # tags = exhibit.get('tags', [])
        for tag in product_tags:
            new_tag = ProductTag(
                product_id=new_product.product_id,
                product_tag_name=tag
            )
            db.session.add(new_tag)


        # 出品情報と出品商品情報の登録
        exhibit_infos = data.get('exhibit_info', [])
        for exhibit in exhibit_infos:
            new_exhibit_info = ExhibitInfo(
                exhibit_display_name=exhibit['exhibit_display_name'],
                low_price=exhibit['min_price'],
                current_exhibit_price=exhibit.get('current_exhibit_price'),
                exhibitor_platform_id=exhibit.get('exhibitor_platform_id'),
                money_currency_id=exhibit.get('money_currency_id')
            )
            db.session.add(new_exhibit_info)
            db.session.flush()  # ExhibitInfo IDを取得するためにflush

            # ExhibitProductの登録
            new_exhibit_product = ExhibitProduct(
                exhibit_info_id=new_exhibit_info.exhibit_info_id,
                product_id=new_product.product_id,
                exhibit_quantity_in_stock=exhibit['exhibit_quantity_in_stock']
            )
            db.session.add(new_exhibit_product)

            # exhibitor_platform_id = exhibit.get('exhibitor_platform_id')
            # if exhibitor_platform_id:
            #     new_exhibit_info.exhibitor_platform_id = exhibitor_platform_id

        db.session.commit()
        return {
            'status': 'success',
            'message': '商品の登録が完了しました'
        }, 201
    except Exception as e:
        db.session.rollback()
        return {
            'status': 'fail',
            'message': f'商品の登録に失敗しました: {str(e)}'
        }, 500
    
# 商品項目_取得
def get_product_items():
    try:
        works = Work.query.all()
        characters = Character.query.all()
        categories = Category.query.all()
        storage_spaces = StorageSpace.query.all()
        platforms = ExhibitorPlatform.query.all()
        currencies = MoneyCurrency.query.all()

        work_data_list = []
        character_data_list = []
        category_data_list = []
        storage_space_data_list = []
        platform_data_list = []
        currency_data_list = []

        # オブジェクトを辞書に変換
        for work in works:
            work_data = {
                "work_id": work.work_id,
                "work_name": work.work_name,
                "created_at": work.created_at,
                "updated_at": work.updated_at,
            }

            work_data_list.append(work_data)

        for character in characters:
            character_data = {
                "character_id": character.character_id,
                "character_name": character.character_name,
                "work_id": character.work_id,
                "created_at": character.created_at,
                "updated_at": character.updated_at,
            }

            character_data_list.append(character_data)

        for category in categories:
            category_data = {
                "category_id": category.category_id,
                "category_name": category.category_name,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
            }

            category_data_list.append(category_data)

        for storage_space in storage_spaces:
            storage_space_data = {
                "storage_space_id": storage_space.storage_space_id,
                "storage_space_name": storage_space.storage_space_name,
                "created_at": storage_space.created_at,
                "updated_at": storage_space.updated_at,
            }

            storage_space_data_list.append(storage_space_data)
        
        for platform in platforms:
            platform_data = {
                "exhibitor_platform_id": platform.exhibitor_platform_id,
                "exhibitor_platform_name": platform.exhibitor_platform_name,
                "money_currency_id": platform.money_currency_id,
                "created_at": platform.created_at,
                "updated_at": platform.updated_at,
            }

            platform_data_list.append(platform_data)

        for currency in currencies:
            currency_data = {
                "money_currency_id": currency.money_currency_id,
                "currency_code": currency.currency_code,
                "created_at": currency.created_at,
                "updated_at": currency.updated_at,
            }

            currency_data_list.append(currency_data)

        result = {
            "work_data": work_data_list,
            "character_data": character_data_list,
            "category_data": category_data_list,
            "storage_space_data": storage_space_data_list,
            "platform_data": platform_data_list,
            "currency_data": currency_data_list,
            "status": "success"
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

# 商品情報_一括取得
def get_all_products():
    try:
        products = Product.query.filter(Product.deleted_at.is_(None)).all()
        product_list = []

        # Productオブジェクトを辞書に変換
        for product in products:
            product_data = {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "product_code": product.product_code,
                "price": product.price,
                "description": product.description,
                "quantity_in_stock": product.quantity_in_stock,
                "product_url": product.product_url,
                "work_id": product.work_id,
                "character_id": product.character_id,
                "category_id": product.category_id,
                "storage_space_id": product.storage_space_id,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
                "photos": [{"image_path": photo.image_path} for photo in product.photos],
                "tags": [{"tag_name": tag.product_tag_name} for tag in product.tags],
                "exhibit_infos": []
            }

            # ExhibitInfoとExhibitProductを取得
            exhibit_products = ExhibitProduct.query.filter_by(product_id=product.product_id).all()
            
            for exhibit_product in exhibit_products:
                exhibit_info = ExhibitInfo.query.filter_by(exhibit_info_id=exhibit_product.exhibit_info_id).first()
                
                exhibit_data = {
                    "exhibit_display_name": exhibit_info.exhibit_display_name,
                    "min_price": exhibit_info.low_price,
                    "current_exhibit_price": exhibit_info.current_exhibit_price,
                    "exhibit_quantity_in_stock": exhibit_product.exhibit_quantity_in_stock,
                    "exhibitor_platform_id": exhibit_info.exhibitor_platform_id,
                    "money_currency_id": exhibit_info.money_currency_id,
                }
                
                product_data["exhibit_infos"].append(exhibit_data)

            product_list.append(product_data)

        return jsonify({"status": "success", "products": product_list}), 200

    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

# 商品情報_個別取得
def get_unique_product_item(product_id):
    try:
        product = Product.query.filter(Product.product_id == product_id, Product.deleted_at.is_(None)).first()

        if not product:
            return jsonify({"status": "fail", "message": "Product not found"}), 404

        # Productオブジェクトを辞書に変換
        product_data = {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_code": product.product_code,
            "price": product.price,
            "description": product.description,
            "quantity_in_stock": product.quantity_in_stock,
            "product_url": product.product_url,
            "work_id": product.work_id,
            "character_id": product.character_id,
            "category_id": product.category_id,
            "storage_space_id": product.storage_space_id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
            "photos": [{"image_path": photo.image_path} for photo in product.photos],
            "tags": [{"tag_name": tag.product_tag_name} for tag in product.tags],
            "exhibit_infos": []
        }

        # ExhibitInfoとExhibitProductを取得
        exhibit_products = ExhibitProduct.query.filter_by(product_id=product.product_id).all()

        for exhibit_product in exhibit_products:
            exhibit_info = ExhibitInfo.query.filter_by(exhibit_info_id=exhibit_product.exhibit_info_id).first()

            if exhibit_info:  # exhibit_info が存在する場合のみ追加
                exhibit_data = {
                    "exhibit_display_name": exhibit_info.exhibit_display_name,
                    "min_price": exhibit_info.low_price,
                    "current_exhibit_price": exhibit_info.current_exhibit_price,
                    "exhibit_quantity_in_stock": exhibit_product.exhibit_quantity_in_stock,
                    "exhibitor_platform_id": exhibit_info.exhibitor_platform_id,
                    "money_currency_id": exhibit_info.money_currency_id,
                }
                product_data["exhibit_infos"].append(exhibit_data)

        return jsonify({"status": "success", "product": product_data}), 200

    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

# 商品情報_更新

# 商品情報_削除
def delete_product_info(product_id):
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"status": "fail", "message": "Product not found"}), 404
        
        # 論理削除（deleted_atに日時を設定）
        product.deleted_at = datetime.utcnow()
        
        # 関連するデータを削除または論理削除
        for photo in product.photos:
            photo.deleted_at = datetime.utcnow()
        
        for tag in product.tags:
            tag.deleted_at = datetime.utcnow()
        
        for exhibit_product in product.exhibit_products:
            exhibit_product.deleted_at = datetime.utcnow()

        # データベースに変更をコミット
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Product deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "fail", "message": str(e)}), 500