import traceback
import unittest, os, json, io
from app import app as client_app
from base64 import b64encode
from datetime import datetime, timedelta
import random
import string
import modules.database as database


class Tests(unittest.TestCase):
    def __init__(self):
        super().__init__()
        client_app.debug = True
        self.client = client_app.test_client()
        self.token = ""
        self.user_id = -1

    def test_1_get_health(self):
        r = self.client.get("/health")
        print(r.data)
        print(r.status_code)
        r_json = json.loads(r.data)
        self.assertEqual(r.status_code,200)
        self.assertEqual(r_json['success'],True)
        print("Test 1 Completed.")


    def test_2_login(self,email,password,should_fail=False):
        credentials = b64encode((email+":"+str(password)).encode("utf-8")).decode('utf-8')
        r = self.client.post("/login",headers={"Authorization": f"Basic {credentials}"})
        print(r)
        r_json = json.loads(r.data)
        print(r_json)
        if should_fail:
            self.assertEqual(r_json['success'],False)
        else:
            self.token = r_json['token']
            self.user_id = r_json['user_id']
            print(self.token)
            self.assertEqual(r_json['success'],True)

        print("Test 2 Completed.")

    def test_3_can_access(self,should_fail=False):
        r = self.client.get("/must_be_logged_in", headers={"x-access-token":str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],not should_fail)
        print("Test 3 completed.")

    def test_4_logout(self):
        r = self.client.get("/logout",headers={"x-access-token":str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 4 completed")
        return

    def test_5_renew_token(self):
        r = self.client.get("/renew-token", headers={"x-access-token":str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        self.token = r_json['token']
        print("Test 5 completed.")

    def test_6_register_user(self,data):
        r = self.client.post("/registration",data=json.dumps(data),headers={"content-type":"application/json"})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 6 completed.")

    def test_7_validate_email(self,email,token):
        print(email)
        # email = email.replace("@","%40")
        print(token)
        r = self.client.get("/validate_email?email="+str(email)+"&token="+str(token))
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 7 completed.")

    def test_8_upload_image(self,data,should_fail=False):
        r = self.client.post("/images",data=data,headers={
            "x-access-token": str(self.token)
        },content_type="multipart/form-data",follow_redirects=True)
        r_json = json.loads(r.data)
        print(r_json)
        result = False
        if not should_fail:
            self.assertEqual(r_json['success'],True)
            result =  r_json['data']
        else:
            self.assertEqual(r_json['success'],False)
            result = False
        print("Test 8 Completed.")
        return result

    def test_9_get_self(self):
        r = self.client.get("/users/self",headers={"x-access-token":str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 9 completed.")

    def test_10_create_listing(self,data,should_fail=False):
        r = self.client.post("/listings",data=json.dumps(data),headers={"x-access-token":str(self.token),"content-type":"application/json"})
        r_json = json.loads(r.data)
        print(r_json)
        result = False
        if not should_fail:
            self.assertEqual(r_json['success'],True)
            result = r_json['data']
        else:
            self.assertEqual(r_json['success'],False)
        print("Test 10 completed.")
        return result

    def test_11_create_offer(self,data):
        r = self.client.post("/offers",data=json.dumps(data),headers={"x-access-token":str(self.token),"content-type":"application/json"})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 11 completed.")
        return r_json['data']

    def test_12_create_bid(self,data,should_fail=False):
        r = self.client.post("/bids",data=json.dumps(data),headers={"x-access-token":str(self.token),"content-type":"application/json"})
        r_json = json.loads(r.data)
        print(r_json)
        if not should_fail:
            self.assertEqual(r_json['success'],True)
            result =  r_json['data']
        else:
            self.assertEqual(r_json['success'],False)
            result = False
        print("Test 12 completed.")
        return result

    def test_13_get_listing(self,id):
        r = self.client.get("/listings/"+str(id),headers={'x-access-token':str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 13 completed")
        return r_json['data']

    def test_14_get_bid(self,id):
        r = self.client.get("/bids/"+str(id),headers={'x-access-token':str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 14 completed")
        return r_json['data']

    def test_15_get_offer(self,id):
        r = self.client.get("/offers/"+str(id),headers={'x-access-token':str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 15 completed")
        return r_json['data']

    def test_16_get_user_by_id(self,id):
        r = self.client.get("/users/"+str(id),headers={'x-access-token':str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 16 completed")
        return r_json['data']

    def test_17_change_password(self,data):
        r = self.client.post("/change_password",data=json.dumps(data),headers={"x-access-token":str(self.token),"content-type":"application/json"})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 17 completed.")

    def test_18_trigger_password_reset(self,email):
        r = self.client.get("/reset_password?email="+str(email),headers={'x-access-token':str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 18 completed")

    def test_19_submit_password_reset(self,data):
        r = self.client.post("/reset_password",data=json.dumps(data),headers={"x-access-token":str(self.token),"content-type":"application/json"})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 19 completed.")

    def test_20_get_all_listings(self):
        r = self.client.get("/listings",headers={'x-access-token':str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 20 completed")
        return r_json['data']
    
    def test_21_get_public_user(self,id):
        r = self.client.get("/users/"+str(id)+"/public")
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 21 completed")
        return r_json['data']

    def test_22_upload_auth_file(self,data,should_fail=False):
        r = self.client.post("/authorization_file",data=data,headers={
            "x-access-token": str(self.token)
        },content_type="multipart/form-data",follow_redirects=True)
        r_json = json.loads(r.data)
        print(r_json)
        result = False
        if not should_fail:
            self.assertEqual(r_json['success'],True)
            result =  r_json['data']
        else:
            self.assertEqual(r_json['success'],False)
            result = False
        print("Test 22 Completed.")
        return result

    def test_23_get_auth_file(self,user_id):
        r = self.client.get("/authorization_file/"+str(user_id),headers={"x-access-token":str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        self.assertEqual(r_json['success'],True)
        print("Test 23 completed")
        return r_json['data']

    def test_24_approve_auth_file(self,file_id,decline=False,should_fail=False):
        data = {}
        if decline:
            data['decline'] = 1
        r = self.client.post("/admin/approve/"+str(file_id),data=json.dumps(data),headers={"x-access-token":str(self.token),"content-type":"application/json"})
        r_json = json.loads(r.data)
        print(r_json)
        if not should_fail:
            self.assertEqual(r_json['success'],True)
        else:
            self.assertEqual(r_json['success'],False)
        print("Test 24 completed.")

    def test_25_get_userlist(self,should_fail=False):
        r = self.client.get("/admin/userlist",headers={"x-access-token":str(self.token)})
        r_json = json.loads(r.data)
        print(r_json)
        result = False
        if not should_fail:
            self.assertEqual(r_json['success'],True)
            result =  r_json['data']
        else:
            self.assertEqual(r_json['success'],False)
            result = False
        print("Test 25 completed")
        return result


if __name__ == "__main__":
    tester = Tests()
    tester.test_1_get_health()

    db = next(database.get_db())
    # clean db
    db.query(database.AuthorizationFile).delete()
    db.query(database.Offer).delete()
    db.query(database.Bid).delete()
    db.query(database.Image).delete()
    db.query(database.Listing).delete()
    db.query(database.User).delete()
    db.commit()
    # exit()

    admin = database.User(email='someadmin.garafoni@someemail.com',password='312545688',first_name='Matias',last_name='Admin',email_validated=True,type=99,authorized=True)
    db.add(admin)
    user = database.User(email="matias.garafoni@gmail.com",password='12345678',first_name='Matias',last_name='Garafoni',email_validated=True)
    db.add(user)
    db.commit()
    tester.test_2_login(email="matias.garafoni@gmail.com",password='12345678')
    
    tester.test_3_can_access()
    tester.test_5_renew_token()
    tester.test_3_can_access()
    tester.test_4_logout()
    tester.test_3_can_access(should_fail=True)
    db.query(database.User).filter_by(email='matias.garafoni@gmail.com').delete()
    db.commit()
    tester.test_6_register_user(data={
        "email":"matias.garafoni@gmail.com",
        "password":"12345678",
        "first_name":"Matias",
        "last_name":"Garafoni",
        "type":0
    })
    tester.test_2_login(email="matias.garafoni@gmail.com",password='12345678',should_fail=True)
    tester.test_3_can_access(should_fail=True)
    user = db.query(database.User).filter_by(email='matias.garafoni@gmail.com').first()
    tester.test_7_validate_email(email="matias.garafoni@gmail.com",token=user.email_validation_token)
    tester.test_2_login(email="matias.garafoni@gmail.com",password='12345678')
    tester.test_3_can_access()
    tester.test_9_get_self()
    tester.test_25_get_userlist(should_fail=True) # this is an admin route. should not have access to this
    image_data = {"file": (open("test-image-1.jpg","rb"),"test-image-1.jpg")}
    img = tester.test_8_upload_image(image_data,should_fail=False)

    listing_data = {
        "address" : "21 street ab corner, CA",
        "city": "corner",
        "state": "CA",
        "zip_code": "123",
        "description": "Beautiful place.",
        "listing_type": "standard",
        "property_type": "house",
        "property_size": 234.0,
        "land_size": 360.6,
        "bedrooms": 2,
        "bathrooms" : 1,
        "images":[img['url']],
        "price": 150000,
        "year_built": 2010
    }

    listing = tester.test_10_create_listing(listing_data)

    tester.test_13_get_listing(listing['id'])
    tester.test_4_logout()
    tester.test_21_get_public_user(user.id)
    # buyer
    tester.test_6_register_user(data={
        "email":"matovolador@gmail.com",
        "password":"12345678",
        "first_name":"george",
        "last_name":"alias",
        "type":0
    })
    buyer_user = db.query(database.User).filter_by(email='matovolador@gmail.com').first()
    tester.test_7_validate_email(email="matovolador@gmail.com",token=buyer_user.email_validation_token)
    tester.test_2_login(buyer_user.email,buyer_user.password,should_fail=False)
    offer_data = {
        "listing_id": listing['id'],
        "amount": 125500
    }
    offer = tester.test_11_create_offer(offer_data)
    tester.test_15_get_offer(offer['id'])
    tester.test_4_logout()
    tester.test_2_login(user.email,user.password)
    listing_data = {
        "address" : "21 street ab corner, CA",
        "city": "corner",
        "state": "CA",
        "zip_code": "123",
        "description": "Beautiful place.",
        "listing_type": "auction",
        "property_type": "house",
        "property_size": 234.0,
        "land_size": 360.6,
        "bedrooms": 2,
        "bathrooms" : 1,
        "images":[img['url']],
        "price": 150000,
        "incremental_price_amount": 500,
        "year_built": 2012,
        "start_date": datetime.strftime(datetime.utcnow(),"%Y-%m-%d %H:%M:%S"),
        "end_date": datetime.strftime(datetime.utcnow()+timedelta(days=14),"%Y-%m-%d %H:%M:%S")
    }

    listing = tester.test_10_create_listing(listing_data)

    listing_data = {
        "address" : "21 street ab corner, CA",
        "city": "corner",
        "state": "CA",
        "zip_code": "123",
        "description": "Beautiful place.",
        "listing_type": "auction",
        "property_type": "house",
        "property_size": 234.0,
        "land_size": 360.6,
        "bedrooms": 2,
        "bathrooms" : 1,
        "images":["something.com"],
        "price": 150000,
        "incremental_price_amount": 500,
        "year_built": 2010,
        "start_date": datetime.strftime(datetime.utcnow(),"%Y-%m-%d %H:%M:%S %Z"),
        "end_date": datetime.strftime(datetime.utcnow()+timedelta(days=14),"%Y-%m-%d %H:%M:%S %Z")
    }

    tester.test_10_create_listing(listing_data,should_fail=True)

    tester.test_4_logout()

    tester.test_2_login(buyer_user.email,buyer_user.password)
    
    bid_data = {
        "listing_id": listing['id'],
        "amount": 150500
    }
    tester.test_12_create_bid(bid_data,should_fail=True) # user is not authorized

    auth_file_data = {"file": (open("test_auth_file.pdf","rb"),"test_auth_file.pdf")}
    
    tester.test_22_upload_auth_file(auth_file_data,should_fail=False)
    
    auth_file_out = tester.test_23_get_auth_file(buyer_user.id)
    
    tester.test_24_approve_auth_file(auth_file_out['id'],should_fail=True) # should fail cause this is not an admin

    bid_data = {
        "listing_id": listing['id'],
        "amount": 150500
    }
    tester.test_12_create_bid(bid_data,should_fail=True) # user is not authorized although he/she uploaded the auth file


    tester.test_4_logout()

    tester.test_2_login(email='someadmin.garafoni@someemail.com',password='312545688')

    auth_file_out = tester.test_23_get_auth_file(buyer_user.id)  # get file again but logged in as admin and getting the file from another user

    tester.test_24_approve_auth_file(auth_file_out['id'],decline=True) # decline auth
    tester.test_4_logout()

    tester.test_2_login(buyer_user.email,buyer_user.password)
    auth_file_data = {"file": (open("test_auth_file.pdf","rb"),"test_auth_file.pdf")}
    
    tester.test_22_upload_auth_file(auth_file_data,should_fail=False)
    
    auth_file_out = tester.test_23_get_auth_file(buyer_user.id)
    
    tester.test_24_approve_auth_file(auth_file_out['id'],should_fail=True) # should fail cause this is not an admin

    bid_data = {
        "listing_id": listing['id'],
        "amount": 150500
    }
    tester.test_12_create_bid(bid_data,should_fail=True) # user is not authorized although he/she uploaded the auth file


    tester.test_4_logout()

    tester.test_2_login(email='someadmin.garafoni@someemail.com',password='312545688')

    auth_file_out = tester.test_23_get_auth_file(buyer_user.id)  # get file again but logged in as admin and getting the file from another user

    tester.test_24_approve_auth_file(auth_file_out['id'],decline=False)

    tester.test_4_logout()

    tester.test_2_login(buyer_user.email,buyer_user.password)

    bid_data = {
        "listing_id": listing['id'],
        "amount": 150200   # price is under incremental_price_amount, thus it should fail
    }
    tester.test_12_create_bid(bid_data,should_fail=True)
    
    bid_data = {
        "listing_id": listing['id'],
        "amount": 150500
    }
    bid = tester.test_12_create_bid(bid_data)

    bid_data = {
        "listing_id": listing['id'],
        "amount": 150700   # price is under incremental_price_amount, thus it should fail
    }
    tester.test_12_create_bid(bid_data,should_fail=True)

    bid_data = {
        "listing_id": listing['id'],
        "amount": 151000
    }


    tester.test_14_get_bid(bid['id'])
    tester.test_16_get_user_by_id(user.id)
    tester.test_17_change_password({'old_password':buyer_user.password,'new_password':'621344667'})
    tester.test_3_can_access(should_fail=False)
    tester.test_4_logout()
    tester.test_18_trigger_password_reset(buyer_user.email)
    buyer_user = db.query(database.User).get(buyer_user.id)
    tester.test_19_submit_password_reset({'email':buyer_user.email,'reset_token':buyer_user.password_reset_token,'password':"21456924568"})
    tester.test_2_login(buyer_user.email,"21456924568")
    tester.test_4_logout()
    tester.test_20_get_all_listings()

    # request all users data from admin route
    tester.test_2_login(email='someadmin.garafoni@someemail.com',password='312545688')  # admin
    user_list = tester.test_25_get_userlist()
    db.close()