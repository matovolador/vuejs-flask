<template>
    <div>
      <LogoutComponent/>
    </div>
  </template>
  
  <script>
  // @ is an alias to /src
  import LogoutComponent from "@/components/LogoutComponent.vue";
  
  export default {
    name: "LogoutView",
    components: {
      LogoutComponent,
    },
  };
  </script>