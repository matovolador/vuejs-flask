<template>
  <!-- ========== MAIN CONTENT ========== -->
  <main id="content" role="main">
    <!-- Filter Form -->
    <div class="container content-space-t-3 content-space-t-lg-4">
      <form>
        <div class="row gx-2">
          <div class="col-lg mb-2 mb-lg-0">
            <!-- Form -->
            <label for="searchPropertyFilterForm" class="visually-hidden form-label">Search property</label>
            <div class="input-group input-group-merge">
              <span class="input-group-prepend input-group-text">
                <i class="bi-search"></i>
              </span>
              <input type="text" class="form-control form-control-sm" id="searchPropertyFilterForm" placeholder="Search property" aria-label="Search property" value="London, England">
            </div>
            <!-- End Form -->
          </div>
          <!-- End Col -->

          <div class="col-auto mb-2 mb-lg-0">
            <!-- Dropdown -->
            <div class="dropdown">
              <a class="btn btn-white btn-sm dropdown-toggle" href="#" id="priceFilterFormDropdown" role="button" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">Price</a>

              <div class="dropdown-menu dropdown-menu-end dropdown-card" aria-labelledby="priceFilterFormDropdown" style="min-width: 21rem;">
                <!-- Card -->
                <div class="card card-sm">
                  <div class="card-body">
                    <!-- Bar Chart -->
                    <div class="position-relative overflow-hidden" style="height: 6rem; width: 18rem;">
                      <div class="position-absolute w-100 overflow-hidden">
                        <div style="height: 6rem; width: 18rem;">
                          <canvas class="js-chart"
                                  width='300px'
                                  data-hs-chartjs-options='{
                                    "type": "bar",
                                    "data": {
                                      "labels": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                                      "datasets": [{
                                        "data": [2, 3, 5, 7, 8, 5, 3, 2, 3, 6, 5, 4, 7, 5, 4, 3, 2],
                                        "backgroundColor": "#e7eaf3",
                                        "borderColor": "#e7eaf3"
                                      }]
                                    },
                                    "options": {
                                      "animation": {
                                        "duration": 0
                                      },
                                      "responsive": true,
                                      "scales": {
                                        "y": {
                                          "display": false,
                                          "gridLines": {
                                            "display": false,
                                            "drawBorder": false
                                          },
                                          "ticks": {
                                            "beginAtZero": true
                                          }
                                        },
                                        "x": {
                                          "display": false,
                                          "gridLines": {
                                            "display": false,
                                            "drawBorder": false
                                          }
                                        }
                                      },
                                      "plugins": {
                                        "tooltips": {
                                          "custom": false
                                        }
                                      }
                                    }
                                  }'></canvas>
                        </div>
                      </div>

                      <div id="foregroundBarChartDoubleResult" class="position-absolute overflow-hidden">
                        <div style="height: 6rem; width: 18rem;">
                          <canvas class="js-chart"
                                  data-hs-chartjs-options='{
                                    "type": "bar",
                                    "data": {
                                      "labels": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                                      "datasets": [{
                                        "data": [2, 3, 5, 7, 8, 5, 3, 2, 3, 6, 5, 4, 7, 5, 4, 3, 2],
                                        "backgroundColor": "#377dff",
                                        "borderColor": "#377dff"
                                      }]
                                    },
                                    "options": {
                                      "animation": {
                                        "duration": 0
                                      },
                                      "scales": {
                                        "y": {
                                          "display": false,
                                          "gridLines": {
                                            "display": false,
                                            "drawBorder": false
                                          },
                                          "ticks": {
                                            "beginAtZero": true
                                          }
                                        },
                                        "x": {
                                          "display": false,
                                          "gridLines": {
                                            "display": false,
                                            "drawBorder": false
                                          }
                                        }
                                      },
                                      "plugins": {
                                        "tooltips": {
                                          "custom": false
                                        }
                                      }
                                    }
                                  }'></canvas>
                        </div>
                      </div>
                    </div>
                    <!-- End Bar Chart -->

                    <div class="range-slider">
                      <div class="js-nouislider"
                           data-hs-nouislider-options='{
                               "range": {
                                 "min": 0,
                                 "max": 1000
                               },
                               "start": [250, 750],
                               "result_min_target_el": "#rangeSliderExampleDouble4MinResult",
                               "result_max_target_el": "#rangeSliderExampleDouble4MaxResult",
                               "foreground_target_el": "#foregroundBarChartDoubleResult"
                             }'>
                      </div>
                    </div>

                    <div class="row justify-content-center mt-5">
                      <div class="col">
                        <span class="d-block small mb-1">Min price:</span>
                        <input type="text" class="form-control form-control-sm" id="rangeSliderExampleDouble4MinResult">
                      </div>
                      <!-- End Col -->

                      <div class="col">
                        <span class="d-block small mb-1">Max price:</span>
                        <input type="text" class="form-control form-control-sm" id="rangeSliderExampleDouble4MaxResult">
                      </div>
                      <!-- End Col -->
                    </div>
                    <!-- End Row -->
                  </div>

                  <div class="card-footer border-top">
                    <div class="d-flex justify-content-end gap-2">
                      <a class="btn btn-white btn-sm" href="#">Clear</a>
                      <a class="btn btn-primary btn-sm" href="#">Save</a>
                    </div>
                  </div>
                </div>
                <!-- End Card -->
              </div>
            </div>
            <!-- End Dropdown -->
          </div>
          <!-- End Col -->

          <div class="col-auto mb-2 mb-lg-0">
            <!-- Dropdown -->
            <div class="dropdown">
              <a class="btn btn-white btn-sm dropdown-toggle" href="#" id="bedsFilterFormDropdown" role="button" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">All beds</a>

              <div class="dropdown-menu dropdown-menu-end dropdown-card" aria-labelledby="bedsFilterFormDropdown" style="min-width: 25rem;">
                <!-- Card -->
                <div class="card card-sm">
                  <div class="card-body">
                    <!-- Radio Button Group -->
                    <div class="btn-group btn-group-segment d-flex" role="group" aria-label="Beds radio button group">
                      <input type="radio" class="btn-check flex-fill" name="bedsBtnRadio" id="bedsBtnRadioStudio" autocomplete="off" checked>
                      <label class="btn btn-sm" for="bedsBtnRadioStudio">Studio</label>

                      <input type="radio" class="btn-check flex-fill" name="bedsBtnRadio" id="bedsBtnRadio1" autocomplete="off">
                      <label class="btn btn-sm" for="bedsBtnRadio1">1+</label>

                      <input type="radio" class="btn-check flex-fill" name="bedsBtnRadio" id="bedsBtnRadio2" autocomplete="off">
                      <label class="btn btn-sm" for="bedsBtnRadio2">2+</label>

                      <input type="radio" class="btn-check flex-fill" name="bedsBtnRadio" id="bedsBtnRadio3" autocomplete="off">
                      <label class="btn btn-sm" for="bedsBtnRadio3">3+</label>

                      <input type="radio" class="btn-check flex-fill" name="bedsBtnRadio" id="bedsBtnRadio4" autocomplete="off">
                      <label class="btn btn-sm" for="bedsBtnRadio4">4+</label>
                    </div>
                    <!-- End Radio Button Group -->
                  </div>
                </div>
                <!-- End Card -->
              </div>
            </div>
            <!-- End Dropdown -->
          </div>
          <!-- End Col -->

          <div class="col-auto mb-2 mb-lg-0">
            <!-- Dropdown -->
            <div class="dropdown">
              <a class="btn btn-white btn-sm dropdown-toggle" href="#" id="propertyTypeFilterFormDropdown" role="button" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">Property type</a>

              <div class="dropdown-menu dropdown-menu-end dropdown-card" aria-labelledby="propertyTypeFilterFormDropdown" style="min-width: 20rem;">
                <!-- Card -->
                <div class="card card-sm">
                  <div class="card-body">
                    <div class="d-grid gap-2">
                      <!-- Check -->
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="propertyTypeHouseCheckbox" checked>
                        <label class="form-check-label" for="propertyTypeHouseCheckbox">
                          House
                          <span class="d-block small text-muted">Find a cozy place</span>
                        </label>
                      </div>
                      <!-- End Check -->

                      <!-- Check -->
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="propertyTypeFlatsCheckbox">
                        <label class="form-check-label" for="propertyTypeFlatsCheckbox">
                          Flats
                          <span class="d-block small text-muted">Flats for sale or to rent</span>
                        </label>
                      </div>
                      <!-- End Check -->

                      <!-- Check -->
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="propertyTypeMultiFamilyCheckbox" checked>
                        <label class="form-check-label" for="propertyTypeMultiFamilyCheckbox">
                          Multi-family
                          <span class="d-block small text-muted">Multi-family houses or flats</span>
                        </label>
                      </div>
                      <!-- End Check -->

                      <!-- Check -->
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="propertyTypeFarmsLandCheckbox">
                        <label class="form-check-label" for="propertyTypeFarmsLandCheckbox">
                          Farms/land
                          <span class="d-block small text-muted">Own a property for farming</span>
                        </label>
                      </div>
                      <!-- End Check -->
                    </div>
                  </div>

                  <div class="card-footer border-top">
                    <div class="d-flex justify-content-end gap-2">
                      <a class="btn btn-white btn-sm" href="#">Clear</a>
                      <a class="btn btn-primary btn-sm" href="#">Save</a>
                    </div>
                  </div>
                </div>
                <!-- End Card -->
              </div>
            </div>
            <!-- End Dropdown -->
          </div>
          <!-- End Col -->

          <div class="col-auto mb-2 mb-lg-0">
            <a class="btn btn-white btn-sm" href="#" data-bs-toggle="modal" data-bs-target="#realEstateMoreFiltersModal">
              <i class="bi-sliders me-2"></i> More
            </a>
          </div>
          <!-- End Col -->
        </div>
        <!-- End Row -->
      </form>
    </div>
    <!-- End Filter Form -->
        <ListingsComponent :grid=true />
  </main>
  <!-- ========== END MAIN CONTENT ========== -->
  
  </template>
  
  <script>
  // @ is an alias to /src
  import ListingsComponent from "@/components/ListingsComponent.vue";
  
  export default {
    name: "ListingsView",
    components: {
      ListingsComponent,
    },
    mounted(){
      this.scrollToTop()
    }
  };
  </script>