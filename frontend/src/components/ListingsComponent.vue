<template>
  <!-- Card List -->
  <div class="container content-space-t-1 content-space-b-2 content-space-b-lg-3">
      <!-- Heading -->
      <div class="mb-5">
        <div class="row align-items-center">
          <div class="col-sm mb-3 mb-sm-0" style="text-align:left">
            <span class="d-block" v-if="this.countHomes">{{this.countHomes}} homes</span>
            <h1 class="h2 mb-0">Property for sale in London</h1>
          </div>
          <!-- End Col -->

          <div class="col-sm-auto">
            <!-- Select -->
            <select class="form-select form-select-sm">
              <option value="mostRecent" selected>Most recent</option>
              <option value="HighestPrice">Highest price</option>
              <option value="LowestPrice">Lowest price</option>
              <option value="mostReduced">Most reduced</option>
              <option value="mostPopular">Most popular</option>
            </select>
            <!-- End Select -->
          </div>
          <!-- End Col -->
        </div>
        <!-- End Row -->
      </div>
      <!-- End Heading -->

      <div class="d-grid gap-5 mb-7">
      <div v-if="!grid">
        <!-- Card -->
        <div class="card card-flush card-stretched-vertical" v-for="(listing,i) in showListings" :key="i">
            <div class="row">
            <div class="col-md-4">
                <!-- Card Pinned -->
                <a class="card-pinned" :href="listing.images[0]" data-fslightbox="propertyListGallery1">
                <img class="card-img" :src="listing.images[0]" alt="Image Description">

                <div class="card-pinned-top-start">
                    <span class="badge bg-success">New</span>
                </div>

                <div class="card-pinned-bottom-end">
                    <span class="btn btn-light btn-xs btn-icon">
                    <i class="bi-images"></i>
                    </span>
                </div>
                </a>
                <!-- End Card Pinned -->
                <a class="d-none" href="/assets/img/1920x1080/img20.jpg" data-fslightbox="propertyListGallery1"></a>
                <a class="d-none" href="/assets/img/1920x1080/img17.jpg" data-fslightbox="propertyListGallery1"></a>
                <a class="d-none" href="/assets/img/1920x1080/img16.jpg" data-fslightbox="propertyListGallery1"></a>
            </div>
            <!-- End Col -->

            <div class="col-md-8">
                <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-7">
                    
                        <span class="card-subtitle text-body" v-if="listing.listing_type == 'standard'">For sale</span>
                        <span class="card-subtitle text-body" v-if="listing.listing_type == 'auction'">For auction</span>

                    <h3 class="card-title">
                        <a class="text-dark" href="#" @click.prevent="this.$router.push('/property?listing_id='+listing.id)">{{listing.address}}</a>
                    </h3>
                    </div>
                    <!-- End Col -->

                    <div class="col-md-5 text-md-end">
                    <h3 class="card-title">
                        <a href="../demo-real-estate/property-overview.html">$ {{listing.price}}</a>
                    </h3>
                    </div>
                    <!-- End Col -->
                </div>
                <!-- End Row -->

                <ul class="list-inline list-separator text-body small mb-3">
                    <li class="list-inline-item">
                    <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 640 512"><path d="M176 256c44.11 0 80-35.89 80-80s-35.89-80-80-80-80 35.89-80 80 35.89 80 80 80zm352-128H304c-8.84 0-16 7.16-16 16v144H64V80c0-8.84-7.16-16-16-16H16C7.16 64 0 71.16 0 80v352c0 8.84 7.16 16 16 16h32c8.84 0 16-7.16 16-16v-48h512v48c0 8.84 7.16 16 16 16h32c8.84 0 16-7.16 16-16V240c0-61.86-50.14-112-112-112z"/></svg>
                    </span>
                    {{listing.bedrooms}} bed
                    </li>
                    <li class="list-inline-item">
                    <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 512 512"><path d="M304,320a16,16,0,1,0,16,16A16,16,0,0,0,304,320Zm32-96a16,16,0,1,0,16,16A16,16,0,0,0,336,224Zm32,64a16,16,0,1,0-16-16A16,16,0,0,0,368,288Zm-32,32a16,16,0,1,0-16-16A16,16,0,0,0,336,320Zm-32-64a16,16,0,1,0,16,16A16,16,0,0,0,304,256Zm128-32a16,16,0,1,0-16-16A16,16,0,0,0,432,224Zm-48,16a16,16,0,1,0,16-16A16,16,0,0,0,384,240Zm-16-48a16,16,0,1,0,16,16A16,16,0,0,0,368,192Zm96,32a16,16,0,1,0,16,16A16,16,0,0,0,464,224Zm32-32a16,16,0,1,0,16,16A16,16,0,0,0,496,192Zm-64,64a16,16,0,1,0,16,16A16,16,0,0,0,432,256Zm-32,32a16,16,0,1,0,16,16A16,16,0,0,0,400,288Zm-64,64a16,16,0,1,0,16,16A16,16,0,0,0,336,352Zm-32,32a16,16,0,1,0,16,16A16,16,0,0,0,304,384Zm64-64a16,16,0,1,0,16,16A16,16,0,0,0,368,320Zm21.65-218.35-11.3-11.31a16,16,0,0,0-22.63,0L350.05,96A111.19,111.19,0,0,0,272,64c-19.24,0-37.08,5.3-52.9,13.85l-10-10A121.72,121.72,0,0,0,123.44,32C55.49,31.5,0,92.91,0,160.85V464a16,16,0,0,0,16,16H48a16,16,0,0,0,16-16V158.4c0-30.15,21-58.2,51-61.93a58.38,58.38,0,0,1,48.93,16.67l10,10C165.3,138.92,160,156.76,160,176a111.23,111.23,0,0,0,32,78.05l-5.66,5.67a16,16,0,0,0,0,22.62l11.3,11.31a16,16,0,0,0,22.63,0L389.65,124.28A16,16,0,0,0,389.65,101.65Z"/></svg>
                    </span>
                    {{listing.bathrooms}} bath
                    </li>
                    <li class="list-inline-item">
                    <i class="bi-rulers text-muted me-1"></i> {{listing.property_size}} sqft
                    </li>
                </ul>

                <p class="card-text">{{listing.description}}</p>

                <div class="card-footer">
                    <div class="row align-items-center">
                    <div class="col-lg mb-2 mb-lg-0">
                        <!-- Media -->
                        <div class="d-flex">
                        <!-- <div class="flex-shrink-0">
                            <img class="avatar avatar-sm avatar-circle" src="/assets/img/160x160/img9.jpg" alt="Image Description" title="Monica Fox">
                        </div> -->

                        <div class="flex-grow-1 ms-3">
                            <p class="card-text small mb-0">Listed on {{listing.created}} by</p>
                            <a class="card-link link-dark" href="#">{{listing.listed_by}}</a>
                        </div>
                        </div>
                        <!-- End Media -->
                    </div>
                    <!-- End Col -->

                    <div class="col-lg-auto">
                        <!-- Contacts -->
                        <div class="d-flex gap-2">
                        <a class="btn btn-ghost-secondary btn-sm" href="javascript:;">
                            <i class="bi-telephone-inbound-fill me-1"></i> (0161) 347 8854
                        </a>
                        <a class="btn btn-ghost-secondary btn-sm" href="javascript:;">
                            <i class="bi-envelope-fill me-1"></i> Contact
                        </a>
                        <a class="btn btn-ghost-secondary btn-sm" href="javascript:;">
                            <i class="bi-star-fill me-1"></i> Save
                        </a>
                        </div>
                        <!-- End Contacts -->
                    </div>
                    <!-- End Col -->
                    </div>
                    <!-- End Row -->
                </div>
                </div>
            </div>
            <!-- End Col -->
            </div>
            <!-- End Row -->
        </div>
        <!-- End Card -->
    </div>
    <div v-else>
      <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 mb-5">
        <div class="col mb-3"  v-for="(listing, i) in showListings" :key="i">
          <!-- Card -->

          <div class="card card-flush shadow-none h-100">
            <a class="card-pinned" :href="listing.images[0]" data-fslightbox="propertyGridGallery1">
              <img class="card-img" :src="listing.images[0]" alt="Image Description">

              <div class="card-pinned-top-start">
                <span class="badge bg-success">New</span>
              </div>

              <div class="card-pinned-bottom-end">
                <span class="btn btn-light btn-xs btn-icon">
                  <i class="bi-images"></i>
                </span>
              </div>
            </a>

            <a class="d-none" href="../assets/img/1920x1080/img20.jpg" data-fslightbox="propertyGridGallery1"></a>
            <a class="d-none" href="../assets/img/1920x1080/img17.jpg" data-fslightbox="propertyGridGallery1"></a>
            <a class="d-none" href="../assets/img/1920x1080/img16.jpg" data-fslightbox="propertyGridGallery1"></a>

            <!-- Body -->
            <a class="card-body" href="#" @click.prevent="this.$router.push('/property?listing_id='+listing.id)">
              <span class="card-subtitle text-body">{{listing.listing_type}}</span>

              <div class="row align-items-center mb-3">
                <div class="col">
                  <h4 class="card-title text-inherit">{{listing.address}}</h4>
                </div>
                <!-- End Col -->

                <div class="col-auto">
                  <h3 class="card-title text-primary">${{listing.price}}</h3>
                </div>
                <!-- End Col -->
              </div>
              <!-- End Row -->

              <ul class="list-inline list-separator text-body small">
                <li class="list-inline-item">
                  <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24"><path d="M22,19.5a.5.5,0,0,1-.5.5h-1a.5.5,0,0,1-.5-.5V16H4v3.5a.5.5,0,0,1-.5.5h-1a.5.5,0,0,1-.5-.5V4.5A.5.5,0,0,1,2.5,4h1a.5.5,0,0,1,.5.5V13H21a1,1,0,0,1,1,1ZM20,8H12a2,2,0,0,0-2,2v1.5a.5.5,0,0,0,.5.5h11a.5.5,0,0,0,.5-.5V10A2,2,0,0,0,20,8ZM5.5,12h3a.5.5,0,0,0,.5-.5V11a2,2,0,0,0-4,0v.5A.5.5,0,0,0,5.5,12Z"/></svg>
                  </span>
                  {{listing.bedrooms}} bed
                </li>
                <li class="list-inline-item">
                  <span class="svg-icon svg-icon-xs svg-inline text-muted me-1">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 512 512"><path d="M304,320a16,16,0,1,0,16,16A16,16,0,0,0,304,320Zm32-96a16,16,0,1,0,16,16A16,16,0,0,0,336,224Zm32,64a16,16,0,1,0-16-16A16,16,0,0,0,368,288Zm-32,32a16,16,0,1,0-16-16A16,16,0,0,0,336,320Zm-32-64a16,16,0,1,0,16,16A16,16,0,0,0,304,256Zm128-32a16,16,0,1,0-16-16A16,16,0,0,0,432,224Zm-48,16a16,16,0,1,0,16-16A16,16,0,0,0,384,240Zm-16-48a16,16,0,1,0,16,16A16,16,0,0,0,368,192Zm96,32a16,16,0,1,0,16,16A16,16,0,0,0,464,224Zm32-32a16,16,0,1,0,16,16A16,16,0,0,0,496,192Zm-64,64a16,16,0,1,0,16,16A16,16,0,0,0,432,256Zm-32,32a16,16,0,1,0,16,16A16,16,0,0,0,400,288Zm-64,64a16,16,0,1,0,16,16A16,16,0,0,0,336,352Zm-32,32a16,16,0,1,0,16,16A16,16,0,0,0,304,384Zm64-64a16,16,0,1,0,16,16A16,16,0,0,0,368,320Zm21.65-218.35-11.3-11.31a16,16,0,0,0-22.63,0L350.05,96A111.19,111.19,0,0,0,272,64c-19.24,0-37.08,5.3-52.9,13.85l-10-10A121.72,121.72,0,0,0,123.44,32C55.49,31.5,0,92.91,0,160.85V464a16,16,0,0,0,16,16H48a16,16,0,0,0,16-16V158.4c0-30.15,21-58.2,51-61.93a58.38,58.38,0,0,1,48.93,16.67l10,10C165.3,138.92,160,156.76,160,176a111.23,111.23,0,0,0,32,78.05l-5.66,5.67a16,16,0,0,0,0,22.62l11.3,11.31a16,16,0,0,0,22.63,0L389.65,124.28A16,16,0,0,0,389.65,101.65Z"/></svg>
                  </span>
                  {{listing.bathrooms}} bath
                </li>
                <li class="list-inline-item">
                  <i class="bi-rulers text-muted me-1"></i> {{listing.property_size}} sqft
                </li>
              </ul>
            </a>
            <!-- End Body -->
          </div>
          <!-- End Card -->
        </div>
        <!-- End Col -->
      </div>
    </div>
    </div>

      <!-- Pagination -->
      <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
          <li class="page-item">
            <a class="page-link" href="#" aria-label="Previous" @click.prevent="setPreviousPage()">
              <span aria-hidden="true">
                <i class="bi-chevron-double-left small"></i>
              </span>
            </a>
          </li>
          <span v-for="(pag,i) in pages" :key="i">
          <li class="page-item" :class="{active:isCurrentPage(i)}"><a class="page-link" href="#" @click.prevent="setPage(i)">{{i+1}}</a></li>
          </span>
          <li class="page-item">
            <a class="page-link" href="#" aria-label="Next" @click.prevent="setNextPage()">
              <span aria-hidden="true">
                <i class="bi-chevron-double-right small"></i>
              </span>
            </a>
          </li>
        </ul>
      </nav>
      <!-- End Pagination -->
    </div>
    <!-- End Card List -->
</template>
<style></style>
<script>
import axios from 'axios'
export default {
    name: "ListingsComponent",
    data () {
        return {
            listings: [],
            listItemsPerPage: 20,
            gridItemsPerPage: 30,
            currentPage: 0
        }
    },
    props:["grid"],
    computed:{
      countHomes(){
        return this.listings.length
      },
      pages (){
        if (this.grid){
          return Math.ceil(this.countHomes/this.gridItemsPerPage)
        }else{
          return Math.ceil(this.countHomes/this.listItemsPerPage)
        }
      },
      showListings(){
        if (this.grid){
          return this.listings.slice(this.gridItemsPerPage*this.currentPage,this.gridItemsPerPage*this.currentPage+this.gridItemsPerPage)
        }else{
          return this.listings.slice(this.listItemsPerPage*this.currentPage,this.listItemsPerPage*this.currentPage+this.listItemsPerPage)
        }
        
      }
    },
    methods:{
      isCurrentPage(i){
        return i == this.currentPage
      },
      setPage(i){
        this.currentPage=i;
        this.scrollToTop()
      },
      setPreviousPage(){
        if (this.currentPage>0){
          this.currentPage-=1;
          this.scrollToTop()
        }
      },
      setNextPage(){
        if (this.currentPage<this.pages-1){
          this.currentPage+=1;
          this.scrollToTop()
        }
      }
    },
    mounted(){
        axios.get("/api/listings").then((response) => {
            console.log(response.data)
            for (let i = 0; i < response.data.data.length; i++){
              this.listings.unshift(response.data.data[i])
            }
            
            for (let i = 0; i<this.listings.length;i++){
              this.listings[i].created = this.listings[i].created.slice(0,this.getCharPosition(this.listings[i].created, " ", 4))
              axios.get("/api/users/"+this.listings[i].created_by+"/public").then((response)=>{
                this.listings[i].listed_by = response.data.data.first_name + " "+ response.data.data.last_name+"."
              }).catch((err)=>{
                console.log(err)
              })
            }
            
            // for (var i = 0 ; i<100; i++){
            //   this.listings = this.listings.concat(response.data.data)
            // }
            
        })
    }
}
</script>
