<template>
    <main>
      <!-- <img class="logo" src="https://unsplash.it/80/80/?house" alt="Logo" loading="lazy"> -->
        <h2 class="h2">{{this.title}}</h2>
        <div v-if="this.message" :class="{'error':this.error}">{{message}}</div>      
        <div v-if="this.state=='usersList' && this.obj.users">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">ID</th>
                        <th scope="col">First Name</th>
                        <th scope="col">Last Name</th>
                        <th scope="col">Email</th>
                        <th scope="col">Email Validated</th>
                        <th scope="col">Authorized</th>
                        <th scope="col">User Type</th>
                        <th scope="col">Last Seen</th>
                        <th scope="col">Listings</th>
                        <th scope="col">Offers</th>
                        <th scope="col">Bids</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(usr,i) in this.obj.users" :key="i">
                        <th scope="row">{{i+1}}</th>
                        <td>{{usr.id}}</td>
                        <td>{{usr.first_name}}</td>
                        <td>{{usr.last_name}}</td>
                        <td>{{usr.email}}</td>
                        <td>{{usr.email_validated}}</td>
                        <td>{{usr.authorized}}</td>
                        <td>
                            <span v-if="usr.type==0">Standard</span>
                            <span v-else-if="usr.type==1">Agent</span>
                            <span v-else-if="usr.type==99">Admin</span>
                        </td>
                        <td>{{usr.last_seen}}</td>
                        <td><a href="#" @click.prevent="this.getUserListings(i)">Listings</a></td>
                        <!-- <td><a href="#" @click.prevent="">Offers</a></td>
                        <td><a href="#" @click.prevent="">Bids</a></td> -->
                        <td><a href="#" @click.prevent="this.getAuthFile(i)">Authorization Data</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="this.state=='userListings'">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">ID</th>
                        <th scope="col">Address</th>
                        <th scope="col">City</th>
                        <th scope="col">State</th>
                        <th scope="col">Zip code</th>
                        <th scope="col">Description</th>
                        <th scope="col">Listing Type</th>
                        <th scope="col">Property Type</th>
                        <th scope="col">Property Size</th>
                        <th scope="col">Land Size</th>
                        <th scope="col">Bedrooms</th>
                        <th scope="col">Bathrooms</th>
                        <th scope="col">Images</th>
                        <th scope="col">Price</th>
                        <th scope="col">Incremental Price Amount</th>
                        <th scope="col">Year Built</th>
                        <th scope="col">Start Date</th>
                        <th scope="col">End Date</th>
                        <th scope="col">Created By</th>
                        <th scope="col">Created</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- "address": obj.address,
                    "city": obj.city,
                    "state":obj.state,
                    "zip_code": obj.zip_code,
                    "description": obj.description,
                    "listing_type": obj.listing_type,
                    "property_type": obj.property_type,
                    "property_size": obj.property_size,
                    "land_size": obj.land_size,
                    "bedrooms": obj.bedrooms,
                    "bathrooms": obj.bathrooms,
                    "images": obj.images,
                    "price": obj.price,
                    "incremental_price_amount": obj.incremental_price_amount,
                    "year_built": obj.year_built,
                    "start_date": obj.start_date,
                    "end_date": obj.end_date,
                    "created_by": obj.created_by,
                    "created": obj.created -->
                    <tr v-for="(listing,h) in this.obj.listings" :key="h">
                        <th scope="row">{{i+1}}</th>
                        <td>{{listing.id}}</td>
                        <td>{{listing.address}}</td>
                        <td>{{listing.city}}</td>
                        <td>{{listing.state}}</td>
                        <td>{{listing.zip_code}}</td>
                        <td>{{listing.description}}</td>
                        <td>{{listing.listing_type}}</td>
                        <td>{{listing.property_type}}</td>
                        <td>{{listing.property_size}}</td>
                        <td>{{listing.land_size}}</td>
                        <td>{{listing.bedrooms}}</td>
                        <td>{{listing.bathrooms}}</td>
                        <td>{{listing.images}}</td>
                        <td>{{listing.price}}</td>
                        <td>{{listing.incremental_price_amount}}</td>
                        <td>{{listing.year_built}}</td>
                        <td>{{listing.start_date}}</td>
                        <td>{{listing.end_date}}</td>
                        <td>{{listing.created_by}}</td>
                        <td>{{listing.created}}</td>
                    </tr>
                </tbody>
            </table>
            <a href="#" @click.prevent="this.getUserList()">Back</a>
        </div>
        <div v-if="this.state=='userAuthFile'">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">File URL</th>
                        <th scope="col">Created By</th>
                        <th scope="col">Approved</th>
                        <th scope="col">Updated Time</th>
                        <th scope="col">Updated By</th>
                        <th scope="col">Declined</th>
                        <th scope="col">Last Updated</th>
                        <th scope="col">Approve</th>
                        <th scope="col">Decline</th>
                    </tr>
                </thead>
                <tbody v-if="this.obj.auth_file!={}">
                    <tr>
                        <td>{{this.obj.auth_file.id}}</td>
                        <td><a :href="this.obj.auth_file.authorization_file_url">{{this.obj.auth_file.authorization_file_url}}</a></td>
                        <td>{{this.obj.auth_file.created_by}}</td>
                        <td>{{this.obj.auth_file.approved}}</td>
                        <td>{{this.obj.auth_file.updated_time}}</td>
                        <td>{{this.obj.auth_file.updated_by}}</td>
                        <td>{{this.obj.auth_file.declined}}</td>
                        <td>{{this.obj.auth_file.last_updated}}</td>
                        <td><a href="#" @click.prevent="this.approveAuthFile(this.obj.auth_file.id)">Approve</a></td>
                        <td><a href="#" @click.prevent="this.declineAuthFile(this.obj.auth_file.id)">Decline</a></td>
                    </tr>
                </tbody>
            </table>
            <a href="#" @click.prevent="this.getUserList()">Back</a>
        </div>
    </main>
</template>
<script>
import axios from 'axios'
export default {
    name: "AdminComponent",
    data () {
        return {
            message: "",
            error:false,
            title:"Admin Dashboard",
            state:"usersList",
            obj:{},
            userIndex:-1
        }
    },
    mounted(){
        if (!this.isLoggedIn || this.user.type!=99){
            this.$router.push("/login?returnURL="+encodeURIComponent("/admin"))
        }
        this.scrollToTop()
        this.getUserList()
    },
    methods:{
        async reload(){
            this.message = ""
            let preState = this.state
            let preUserIndex = this.userIndex
            await this.getUserList().then(()=>{
                this.state = preState
                this.userIndex = preUserIndex
                if (this.state == "userListings") this.getUserListings(this.userIndex)
                if (this.state=="userAuthFile") this.getAuthFile(this.userIndex)
            })
            
        },
        async approveAuthFile(fileId){
            this.message = ""
            await axios.post("/api/admin/approve/"+fileId,{},{
                headers:{
                    "x-access-token": this.xAccessToken,
                    "Content-Type": "application/json"
                }
            }).then((res)=>{
                console.log(res)
                this.error=false
                this.messsage = res.data.message
                this.reload()
            }).catch((err)=>{
                console.log(err)
                this.message = err.response.data.message
            })
        },
        async declineAuthFile(fileId){
            this.message = ""
            await axios.post("/api/admin/approve/"+fileId,
                {
                    decline:1
                },
                {
                headers:{
                    "x-access-token": this.xAccessToken
                }
            }).then((res)=>{
                console.log(res)
                this.error=false
                this.message = res.data.message
                this.reload()
            }).catch((err)=>{
                console.log(err)
                this.message = err.response.data.message
            })
        },
        getAuthFile(userId){
            this.userIndex = userId
            this.message = ""
            this.obj.auth_file = this.obj.users[userId].authorization_file
            this.obj.user = this.obj.users[userId]
            console.log(this.obj.auth_file)
            if (this.isEmptyObject(this.obj.auth_file)){
                this.message ="No authorization file was found for this user."
                this.obj.auth_file = {}
            }else{
                this.state="userAuthFile"
            }
        },
        getUserListings(userId){
            this.userIndex = userId
            this.message = ""
            this.state="userListings"
            this.obj.listings = this.obj.users[userId].listings
            this.obj.user = this.obj.users[userId]
            if (this.isEmptyObject(this.obj.listings)){
                this.message = "No listings were found for this user."
            }
        },
        async getUserList(){
            this.message = ""
            this.error = false
            this.obj = {}
            this.userIndex = -1
            this.state="usersList"
            await axios.get("/api/admin/userlist",{
                headers:{
                    "x-access-token": this.xAccessToken
                }
            }).then((response)=>{
                console.log(response)
                this.obj.users = response.data.data
            }).catch((err)=>{
                console.log(err)
            })
        }
    }
}
</script>