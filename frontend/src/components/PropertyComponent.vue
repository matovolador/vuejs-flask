<template>
    
      <!-- <img class="logo" src="https://unsplash.it/80/80/?house" alt="Logo" loading="lazy"> -->
      <h2 class="h2" v-if="this.listing">{{this.listing.address}}</h2>
        <div v-if="this.message" :class="{'error':this.error}">{{message}}</div>
        <div v-if="this.auth"><span><a href="#" @click.prevent="this.$router.push('/authorization')">Get Approved!</a></span></div>
      <div>
        <ul>
            <li>
                Cost {{this.listing.price}}
            </li>
            <li>
                Property Size: {{this.listing.property_size}}
            </li>
            <li>
                Land Size: {{this.listing.land_size}}
            </li>
            <li>
                Bedrooms: {{this.listing.bedrooms}}
            </li>
            <li>
                Bathrooms: {{this.listing.bathrooms}}
            </li>
            <span v-if="!this.is_standard">
                <li>From {{this.listing.start_date}} to {{this.listing.end_date}}</li>
                <li>{{this.clock}}</li>
            </span>
        </ul>
      </div>
    <div v-if="this.is_standard">
        <CreateOfferComponent :listing="this.listing" v-model:message="this.message" v-model:error="this.error" />
    </div>
    <div v-else>
        <CreateBidComponent :listing="this.listing" v-model:message="this.message" v-model:error="this.error" v-model:auth="this.auth" />
        <!-- TODO Render Clock and extra info -->
    </div>
</template>
<script>
import axios from 'axios'
import CreateOfferComponent from "@/components/CreateOfferComponent.vue";
import CreateBidComponent from "@/components/CreateBidComponent.vue";
export default {
    name: "PropertyComponent",
    components: {
        CreateOfferComponent,
        CreateBidComponent
    },
    data () {
        return {
            listing_id:"",
            listing: {},
            message: "",
            error:false,
            is_standard: true,
            auth:false,
            clock:""
        }
    },
    methods:{
        startClock(endDate) {
            let countDownDate = new Date(endDate).getTime();

            // Run myfunc every second
            let myClockFunc = ()=> {
                let now = new Date().getTime();
                console.log(countDownDate)
                console.log(now)
                let timeleft = countDownDate - now;
                    
                // Calculating the days, hours, minutes and seconds left
                let days = Math.floor(timeleft / (1000 * 60 * 60 * 24));
                let hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                let minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
                let seconds = Math.floor((timeleft % (1000 * 60)) / 1000);
                this.clock = seconds+" seconds."
                if (minutes>0) this.clock= minutes+" minutes, "+this.clock
                if (hours>0) this.clock = hours+" hours, "+this.clock
                if (days>0) this.clock = days+" days, "+this.clock
                this.clock = "Auction ends in: "+this.clock
                // Display the message when countdown is over
                if (timeleft < 0) {
                    this.clock = "Auction ended."
                }else{
                    setTimeout(myClockFunc,1000);
                }
                // console.log(this.clock)
            }
            myClockFunc()
        }
    },
    mounted(){
        this.listing_id = this.$router.currentRoute._value.query.listing_id
        axios.get("/api/listings/"+this.listing_id).then((response)=>{
            console.log(response.data)
            this.listing = response.data.data
            if (this.listing.listing_type == "standard"){
                this.is_standard = true
            }else{
                this.is_standard = false
                this.startClock(this.listing.end_date)
                this.listing.start_date = this.convertDateStringToLocale(this.listing.start_date)
                this.listing.end_date = this.convertDateStringToLocale(this.listing.end_date)
                
            }
            for (let i =0;i<this.listing.bids;i++){
                this.listings.bids[i].created_at = this.convertDateStringToLocale(this.listings.bids[i].created_at)
            }
        }).catch((err)=>{
            console.log(err)
            this.message = err.reponse.data.message
        })

    }
}
</script>