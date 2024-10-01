import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from app.main.s3_photo import upload_file_s3
from werkzeug.datastructures import FileStorage

# テスト用の画像ファイルパスを指定
file_path = './ebay.png'  # 実際のファイルパスに変更してください
bucket_name = os.getenv('AWS_BUCKET_NAME')
s3_file_key = 'test-folder/test-image.png'

# ファイルオブジェクトを作成
with open(file_path, 'rb') as file:
    file_obj = FileStorage(file)

    # S3にアップロード
    s3_url = upload_file_s3(file_obj, bucket_name, s3_file_key)

    if s3_url:
        print(f"ファイルがS3にアップロードされました: {s3_url}")
    else:
        print("S3へのファイルアップロードに失敗しました")
