# Overview

オンラインでの LINE Pay 決済を簡単に導入できるスターターアプリです。

# 注意

2020/7/15より、店頭にプリントQRを置くタイプの店頭決済サービス加盟店は、[LINE上でお支払いリクエストの送信が可能に](http://pay-merchant-blog.line.me/archives/25349264.html)なりました。手動の一般決済だけを利用したい場合はそちらをご利用ください（オンライン決済加盟店とは別IDで加盟店申請が必要です。実店舗がない事業者は許可されなかもしれません）

# Usage

## LINE Pay 加盟店情報の準備

LINE Pay 加盟店申請を済ませておき、[加盟店MyPage](https://pay.line.me/portal/jp/mypage)にログインできるようにしておく。

決済連動管理＞連動キー管理から

* Channel ID
* Channel Secret Key

を確認し、控えておく。


## Herokuにデプロイする

`xxx`はそれぞれ任意の値を設定

```
$ git clone https://github.com/maztak/line-pay-v3-python-starter.git line-pay-app-xxx

$ heroku login
$ heroku create line-pay-app-xxx

$ cd line-pay-app-xxx
$ git init

$ heroku git:remote -a line-pay-app-xxx
$ git push heroku master

$ heroku config:set LINE_PAY_CHANNEL_ID=xxx
$ heroku config:set LINE_PAY_CHANNEL_SECRET=xxx
```

[https://line-pay-app-xxx.herokuapp.com](https://line-pay-app-xxx.herokuapp.com)にアクセスし`LINE Pay で決済する`ボタンを押して一般決済を試す。

問題なければボタンのリンク先である[https://line-pay-app-xxx.herokuapp.com/request/capture](https://line-pay-app-xxx.herokuapp.com/request/capture)をユーザーにLINEで送信し、決済してもらう。

金額を変えたい場合は`app.py`の51行目付近にある`reserve_payment`メソッドの`amount`の値を変更してください。

```app.py
@app.route('/request/<param_capture>')
def reserve_payment(param_capture):
    order_id = str(uuid.uuid4())
    amount = 1 # ここを変更
    currency = "JPY"
    CACHE["order_id"] = order_id
    CACHE["amount"] = amount
    CACHE["currency"] = currency
    request_options = {

```

## 取引履歴の確認や返金

取引履歴の確認や返金は [LINE Pay 加盟店 My Page](https://pay.line.me/portal/jp/mypage) で行ってください。

## その他の決済方法

トップページには売上確定（キャプチャ）まで自動で行う`Request & Capture`ボタンを`LINE Pay で決済する`という文言にして、これのみ表示しています。

売上確定は手動で行う`Request`ボタン, 配送を伴なう決済である`Checkout`ボタン, 自動決済（サブスク）をするための`Get RegKey`ボタンはコメントアウトしています。

Checkoutを利用するには、プライバシーポリシーのリンクと、配送方法と送料を照会できる`inquiryShippingMethods`のカスタマイズも同時に行う必要があり少し高度です。

またRegKeyの取得や自動決済は事前に許可された加盟店しか利用できません。

# テストで利用したい場合

## Sandboxの利用

加盟店申請をしなくとも[Sandbox](https://pay.line.me/jp/developers/techsupport/sandbox/testflow?locale=ja_JP)でテストアカウントを作成し試すこともできます。

## Sandboxのウォレットから引き落とす

`app.py`の上の方の`LINE_PAY_IS_SANDBOX`を`True`に変更すると実際のウォレットからは引き落とされずSandboxのテストウォレットで決済を試すことができます。

## ローカルで試す場合

Herokuへのデプロイもせずローカルで試すこともできます。

ただしPython3.6以上が必要です。

* `.env_sample`を`.env`にリネーム
* `.env`に記載のID、SECRETをご自身のSandboxのものに置き換え

```bash
$ git clone https://github.com/maztak/line-pay-v3-python-starter.git line-pay-app-xxx
$ cd line-pay-app-xxx

$ pip install -r requirements.txt
$ python app.py
```

[localhost:5000](localhost:5000)にアクセスし`LINE Pay で支払う`ボタンを押して一般決済を試す。

# Based On

SDKを作ってくれた加川さん、それをWeb上で試せるアプリにしてくれた立花さんのアプリをベースにさせていただいています。具体的には立花さんのアプリからkintone連携なしで利用できる形にしています。

* [LINE Pay v3 SDK Python](https://github.com/sumihiro3/line-pay-sdk-python)
* [LINE Pay v3 SDK Python Sample with kintone](https://github.com/stachibana/line-pay-v3-python-sdk-sample)