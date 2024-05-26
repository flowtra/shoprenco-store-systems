import pymongo.errors
from flask import Flask
import requests
from flask import request, redirect
import json
global req_headers
from app import dbhelper

itemRef = {
  'itemList': [
    {
      'apiRef': 'Black XXS',
      'id': 99784,
      'ticketId': 'tid_s7Q0tzABAA',
      'ticketName': 'Black Sweater - XXS'
    },
    {
      'apiRef': 'Black XS',
      'id': 99785,
      'ticketId': 'tid_s7Q0tzAFAA',
      'ticketName': 'Black Sweater - XS'
    },
    {
      'apiRef': 'Black S',
      'id': 99786,
      'ticketId': 'tid_s7Q0tzADAA',
      'ticketName': 'Black Sweater - S'
    },
    {
      'apiRef': 'Black M',
      'id': 99787,
      'ticketId': 'tid_s7Q0tzAHAA',
      'ticketName': 'Black Sweater - M'
    },
    {
      'apiRef': 'Black L',
      'id': 99788,
      'ticketId': 'tid_s7Q0t7AAAA',
      'ticketName': 'Black Sweater - L'
    },
    {
      'apiRef': 'Black XL',
      'id': 99790,
      'ticketId': 'tid_s7Q0tzQAAA',
      'ticketName': 'Black Sweater - XL'
    },
    {
      'apiRef': 'White XXS',
      'id': 99791,
      'ticketId': 'tid_s7Q0tzQEAA',
      'ticketName': 'White Sweater - XXS'
    },
    {
      'apiRef': 'White XS',
      'id': 99792,
      'ticketId': 'tid_s7Q0tzQCAA',
      'ticketName': 'White Sweater - XS'
    },
    {
      'apiRef': 'White S',
      'id': 99793,
      'ticketId': 'tid_s7Q0tzQGAA',
      'ticketName': 'White Sweater - S'
    },
    {
      'apiRef': 'White M',
      'id': 99794,
      'ticketId': 'tid_s7Q0tzQBAA',
      'ticketName': 'White Sweater - M'
    },
    {
      'apiRef': 'White L',
      'id': 99795,
      'ticketId': 'tid_s7Q0tzQFAA',
      'ticketName': 'White Sweater - L'
    },
    {
      'apiRef': 'White XL',
      'id': 99796,
      'ticketId': 'tid_s7Q0tzQDAA',
      'ticketName': 'White Sweater - XL'
    },
    {
      'apiRef': 'Cream XXS',
      'id': 99797,
      'ticketId': 'tid_s7Q0tzQHAA',
      'ticketName': 'Cream Sweater - XXS'
    },
    {
      'apiRef': 'Cream XS',
      'id': 99798,
      'ticketId': 'tid_s7Q0t7QAAA',
      'ticketName': 'Cream Sweater - XS'
    },
    {
      'apiRef': 'Cream S',
      'id': 99799,
      'ticketId': 'tid_s7Q0t7QEAA',
      'ticketName': 'Cream Sweater - S'
    },
    {
      'apiRef': 'Cream M',
      'id': 99800,
      'ticketId': 'tid_s7S0MDAAAA',
      'ticketName': 'Cream Sweater - M'
    },
    {
      'apiRef': 'Cream L',
      'id': 99801,
      'ticketId': 'tid_s7S0MDAEAA',
      'ticketName': 'Cream Sweater - L'
    },
    {
      'apiRef': 'Cream XL',
      'id': 99802,
      'ticketId': 'tid_s7S0MDACAA',
      'ticketName': 'Cream Sweater - XL'
    }
  ]
}

db = dbhelper.DBHelper("mongodb+srv://doadmin:REDACTED@REDACTED.mongo.ondigitalocean.com/admin?authSource=admin", "shirts22")

req_headers = {
        "Cookie": f"",
        "x-csrf-token": f"",
        "content-type": "application/json"
    }

def newHeaders():
    global req_headers
    s = requests.Session()

    r = s.get('https://appv3.eventnook.com/account/login')
    csrf = r.text.split('name="X_CSRF_TOKEN" value="')[1].split('"')[0]
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = f'username=REDACTED&password=REDACTED&X_CSRF_TOKEN={csrf}&X_CSRF_TOKEN={csrf}'
    r = s.post('https://appv3.eventnook.com/account/login', headers=headers, data=data)

    cookie_dict = s.cookies.get_dict()

    cookie_aspnetcore = cookie_dict['.AspNetCore.Antiforgery.RtGCWVXC8-4']
    cookie_eventuseradmin = cookie_dict['EventUserAdmin.Cookie']

    r = s.get('https://appv3.eventnook.com/manage/report/vieworders/REDACTED')
    print(r.text)
    csrf = r.text.split('data-serialized-id="csrf-token">"')[1].split('"')[0]
    req_headers['Cookie'] = f"EventUserAdmin.Cookie={cookie_eventuseradmin}; .AspNetCore.Antiforgery.RtGCWVXC8-4={cookie_aspnetcore}"
    req_headers['x-csrf-token'] = f"{csrf}"

    return req_headers

def getOrders(eventID, orderStatus):
    global req_headers
    data = '{"eventIds":null,"orderNo":null,"orderStatus":"' + orderStatus + '","orderType":null,"paymentTypes":["all"],"tickets":null,"orderedStartDate":null,"orderedEndDate":null,"customSearchFields":[],"sortField":"id","sortOrder":"desc","page":1,"pageSize":60000}'
    while True:
        try:
            r = requests.post(f'https://appv3.eventnook.com/api/v1/order/list/{eventID}', data=data, headers=req_headers)
            r = r.json()
            if r["status"] == "success":
                return r["data"]["orders"]
            else:
                req_headers = newHeaders()
        except json.decoder.JSONDecodeError:
            print(f"ERROR | JSON Not Found/Could not be decoded - {r}")
            return False

def getOrderDetails(eventID, orderNo):
    all_orders = getOrders(eventID, 'all')
    for order in all_orders:
        if order['orderNo'] == orderNo:
            return order

def getOrderItems(eventID, orderNo):
    global req_headers

    orderDetails = getOrderDetails(eventID, orderNo)
    try:
        orderID = orderDetails['uid']
    except TypeError:
        return "Order ID Not Found"

    r = requests.get(
        f'https://appv3.eventnook.com/manage/order/vieworder/{eventID}/{orderID}/{orderNo}',
        headers=req_headers)

    orderDetails = json.loads(str(r.text).split('_ss.xw = ')[1].split(';')[0])
    print(orderDetails)
    orderStatus = orderDetails['order']['orderStatus']
    orderItems = orderDetails['order']['orderItems']
    orderName = orderDetails['order']['fullName']
    responseDict = {'_id': orderNo, 'orderName': orderName, 'payment_status': orderStatus, 'items': [], 'collected': 'false'}

    for item in orderItems:
        itemName = item['itemName']
        itemQuantity = item['quantity']
        responseDict['items'].append({'itemName': itemName, 'itemQuantity': itemQuantity})

    return responseDict

def submitOrder(orderItems, buyer_email, buyer_name, buyer_class):

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15',
    }

    data = {
          "email": None,
          "mobile": None,
          "discountCode": None,
          "invitationCode": None,
          "priceCategoryCode": None,
          "orderItems": orderItems,
          "params": {
          },
          "bookingAdmissionDateId": None,
          "bookingSessionId": None
        }
    r1 = requests.post('https://reg.eventnook.com/api/v1/checkout/createsession/REDACTED', json=data, headers=headers)
    print(r1.text)
    try:
        uid = r1.json()["data"]["uid"]
        publishableKey = r1.json()["data"]["publishableKey"]
    except Exception as e:
        print(e)

    data = {
      "eid": "REDACTED",
      "uid": uid,
      "formList": [],
      "buyerForm": {
        "buyerfirstname": None,
        "buyerlastname": None,
        "buyeremail": None
      },
      "publishableKey": publishableKey,
      "params": {}
    }

    firstCheck = True
    for x in r1.json()['data']['orderItems']:
        print(x)
        for i in range(int(x["quantity"])):
            if firstCheck:
                data["formList"].append({
                                      "uid": None,
                                      "id": x["id"],
                                      "itemId": x["itemId"],
                                      "itemName": x["itemName"],
                                      "issuedTicketCode": None,
                                      "ticketStatus": None,
                                      "tagging": None,
                                      "tableNo": None,
                                      "seatNo": None,
                                      "attendeeCategory": None,
                                      "formDetails": {
                                        "fullname": buyer_name,
                                        "116342_customfield6": buyer_class,
                                        "email": buyer_email
                                      }
                                    })
                firstCheck = False
            else:
                data["formList"].append({
                                      "uid": None,
                                      "id": x["id"],
                                      "itemId": x["itemId"],
                                      "itemName": x["itemName"],
                                      "issuedTicketCode": None,
                                      "ticketStatus": None,
                                      "tagging": None,
                                      "tableNo": None,
                                      "seatNo": None,
                                      "attendeeCategory": None,
                                      "formDetails": {
                                        "fullname": None,
                                        "116342_customfield6": None,
                                        "email": None
                                      }
                                    })


    r2 = requests.post('https://reg.eventnook.com/api/v1/checkout/form/REDACTED', json=data, headers=headers)
    publishableKey = r2.json()['data']['publishableKey']
    headers['publishable_key'] = publishableKey

    data = {"uid": uid,"paymentType":"PAYNOW"}

    r3 = requests.post('https://reg.eventnook.com/api/v1/checkout/payment/REDACTED', json=data, headers=headers)
    redirectUrl = r3.json()['redirectUrl']

    return redirectUrl


app = Flask(__name__)


@app.route("/newOrder", methods=['POST'])
def newOrder():
    orderItems = []
    buyer_email = request.form.get("buyer_email")
    buyer_name = request.form.get("buyer_name")
    buyer_class = request.form.get("buyer_class")

    items = request.form.items()
    for k, v in items:
        if 'item' in k:
            apiRef, qty = v.split(' ,')
            for item in itemRef["itemList"]:
                if item["apiRef"] == apiRef:
                    itemId = item["id"]
                    ticketId = item["ticketId"]
            orderItems.append(
                {
                    "id": itemId,
                    "itemId": ticketId,
                    "quantity": int(qty),
                    "price": 24.90
                }
            )

    redirectUrl = submitOrder(orderItems, buyer_email, buyer_name, buyer_class)

    return redirect(f"https://reg.eventnook.com{redirectUrl}")

# @app.before_first_request
@app.route("/newHeaders")
def newHeaderLink():
    global req_headers

    req_headers = newHeaders()
    print(req_headers)
    if req_headers:
        return "New Headers Set"

@app.route("/getOrder")
def getOrder():
    orderNo = request.args.get('orderNo')

    return getOrderItems(eventID, orderNo)

@app.route("/db/addOrder")
def db_addOrder():
    orderNo = request.args.get('orderNo')
    to_add = getOrderItems(eventID, orderNo)
    try:
        db.order_add(to_add)
    except pymongo.errors.DuplicateKeyError:
        return "Order already exists in the database!"

    return f'Added the following: \n {str(to_add)}'

# orderItems = [{'id': 99801, 'itemId': 'tid_s7S0MDAEAA', 'quantity': 2, 'price': 24.9}, {'id': 99800, 'itemId': 'tid_s7S0MDAAAA', 'quantity': 1, 'price': 24.9}, {'id': 99784, 'itemId': 'tid_s7Q0tzABAA', 'quantity': 2, 'price': 24.9}]
# submitOrder(orderItems)