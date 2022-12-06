<template>
  <section id="signin" class="sign">
  <main class="">
    <VerifyEmailComponent/>
  </main> 
</section>
</template>
<style>
</style>
  <script>
  // @ is an alias to /src
  import VerifyEmailComponent from "@/components/VerifyEmailComponent.vue";
  
  export default {
    name: "VerifyEmailView",
    components: {
      VerifyEmailComponent,
    },
    mounted(){
      this.scrollToTop()
    }
  };
  </script>