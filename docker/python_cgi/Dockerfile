# pythonはイメージから
FROM python:3.8.5

# ユーザ作成
RUN groupadd web
RUN useradd -d /home/python -m python

WORKDIR /home/python

# pipインストール(最新版)
RUN wget https://bootstrap.pypa.io/get-pip.py | python

# for psycopg2のインストール
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install urllib3 requests_oauthlib requests psycopg2

# サーバ設置ファイル
COPY cgiserver.py /home/python
# テスト用のHTML
COPY html/index.html /home/python
# cgi-binフォルダを作成
RUN mkdir -p cgi-bin
COPY cgi-bin/search.py /home/python/cgi-bin
COPY cgi-bin/config.py /home/python/cgi-bin
RUN chmod 755 /home/python/cgi-bin/search.py

# ポート番号を指定して、CGIサーバを起動
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/python", "/home/python/cgiserver.py"]
USER python
