import { createRouter, createWebHashHistory } from "vue-router";
import ListingsView from "../views/ListingsView"
import ListingsGridView from "../views/ListingsGridView"
import LoginView from "../views/LoginView"
import LogoutView from "../views/LogoutView"
import RegistrationView from "../views/RegistrationView"
import VerifyEmailView from "../views/VerifyEmailView"
import CreateListingView from "../views/CreateListingView"
import PropertyView from "../views/PropertyView"
import AuthFileView from "../views/AuthFileView"
import AdminView from "../views/AdminView"
import PasswordResetView from "../views/PasswordResetView"

const routes = [
  {
    path: "/",
    name: "home",
    component: ListingsView,
  },
  {
    path: "/grid",
    name: "grid",
    component: ListingsGridView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/logout",
    name: "logout",
    component: LogoutView,
  },
  {
    path: "/register",
    name: "register",
    component: RegistrationView,
  },
  {
    path: "/validate_email",
    name: "validateEmail",
    component: VerifyEmailView,
  },
  {
    path: "/create_listing",
    name: "createListing",
    component: CreateListingView,
  },
  {
    path: "/property",
    name: "property",
    component: PropertyView,
  },
  {
    path: "/authorization",
    name: "authorization",
    component: AuthFileView,
  },
  {
    path: "/password_reset",
    name: "password_reset",
    component: PasswordResetView,
  },
  {
    path: "/admin",
    name: "admin",
    component: AdminView,
  }
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
