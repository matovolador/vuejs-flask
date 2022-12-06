<template>
    <main id="content" role="main">
    <!-- Form -->
    <div class="container content-space-3 content-space-lg-4">
      <div class="w-lg-75 mx-lg-auto">
        <!-- Heading -->
        <div class="text-center mb-2">
          <h1 class="h2">Loan authorization upload form</h1>
        </div>
        <!-- End Heading -->

        <div class="text-center mb-2" v-if="this.currentAuthFileUrl">
            <p>Current file: <a :href="this.currentAuthFileUrl">Download</a></p>
            <p>
              <span v-if="this.currentAuthFile.declined">Your authorization was declined. Please submit another one.</span>
              <span v-else-if="this.currentAuthFile.approved">Your authorization is pending approval.</span>
              <span v-else>Congratulations! You have been approved for bidding. <br>If you submit a new file, you will have to be authorized again in order to place bids.</span>
              
            </p>
        </div>

        <!-- <form @submit.prevent="uploadAuthFile()" v-if="this.currentAuthFile.declined || !this.currentAuthFile.approved"> -->
        <form @submit.prevent="uploadAuthFile()" v-if="this.currentAuthFile.declined || !this.currentAuthFile.approved">
          <div class="mb-5">
            <div v-if="this.message" :class="{'error':this.error}">{{message}}</div>
            

            <h4 class="my-7">Upload Loan Form</h4>

            <div class="row">
              <div class="col-lg-6 mb-3">
                <label class="form-label">File Upload</label>

                <!-- File Attachment Input -->
                <div id="imageDropzone" class="js-dropzone dz-dropzone dz-dropzone-card">
                  <div class="dz-message">
                    <input type="file" ref="file"/>
                    <img class="avatar mb-3" src="/assets/svg/illustrations/add-file.svg" alt="SVG">
                    <span class="d-block">Browse your device</span>
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
        <a href="#" @click.prevent="this.$router.go(-1)">Back</a>
      </div>
    </div>
    <!-- End Form -->
  </main>
</template>
<script>
import axios from 'axios'
export default {
    name: "AuthFileComponent",
    data () {
        return {
            message: "",
            error:false,
            currentAuthFile:{
              url : "",
              declined: false,
              approved: false
            },
            buttonState: "Submit"
        }
    },
    mounted(){
        if (!this.isLoggedIn){
          this.$router.push("/")
        }
        this.getCurrentAuthFile()

    },
    methods:{
      getCurrentAuthFile(){
        axios.get("/api/authorization_file/"+this.user.id,{
          headers:{
            "x-access-token": this.xAccessToken
          }
        }).then((response)=>{
          console.log(response.data)
          this.currentAuthFile.url = response.data.data.authorization_file_url
          this.currentAuthFile.declined = response.data.data.declined
          this.currentAuthFile.approved = response.data.data.approved

        }).catch((err)=>{
          console.log(err)
          this.message = err.response.data.message
          if (err.response.status==400){ // user has no file
            this.error = false
          }else{
            this.error = true
          }
          
        })
        return
      },
      uploadAuthFile(){
        this.message= ""
        this.error = false
        this.buttonState = "Processing"
        let files = this.$refs.file.files;
        console.log(files)
        let formData = new FormData();
        formData.append("file",files[0])
        axios.post("/api/authorization_file",formData, {
          headers:{
            "x-access-token": this.xAccessToken
          }
        }).then((response)=>{
          console.log(response.data)
          this.error = false
          this.message = "File was uploaded! An admin needs to approve your submission."
          this.buttonState = "Submit"
          return true
        }).catch((err) =>{
          console.log(err)
          this.message = err.reponse.data.message
          this.error = true
          this.buttonState = "Submit"
          return false
        })
      }
    }
}
</script>