import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

ENABLE_NOTIFICATIONS = True

def notify_offer_made(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_offer_made' - {} - {}".format(r.text,r.raw))
    return False, r.status_code


def notify_verify_email(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_verify_email' - {} - {}".format(r.text,r.raw))
    return False, r.status_code


def notify_email_verified(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_email_verified' - {} - {}".format(r.text,r.raw))
    return False, r.status_code
    
def notify_bid_made(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_bid_made' - {} - {}".format(r.text,r.raw))
    return False, r.status_code


def notify_auction_ended(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_auction_ended' - {} - {}".format(r.text,r.raw))
    return False, r.status_code

def notify_auction_won(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_auction_won' - {} - {}".format(r.text,r.raw))
    return False, r.status_code

def notify_auction_sold(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_auction_sold' - {} - {}".format(r.text,r.raw))
    return False, r.status_code

def notify_password_reset_token(data):
    if not ENABLE_NOTIFICATIONS:
        return
    url = "<Your webhook url>"
    r = requests.post(url,data=json.dumps(data),headers={'content-type':'application/json'})
    if r.status_code == 200:
        print(r.text)
        print(r.raw)
        return True, 200
    print(r.raw)
    print(r.text)
    logging.error("Could not send 'notify_password_reset_token' - {} - {}".format(r.text,r.raw))
    return False, r.status_code