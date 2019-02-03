import Vue from 'vue'
import VueRouter from 'vue-router'

import DashboardPage from '../components/dashboard/dashboard.vue'
import NotFound from '../components/NotFound'
import RegisterPage from '../components/auth/register.vue'
import LoginPage from '../components/auth/login.vue'
import HomePage from '../components/home/home.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: HomePage },
  { path: '/register', component: RegisterPage },
  { path: '/login', component: LoginPage },
  { path: '/dashboard', component: DashboardPage },
  { path: '*', component: NotFound }
]

export default new VueRouter({ mode: 'history', routes })
