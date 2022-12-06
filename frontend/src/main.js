import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueCookies from 'vue-cookies';
import { myMixin } from "./mixins";
import 'bootstrap/dist/js/bootstrap.js'
const app = createApp(App).use(store).use(router).use(VueCookies);
app.mixin(myMixin);
app.mount("#app");