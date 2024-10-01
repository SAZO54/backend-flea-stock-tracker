from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(64), nullable=True)
    product_name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric, nullable=False)
    product_url = db.Column(db.Text, nullable=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.work_id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.character_id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    total_exhibit_quantity = db.Column(db.Integer, nullable=True)
    exhibitor_platform_id = db.Column(db.Integer, db.ForeignKey('exhibitor_platform.exhibitor_platform_id'), nullable=True)
    storage_space_id = db.Column(db.Integer, db.ForeignKey('storage_space.storage_space_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

    photos = db.relationship('Photo', backref='product', lazy=True)
    tags = db.relationship('ProductTag', backref='product', lazy=True)
    exhibit_products = db.relationship('ExhibitProduct', backref='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    trade_name = db.Column(db.String(128), nullable=True)
    purchaser_name = db.Column(db.String(128), nullable=True)
    total_amount = db.Column(db.Numeric, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'), nullable=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.world_id'), nullable=True)
    japan_id = db.Column(db.Integer, db.ForeignKey('japan.prefecture_id'), nullable=True)
    exhibitor_platform_id = db.Column(db.Integer, db.ForeignKey('exhibitor_platform.exhibitor_platform_id'), nullable=False)
    now_location = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class OrderDetail(db.Model):
    __tablename__ = 'order_detail'
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Work(db.Model):
    __tablename__ = 'work'
    work_id = db.Column(db.Integer, primary_key=True)
    work_name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class ExhibitorPlatform(db.Model):
    __tablename__ = 'exhibitor_platform'
    exhibitor_platform_id = db.Column(db.Integer, primary_key=True)
    exhibitor_platform_name = db.Column(db.String(128), nullable=False)
    money_currency_id = db.Column(db.Integer, db.ForeignKey('money_currency.money_currency_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Status(db.Model):
    __tablename__ = 'status'
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Shipment(db.Model):
    __tablename__ = 'shipment'
    shipment_id = db.Column(db.Integer, primary_key=True)
    shipment_name = db.Column(db.String(128), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Area(db.Model):
    __tablename__ = 'area'
    area_id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class World(db.Model):
    __tablename__ = 'world'
    world_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(128), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Japan(db.Model):
    __tablename__ = 'japan'
    prefecture_id = db.Column(db.Integer, primary_key=True)
    prefecture_name = db.Column(db.String(128), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.area_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Photo(db.Model):
    __tablename__ = 'photo'
    photo_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    image_path = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)


class ProductTag(db.Model):
    __tablename__ = 'product_tag'
    product_tag_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    product_tag_name = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class MoneyCurrency(db.Model):
    __tablename__ = 'money_currency'
    money_currency_id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class Character(db.Model):
    __tablename__ = 'character'
    character_id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(256), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey('work.work_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class StorageSpace(db.Model):
    __tablename__ = 'storage_space'
    storage_space_id = db.Column(db.Integer, primary_key=True)
    storage_space_name = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

class ExhibitInfo(db.Model):
    __tablename__ = 'exhibit_info'
    exhibit_info_id = db.Column(db.Integer, primary_key=True)
    exhibitor_platform_id = db.Column(db.Integer, db.ForeignKey('exhibitor_platform.exhibitor_platform_id'), nullable=True)
    exhibit_display_name = db.Column(db.String(256), nullable=False)
    low_price = db.Column(db.Numeric, nullable=False)
    current_exhibit_price = db.Column(db.Numeric, nullable=True)
    money_currency_id = db.Column(db.Integer, db.ForeignKey('money_currency.money_currency_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)

    exhibit_products = db.relationship('ExhibitProduct', backref='exhibit_info', lazy=True)

class ExhibitProduct(db.Model):
    __tablename__ = 'exhibit_product'
    exhibit_product_id = db.Column(db.Integer, primary_key=True)
    exhibit_info_id = db.Column(db.Integer, db.ForeignKey('exhibit_info.exhibit_info_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    exhibit_quantity_in_stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime, nullable=True)
