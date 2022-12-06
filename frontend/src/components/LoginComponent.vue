<template>
    <form @submit.prevent="doLogin()">
      <!-- <img class="logo" src="https://unsplash.it/80/80/?house" alt="Logo" loading="lazy"> -->
      <h2 class="h2">Please Sign In</h2>      
        <div v-if="this.message" class="error">{{message}}</div>
      <div class="form-floating">
        <input type="email" v-model="email" class="form-control" id="floatingInput" placeholder="name@example.com" required>
        <label for="floatingInput">Email address</label>
      </div>
      <div class="form-floating">
        <input type="password" v-model="password" class="form-control" id="floatingPassword" placeholder="Password" required>
        <label for="floatingPassword">Password</label>
      </div>
  
      <div class="checkbox remember">
        <label>
          <input type="checkbox" value="remember-me"> Remember me
        </label>
      </div>
      <button class="w-100 btn btn-lg btn-primary btn-sign" type="submit">Sign in</button>  
      
      <p class="divider">or</p>
    </form> 
    <button class="w-100 btn btn-lg btn-secondary btn-sign-google" type="" @click.prevent="google()" >
        <i class="bi bi-google"></i>
        <span>Sign in with Google</span>
      </button>
</template>
<script>
import axios from 'axios'
export default {
    name: "LoginComponent",
    data () {
        return {
            email: "",
            password: "",
            message: "",
            returnURL:""
        }
    },
    mounted(){
        if (this.isLoggedIn){
            this.$router.push("/")
        }
        if (this.$router.currentRoute._value.query.returnURL){
            this.returnURL = this.$router.currentRoute._value.query.returnURL
        }

    },
    methods:{
        google(){
            console.log("Google")
        },
        doLogin (){
            this.message = ""
            if(this.email != "" && this.password != "") {
                axios.post("/api/login",{},{
                    auth: {
                        username: this.email,
                        password : this.password
                    }
                }).then((response) => {
                    console.log(response.data)
                    
                    this.$cookies.set("user",{
                        first_name: response.data.first_name,
                        last_name : response.data.last_name,
                        id : response.data.user_id,
                        email : response.data.email,
                        type: response.data.type
                    })
                    this.setCookieToken(response.data.token)
                    if (!this.returnURL){
                        this.$router.go()
                    }else{
                        this.$router.push(this.returnURL)
                    }
                    
                    
                }).catch((err) => {
                    console.log(err)
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
                console.log("Empty fields")
                console.log(this.email)
                console.log(this.password)
            }   
        }
    }
}
</script>