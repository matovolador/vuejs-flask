<template>
    <form @submit.prevent="createBid()">
        <div class="last_bid">
            <h4>Last Bid:</h4>
            <div v-if="this.listing.bids.length"><span>$ {{this.last_bid.amount}}</span> <span v-if="this.user && (this.user.id!=this.listing.bids[0].created_by)">made by {{this.last_bid.created_by_user}}</span><span v-else-if="!this.user">made by {{this.last_bid.created_by_user}}</span><span v-else>You made this bid</span> <span>at: {{this.last_bid.created_at}}</span></div>
            <div v-else>No bids were made yet.</div>
        </div>
      <div class="form-floating">
        <input type="text" v-model="amount" class="form-control" id="floatingInput" placeholder="Enter amount" required>
        <label for="floatingInput">Amount $</label>
      </div>
      <button class="w-100 btn btn-lg btn-primary btn-sign" type="submit">Make a Bid</button>  
      
    </form>
    <button class="w-100 btn btn-lg btn-secondary" @click.prevent="this.reloadPage()">Refresh</button>
</template>
<script>
import axios from 'axios'
export default {
    name: "CreateBidComponent",
    props:["message","error","listing","auth"],
    data () {
        return {
            listing_id:"",
            amount: 0.0,
            min_amount : "",
            last_bid:{}
        }
    },
    mounted(){
        this.listing_id = this.$router.currentRoute._value.query.listing_id
        console.log(this.listing_id)
        if (this.listing.bids.length){
            this.min_amount = parseFloat(this.listing.bids[0].amount) + parseFloat(this.listing.incremental_price_amount)
        }else{
            this.min_amount = parseFloat(this.listing.price) + parseFloat(this.listing.incremental_price_amount)
        }
        this.amount = this.min_amount
        if (this.listing.bids.length){
            axios.get("/api/users/"+this.listing.bids[0].created_by+"/public").then((response)=>{
                this.last_bid = {
                    amount: this.listing.bids[0].amount,
                    created_at: this.convertDateStringToLocale(this.listing.bids[0].created),
                    created_by_user: response.data.data.first_name+" "+response.data.data.last_name+"."
                }
            }).catch((err)=>{
                console.log(err)
            })
        }
        console.log(this.last_bid)
    },
    methods:{
        createBid (){
            this.$emit('update:message',"" )
            this.$emit('update:error',false)
            this.$emit("update:auth",false)
            this.amount = parseFloat(this.amount)
            if (!this.isLoggedIn){
                this.$router.push("/login?returnURL="+encodeURIComponent("/property?listing_id="+this.listing_id))
                return
            }
            if (this.amount < this.min_amount){
                this.$emit('update:message',"Amount can't be lower than $"+this.min_amount)
                this.$emit('update:error',true)
                return
            }
            if(this.amount != "" && this.amount!=0) {
                axios.post("/api/bids",{
                    listing_id:this.listing_id,
                    amount: this.amount
                },{
                    headers: {
                        "x-access-token":this.xAccessToken
                    }
                }).then((response) => {
                    console.log(response.data)
                    if (response.data.success){
                        this.$emit('update:message',"Bid made!")
                        this.$emit("update:error",false)
                        this.reloadPage()
                    }
                    
                }).catch((err) => {
                    console.log(err)
                    if (err.response.status == 400){
                        if (err.response.data.message){
                            this.$emit('update:message',err.response.data.message)
                            this.$emit('update:error',true)
                            if (err.response.data.message=="You must be authorized to place bids."){
                                this.$emit("update:auth",true)
                            }
                        }
                        return
                    }else if (err.response.status == 401){
                        if (err.response.data.message){
                            this.$emit('update:message',err.response.data.message)
                            this.$emit('update:error',true)
                        }
                        return
                    }
                })
            }else{
                this.$emit('update:message',"Empty fields")
                this.$emit('update:error',true)
            }   
        }
    }
}
</script>