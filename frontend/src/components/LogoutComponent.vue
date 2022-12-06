<template>
    <div></div>
</template>
<script>
import axios from 'axios'
export default {
    name: "LogoutComponent",
    data () {
        return {
            username: "",
            password: ""
        }
    },
    mounted(){
        if (!this.isLoggedIn){
            this.$router.push("/")
        }
        axios.get("/api/logout",{
            headers:{
                "x-access-token" :this.xAccessToken
            }
        }).then((response)=>{
            console.log(response.data)
            this.$cookies.remove("user")
            this.setCookieToken("")
            this.$router.go()
        }).catch((err)=>{
            console.log(err)
            this.$cookies.remove("user")
            this.setCookieToken("")
            this.$router.go()
        })
        
        
    }
}
</script>