<template>
    <form @submit.prevent="resetPassword()" v-if="this.reset_token">
      <!-- <img class="logo" src="https://unsplash.it/80/80/?house" alt="Logo" loading="lazy"> -->
      <h2 class="h2">Reset Password</h2>      
        <div v-if="this.message" :class="{'error':error}">{{message}}</div>
      <div class="form-floating">
        <input type="email" v-model="email" class="form-control" id="floatingInput" placeholder="name@example.com" required>
        <label for="floatingInput">Email address</label>
      </div>
      <div class="form-floating">
        <input type="password" v-model="password" class="form-control" id="floatingPassword" placeholder="Password" required>
        <label for="floatingPassword">New Password</label>
      </div>
      <button v-if="!this.requested" class="w-100 btn btn-lg btn-primary btn-sign" type="submit">Send</button>  
      <button v-else class="w-100 btn btn-lg btn-secondary btn-sign" type="button" disabled>Sent</button>  
    </form>
    <form v-else @submit.prevent="requestPasswordReset()">
        <!-- <img class="logo" src="https://unsplash.it/80/80/?house" alt="Logo" loading="lazy"> -->
      <h2 class="h2">Request Password Reset</h2>      
        <div v-if="this.message" :class="{'error':error}">{{message}}</div>
      <div class="form-floating">
        <input type="email" v-model="email" class="form-control" id="floatingInput" placeholder="name@example.com" required>
        <label for="floatingInput">Email address</label>
      </div>
      <button v-if="!this.requested" class="w-100 btn btn-lg btn-primary btn-sign" type="submit">Request</button>  
      <button v-else class="w-100 btn btn-lg btn-secondary btn-sign" type="button" disabled>Requested</button>  
    </form>
    <a href="#" @click.prevent="this.$router.push('/login')">Back to Login</a>
</template>
<script>
import axios from 'axios'
export default {
    name: "ResetPasswordComponent",
    data () {
        return {
            email: "",
            password: "",
            message: "",
            reset_token:"",
            error:false,
            requested:false,
        }
    },
    mounted(){
        if (this.$router.currentRoute._value.query.reset_token){
            this.reset_token = this.$router.currentRoute._value.query.reset_token
        }else{
            this.reset_token = ""
        }
        this.email=""
        this.password=""
        this.requested=false
        this.error = false
        this.message = ""

    },
    methods:{
        requestPasswordReset(){
            this.error = false,
            this.message = ""
            if (this.email!=""){
                axios.get("/api/reset_password?email="+this.email).then((res)=>{
                    console.log(res)
                    this.error = false
                    this.message = res.data.message
                    this.$cookies.remove("user")
                    this.setCookieToken("")
                    this.requested=true
                }).catch((err)=>{
                    console.log(err)
                    this.message = err.request.data.message
                    this.error = true
                })
            }
        },  
        resetPassword (){
            this.message = ""
            this.error = false
            if(this.email != "" && this.password != "" && this.reset_token != "") {
                axios.post("/api/reset_password",{
                    email:this.email,
                    password:this.password,
                    reset_token: this.reset_token
                }).then((response) => {
                    console.log(response.data)
                    this.message="Your password has been reset."
                    this.error = false
                    this.$cookies.remove("user")
                    this.setCookieToken("")
                    this.requested=true
                }).catch((err) => {
                    console.log(err)
                    this.error = true
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
            }else{
                this.error = true
                console.log("Empty fields")
                console.log(this.email)
                console.log(this.password)
                console.log(this.reset_token)
            }   
        }
    }
}
</script>