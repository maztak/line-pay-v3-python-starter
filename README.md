# Overview

オンラインでの LINE Pay 決済を簡単に導入できるスターターアプリです。

# 注意

2020/7/15より、店頭にプリントQRを置くタイプの店頭決済サービス加盟店は、[LINE上でお支払いリクエストの送信が可能に](http://pay-merchant-blog.line.me/archives/25349264.html)なりました。手動の一般決済だけを利用したい場合はそちらをご利用ください（オンライン決済加盟店とは別IDで加盟店申請が必要です。実店舗がない事業者は許可されなかもしれません）

# Usage

## LINE Pay 加盟店情報の準備

加盟店審査が完了している方はご自身のもので、まだの方は[Sandbox](https://pay.line.me/jp/developers/techsupport/sandbox/testflow?locale=ja_JP)を作成


## Herokuにデプロイする

`xxx`はそれぞれ任意の値を設定

```
$ git clone https://github.com/maztak/line-pay-v3-python-starter.git line-pay-app-xxx
$ heroku login

$ heroku create line-pay-app-xxx
$ heroku git:remote -a line-pay-app-xxx
$ git push heroku master

$ heroku config:set LINE_PAY_CHANNEL_ID=xxx
$ heroku config:set LINE_PAY_CHANNEL_SECRET=xxx
```

[https://line-pay-app-xxx.herokuapp.com](https://line-pay-app-xxx.herokuapp.com)にアクセスし`LINE Pay で決済する`ボタンを押して一般決済を試す。

問題なければボタンのリンク先である[https://line-pay-app-xxx.herokuapp.com/request/capture](https://line-pay-app-xxx.herokuapp.com/request/capture)をユーザーにLINEで送信し、決済してもらう。

金額を変えたい場合は`app.py`の51行目付近にある`reserve_payment`メソッドの`amount`の値を変更してください。

```python

request_options = {
    "amount": amount,
    "currency": currency,
    "orderId": order_id,
    "packages": [
        {
            "id": "package-999",
            "amount": 1,
            "name": "Sample package",
            "products": [
                    {
                        "id": "product-001",
                        "name": "Sample product",
                        "imageUrl": "https://placehold.jp/99ccff/003366/150x150.png?text=Sample%20product",
                                    "quantity": 1,
                                    "price": 1
                    }
            ]
        }
    ],

```

### 取引履歴の確認や返金

取引履歴の確認や返金は[LINE Pay 加盟店 My Page](https://pay.line.me/portal/jp/mypage)で行ってください。

#️## その他の決済方法

トップページには売上確定（キャプチャ）まで自動で行う`Request & Capture`ボタンを`LINE Pay で決済する`という文言にして、これのみ表示しています。

売上確定は手動で行う`Request`ボタン, 配送を伴なう決済である`Checkout`ボタン, 自動決済（サブスク）をするための`Get RegKey`ボタンはコメントアウトしています。

Checkoutを利用するには、プライバシーポリシーのリンクと、配送方法と送料を照会できる`inquiryShippingMethods`のカスタマイズも同時に行う必要があり少し高度です。

またRegKeyを取得や自動決済は事前に許可された加盟店しか利用できません。

### ローカルで試す場合

* Sandboxを利用しない方は`app.py`の上の方の`LINE_PAY_IS_SANDBOX`を`False`に変更

* `.env_sample`を`.env`にリネーム
* `.env`記載のID、SECRETをご自身のものに置き換え


```bash
$ pip install -r requirements.txt
$ python app.py
```

[localhost:5000](localhost:5000)にアクセスし`LINE Pay で支払う`ボタンを押して一般決済を試す。

### Based On

SDKを作ってくれた加川さん、それをWeb上で試せるアプリにしてくれた立花さんのアプリをベースにさせていただいています。

具体的には立花さんのアプリからkintone連携なしで利用できる形にしています。

* [LINE Pay v3 SDK Python](https://github.com/sumihiro3/line-pay-sdk-python)
* [LINE Pay v3 SDK Python Sample with kintone](https://github.com/stachibana/line-pay-v3-python-sdk-sample)