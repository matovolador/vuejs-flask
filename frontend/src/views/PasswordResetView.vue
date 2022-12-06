<template>
  <section id="signin" class="sign">
  <main class="form-sign form-signin">
    <PasswordResetComponent/>
  </main> 
</section>
</template>
<style lang="scss" scoped>
.sign {
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

  .form-sign {
    width: 100%;
    max-width: 360px;
    padding: 15px;
  
    .logo {
      border-radius: 6px;
      margin: 0 auto 1.5rem;
      display: block;
      --logo-size: 80px;
      height: var(--logo-size);
      width: var(--logo-size);
      object-fit: contain;
    }
    
    .h2 {
      text-align: center;
      margin-bottom: 1.5rem;
    }    
    
    .form-floating {
      margin-bottom: 6px;
      &:focus-within {
        z-index: 2;
      }
      .form-control {
        height: 3.3rem;
      }
      & > label {
        padding: .8rem 1rem;
      }
      @media (max-width: 767px){
        .form-control {
        height: 3rem;
      }
      & > label {
        padding: .7rem 1rem;
      }
      }
    }    
    
    input[type="email"] {
      margin-bottom: -1px;
      border-bottom-right-radius: 0;
      border-bottom-left-radius: 0;
    }
    
    input[type="password"] {
      margin-bottom: 10px;
      border-top-left-radius: 0;
      border-top-right-radius: 0;
    }
  }

  .remember {
    margin: 1rem 0 1.5rem;
  }

  .divider {
    position: relative;
    text-align: center;
    margin: 1rem 0;
    &:before, &:after {
      content:"";
      position: absolute;
      top: .8rem;
      height: 2px;
      width: calc(50% - 1.5rem);
      background-color: rgba(0,0,0,0.1);
    }
    &:before {
      left: 0;
    }
    &:after {
      right: 0;
    }
  }
  
  .btn-sign-google {
    position: relative;
    i {
      position: absolute;
      left: 1rem;
      top: 50%;
      transform: translateY(-50%);
    }
    span {
      padding: 0 2rem;
    }
  }
}

#signup {
  .user-type {
    margin: 1rem 0;
  }
}
</style>
  <script>
  // @ is an alias to /src
  import PasswordResetComponent from "@/components/PasswordResetComponent.vue";
  
  export default {
    name: "PasswordResetView",
    components: {
      PasswordResetComponent,
    },
    mounted(){
      this.scrollToTop()
    }
  };
  </script>