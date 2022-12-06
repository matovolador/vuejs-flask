<template>
  <!-- ========== HEADER ========== -->
  <header id="header" class="navbar navbar-expand-lg navbar-end navbar-absolute-top navbar-light">
    <div class="container">
      <nav class="js-mega-menu navbar-nav-wrap">
        <!-- Default Logo -->
        <a class="navbar-brand" href="#" aria-label="Front">
          <img class="navbar-brand-logo" src="/assets/svg/logos/logo.svg" alt="Logo">
        </a>
        <!-- End Default Logo -->

        <!-- Toggler -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-default">
            <i class="bi-list"></i>
          </span>
          <span class="navbar-toggler-toggled">
            <i class="bi-x"></i>
          </span>
        </button>
        <!-- End Toggler -->
      
        <!-- Collapse -->
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link " href="#" @click.prevent="">Home</a>
            </li>

            <!-- Dropdown -->
            <li class="hs-has-sub-menu nav-item">
              <a id="listingsDropdown" class="hs-mega-menu-invoker nav-link dropdown-toggle active" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Listings</a>
              <div class="hs-sub-menu dropdown-menu" aria-labelledby="listingsDropdown" style="min-width: 14rem;">
                <a class="dropdown-item mousePointer" :class="{active:isPlain}" @click="listingPlain()">Listing</a>
                <a class="dropdown-item mousePointer" :class="{active:!isPlain}" @click="listingGrid()">Listing (Grid)</a>
              </div>
            </li>
            <!-- End Dropdown -->
            <li class="nav-item">
              <a class="btn btn-primary btn-transition" href="#" @click.prevent="this.$router.push('/create_listing')">Start selling</a>
            </li>
            <li class="nav-item">
              <a class="btn btn-primary btn-transition" v-if="!this.isLoggedIn" @click.prevent="this.$router.push('/login')">Sign In</a>
              <a class="btn btn-primary btn-transition" v-else @click.prevent="this.$router.push('/logout')">Sign Out</a>
            </li>
          </ul>
        </div>
        <!-- End Collapse -->
      </nav>
    </div>
  </header>
  
  <!-- ========== END HEADER ========== -->
  <router-view />
  <div class="row" v-if="this.isLoggedIn">
    <span>{{this.user}}</span>
  </div>
  <!-- ========== FOOTER ========== -->
  <footer class="bg-dark">
    <div class="container pb-1 pb-lg-5">
      <div class="row content-space-t-2">
        <div class="col-lg-3 mb-7 mb-lg-0">
          <!-- Logo -->
          <div class="mb-5">
            <a class="navbar-brand" href="#" aria-label="Space">
              <img class="navbar-brand-logo" src="/assets/svg/logos/logo-white.svg" alt="Image Description">
            </a>
          </div>
          <!-- End Logo -->

          <!-- List -->
          <ul class="list-unstyled list-py-1">
            <li><a class="link-sm link-light" href="#"><i class="bi-geo-alt-fill me-1"></i> 153 Williamson Plaza, Maggieberg</a></li>
            <li><a class="link-sm link-light" href="tel:1-062-109-9222"><i class="bi-telephone-inbound-fill me-1"></i> +1 (062) 109-9222</a></li>
          </ul>
          <!-- End List -->
        
        </div>
        <!-- End Col -->

        <div class="col-sm mb-7 mb-sm-0">
          <h5 class="text-white mb-3">Company</h5>

          <!-- List -->
          <ul class="list-unstyled list-py-1 mb-0">
            <li><a class="link-sm link-light" href="#">About</a></li>
            <li><a class="link-sm link-light" href="#">Careers <span class="badge bg-warning text-dark rounded-pill ms-1">We're hiring</span></a></li>
            <li><a class="link-sm link-light" href="#">Blog</a></li>
            <li><a class="link-sm link-light" href="#">Customers <i class="bi-box-arrow-up-right small ms-1"></i></a></li>
            <li><a class="link-sm link-light" href="#">Hire us</a></li>
          </ul>
          <!-- End List -->
        </div>
        <!-- End Col -->

        <div class="col-sm mb-7 mb-sm-0">
          <h5 class="text-white mb-3">Features</h5>

          <!-- List -->
          <ul class="list-unstyled list-py-1 mb-0">
            <li><a class="link-sm link-light" href="#">Press <i class="bi-box-arrow-up-right small ms-1"></i></a></li>
            <li><a class="link-sm link-light" href="#">Release Notes</a></li>
            <li><a class="link-sm link-light" href="#">Integrations</a></li>
            <li><a class="link-sm link-light" href="#">Pricing</a></li>
          </ul>
          <!-- End List -->
        </div>
        <!-- End Col -->

        <div class="col-sm mb-7 mb-sm-0">
          <h5 class="text-white mb-3">Documentation</h5>

          <!-- List -->
          <ul class="list-unstyled list-py-1 mb-0">
            <li><a class="link-sm link-light" href="#">Support</a></li>
            <li><a class="link-sm link-light" href="#">Docs</a></li>
            <li><a class="link-sm link-light" href="#">Status</a></li>
            <li><a class="link-sm link-light" href="#" @click.prevent="this.$router.push('/admin')">Admin Panel</a></li>
            <li><a class="link-sm link-light" href="#">Tech Requirements</a></li>
          </ul>
          <!-- End List -->
        </div>
        <!-- End Col -->

        <div class="col-sm">
          <h5 class="text-white mb-3">Resources</h5>

          <!-- List -->
          <ul class="list-unstyled list-py-1 mb-5">
            <li><a class="link-sm link-light" href="#"><i class="bi-question-circle-fill me-1"></i> Help</a></li>
            <li><a class="link-sm link-light" href="#"><i class="bi-person-circle me-1"></i> Your Account</a></li>
          </ul>
          <!-- End List -->
        </div>
        <!-- End Col -->
      </div>
      <!-- End Row -->

      <div class="border-top border-white-10 my-7"></div>

      <div class="row mb-7">
        <div class="col-sm mb-3 mb-sm-0">
          <!-- Socials -->
          <ul class="list-inline list-separator list-separator-light mb-0">
            <li class="list-inline-item">
              <a class="link-sm link-light" href="#">Privacy &amp; Policy</a>
            </li>
            <li class="list-inline-item">
              <a class="link-sm link-light" href="#">Terms</a>
            </li>
            <li class="list-inline-item">
              <a class="link-sm link-light" href="#">Site Map</a>
            </li>
          </ul>
          <!-- End Socials -->
        </div>

        <div class="col-sm-auto">
          <!-- Socials -->
          <ul class="list-inline mb-0">
            <li class="list-inline-item">
              <a class="btn btn-soft-light btn-xs btn-icon" href="#">
                <i class="bi-facebook"></i>
              </a>
            </li>
          
            <li class="list-inline-item">
              <a class="btn btn-soft-light btn-xs btn-icon" href="#">
                <i class="bi-google"></i>
              </a>
            </li>
          
            <li class="list-inline-item">
              <a class="btn btn-soft-light btn-xs btn-icon" href="#">
                <i class="bi-twitter"></i>
              </a>
            </li>
          
            <li class="list-inline-item">
              <a class="btn btn-soft-light btn-xs btn-icon" href="#">
                <i class="bi-github"></i>
              </a>
            </li>
          
            <li class="list-inline-item">
              <!-- Button Group -->
              <div class="btn-group">
                <button type="button" class="btn btn-soft-light btn-xs dropdown-toggle" id="footerSelectLanguage" data-bs-toggle="dropdown" aria-expanded="false" data-bs-dropdown-animation>
                  <span class="d-flex align-items-center">
                    <img class="avatar avatar-xss avatar-circle me-2" src="/assets/vendor/flag-icon-css/flags/1x1/us.svg" alt="Image description" width="16"/>
                    <span>English (US)</span>
                  </span>
                </button>

                <div class="dropdown-menu" aria-labelledby="footerSelectLanguage">
                  <a class="dropdown-item d-flex align-items-center active" href="#">
                    <img class="avatar avatar-xss avatar-circle me-2" src="/assets/vendor/flag-icon-css/flags/1x1/us.svg" alt="Image description" width="16"/>
                    <span>English (US)</span>
                  </a>
                  <a class="dropdown-item d-flex align-items-center" href="#">
                    <img class="avatar avatar-xss avatar-circle me-2" src="/assets/vendor/flag-icon-css/flags/1x1/de.svg" alt="Image description" width="16"/>
                    <span>Deutsch</span>
                  </a>
                  <a class="dropdown-item d-flex align-items-center" href="#">
                    <img class="avatar avatar-xss avatar-circle me-2" src="/assets/vendor/flag-icon-css/flags/1x1/es.svg" alt="Image description" width="16"/>
                    <span>Español</span>
                  </a>
                  <a class="dropdown-item d-flex align-items-center" href="#">
                    <img class="avatar avatar-xss avatar-circle me-2" src="/assets/vendor/flag-icon-css/flags/1x1/cn.svg" alt="Image description" width="16"/>
                    <span>中文 (繁體)</span>
                  </a>
                </div>
              </div>
              <!-- End Button Group -->
            </li>
          </ul>
          <!-- End Socials -->
        </div>
      </div>

      <!-- Copyright -->
      <div class="w-md-85 text-lg-center mx-lg-auto">
        <p class="text-white-50 small">&copy; Front. 2021 Htmlstream. All rights reserved.</p>
        <p class="text-white-50 small">When you visit or interact with our sites, services or tools, we or our authorised service providers may use cookies for storing information to help provide you with a better, faster and safer experience and for marketing purposes.</p>
      </div>
      <!-- End Copyright -->
    </div>
    <!-- <router-link to="/login" v-if="!this.loggedIn">Login</router-link> | 
    <router-link to="/logout" v-if="this.loggedIn">Logout</router-link>
    <div v-if="loggedIn">
      {{this.userObj}}
    </div> -->
  </footer>

  <!-- ========== END FOOTER ========== -->

  <!-- ========== SECONDARY CONTENTS ========== -->
  <!-- Real Estate More Filters Modal -->
  <div class="modal fade" id="realEstateMoreFiltersModal" tabindex="-1" aria-labelledby="realEstateMoreFiltersModalLabel" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <!-- Header -->
        <div class="modal-header">
          <h3 class="modal-title" id="realEstateMoreFiltersModalLabel">More filters</h3>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <!-- End Header -->

        <!-- Body -->
        <div class="modal-body">
          <label class="input-label">Status</label>

          <!-- Radio Button Group -->
          <div class="btn-group btn-group-segment d-flex mb-4" role="group" aria-label="Status radio button group">
            <input type="radio" class="btn-check flex-fill" name="statusBtnRadioMoreFilters" id="statusBtnRadioBuyMoreFilters" autocomplete="off" checked>
            <label class="btn btn-sm" for="statusBtnRadioBuyMoreFilters">Buy</label>

            <input type="radio" class="btn-check flex-fill" name="statusBtnRadioMoreFilters" id="statusBtnRadioRentMoreFilters" autocomplete="off">
            <label class="btn btn-sm" for="statusBtnRadioRentMoreFilters">Rent</label>

            <input type="radio" class="btn-check flex-fill" name="statusBtnRadioMoreFilters" id="statusBtnRadioSoldMoreFilters" autocomplete="off">
            <label class="btn btn-sm" for="statusBtnRadioSoldMoreFilters">Sold</label>
          </div>
          <!-- End Radio Button Group -->

          <div class="mb-4">
            <label for="featuresLabelMoreFilters" class="form-label">Features</label>

            <!-- Select -->
            <select id="featuresLabelMoreFilters" class="js-select form-select" multiple
                    data-hs-tom-select-options='{
                      "hideSearch": true
                    }'>
              <option value="bedValueAny" selected>Any</option>
              <option value="Pets allowed">Pets allowed</option>
              <option value="Parking lot">Parking lot</option>
              <option value="Balcony">Balcony</option>
              <option value="Garden">Garden</option>
              <option value="Laundry">Laundry</option>
              <option value="Heating">Heating</option>
              <option value="AC">AC</option>
            </select>
            <!-- End Select -->
          </div>

          <div class="row gx-3">
            <div class="col-6">
              <div class="mb-4">
                <label for="bedsLabelMoreFilters" class="form-label">Beds</label>

                <!-- Select -->
                <select id="bedsLabelMoreFilters" class="js-select form-select"
                        data-hs-tom-select-options='{
                          "hideSearch": true
                        }'>
                  <option value="bedValueAny" selected>Any</option>
                  <option value="bedValueMin1">1</option>
                  <option value="bedValueMin2">2</option>
                  <option value="bedValueMin3">3</option>
                  <option value="bedValueMin4">4</option>
                  <option value="bedValueMin5">5</option>
                </select>
                <!-- End Select -->
              </div>
            </div>
            <!-- End Col -->

            <div class="col-6">
              <div class="mb-4">
                <label for="bathLabelMoreFilters" class="form-label">Baths</label>

                <!-- Select -->
                <select id="bathLabelMoreFilters" class="js-select form-select"
                        data-hs-tom-select-options='{
                          "hideSearch": true
                        }'>
                  <option value="bedValueAny" selected>Any</option>
                  <option value="bedValueMax1">1</option>
                  <option value="bedValueMax2">2</option>
                  <option value="bedValueMax3">3</option>
                  <option value="bedValueMax4">4</option>
                  <option value="bedValueMax5">5</option>
                </select>
                <!-- End Select -->
              </div>
            </div>
            <!-- End Col -->
          </div>
          <!-- End Row -->

          <label for="squareFeetLabelMoreFilters" class="form-label">Square feet</label>

          <div class="row gx-3">
            <div class="col-6">
              <div class="mb-4">
                <input type="text" class="form-control" id="squareFeetLabelMoreFilters" placeholder="No min">
              </div>
            </div>
            <!-- End Col -->

            <div class="col-6">
              <div class="mb-4">
                <input type="text" class="form-control" placeholder="No max">
              </div>
            </div>
            <!-- End Col -->
          </div>
          <!-- End Row -->

          <div class="mb-4">
            <label for="lotSizeLabelMoreFilters" class="form-label">Lot size</label>

            <!-- Select -->
            <select id="lotSizeLabelMoreFilters" class="js-select form-select"
                    data-hs-tom-select-options='{
                      "hideSearch": true
                    }'>
              <option value="No Min">No Min</option>
              <option value="2000+ sqft">2000+ sqft</option>
              <option value="3000+ sqft">3000+ sqft</option>
              <option value="4000+ sqft">4000+ sqft</option>
              <option value="5000+ sqft">5000+ sqft</option>
              <option value="7500+ sqft">7500+ sqft</option>
              <option value="0.25+ acre / 10890+ sqft">0.25+ acre / 10890+ sqft</option>
              <option value="0.5+ acre / 21780+ sqft">0.5+ acre / 21780+ sqft</option>
              <option value="1+ acre">1+ acre</option>
              <option value="2+ acre">2+ acre</option>
              <option value="5+ acre">5+ acre</option>
              <option value="10+ acre">10+ acre</option>
            </select>
            <!-- End Select -->
          </div>

          <div class="mb-4">
            <label for="yearBuiltLabelMoreFilters" class="form-label">Year built</label>

            <div class="row gx-3">
              <div class="col-6">
                <input type="text" class="form-control" id="yearBuiltLabelMoreFilters" placeholder="Min year">
              </div>
              <!-- End Col -->

              <div class="col-6">
                <input type="text" class="form-control" placeholder="Max year">
              </div>
              <!-- End Col -->
            </div>
            <!-- End Row -->
          </div>
        </div>
        <!-- End Body -->

        <div class="card-footer border-top">
          <div class="d-flex justify-content-end gap-3">
            <a class="btn btn-white" href="#">Clear</a>
            <a class="btn btn-primary" href="#">Show 100+ homes</a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Go To -->
  <a class="js-go-to go-to position-fixed" href="javascript:;" style="visibility: hidden;"
     data-hs-go-to-options='{
       "offsetTop": 700,
       "position": {
         "init": {
           "right": "2rem"
         },
         "show": {
           "bottom": "2rem"
         },
         "hide": {
           "bottom": "-2rem"
         }
       }
     }'>
    <i class="bi-chevron-up"></i>
  </a>
  <!-- ========== END SECONDARY CONTENTS ========== -->

</template>
<script>
import axios from 'axios'

export default{
  data () {
    return {
      isPlain:true
    }
    
  },
  methods:{
    listingPlain(){
      this.isPlain=true
      this.$router.push("/")
      
    },
    listingGrid(){
      this.isPlain=false
      this.$router.push("/grid")
      
    },
  },  
  computed:{
    userObj(){
      return this.user
    },
    loggedIn(){
      return this.isLoggedIn
    } 
  },
  mounted(){
    
    setInterval(() => {
      if (this.isLoggedIn){
          axios.get("/api/renew-token",{
              headers:{
                  "x-access-token": this.xAccessToken
              }
          }).then((response) => {
              this.setCookieToken(response.data.token)              
          }).catch((err)=>{
            console.log(err)
            this.$cookies.remove("user")
            this.setCookieToken("")
          })
      }
    },60000*2)
  }

}

</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
