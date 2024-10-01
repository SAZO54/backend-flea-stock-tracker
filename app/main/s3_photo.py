import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from dotenv import load_dotenv
import os
import mimetypes

load_dotenv()

s3_client = boto3.client(
  's3',
  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
,)

# アップロードを許可するファイル拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_s3(file, bucketname, s3_file_key):
    if not allowed_file(file.filename):
        print("許可されていないファイルタイプです")
        return None
    
    try:
        # ファイルのMIMEタイプを取得
        content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'

        s3_client.upload_fileobj(file, bucketname, s3_file_key, ExtraArgs={"ContentType": content_type})

        s3_bucket_name = os.getenv('AWS_BUCKET_NAME')
        s3_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_file_key}"
        print("s3_url", s3_url)
        return s3_url

    except FileNotFoundError:
        print('ファイルが見つかりませんでした')
        return None
    except NoCredentialsError:
        print('AWS認証情報が提供されていません')
        return None
    except PartialCredentialsError:
        print('AWS認証情報が不完全です')
        return None
    except ClientError as e:
        print(f"S3エラーが発生しました: {e}")
        return None
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return None
