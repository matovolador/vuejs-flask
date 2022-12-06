from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql import func
from datetime import datetime
import string,random
import logging
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


AUTHORIZATION_VALID_TIME = 10 # days
VALIDATION_TOKEN_LIFE = 3 # days
PASSWORD_RESET_TOKEN_LIFE = 2 # days

class BaseMixin(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(BaseMixin,Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False,unique=True)
    first_name = Column(String,nullable=True,default=None)
    last_name = Column(String,nullable=True,default=None)
    created = Column(DateTime(timezone=True),nullable=False, default=func.now())
    last_seen = Column(DateTime(timezone=True),default=func.now())
    password = Column(String,nullable=False)
    password_created = Column(DateTime(timezone=True),nullable=False,default=func.now())
    email_validated = Column(Boolean,nullable=False,default=False)
    email_validation_token = Column(String,nullable=True,default=None)
    email_validation_token_created = Column(DateTime(timezone=True),nullable=True, default=None)
    authorized = Column(Boolean,nullable=False,default=False)
    authorized_time = Column(DateTime(timezone=True),nullable=False, default=func.now())
    type = Column(Integer,nullable=False,default=0)
    token = Column(String,nullable=True,default=None)
    password_reset_token = Column(String,nullable=True,default=None)
    password_reset_token_created = Column(DateTime(timezone=True),nullable=True, default=None)

    @staticmethod
    def retrieve_clean_obj_data(obj,include_token = False,public=False):
        obj = obj.as_dict()
        if include_token:
            return {
                "id": obj['id'],
                "email": obj['email'],
                "token": obj['token'],
                "first_name": obj['first_name'],
                "last_name": obj['last_name'],
                "type": obj['type']
            }
        elif public:
            return {
                "id": obj['id'],
                "first_name": obj['first_name'],
                "last_name": obj['last_name'][:1]
            }
        else:
            return {
                "id": obj['id'],
                "email": obj['email'],
                "first_name": obj['first_name'],
                "last_name": obj['last_name'],
                "type": obj['type']
            }


    @staticmethod
    def login_user(email_or_username,password):
        db = next(get_db())
        user = False
        user = db.query(User).filter_by(email=email_or_username).first()
        if not user:
            db.close()
            return False, "User not found."

        if user.password != password:
            db.close()
            return False, "Invalid password."

        if user.email_validated == False:
            db.close()
            return False, "You must first verify your email."
        
        user.last_seen = datetime.now()
        db.commit()
        user_as_dict = user.as_dict()
        db.close()
        return True, user_as_dict

    @staticmethod
    def user_types():
        return {
            0:"User",
            1:"Agent",
            99:"Admin"
        }

    @staticmethod
    def is_authorized(id):
        db = next(get_db())
        user = db.query(User).get(id)
        db.close()
        return user.authorized and (datetime.today()-user.authorized_time).total_seconds()/60/60/24 < AUTHORIZATION_VALID_TIME

    @classmethod
    def authorize(id):
        db = next(get_db())
        user = db.query(User).get(id)
        user.authorized=True
        user.authorized_time = datetime.now()
        db.commit()
        db.close()
        return True

    @staticmethod
    def validate_email(id,validation_token):
        db = next(get_db())
        user = db.query(User).get(id)
        print(user.email_validation_token_created)
        print(datetime.now())
        if user.email_validation_token == validation_token and (datetime.now() - user.email_validation_token_created).total_seconds()/60/60/24 < VALIDATION_TOKEN_LIFE:
            user.email_validated = True
            user.email_validation_token = None
            db.commit()
            db.close()
            return True, "", -1
        elif user.email_validation_token != validation_token:
            db.close()
            return False, "Email validation token is not correct.", 1
        else:
            # time expired
            db.close()
            return False, "Email validation token expired. Please request another.", 2

    @staticmethod
    def generate_password_reset_token(id):
        db = next(get_db())
        user = db.query(User).get(id)
        size = 25
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = size))
        user.password_reset_token = token
        user.password_reset_token_created = datetime.now()
        db.commit()
        db.close()
        return token

    @staticmethod
    def update_user_password(id,password,password_reset_token=False):
        db = next(get_db())
        user = db.query(User).get(id)
        if password_reset_token:
            if not user.password_reset_token:
                return False,"There isn't a password reset request for this user."
            if (datetime.now().astimezone() - user.password_reset_token_created).total_seconds()/60/60/24 > PASSWORD_RESET_TOKEN_LIFE:
                return False, "Your password reset token has expired."
            if user.password_reset_token != password_reset_token:
                return False, "Reset token invalid."
        success, msg = User.validate_password_field(password)
        if not success:
            db.close()
            return success, msg
        user.password=password
        user.password_created = datetime.now()
        user.password_reset_token = None
        user.password_reset_token_created = None
        db.commit()
        db.close()
        return True, "Your password has been changed."
            
    @staticmethod
    def validate_password_field(password):
        password = str(password)
        if len(password)<8:
            return False, "Password must be at least 8 characters long"
        return True, ""

    @staticmethod
    def generate_email_validation_token(id):
        db = next(get_db())
        user = db.query(User).get(id)
        if user.email_validated:
            db.close()
            return False, "Email already validated"
        size = 25
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = size))
        user.email_validation_token = token
        user.email_validation_token_created = datetime.now()
        db.commit()
        db.close()
        return token, ""




class Listing(BaseMixin,Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    address = Column(String,nullable=False,default="N/A")
    city = Column(String,nullable=False,default="N/A")
    state = Column(String,nullable=False,default="N/A")
    zip_code = Column(String,nullable=False,default="N/A")
    description = Column(String,nullable=True)
    listing_type = Column(String,nullable=False)
    property_type = Column(String,nullable=False)
    property_size = Column(Numeric,nullable=False)
    land_size = Column(Numeric,nullable=False)
    bedrooms = Column(Integer,nullable=False)
    bathrooms = Column(Integer,nullable=False)
    images = Column(JSON,nullable=False)
    price = Column(Numeric,nullable=False)
    incremental_price_amount = Column(Numeric,nullable=True)
    year_built = Column(String,nullable=True)
    start_date = Column(DateTime(timezone=True),nullable=True)
    end_date = Column(DateTime(timezone=True),nullable=True)
    created = Column(DateTime(timezone=True),nullable=False, default=func.now())
    last_updated = Column(DateTime(timezone=True),default=func.now())
    created_by = Column(Integer,ForeignKey(User.id))
    auction_closed = Column(Boolean,nullable=False,default=False)


    @staticmethod
    def retrieve_clean_obj_data(obj):
        obj = obj.as_dict()
        return {
            "id": obj['id'],
            "address": obj['address'],
            "city": obj['city'],
            "state":obj['state'],
            "zip_code": obj['zip_code'],
            "description": obj['description'],
            "listing_type": obj['listing_type'],
            "property_type": obj['property_type'],
            "property_size": obj['property_size'],
            "land_size": obj['land_size'],
            "bedrooms": obj['bedrooms'],
            "bathrooms": obj['bathrooms'],
            "images": obj['images'],
            "price": obj['price'],
            "incremental_price_amount": obj['incremental_price_amount'],
            "year_built": obj['year_built'],
            "start_date": obj['start_date'],
            "end_date": obj['end_date'],
            "created_by": obj['created_by'],
            "created": obj['created']
        }

    
class Bid(BaseMixin,Base):
    __tablename__ = 'bids'

    id = Column(Integer, primary_key=True)
    created_by = Column(Integer,ForeignKey(User.id),nullable=False)
    amount = Column(Numeric,nullable=False)
    listing_id = Column(Integer,ForeignKey(Listing.id),nullable=False)
    created = Column(DateTime(timezone=True),nullable=False, default=func.now())
    last_updated = Column(DateTime(timezone=True),default=func.now())

    @staticmethod
    def retrieve_clean_obj_data(obj):
        obj = obj.as_dict()
        return {
            "id": obj['id'],
            "created_by": obj['created_by'],
            "amount": obj['amount'],
            "listing_id": obj['listing_id'],
            "created": obj['created']
        }


class Image(BaseMixin,Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False,unique=True)
    url = Column(String,nullable=False)
    created = Column(DateTime(timezone=True),nullable=False, default=func.now())
    last_updated = Column(DateTime(timezone=True),default=func.now())
    created_by = Column(Integer,ForeignKey(User.id),nullable=False)

    @staticmethod
    def retrieve_clean_obj_data(obj):
        obj = obj.as_dict()
        return {
            "id": obj['id'],
            "uuid": obj['uuid'],
            "url": obj['url']
        }
        



class Offer(BaseMixin,Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric,nullable=False)
    accepted = Column(Boolean,nullable=False,default=False)
    listing_id = Column(Integer,ForeignKey(Listing.id))
    created = Column(DateTime(timezone=True),nullable=False, default=func.now())
    last_updated = Column(DateTime(timezone=True),default=func.now())
    created_by = Column(Integer,ForeignKey(User.id))


    @staticmethod
    def retrieve_clean_obj_data(obj):
        obj = obj.as_dict()
        return {
            "id": obj['id'],
            "amount": obj['amount'],
            "listing_id": obj['listing_id'],
            "accepted": obj['accepted'],
            "created_by": obj['created_by']
        }

class AuthorizationFile(BaseMixin,Base):
    __tablename__ = 'authorization_files'

    id = Column(Integer, primary_key=True)
    authorization_file_url = Column(String,nullable=True)
    created_by = Column(Integer,ForeignKey(User.id),nullable=False)
    created = Column(DateTime(timezone=True),nullable=False, default=func.now())
    last_updated = Column(DateTime(timezone=True),default=func.now())
    approved = Column(Boolean,default=False)
    updated_time = Column(DateTime(timezone=True),nullable=True)
    updated_by = Column(Integer,ForeignKey(User.id),nullable=True)
    declined = Column(Boolean,default=False,nullable=False)


    @staticmethod
    def retrieve_clean_obj_data(obj,show_updated_by=False):
        obj = obj.as_dict()
        if not show_updated_by:
            return {
                "id": obj['id'],
                "created_by": obj['created_by'],
                "authorization_file_url": obj['authorization_file_url'],
                "last_updated": obj['last_updated'],
                "created": obj['created'],
                "approved":obj['approved'],
                "updated_time":obj['updated_time'],
                "declined": obj['declined']
            }
        else:
            return {
                "id": obj['id'],
                "created_by": obj['created_by'],
                "authorization_file_url": obj['authorization_file_url'],
                "last_updated": obj['last_updated'],
                "created": obj['created'],
                "approved":obj['approved'],
                "updated_time":obj['updated_time'],
                "updated_by": obj['updated_by'],
                "declined": obj['declined']
            }
