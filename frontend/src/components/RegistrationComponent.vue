<template>
    <form @submit.prevent="doRegister()">
      <!-- <img class="logo" src="https://unsplash.it/80/80/?house" alt="Logo" loading="lazy"> -->
      <h2 class="h2">Please Sign Up</h2>  
      <div v-if="this.message" class="error">{{message}}</div>
      <div class="user-type">
        <span class="me-3">Signing up as:</span>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" v-model="type" name="inlineRadioOptions" id="inlineRadio1" value="0">
          <label class="form-check-label" for="inlineRadio1">User</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" v-model="type" name="inlineRadioOptions" id="inlineRadio2" value="1">
          <label class="form-check-label" for="inlineRadio2">Agent</label>
        </div>
      </div>

      <div class="form-floating">
        <input type="fisrt-name" v-model="first_name" class="form-control" id="floatingInput" placeholder="First Name" required>
        <label for="floatingInput">First name</label>
      </div>

      <div class="form-floating">
        <input type="last-name" v-model="last_name" class="form-control" id="floatingInput" placeholder="Last Name" required>
        <label for="floatingInput">Last name</label>
      </div>

      <!-- <div class="form-floating">
        <input type="user-name" class="form-control" id="floatingInput" placeholder="username">
        <label for="floatingInput">Username</label>
      </div> -->
  
      <div class="form-floating">
        <input type="email" class="form-control" v-model="email" id="floatingInput" placeholder="name@example.com" required>
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
      <button class="w-100 btn btn-lg btn-primary btn-sign" type="submit">Sign up</button>  
      
      <p class="divider">or</p>
    </form>
    <button class="w-100 btn btn-lg btn-secondary btn-sign-google" type=""  @click.prevent="google()">
        <i class="bi bi-google"></i>
        <span>Sign up with Google</span>
      </button>
</template>
<script>
import axios from 'axios'
export default {
    name: "RegistrationComponent",
    data () {
        return {
            password: "",
            email: "",
            first_name:"",
            last_name:"",
            type:"0",
            message: ""
        }
    },
    mounted(){
        if (this.isLoggedIn){
            this.$router.push("/")
        }

    },
    methods:{
        google(){
          console.log("Google")
        },
        doRegister (){
          this.message = ""
            if(this.email != "" && this.password != "" && this.first_name != "" && this.last_name != "") {
                axios.post("/api/registration",{
                    email:this.email,
                    password: this.password,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    type: this.type
                },{
                    headers:{
                        "Content-Type":"application/json"
                    }
                }).then((response) => {
                    console.log(response.data)
                    // this.setCookieToken(response.data.token)
                    // this.$cookies.set("user",{
                    //     first_name: response.data.first_name,
                    //     last_name : response.data.last_name,
                    //     id : response.data.user_id,
                    //     email : response.data.email
                    // })
                    // TODO SEND TO EMAIL MUST BE VALIDATED WINDOW
                    this.$router.go()
                    
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
            }   
        }
    }
}
</script>