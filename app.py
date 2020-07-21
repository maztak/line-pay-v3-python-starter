from flask import Flask, request, render_template, abort, redirect, jsonify
from flask_bootstrap import Bootstrap
import uuid
import os
from os.path import join, dirname
from dotenv import load_dotenv
from linepay import LinePayApi
import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)

# dotenv
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# LINE Pay API
LINE_PAY_CHANNEL_ID = os.environ.get("LINE_PAY_CHANNEL_ID")
LINE_PAY_CHANNEL_SECRET = os.environ.get("LINE_PAY_CHANNEL_SECRET")
LINE_PAY_IS_SANDBOX = True  # True | False
api = LinePayApi(LINE_PAY_CHANNEL_ID,
                 LINE_PAY_CHANNEL_SECRET, is_sandbox=LINE_PAY_IS_SANDBOX)

# Cache
CACHE = {}

def get_environment():
    return LINE_PAY_IS_SANDBOX


app.jinja_env.globals.update(get_environment=get_environment)


@app.route('/')
def do_get():
    return render_template('index.html')


@app.route('/cancel')
def cancel():
    return redirect('/')


@app.route('/request/<param_capture>')
def reserve_payment(param_capture):
    order_id = str(uuid.uuid4())
    amount = 1
    currency = "JPY"
    CACHE["order_id"] = order_id
    CACHE["amount"] = amount
    CACHE["currency"] = currency
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
        "options": {
            "payment": {
                "capture": True if param_capture == 'capture' else False
            }
        },
        "redirectUrls": {
            "confirmUrl": request.host_url + "confirm",
            "cancelUrl": request.host_url + "cancel"
        }
    }
    response = api.request(request_options)

    return redirect(response['info']['paymentUrl']['web'])


@app.route('/checkout/')
def checkout():
    order_id = str(uuid.uuid4())
    amount = 1
    currency = "JPY"
    CACHE["order_id"] = order_id
    CACHE["amount"] = amount
    CACHE["currency"] = currency
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
        "options": {
            "payment": {
                "capture": True
            },
            "shipping": {
                "type": "SHIPPING",
                "feeInquiryUrl": request.host_url.replace('http', 'https') + "v1/shippings/methods/get/"
            }
        },
        "redirectUrls": {
            "confirmUrl": request.host_url.replace('http', 'https') + "confirm",
            "cancelUrl": request.host_url.replace('http', 'https') + "cancel"
        }
    }
    response = api.request(request_options)

    return redirect(response['info']['paymentUrl']['web'])


@app.route('/v1/shippings/methods/get/', methods=["POST"])
def inquiryShippingMethods():
    result = {
        "returnCode": "0000",
        "returnMessage": "Example",
        "info": {
            "shippingMethods": [
                {
                    "id": "hoge",
                    "name": "hogehoge express",
                    "amount": "1000",
                    "toDeliveryYmd": datetime.datetime.now().strftime("%Y%m%d")
                }
            ]
        }
    }
    return jsonify(result)


@app.route('/pay_get_regkey/')
def pay_get_regkey():
    order_id = str(uuid.uuid4())
    amount = 1
    currency = "JPY"
    CACHE["order_id"] = order_id
    CACHE["amount"] = amount
    CACHE["currency"] = currency
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
        "options": {
            "payment": {
                "capture": True,
                "payType": "PREAPPROVED"
            }
        },
        "redirectUrls": {
            "confirmUrl": request.host_url.replace('http', 'https') + "confirm",
            "cancelUrl": request.host_url.replace('http', 'https') + "cancel"
        }
    }
    response = api.request(request_options)

    return redirect(response['info']['paymentUrl']['web'])


@app.route('/capture/<int:transaction_id>/<float:amount>/<currency>/')
def capture_transaction(transaction_id, amount, currency):
    response = api.capture(transaction_id, amount, currency)
    return redirect('/')


@app.route('/void/<int:transaction_id>/')
def void_authorization(transaction_id):
    response = api.void(transaction_id)
    return redirect('/')


@app.route('/refund/<int:transaction_id>/<float:refund_amount>/')
def refund(transaction_id, refund_amount):
    response = api.refund(transaction_id)
    return redirect('/')


@app.route("/confirm")
def pay_confirm():
    transaction_id = int(request.args.get('transactionId'))

    CACHE["transaction_id"] = int(transaction_id)
    response = api.confirm(
        transaction_id,
        float(CACHE.get("amount", 0)),
        CACHE.get("currency", "JPY")
    )

    return redirect('/')


@app.route("/pay_preapproved/<reg_key>/")
def pay_preapproved(reg_key):

    order_id = str(uuid.uuid4())
    amount = 1
    currency = "JPY"
    product_name = "定期購入アイテム"

    response = api.pay_preapproved(
        reg_key, product_name, float(amount), currency, order_id, True)

    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run()
