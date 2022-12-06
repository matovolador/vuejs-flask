<template>
    <form @submit.prevent="createOffer()">
    <div class="form-floating">
        <input type="text" v-model="amount" class="form-control" id="floatingInput" placeholder="Enter amount" required>
        <label for="floatingInput">Amount $</label>
      </div>
      <button class="w-100 btn btn-lg btn-primary btn-sign" type="submit">Make Offer</button>  
      
    </form>
</template>
<style>
</style>
<script>
import axios from 'axios'
export default {
    name: "CreateOfferComponent",
    data () {
        return {
            listing_id:"",
            amount: ""
        }
    },
    props: ['listing','message','error'],
    mounted(){
        // if (!this.isLoggedIn){
        //     this.$router.push("/")
        // }
        this.listing_id = this.$router.currentRoute._value.query.listing_id
        console.log(this.listing_id)
    },
    methods:{
        createOffer (){
            this.$emit('update:message',"")
            this.$emit('update:error',false)
            if (!this.isLoggedIn){
                this.$router.push("/login?returnURL="+encodeURIComponent("/property?listing_id="+this.listing_id))
                return
            }
            if(this.amount != "") {
                axios.post("/api/offers",{
                    listing_id:this.listing_id,
                    amount: this.amount
                },{
                    headers: {
                        "x-access-token":this.xAccessToken
                    }
                }).then((response) => {
                    console.log(response.data)
                    if (response.data.success){
                        this.$emit('update:message',"Offer made! An email was sent to the owner of this property.")
                        this.$emit('update:error',false)
                        this.amount = ""
                        this.scrollToTop()
                    }
                    
                }).catch((err) => {
                    console.log(err)
                    if (err.response.status == 400){
                        if (err.response.data.message){
                            this.$emit('update:message',err.response.data.message)
                            this.$emit('update:error',true)
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
                console.log("Empty fields")
                this.$emit('update:message',"There are empty fields")
                this.$emit('update:error',true)
            }   
        }
    }
}
</script>