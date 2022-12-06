<template>
    <div class="row">
      <!-- <img class="logo" src="https://unsplash.it/80/80/?house" alt="Logo" loading="lazy"> -->
      <h2 class="h2">{{this.outcome}}</h2>  
      <div v-if="this.message" class="error">{{message}}</div>
      <a href="#" v-if="emailVerified" @click.prevent="login()">Sign In</a>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: "VerifyEmailComponent",
    data () {
        return {
            outcome: "Verifying your email. Please wait...",
            message: "",
            emailVerified:false
        }
    },
    mounted(){
        if (this.isLoggedIn){
            this.$router.push("/")
        }
        axios.get("/api/validate_email",{params:{
            "email":this.$route.query.email,
            "token": this.$route.query.token
        }}).then((response)=>{
            console.log(response.data)
            this.outcome = "Your email has been verified!"
            this.emailVerified=true
        }).catch((err)=>{
            console.log(err)
            this.outcome = "Your email could not be verified."
            if (err.response.status == 400){
                if (err.response.data.message){
                    this.message = err.response.data.message
                }
                return
            }else if (err.response.status == 401){
                if (err.response.data.message){
                    this.message = err.response.data.message
                }
                return
            }
        })

    },
    methods:{
        login(){
            this.$router.push("/login")
        }
    }
}
</script>