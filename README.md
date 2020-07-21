# Overview

[LINE Pay v3 SDK](https://github.com/sumihiro3/line-pay-sdk-python)をベースにしたオンラインでの LINE Pay 決済を簡単に導入できるようにするスターターアプリです。

# Prepare

## LINE Pay 加盟店情報

* 加盟店審査が完了している方はご自身のもので、まだの方は[Sandbox](https://pay.line.me/jp/developers/techsupport/sandbox/testflow?locale=ja_JP)を作成


### Herokuにデプロイする場合

* `xxx`はそれぞれ任意の値を設定

```
$ heroku login

$ heroku create line-pay-app-xxx
$ heroku git:remote -a line-pay-app-xxx
$ git push heroku master

$ heroku config:set LINE_PAY_CHANNEL_ID=xxx
$ heroku config:set LINE_PAY_CHANNEL_SECRET=xxx
```

[https://line-pay-app-xxx.herokuapp.com](https://line-pay-app-xxx.herokuapp.com)にアクセスし`Request`ボタンを押して一般決済を試す。

問題なければ[https://line-pay-app-xxx.herokuapp.com/request/nocapture](https://line-pay-app-xxx.herokuapp.com/request/nocapture)をユーザーにLINE上で送信し決済してもらう。

金額を変えたい場合は`app.py`の`amount`の値を変更する。

### ローカルで試す場合

* Sandboxを利用しない方は`app.py`の上の方の`LINE_PAY_IS_SANDBOX`を`False`に変更

* `.env_sample`を`.env`にリネーム
* `.env`記載のID、SECRETをご自身のものに置き換え


```bash
$ pip install -r requirements.txt
$ python app.py
```

[localhost:8000](localhost:8000)にアクセスし`Request`ボタンを押して一般決済を試す。
