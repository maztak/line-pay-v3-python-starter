# Overview

オンラインでの LINE Pay 決済を簡単に導入できるスターターアプリです。

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

[localhost:5000](localhost:5000)にアクセスし`Request`ボタンを押して一般決済を試す。

### Based On

SDKを作ってくれた加川さん、それをWeb上で試せるアプリにしてくれた立花さんのアプリをベースにさせていただいています。

具体的には立花さんのアプリからkintone連携なしで利用できる形にしています。

* [LINE Pay v3 SDK Python](https://github.com/sumihiro3/line-pay-sdk-python)
* [LINE Pay v3 SDK Python Sample with kintone](https://github.com/stachibana/line-pay-v3-python-sdk-sample)