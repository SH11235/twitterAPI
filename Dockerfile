# pythonはイメージから
FROM python:3.8.5

# ユーザ作成
RUN groupadd web
RUN useradd -d /home/python -m python

WORKDIR /home/python

# pipインストール(最新版)
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

RUN pip install urllib3
RUN pip install requests_oauthlib
RUN pip install requests

# サーバ設置ファイル
ADD cgiserver.py /home/python
# テスト用のHTML
ADD index.html /home/python
# cgi-binフォルダを作成
RUN mkdir cgi-bin
ADD search.py /home/python/cgi-bin
ADD config.py /home/python/cgi-bin
RUN chmod 755 /home/python/cgi-bin/search.py

# ポート番号を指定して、CGIサーバを起動
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/python", "/home/python/cgiserver.py"]
USER python
