from app import db, create_app
from app.main.models import Character, MoneyCurrency, StorageSpace, Work, Category, ExhibitorPlatform, Status, Shipment, Area, World, Japan

def seed_data():
    # Workデータ
    work1 = Work(work_name='ONE PIECE')
    work2 = Work(work_name='銀魂')
    work3 = Work(work_name='参考書')

    db.session.add(work1)
    db.session.add(work2)
    db.session.add(work3)
    db.session.commit()

    # Characterデータ
    characters = [
        Character(character_name='ゾロ', work_id=work1.work_id),
        Character(character_name='ルフィ', work_id=work1.work_id),
        Character(character_name='サンジ', work_id=work1.work_id),
        Character(character_name='ロー', work_id=work1.work_id),
        Character(character_name='キッド', work_id=work1.work_id),
        Character(character_name='サボ', work_id=work1.work_id),
        Character(character_name='エース', work_id=work1.work_id),
        Character(character_name='神楽', work_id=work2.work_id),
        Character(character_name='沖田総悟', work_id=work2.work_id),
        Character(character_name='土方十四郎', work_id=work2.work_id),
        Character(character_name='坂田銀時', work_id=work2.work_id),
    ]

    # Categoryデータ
    categories = [
        Category(category_name='缶バッジ'),
        Category(category_name='アートコースター'),
        Category(category_name='ステータスカードコレクション'),
        Category(category_name='マスコット'),
        Category(category_name='ウエハースカード'),
        Category(category_name='ステッカー'),
        Category(category_name='アクリルフィギュア'),
        Category(category_name='紙類'),
        Category(category_name='フィギュア'),
        Category(category_name='色紙'),
        Category(category_name='その他'),
    ]

    # MoneyCurrency データ
    curency_usd = MoneyCurrency(currency_code='USD')
    curency_jpy = MoneyCurrency(currency_code='JPY')

    db.session.add(curency_usd)
    db.session.add(curency_jpy)
    db.session.commit()

    # ExhibitorPlatformデータ
    exhibitor_platforms = [
        ExhibitorPlatform(exhibitor_platform_name='merukari', money_currency_id=curency_jpy.money_currency_id),
        ExhibitorPlatform(exhibitor_platform_name='eBay', money_currency_id=curency_usd.money_currency_id),
        ExhibitorPlatform(exhibitor_platform_name='Amazon', money_currency_id=curency_jpy.money_currency_id),
        ExhibitorPlatform(exhibitor_platform_name='楽天市場', money_currency_id=curency_jpy.money_currency_id),
        ExhibitorPlatform(exhibitor_platform_name='ラクマ', money_currency_id=curency_jpy.money_currency_id),
        ExhibitorPlatform(exhibitor_platform_name='ヤフオク', money_currency_id=curency_jpy.money_currency_id),
    ]

    # Statusデータ
    statuses = [
        Status(status_name='入金待ち'),
        Status(status_name='発送準備中'),
        Status(status_name='発送中'),
        Status(status_name='受け取り評価待ち'),
        Status(status_name='取引完了'),
        Status(status_name='キャンセル対応中'),
        Status(status_name='その他'),
    ]

    # Areaデータ
    area_global = Area(area_name='Global')
    area_japan = Area(area_name='Japan')

    db.session.add(area_global)
    db.session.add(area_japan)
    db.session.commit()

    # Shipmentデータ
    shipments = [
        Shipment(shipment_name='飛行機', area_id=area_global.area_id),
        Shipment(shipment_name='佐川急便', area_id=area_japan.area_id),
        Shipment(shipment_name='ヤマト運輸', area_id=area_japan.area_id),
        Shipment(shipment_name='日本郵便', area_id=area_japan.area_id),
        Shipment(shipment_name='船', area_id=area_global.area_id),
        Shipment(shipment_name='その他', area_id=area_global.area_id),
    ]

    # Worldデータ
    worlds = [
        World(country_name='United States', area_id=area_global.area_id),
        World(country_name='Canada', area_id=area_global.area_id),
        World(country_name='China', area_id=area_global.area_id),
        World(country_name='Korea', area_id=area_global.area_id),
        World(country_name='Australia', area_id=area_global.area_id),
        World(country_name='Indonesia', area_id=area_global.area_id),
    ]

    # Japanデータ
    japans = [
        Japan(prefecture_name='Tokyo', area_id=area_japan.area_id),
        Japan(prefecture_name='Osaka', area_id=area_japan.area_id),
        Japan(prefecture_name='Kyoto', area_id=area_japan.area_id),
        Japan(prefecture_name='Saitama', area_id=area_japan.area_id),
    ]

    # StorageSpaceデータ
    storage_spaces = [
        StorageSpace(storage_space_name='BoxA'),
        StorageSpace(storage_space_name='BoxB'),
        StorageSpace(storage_space_name='BoxC'),
        StorageSpace(storage_space_name='FileA'),
        StorageSpace(storage_space_name='FileB'),
        StorageSpace(storage_space_name='FileC'),
        StorageSpace(storage_space_name='FileD'),
    ]

    # データベースに追加
    for character in characters:
        db.session.add(character)
    for category in categories:
        db.session.add(category)
    for platform in exhibitor_platforms:
        db.session.add(platform)
    for status in statuses:
        db.session.add(status)
    for shipment in shipments:
        db.session.add(shipment)
    for world in worlds:
        db.session.add(world)
    for japan in japans:
        db.session.add(japan)
    for storage in storage_spaces:
        db.session.add(storage)

    # 変更をコミット
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_data()
