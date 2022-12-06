from flask import Flask, request,jsonify, make_response, render_template, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from flask_sslify import SSLify
from flask_session import Session
import requests
import json
import logging
import jwt
import traceback
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps
from modules import database
from aws import AWS_Hook
from uuid import uuid4
import os
import zapier
from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = "<>"

logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

app = Flask(__name__)
app.secret_key = '1234089eohrsdf230845509sjjgrkjt24i5'
CORS(app, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = "uploads"

def get_db():
    return next(database.get_db())

@app.route("/health")
def health():
    return jsonify({
        "success": True
    })

TOKEN_LIFE_MINUTES = 60 * 24 * 5  # 5 days

def generate_token(user):
    exp = int((datetime.now() + timedelta(minutes=TOKEN_LIFE_MINUTES)).timestamp())
    token = jwt.encode({'email':user['email'],'exp':exp},app.secret_key,algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        db = next(database.get_db())
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            db.close()
            return jsonify({
                "success": False,
                "message": "Token is missing!"
            }), 401

        try:
            data = jwt.decode(token,app.secret_key,algorithms="HS256")
            # validate token life:
            life = data['exp']
            rnow = int(datetime.now().timestamp())
            if rnow > life:
                # token no longer valid:
                db.close()
                return jsonify({
                    "message":"Token has expired. Please login again.",
                    "success": False
                }), 401
            current_user = db.query(database.User).filter_by(email=data['email']).first()
            #print(current_user.token)
            if current_user.token is None:
                db.close()
                return jsonify({
                    "success": False,
                    "message": "You must login."
                }),401
            if current_user.token != token:
                db.close()
                return jsonify({
                    "success": False,
                    "message": "Token invalid."
                }),401
            current_user = current_user.as_dict()
            
            db.close()
        except Exception as e:
            return jsonify({
                "message": "Token is invalid. "+str(e),
                "success": False
            }), 401
        if not current_user:
            return jsonify({
                    "message": "User is invalid",
                    "success": False
                }), 401
        return f(current_user,*args,**kwargs)
    return decorated

@app.route("/must_be_logged_in",methods=["GET"])
@token_required
def must_be_logged_in(current_user):
    print(current_user)
    return jsonify({
        "success": True,
        "message": "You are logged in!"
    }),200

@app.route("/login",methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    email_or_username = auth.username
    password = auth.password
    result, data = database.User.login_user(email_or_username=email_or_username,password=password)
    print(result)
    print(data)
    if result:
        db = next(database.get_db())
        token = generate_token(data)
        user = db.query(database.User).get(data['id'])
        user.token = token
        user_ = database.User.retrieve_clean_obj_data(user)
        db.commit()
        db.close()
        return jsonify({
            "success": True,
            "message": "You are now logged in.",
            "token": token,
            "user_id": user_['id'],
            "first_name": user_['first_name'],
            "last_name": user_['last_name'],
            "email": user_['email'],
            "type": user_['type']

        })
    else:
        try:
            db.close()
        finally:
            return jsonify({
                "success":False,
                "message": str(data)
            }),401

@app.route("/logout",methods=["GET"])
@token_required
def logout(current_user):
    db = next(database.get_db())
    user = db.query(database.User).get(current_user['id'])
    user.token = None
    user.last_seen = datetime.now()
    db.commit()
    db.close()
    return jsonify({
        "success":True
    })

@app.route("/renew-token", methods=["GET"])
@token_required
def renew_token(current_user):
    token = generate_token(current_user)
    db = next(database.get_db())
    user = db.query(database.User).filter_by(email=current_user['email']).first()
    user.token = token
    db.commit()
    db.close()
    return jsonify({
        "token": token,
        "success": True
    }), 200


@app.route("/registration",methods=["POST"])
def register():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    verify = False
    if "type" in data:
        user_type = data["type"]
    else:
        user_type = 0
    if user_type not in [0,1]:
        return jsonify({
            "success":False,
            "message":"Invalid user type {}".format(user_type)
        }),400
    db = get_db()
    user = db.query(database.User).filter_by(email=email).first()
    if user:
        db.close()
        return jsonify({
            "success": False,
            "message": "Email already taken."
        }),400
    success, msg = database.User.validate_password_field(password)
    if not success:
        db.close()
        return jsonify({
            "success":success,
            "message": msg
        })
    try:
        user = database.User(email=email,password=password,first_name=first_name,last_name=last_name,type=user_type)
        db.add(user)
        db.commit()
        validation_token,msg = database.User.generate_email_validation_token(user.id)
        if verify:
            r = database.User.validate_email(user.id,validation_token)
            print(r)
        else:
            zapier.notify_verify_email({"email":user.email,"token":validation_token})
        clean_data = database.User.retrieve_clean_obj_data(user)
        db.close()
        return jsonify({
            "success": True,
            "data": clean_data
        })
    except Exception as e:
        logging.error(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": "Exception "+str(e)
            }),400

@app.route("/reset_password",methods=["POST","GET"])
def reset_password():
    if request.method == "GET":
        email = request.values.get("email")
        db = get_db()
        user = db.query(database.User).filter_by(email=email).first()
        if not user:
            db.close()
            return jsonify({
                "success": False,
                "message": "User not found"
            })
        reset_token = database.User.generate_password_reset_token(user.id)
        db.close()
        zapier.notify_password_reset_token({"email":user.email,"reset_token":reset_token})
        return jsonify({
            "success": True,
            "message": "An email has been sent to you with a link to reset your password."
        })
    elif request.method == "POST":
        data = request.get_json()
        new_password = data["password"]
        reset_token = data["reset_token"]
        email = data['email']
        db = get_db()
        user = db.query(database.User).filter_by(email=email).first()
        if not user:
            db.close()
            return jsonify({
                "success": False,
                "message": "User not found"
            })
        success, msg = database.User.update_user_password(user.id,new_password,reset_token)
        db.close()
        status = 200
        if not success:
            status = 400
        return jsonify({
            "success":success,
            "message": msg
        }),status

@app.route("/change_password",methods=["POST"])
@token_required
def change_password(current_user):
    data = request.get_json()
    old_password = data['old_password']
    new_password = data['new_password']
    db = get_db()
    user = db.query(database.User).get(current_user['id'])
    if user.password != old_password:
        db.close()
        return jsonify({
            "success": False,
            "message": "Your current password field is incorrect."
        })
    
    success,msg = database.User.update_user_password(user.id,new_password,False)
    db.close()
    return jsonify({
        "success": success,
        "message": msg
    })

@app.route("/validate_email",methods=["GET"])
def api_validate_email():
    email = request.values.get("email")
    token = request.values.get("token")
    try:
        db = get_db()
        user = db.query(database.User).filter_by(email=email).first()
        db.close()
        if not user:
            return jsonify({
                "success": False,
                "message": "Email not found."
            })
    
        success, message, code = database.User.validate_email(user.id,token)
        print(success,message,code)
        if success:
            zapier.notify_email_verified({"email":user.email})
            return jsonify({
                "success": True
            })
        else:
            return jsonify({
                "success": False,
                "message": message
            }),400
    except Exception as e:
        print(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": str(e)
            }),500

@app.route("/users/<id>",methods=["GET"])
@token_required
def get_user(current_user,id):
    db = get_db()
    user = db.query(database.User).get(id)
    db.close()
    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }),400
    clean_user = database.User.retrieve_clean_obj_data(user)
    return jsonify({
        "success": True,
        "data": clean_user
    })

@app.route("/users/<id>/public",methods=["GET"])
def get_public_user(id):
    db = get_db()
    user = db.query(database.User).get(id)
    db.close()
    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }),400
    clean_user = database.User.retrieve_clean_obj_data(user,public=True)
    return jsonify({
        "success": True,
        "data": clean_user
    })


@app.route("/users/self",methods=["GET"])
@token_required
def get_user_self(current_user):
    try:
        db = get_db()
        user = db.query(database.User).get(current_user['id'])
        listings = db.query(database.Listing).filter_by(created_by=user.id)
        bids = db.query(database.Bid).filter_by(created_by=user.id)
        offers = db.query(database.Offer).filter_by(created_by=user.id)
        user_obj = database.User.retrieve_clean_obj_data(user)
        output = {}
        output['user'] = user_obj
        clean_listings = []
        for listing in listings:
            clean_listings.append(database.Listing.retrieve_clean_obj_data(listing))
        clean_bids = []
        for bid in bids:
            clean_bids.append(database.Bid.retrieve_clean_obj_data(bid))
        clean_offers = []
        for offer in offers:
            clean_offers.append(database.Offer.retrieve_clean_obj_data(offer))

        output['listings'] = clean_listings
        output['bids'] = clean_bids
        output['offers'] = clean_offers
        db.close()
        return jsonify({
            "success": True,
            "data": output
        }),200
    except Exception as e:
        print(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": str(e)
            })


@app.route("/listings",methods=["POST"])
@token_required
def create_listing(current_user):
    try:
        valid_incremental_price_amounts = [500, 1000, 1500, 2000, 2500]
        data = request.get_json()
        address = data['address']
        description = ''
        if 'description' in data:
            description = data['description']
        listing_type = data['listing_type']
        if listing_type not in ['auction','standard']:
            return jsonify({
                "success":False,
                "message": "Invalid listing_type {}".format(listing_type)
            }),400
        property_type = data['property_type']
        if property_type not in ['house','apartment']:
            return jsonify({
                "success":False,
                "message": "Invalid property_type {}".format(property_type)
            }),400
        property_size = float(data['property_size'])
        land_size = float(data['land_size'])
        bedrooms = int(data['bedrooms'])
        bathrooms = int(data['bathrooms'])
        city = data['city']
        state = data['city']
        zip_code = data['zip_code']

        try:
            year_built = int(data['year_built'])
        except:
            if data['year_built'] == "Pre-1985":
                pass
            else:
                return jsonify({
                    "success": False,
                    "message": "Invalid year_built {}".format(data['year_built'])
                }),400
        images = data['images']  # array of urls ['https://s3link.com/asdads','etc']
        if not images:
            return jsonify({
                "success": False,
                "message": "You must provide at least 1 image."
            }),400
        if type(images) != list:
            return jsonify({
                "success": False,
                "message": "'images' must be an array. found {}".format(type(images))
            }),400
        price = float(data['price'])
        if price == 0:
            return jsonify({
                "success": False,
                "message": "Price cant be 0"
            }),400
        incremental_price_amount = None
        if 'incremental_price_amount' in data:
            incremental_price_amount = float(data['incremental_price_amount'])
            if incremental_price_amount not in valid_incremental_price_amounts:
                return jsonify({
                    "success":False,
                    "message":"Invalid incremental_price amount {}. Expected any of {}".format(incremental_price_amount,valid_incremental_price_amounts)
                }),400
        if listing_type == "auction" and (incremental_price_amount is None or incremental_price_amount == '' or incremental_price_amount == 0):
            return jsonify({
                "success": False,
                "message": "Invalid incremental_price_amount {} for listing_type 'auction'.".format(incremental_price_amount)
            }),400
        end_date = None
        start_date = None
        if listing_type == "auction":
            end_date = datetime.strptime(data['end_date'],"%Y-%m-%d %H:%M:%S")
            start_date = datetime.strptime(data['start_date'],"%Y-%m-%d %H:%M:%S")
        # check that user owns the images:
        db = get_db()
        for image in images:
            img = db.query(database.Image).filter_by(url=image).first()
            if img and img.created_by != current_user['id']:
                db.close()
                return jsonify({
                    "success": False,
                    "message": "You dont own this image."
                }),400
            elif not img:
                db.close()
                return jsonify({
                    "success":False,
                    "message":"You need to upload the images to the system instead and use the urls provided by it."
                }),400
        listing = database.Listing(address=address,description=description,listing_type=listing_type,property_type=property_type,property_size=property_size,land_size=land_size,bedrooms=bedrooms,bathrooms=bathrooms,images=images,created_by=current_user['id'],price=price,incremental_price_amount=incremental_price_amount,year_built=year_built,city=city,state=state,zip_code=zip_code,start_date=start_date,end_date=end_date)
        db.add(listing)
        db.commit()
        clean_data = database.Listing.retrieve_clean_obj_data(listing)
        db.close()
        return jsonify({
                "success": True,
                "data": clean_data
            })
    except Exception as e:
        logging.error(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": "Exception "+str(e)
            }),400

@app.route("/listings/<id>",methods=["GET"])
def get_listing(id):
    db = get_db()
    listing = db.query(database.Listing).get(id)
    if not listing:
        db.close()
        return jsonify({
            "success": False,
            "message": "Listing not found"
        })
    if request.method == "GET":
        bids = db.query(database.Bid).filter_by(listing_id=id).order_by(database.Bid.amount.desc())
        clean_bids = []
        for bid in bids:
            clean_bids.append(database.Bid.retrieve_clean_obj_data(bid))
        clean_data = database.Listing.retrieve_clean_obj_data(listing)
        clean_data['bids'] = clean_bids
        db.close()
        return jsonify({
            "success": True,
            "data": clean_data
        })

@app.route("/listings",methods=["GET"])
def get_listings():
    db = get_db()
    listings = db.query(database.Listing).all()
    if not listings:
        return jsonify({
            "success": True,
            "data": []
        })
    output = []
    for listing in listings:
        clean_data = []
        clean_bids = []
        bids = db.query(database.Bid).filter_by(listing_id=listing.id).order_by(database.Bid.amount.desc())
        for bid in bids:
            clean_bids.append(database.Bid.retrieve_clean_obj_data(bid))
        clean_data = database.Listing.retrieve_clean_obj_data(listing)
        clean_data['bids'] = clean_bids
        output.append(clean_data)
    db.close()
    return jsonify({
        "success": True,
        "data": output
    })


@app.route("/bids",methods=["POST"])
@token_required
def create_bid(current_user):
    try:
        data = request.get_json()
        amount = data['amount']
        listing_id = data['listing_id']
        print(listing_id)
        db = get_db()
        buyer = db.query(database.User).get(current_user['id'])
        if not buyer.authorized:
            db.close()
            return jsonify({
                "success":False,
                "message":"You must be authorized to place bids."
            }),400

        listing = db.query(database.Listing).get(listing_id)
        if not listing:
            db.close()
            return jsonify({
                "success": False,
                "message": "That listing does not exist."
            }), 400
        if current_user['id'] == listing.created_by:
            db.close()
            return jsonify({
                "success": False,
                "message": "You cannot create a bid on your own listings."
            }),400
        if listing.listing_type != 'auction':
            db.close()
            return jsonify({
                "success": False,
                "message": "Cannot place a bid on a non-auction listing."
            }),400
        if listing.start_date > datetime.now().astimezone():
            return jsonify({
                "success": False,
                "message": "This auction has not started yet."
            }),400
        if listing.end_date < datetime.now().astimezone():
            return jsonify({
                "success": False,
                "message": "This auction has already finished."
            }),400
        last_bid_on_listing = db.query(database.Bid).order_by(database.Bid.amount.desc()).filter_by(listing_id=listing.id).first()
        current_amount = listing.price + listing.incremental_price_amount
        if last_bid_on_listing:
            current_amount = last_bid_on_listing.amount + listing.incremental_price_amount
        if current_amount > amount:
            db.close()
            return jsonify({
                "success": False,
                "message": "Amount must be higher or equal than {}".format(current_amount)
            }),400
        bid = database.Bid(created_by=current_user['id'],amount=amount,listing_id=listing.id,created=datetime.now(),last_updated=datetime.now())
        db.add(bid)
        db.commit()
        clean_data = database.Bid.retrieve_clean_obj_data(bid)
        seller = db.query(database.User).get(listing.created_by)
        
        zapier.notify_bid_made({"listing_title":listing.address,"listing_id":listing.id,"amount":amount,"seller":{"first_name":seller.first_name,"last_name":seller.last_name, "email": seller.email},"buyer":{"first_name":buyer.first_name,"last_name":buyer.last_name,"email": buyer.email}})
        db.close()
        return jsonify({
                "success": True,
                "data": clean_data
            })
    except Exception as e:
        logging.error(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": "Exception "+str(e)
            }),500

@app.route("/bids/<id>",methods=["GET"])
@token_required
def get_bids(current_user,id):
    db = get_db()
    bid = db.query(database.Bid).get(id)
    listing = db.query(database.Listing).get(bid.listing_id)
    if not bid:
        db.close()
        return jsonify({
            "success": False,
            "message": "Listing not found"
        })
    if request.method == "GET":
        if current_user['id'] != bid.created_by and current_user['id'] != listing.created_by:
            return jsonify({
                "success": False,
                "message": "You cant see this bid."
            }),401
        clean_data = database.Bid.retrieve_clean_obj_data(bid)
        db.close()
        return jsonify({
            "success": True,
            "data": clean_data
        })


@app.route("/offers",methods=["POST"])
@token_required
def create_offer(current_user):
    try:
        data = request.get_json()
        listing_id = data['listing_id']
        db = get_db()
        listing = db.query(database.Listing).get(listing_id)
        if listing.listing_type != 'standard':
            db.close()
            return jsonify({
                "success":False,
                "message": "Cannot create an offer for listing_type {}".format(listing.listing_type)
            }),400
        amount = float(data['amount'])
        if amount == 0:
            db.close()
            return jsonify({
                "success": False,
                "message": "Amount cant be 0"
            }),400
        # if amount < listing.price:
        #     return jsonify({
        #         "success": False,
        #         "message": "This listing's price is bigger than the proposed amount."
        #     })
        
        offer = database.Offer(amount=amount,listing_id=listing.id,created_by=current_user['id'])
        db.add(offer)
        db.commit()
        clean_data = database.Offer.retrieve_clean_obj_data(offer)
        seller = db.query(database.User).get(listing.created_by)
        buyer = db.query(database.User).get(current_user['id'])
        db.close()
        zapier.notify_offer_made({"listing_title":listing.address,"listing_id":listing.id,"amount":amount,"seller":{"first_name":seller.first_name,"last_name":seller.last_name, "email": seller.email},"buyer":{"first_name":buyer.first_name,"last_name":buyer.last_name,"email": buyer.email}})
        return jsonify({
                "success": True,
                "data": clean_data
            })
    except Exception as e:
        logging.error(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": "Exception "+str(e)
            }),400

@app.route("/offers/<id>",methods=["GET"])
@token_required
def get_offer(current_user,id):
    db = get_db()
    offer = db.query(database.Offer).get(id)
    if not offer:
        db.close()
        return jsonify({
            "success": False,
            "message": "Offer not found."
        }),400
    listing = db.query(database.Listing).get(offer.listing_id)
    if listing.created_by != current_user['id'] and offer.created_by != current_user['id']:
        db.close()
        return jsonify({
            "success": False,
            "message":"You cant view offers for listings that you didnt make."
        }),401
    clean_offer = database.Offer.retrieve_clean_obj_data(offer)
    db.close()
    return jsonify({
        "success": True,
        "data": clean_offer
    }),200


def get_file_extension(filename):
    if filename.find(".")!=-1:
        return filename.rsplit(".",1)[1]
    else:
        return False

@app.route("/images",methods=["POST"])
@token_required
def upload_image(current_user):
    bucket_folder = "dev/"+str(current_user['id'])+"/"  # should be = str(current_user['id'])+"/" in production
    try:
        f = request.files['file']
        if get_file_extension(f.filename) not in ['jpg','jpeg','png']:
            return jsonify({
                "success": False,
                "message": "Invalid file format. Accepting only jpeg, jpg or png."
            }),400
        db = get_db()
        found = True
        while found:
            _uuid = uuid4()
            custom_filename = str(_uuid)+"."+get_file_extension(f.filename)
            found = db.query(database.Image).filter_by(url=AWS_Hook.construct_url(bucket_folder+custom_filename)).first()
        # Save file locally in order to upload to S3
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))
        try:
            AWS_Hook.upload_file(app.config['UPLOAD_FOLDER'],bucket_folder,custom_filename)
        except Exception as e:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))    
            logging.error(traceback.print_exc())
            db.close()
            return jsonify({
                "success": False,
                "message": str(e)
            }),500
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))
        image = database.Image(uuid=str(_uuid),created=datetime.now(),last_updated=datetime.now(),created_by=current_user['id'],url=AWS_Hook.construct_url(bucket_folder+custom_filename))
        db.add(image)
        db.commit()
        clean_data = database.Image.retrieve_clean_obj_data(image)
        db.close()
        return jsonify({
            "success": True,
            "data": clean_data
        })
    except Exception as e:
        logging.error(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": str(e)
            }),500


@app.route("/authorization_file",methods=["POST"])
@token_required
def upload_authorization_file(current_user):
    bucket_folder = "dev/"+str(current_user['id'])+"/authorization_files/"  # should be = str(current_user['id'])+"/" in production
    try:
        db = get_db()
        user = db.query(database.User).get(current_user['id'])
        if user.authorized:
            db.close()
            return jsonify({
                "success":False,
                "message":"User is already approved."
            }),400
        
        f = request.files['file']
        if get_file_extension(f.filename) not in ['jpg','jpeg','png','pdf']:
            db.close()
            return jsonify({
                "success": False,
                "message": "Invalid file format. Accepting only jpeg, jpg, png or pdf."
            }),400
        
        found = True
        while found:
            _uuid = uuid4()
            custom_filename = "auth-"+str(_uuid)+"."+get_file_extension(f.filename)
            found = db.query(database.AuthorizationFile).filter_by(authorization_file_url=AWS_Hook.construct_url(bucket_folder+custom_filename)).first()
        # Save file locally in order to upload to S3
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))
        try:
            AWS_Hook.upload_file(app.config['UPLOAD_FOLDER'],bucket_folder,custom_filename)
        except Exception as e:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))    
            logging.error(traceback.print_exc())
            db.close()
            return jsonify({
                "success": False,
                "message": str(e)
            }),500
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))
        
        # Delete old file if any
        db.query(database.AuthorizationFile).filter_by(created_by=current_user['id']).delete()
        user.authorized=False
        user.authorized_time=None
        auth_file = database.AuthorizationFile(created=datetime.now(),last_updated=datetime.now(),created_by=current_user['id'],authorization_file_url=AWS_Hook.construct_url(bucket_folder+custom_filename))
        db.add(auth_file)
        db.commit()
        clean_data = database.AuthorizationFile.retrieve_clean_obj_data(auth_file)
        db.close()
        return jsonify({
            "success": True,
            "data": clean_data
        })
    except Exception as e:
        logging.error(traceback.print_exc())
        try:
            db.close()
        finally:
            return jsonify({
                "success": False,
                "message": str(e)
            }),500

@app.route("/authorization_file/<user_id>",methods=["GET"])
@token_required
def get_authorization_file(current_user,user_id):
    db = get_db()
    user = db.query(database.User).get(user_id)
    if not user:
        db.close()
        return jsonify({
            "success": False,
            "message": "User not found id: {}".format(user_id)
        }),400
    if user.id != current_user['id'] and current_user['type'] != 99:
        db.close()
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }),401
    auth_file = db.query(database.AuthorizationFile).filter_by(created_by=user_id).order_by(database.AuthorizationFile.created.desc()).first()
    if not auth_file:
        db.close()
        return jsonify({
            "success":False,
            "message": "No authorization file found for this user."
        }),400
    clean_data = database.AuthorizationFile.retrieve_clean_obj_data(auth_file)
    db.close()
    return jsonify({
        "success":True,
        "data":clean_data
    }),200



############ ------------ ADMIN ----------------- #################

@app.route("/admin/userlist",methods=["GET"])
@token_required
def userlist(current_user):
    if current_user['type'] != 99:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }),401
    db = get_db()
    users = db.query(database.User).order_by(database.User.id.desc())
    output = []
    for user in users:
        listings = db.query(database.Listing).filter_by(created_by=user.id)
        listings_out = []
        for listing in listings:
            listings_out.append(database.Listing.retrieve_clean_obj_data(listing))
        
        bids = db.query(database.Bid).filter_by(created_by=user.id)
        bids_out = []
        for bid in bids:
            bids_out.append(database.Bid.retrieve_clean_obj_data(bid))

        offers = db.query(database.Offer).filter_by(created_by=user.id)
        offers_out = []
        for offer in offers:
            offers_out.append(database.Offer.retrieve_clean_obj_data(offer))

        auth_file = db.query(database.AuthorizationFile).filter_by(created_by=user.id).first()
        auth_out = {}
        if auth_file:
            auth_out = database.AuthorizationFile.retrieve_clean_obj_data(auth_file,show_updated_by=True)

        output.append({
            "id":user.id,
            "first_name":user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "type": user.type,
            "authorized": user.authorized,
            "authorized_time": user.authorized_time,
            "email_validated": user.email_validated,
            "last_seen": user.last_seen,
            "listings": listings_out,
            "bids": bids_out,
            "offers":offers_out,
            "authorization_file":auth_out
        })

    db.close()

    return jsonify({
        "success":True,
        "data": output
    })

@app.route("/admin/approve/<file_id>",methods=["POST"])
@token_required
def approve_user(current_user,file_id):
    if current_user['type'] != 99:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }),401
    decline = False
    data = request.get_json()
    if 'decline' in data and (data['decline']!="0" or data['decline']!=0):
        decline = True

    db = get_db()
    auth_file = db.query(database.AuthorizationFile).get(file_id)
    if not auth_file and not decline:
        db.close()
        return jsonify({
            "success":False,
            "message":"File not found"
        }),400
    if auth_file.approved and not decline:
        db.close()
        return jsonify({
            "success":False,
            "message":"This file was already approved."
        })
    user = db.query(database.User).get(auth_file.created_by)
    if not decline:
        auth_file.approved = True
        auth_file.updated_by = current_user['id']
        auth_file.updated_time = datetime.now()
        auth_file.declined = False
        user.authorized = True
        user.authorized_time = datetime.now()
    else:
        auth_file.approved = False
        auth_file.updated_by = current_user['id']
        auth_file.updated_time = datetime.now()
        auth_file.declined = True
        user.authorized = False
        user.authorized_time = None
    db.commit()
    db.close()
    if not decline:
        return jsonify({
            "success":True,
            "message": "File and user approved"
        })
    else:
        return jsonify({
            "success":True,
            "message": "File and user was declined"
        })
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=5050)