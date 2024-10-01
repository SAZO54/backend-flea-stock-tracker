# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /code

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコンテナにコピー
COPY . .

# Flaskアプリケーションのポートを公開
EXPOSE 5000

# アプリケーションのエントリーポイントを設定
CMD ["flask", "run", "--host=0.0.0.0"]
