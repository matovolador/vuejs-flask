<template>
    <main id="content" role="main">
    <!-- Form -->
    <div class="container content-space-3 content-space-lg-4">
      <div class="w-lg-75 mx-lg-auto">
        <!-- Heading -->
        <div class="text-center mb-2">
          <h1 class="h2">Real estate listing upload form</h1>
          <p class="mb-0">Please proofread your submission carefully before submitting.</p>
          <p>Submissions which exceed maximum word counts will be edited.</p>
        </div>
        <!-- End Heading -->

        <form @submit.prevent="createListing()">
          <div class="mb-5">
            <div v-if="this.message" class="error">{{message}}</div>
            <h4 class="my-7">Type of listing</h4>

            <div class="row gx-3">
              <div class="col-6 col-md-3 mb-3">
                <!-- Radio Check -->
                <div class="form-check form-check-card text-center">
                  <input class="form-check-input" type="radio" name="typeOfListing" id="typeOfListing1" v-model="listing_type" value="standard">
                  <label class="form-check-label" for="typeOfListing">Standard
                  </label>
                </div>
                <!-- End Radio Check -->
              </div>
              <!-- End Col -->
              <div class="col-6 col-md-3 mb-3">
                <!-- Radio Check -->
                <div class="form-check form-check-card text-center">
                  <input class="form-check-input" type="radio" name="typeOfListing" id="typeOfListing2" v-model="listing_type" value="auction">
                  <label class="form-check-label" for="typeOfListing">Auction
                  </label>
                </div>
                <!-- End Radio Check -->
              </div>
              <!-- End Col -->
            </div>
            <!-- End Row -->


            <h4 class="my-7">Type of property</h4>

            <div class="row gx-3">
              <div class="col-6 col-md-3 mb-3">
                <!-- Radio Check -->
                <div class="form-check form-check-card text-center">
                  <input class="form-check-input" type="radio" name="typeOfProperty" id="typeOfProperty1" v-model="property_type" value="house">
                  <label class="form-check-label" for="typeOfProperty1">
                    <img class="w-50 mb-3" src="/assets/svg/illustrations/small-house.svg" alt="SVG">
                    <span class="d-block">House</span>
                  </label>
                </div>
                <!-- End Radio Check -->
              </div>
              <!-- End Col -->

              <div class="col-6 col-md-3 mb-3">
                <!-- Radio Check -->
                <div class="form-check form-check-card text-center">
                  <input class="form-check-input" type="radio" name="typeOfProperty" id="typeOfProperty2" v-model="property_type" value="apartment">
                  <label class="form-check-label" for="typeOfProperty2">
                    <img class="w-50 mb-3" src="/assets/svg/illustrations/flat-house.svg" alt="SVG">
                    <span class="d-block">Flat</span>
                  </label>
                </div>
                <!-- End Radio Check -->
              </div>
              <!-- End Col -->
            </div>
            <!-- End Row -->

            <h4 class="my-7">Listing information</h4>

            
            <div class="row">
              <div class="col-sm-6">
                <!-- Form -->
                <div class="mb-4">
                  <label class="form-label" for="addressUploadForm">Address</label>
                  
                  <div class="input-group input-group-merge">
                    <span class="input-group-prepend input-group-text">
                      <i class="bi-geo-alt-fill"></i>
                    </span>
                    <!-- <input type="text" class="form-control form-control-lg" id="addressUploadForm" placeholder="Address" aria-label="Address" v-model="address" autocomplete="off"> -->
                    <vue-google-autocomplete id="map" classname="form-control form-control-lg" placeholder="Address" :country="['us']" v-on:placechanged="getAddressData" aria-label="Address"></vue-google-autocomplete>
                  </div>
                </div>
                <!-- End Form -->
              </div>
              <!-- End Col -->
            </div>

            <div class="row">
              <div class="col-sm-6">
                <!-- Form -->
                <div class="mb-4">
                  <label class="form-label" for="currencyUploadForm">Price</label>
              
                  <div class="input-group input-group-merge">
                    <span class="input-group-prepend input-group-text">
                      <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 288 512"><path d="M209.2 233.4l-108-31.6C88.7 198.2 80 186.5 80 173.5c0-16.3 13.2-29.5 29.5-29.5h66.3c12.2 0 24.2 3.7 34.2 10.5 6.1 4.1 14.3 3.1 19.5-2l34.8-34c7.1-6.9 6.1-18.4-1.8-24.5C238 74.8 207.4 64.1 176 64V16c0-8.8-7.2-16-16-16h-32c-8.8 0-16 7.2-16 16v48h-2.5C45.8 64-5.4 118.7.5 183.6c4.2 46.1 39.4 83.6 83.8 96.6l102.5 30c12.5 3.7 21.2 15.3 21.2 28.3 0 16.3-13.2 29.5-29.5 29.5h-66.3C100 368 88 364.3 78 357.5c-6.1-4.1-14.3-3.1-19.5 2l-34.8 34c-7.1 6.9-6.1 18.4 1.8 24.5 24.5 19.2 55.1 29.9 86.5 30v48c0 8.8 7.2 16 16 16h32c8.8 0 16-7.2 16-16v-48.2c46.6-.9 90.3-28.6 105.7-72.7 21.5-61.6-14.6-124.8-72.5-141.7z"/></svg>
                      </span>
                    </span>
                    <input type="text" class="form-control form-control-lg" id="currencyUploadForm" placeholder="Price" aria-label="Price" v-model="price">
                  </div>
                </div>
                <!-- End Form -->
              </div>
              <!-- End Col -->
              <div class="col-sm-6" v-if="this.listing_type=='auction'">
                <!-- Form -->
                <div class="mb-4">
                  <label class="form-label" for="currencyUploadForm">Incremental Price Amount</label>
                  <div class="input-group input-group-merge">
                    <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 288 512"><path d="M209.2 233.4l-108-31.6C88.7 198.2 80 186.5 80 173.5c0-16.3 13.2-29.5 29.5-29.5h66.3c12.2 0 24.2 3.7 34.2 10.5 6.1 4.1 14.3 3.1 19.5-2l34.8-34c7.1-6.9 6.1-18.4-1.8-24.5C238 74.8 207.4 64.1 176 64V16c0-8.8-7.2-16-16-16h-32c-8.8 0-16 7.2-16 16v48h-2.5C45.8 64-5.4 118.7.5 183.6c4.2 46.1 39.4 83.6 83.8 96.6l102.5 30c12.5 3.7 21.2 15.3 21.2 28.3 0 16.3-13.2 29.5-29.5 29.5h-66.3C100 368 88 364.3 78 357.5c-6.1-4.1-14.3-3.1-19.5 2l-34.8 34c-7.1 6.9-6.1 18.4 1.8 24.5 24.5 19.2 55.1 29.9 86.5 30v48c0 8.8 7.2 16 16 16h32c8.8 0 16-7.2 16-16v-48.2c46.6-.9 90.3-28.6 105.7-72.7 21.5-61.6-14.6-124.8-72.5-141.7z"/></svg>
                    </span>
                    <select id="yearBuiltUploadForm" class="form-select form-select-lg" v-model="incremental_price_amount">
                      <option selected disabled>Select amount</option>
                      <option value="500">500</option>
                      <option value="1000">1000</option>
                      <option value="1500">1500</option>
                      <option value="2000">2000</option>
                      <option value="2500">2500</option>
                    </select>
                  </div>
                </div>
                <!-- End Form -->
              </div>
              <!-- End Col -->
            </div>
            <!-- End Row -->
            <div class="row" v-if="this.listing_type=='auction'">
              <div class="col-sm-6">
                <label class="form-label" for="start_date">Start Date</label>
                <input type="date" name="start_date" v-model="start_date_display" @change="setDates()"> 6 am
              </div>
              <div class="col-sm-6">
                <label class="form-label" for="end_date">End Date</label>
                <input type="date" name="end_date" v-model="end_date_display" disabled> 6pm
              </div>
            </div>
            <!-- End Row -->


            <div class="row">
              <div class="col-sm-6">
                <label class="form-label" for="yearBuiltUploadForm">Year built</label>

                  <div class="input-group input-group-merge">
                    <span class="input-group-prepend input-group-text">
                      <i class="bi-calendar-week"></i>
                    </span>
                    <select id="yearBuiltUploadForm" class="form-select form-select-lg" v-model="year_built">
                      <option selected disabled>Select year</option>
                      <option value="Pre-1985">Pre-1985</option>
                      <option value="1985">1985</option>
                      <option value="1986">1986</option>
                      <option value="1987">1987</option>
                      <option value="1988">1988</option>
                      <option value="1989">1989</option>
                      <option value="1990">1990</option>
                      <option value="1991">1991</option>
                      <option value="1992">1992</option>
                      <option value="1993">1993</option>
                      <option value="1994">1994</option>
                      <option value="1995">1995</option>
                      <option value="1996">1996</option>
                      <option value="1997">1997</option>
                      <option value="1998">1998</option>
                      <option value="1999">1999</option>
                      <option value="2000">2000</option>
                      <option value="2001">2001</option>
                      <option value="2002">2002</option>
                      <option value="2003">2003</option>
                      <option value="2004">2004</option>
                      <option value="2005">2005</option>
                      <option value="2006">2006</option>
                      <option value="2007">2007</option>
                      <option value="2008">2008</option>
                      <option value="2009">2009</option>
                      <option value="2010">2010</option>
                      <option value="2011">2011</option>
                      <option value="2012">2012</option>
                      <option value="2013">2013</option>
                      <option value="2014">2014</option>
                      <option value="2015">2015</option>
                      <option value="2016">2016</option>
                      <option value="2017">2017</option>
                      <option value="2018">2018</option>
                      <option value="2019">2019</option>
                      <option value="2020">2020</option>
                      <option value="2021">2021</option>
                      <option value="2022">2022</option>
                    </select>
                  </div>
              </div>
              <!-- End Col -->
            </div>
            <!-- End Row -->
            


            <div class="row">
              <div class="col-sm-6">
                <!-- Form -->
                <div class="mb-4">
                  <label class="form-label" for="propertySizeUploadForm">Property size</label>
                  
                  <div class="input-group input-group-merge">
                    <span class="input-group-prepend input-group-text">
                      <i class="bi-rulers"></i>
                    </span>
                    <input type="text" class="form-control form-control-lg" id="propertySizeUploadForm" placeholder="Property size" aria-label="Property size" v-model="property_size">
                  </div>
                </div>
                <!-- End Form -->
              </div>
              <!-- End Col -->

              <div class="col-sm-6">
                <!-- Form -->
                <div class="mb-4">
                  <label class="form-label" for="landSizeUploadForm">Land size</label>
                  
                  <div class="input-group input-group-merge">
                    <span class="input-group-prepend input-group-text">
                      <i class="bi-rulers"></i>
                    </span>
                    <input type="text" class="form-control form-control-lg" id="landSizeUploadForm" placeholder="Land size" aria-label="Land size" v-model="land_size">
                  </div>
                </div>
                <!-- End Form -->
              </div>
              <!-- End Col -->
            </div>
            <!-- End Row -->

            <div class="row">
              <div class="col-sm-6">
                <!-- Form -->
                <div class="mb-4">
                  <label class="form-label" for="bedroomUploadForm">Bedroom</label>

                  <div class="input-group input-group-merge">
                    <span class="input-group-prepend input-group-text">
                      <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 640 512"><path d="M176 256c44.11 0 80-35.89 80-80s-35.89-80-80-80-80 35.89-80 80 35.89 80 80 80zm352-128H304c-8.84 0-16 7.16-16 16v144H64V80c0-8.84-7.16-16-16-16H16C7.16 64 0 71.16 0 80v352c0 8.84 7.16 16 16 16h32c8.84 0 16-7.16 16-16v-48h512v48c0 8.84 7.16 16 16 16h32c8.84 0 16-7.16 16-16V240c0-61.86-50.14-112-112-112z"/></svg>
                      </span>
                    </span>
                    <select id="bedroomUploadForm" class="form-select form-select-lg" v-model="bedrooms">
                      <option selected disabled>Select amount</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                      <option value="6">6</option>
                      <option value="7">7</option>
                    </select>
                  </div>
                </div>
                <!-- End Form -->
              </div>
              <!-- End Col -->

              <div class="col-sm-6">
                <!-- Form -->
                <div class="mb-4">
                  <label class="form-label" for="BathroomUploadForm">Bathroom</label>

                  <div class="input-group input-group-merge">
                    <span class="input-group-prepend input-group-text">
                      <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 512 512"><path d="M304,320a16,16,0,1,0,16,16A16,16,0,0,0,304,320Zm32-96a16,16,0,1,0,16,16A16,16,0,0,0,336,224Zm32,64a16,16,0,1,0-16-16A16,16,0,0,0,368,288Zm-32,32a16,16,0,1,0-16-16A16,16,0,0,0,336,320Zm-32-64a16,16,0,1,0,16,16A16,16,0,0,0,304,256Zm128-32a16,16,0,1,0-16-16A16,16,0,0,0,432,224Zm-48,16a16,16,0,1,0,16-16A16,16,0,0,0,384,240Zm-16-48a16,16,0,1,0,16,16A16,16,0,0,0,368,192Zm96,32a16,16,0,1,0,16,16A16,16,0,0,0,464,224Zm32-32a16,16,0,1,0,16,16A16,16,0,0,0,496,192Zm-64,64a16,16,0,1,0,16,16A16,16,0,0,0,432,256Zm-32,32a16,16,0,1,0,16,16A16,16,0,0,0,400,288Zm-64,64a16,16,0,1,0,16,16A16,16,0,0,0,336,352Zm-32,32a16,16,0,1,0,16,16A16,16,0,0,0,304,384Zm64-64a16,16,0,1,0,16,16A16,16,0,0,0,368,320Zm21.65-218.35-11.3-11.31a16,16,0,0,0-22.63,0L350.05,96A111.19,111.19,0,0,0,272,64c-19.24,0-37.08,5.3-52.9,13.85l-10-10A121.72,121.72,0,0,0,123.44,32C55.49,31.5,0,92.91,0,160.85V464a16,16,0,0,0,16,16H48a16,16,0,0,0,16-16V158.4c0-30.15,21-58.2,51-61.93a58.38,58.38,0,0,1,48.93,16.67l10,10C165.3,138.92,160,156.76,160,176a111.23,111.23,0,0,0,32,78.05l-5.66,5.67a16,16,0,0,0,0,22.62l11.3,11.31a16,16,0,0,0,22.63,0L389.65,124.28A16,16,0,0,0,389.65,101.65Z"/></svg>
                      </span>
                    </span>
                    <select id="BathroomUploadForm" class="form-select form-select-lg" v-model="bathrooms">
                      <option selected disabled>Select amount</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                      <option value="6">6</option>
                    </select>
                  </div>
                </div>
                <!-- End Form -->
              </div>
              <!-- End Col -->
            </div>
            <!-- End Row -->

            <!-- Form -->
            <div class="mb-4">
              <label class="form-label">Listing description</label>
                <textarea v-model="description" rows="30" cols="30"></textarea>
            </div>
            <!-- End Form -->

            <h4 class="my-7">Upload images</h4>

            <div class="row">
              <div class="col-lg-6 mb-3">
                <label class="form-label">Property media</label>

                <!-- File Attachment Input -->
                <div id="imageDropzone" class="js-dropzone dz-dropzone dz-dropzone-card">
                  <div class="dz-message">
                    <input type="file" ref="file" multiple />
                    <img class="avatar mb-3" src="/assets/svg/illustrations/add-file.svg" alt="SVG">
                    <span class="d-block">Browse your device and upload images</span>
                    <span class="d-block text-muted small">Maximum file size is 2MB</span>
                  </div>
                </div>
                <!-- End File Attachment Input -->
              </div>

            </div>
          </div>
          <!-- End Row -->

          <div class="d-grid">
            <button type="submit" class="btn btn-primary btn-lg" v-if="buttonState=='Submit'">{{buttonState}}</button>
            <button v-else type="submit" class="btn btn-secondary btn-lg" disabled>{{buttonState}}</button>
          </div>
        </form>
      </div>
    </div>
    <!-- End Form -->
  </main>
</template>
<script>
import axios from 'axios'
import VueGoogleAutocomplete from "vue-google-autocomplete";
export default {
    name: "CreateListingComponent",
    components: { VueGoogleAutocomplete },
    data () {
        return {
            buttonState:"Submit",
            addressArray: "",
            city:"",
            state:"",
            zip_code: "",
            price:"",
            description:"",
            land_size:"",
            property_size:"",
            bedrooms:"",
            bathrooms:"",
            listing_type:"",
            property_type: "",
            year_built:"",
            start_date:"",
            start_date_display: "",
            end_date_display:"",
            end_date:"",
            images : [],
            message: ""
        }
    },
    mounted(){
        if (!this.isLoggedIn){
          this.$router.push("/")
        }

    },
    methods:{
        google(){
          console.log("Google")
        },
        setDates(){
          let start_date_local = ""
          console.log(this.start_date_display)
          console.log(new Date(this.start_date_display))
          start_date_local = new Date(this.start_date_display)
          let timezoneOffset = start_date_local.getTimezoneOffset()/60  // hours
          start_date_local.setHours(start_date_local.getHours() + 6 + timezoneOffset)
          console.log(start_date_local)
          this.start_date = start_date_local.toISOString();
          console.log(this.start_date)
          let end_date_local = new Date(this.start_date_display)
          end_date_local.setHours(end_date_local.getHours() + 18 + timezoneOffset)
          end_date_local.setDate(end_date_local.getDate() + 14);
          console.log(end_date_local)
          this.end_date_display = new Date(this.start_date_display)
          this.end_date_display.setDate(start_date_local.getDate()+14)
          this.end_date_display = this.dateToUniformString(this.end_date_display)
          console.log(end_date_local)
          this.end_date = end_date_local.toISOString();
          console.log(this.end_date)

          this.start_date = this.start_date.substring(0,this.start_date.indexOf(".")).replace("T"," ")
          this.end_date = this.end_date.substring(0,this.end_date.indexOf(".")).replace("T"," ")

          console.log("----------")
          console.log(this.start_date)
          console.log(this.end_date)

          // console.log(this.start_date.substring(0,this.start_date.indexOf("T")))
          // console.log(this.end_date.substring(0,this.end_date.indexOf("T")))
          
        },
        async uploadImages(){
           let files = this.$refs.file.files;
           console.log(files)
           this.images = []
           for (let i=0; i<files.length; i++ ){
              let formData = new FormData();
              formData.append("file",files[i])
              await axios.post("/api/images",formData, {
                headers:{
                  "x-access-token": this.xAccessToken
                }
              }).then((response)=>{
                console.log(response.data)
                  this.images.push(response.data.data.url)
                  console.log(this.images)
              }).catch((err) =>{
                console.log(err)
                this.images = []
                return false
              })
           }
           console.log(this.images)
           return true
        },
        getAddressData(addressData, placeResultData, id) {
          this.addressArray = addressData;
          console.log(this.addressArray)
          this.address = this.addressArray.street_number + " " + this.addressArray.route +", "+this.addressArray.locality+" "+this.addressArray.administrative_area_level_1
          this.city = this.addressArray.locality
          this.state = this.addressArray.administrative_area_level_1
          this.zip_code = this.addressArray.postal_code
        },
        async createListing (){
          this.message = ""
            if((this.address != "" && this.bathrooms != "" && this.bedrooms != "" && this.land_size != "" && this.property_size != "" && this.zip_code != "" && this.listing_type != "" && this.property_type != "" && this.year_built != "" && this.images != [] && this.price != "" && parseFloat(this.price.toString()) != 0) && (this.listing_type=='standard' ) || (this.listing_type=="auction" && this.start_date!="" && this.end_date!="" && this.incremental_price_amount!="" )) {
              this.buttonState = "Processing"
              let imagesOk = await this.uploadImages()
              if (!imagesOk) {
                this.scrollToTop()
                return
              }

              axios.post("/api/listings",{
                address:this.address,
                city:this.city,
                state:this.state,
                zip_code: this.zip_code,
                description:this.description,
                price: this.price,
                land_size:this.land_size,
                property_size:this.property_size,
                bedrooms:this.bedrooms,
                bathrooms:this.bathrooms,
                listing_type:this.listing_type,
                property_type: this.property_type,
                year_built: this.year_built,
                images : this.images,
                start_date: this.start_date,
                end_date: this.end_date,
                incremental_price_amount: this.incremental_price_amount
                },{
                    headers:{
                        "Content-Type":"application/json",
                        "x-access-token": this.xAccessToken
                    }
                }).then((response) => {
                    console.log(response.data)
                    this.buttonState ="Submit"
                    this.$router.push("/")
                    
                }).catch((err) => {
                    console.log(err)
                    this.scrollToTop()
                    this.buttonState ="Submit"
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
                this.message = "There are empty fields"
                this.scrollToTop()
            }   
        }
    }
}
</script>