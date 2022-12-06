<template>
  <section id="admin-panel" class="admin">
  <main>
    <AdminComponent />
  </main> 
</section>
</template>
<style lang="scss" scoped>
.admin {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 6rem;
  padding-bottom: 6rem;
  background-color: #f5f5f5;
  @media(max-width: 767px){
    padding-top: 2rem;
  }
}
</style>
<script>
  // @ is an alias to /src
  import AdminComponent from "@/components/AdminComponent.vue";
  
  export default {
    name: "AdminView",
    components: {
      AdminComponent
    },
    data(){
      return {
       
      }
    },
    mounted(){
      // TODO DETERMINE IF ITS STANDARD OR AUCTION
      this.scrollToTop()
    }
  };
  </script>