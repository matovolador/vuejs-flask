from tendo import singleton
from modules import database
import traceback
import logging
from datetime import datetime
import zapier

me = singleton.SingleInstance()

logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

# now = datetime.now().astimezone()
# date_from = datetime(now.year,now.month,now.day,9,0,0,0)
# date_to = datetime(now.year,now.month,now.day,22,0,0,0)
# if (now<date_from or now>=date_to):
#     logging.info("Not running during {}".format(now))
#     exit()

db = next(database.get_db())
try:
    auctions = db.query(database.Listing).filter_by(listing_type='auction',auction_closed=False)
    for auction in auctions:
        if auction.end_date <= datetime.now().astimezone():
            last_bid = db.query(database.Bid).order_by(database.Bid.amount.desc()).filter_by(listing_id=auction.id).first()
            bids = db.query(database.Bid).filter_by(listing_id=auction.id)
            for bid in bids:
                if bid.id!=last_bid.id:
                    buyer = db.query(database.User).get(bid.created_by)
                    zapier.notify_auction_ended({"auction_name":auction.address,"recipient_email":buyer.email,"recipient_name":buyer.first_name+" "+buyer.last_name})
            won_by = db.query(database.User).get(last_bid.created_by)
            seller = db.query(database.User).get(auction.created_by)
            zapier.notify_auction_won({"auction_name":auction.address,"recipient_email":won_by.email,"recipient_name":won_by.first_name+" "+won_by.last_name,"amount":last_bid.amount,"seller_email":seller.email})
            zapier.notify_auction_sold({"auction_name":auction.address,"recipient_email":seller.email,"recipient_name":seller.first_name+" "+seller.last_name,"amount":last_bid.amount,"buyer_email":buyer.email})
            auction.auction_closed=True
    db.commit()    
except Exception as e:
    logging.error(e)
    logging.error(traceback.print_exc())

db.close()
