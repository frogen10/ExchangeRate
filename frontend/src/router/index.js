import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/dashboard/Dashboard.vue'
import MyAccount from '../views/dashboard/MyAccount.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import AddClient from '../views/dashboard/AddClient.vue'
import EditClient from '../views/dashboard/EditClient.vue'
import Calculator from '../views/dashboard/Calculator.vue'
import Currency from '../views/dashboard/Currency.vue'
import BuyCurrency from '../views/dashboard/BuyCurrency.vue'
import SellCurrency from '../views/dashboard/SellCurrency.vue'

import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account/add',
    name: 'AddClient',
    component: AddClient,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account/:id/edit',
    name: 'EditClient',
    component: EditClient,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/:code',
    name: 'Currency',
    component: Currency,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/:code/buy',
    name: 'BuyCurrency',
    component: BuyCurrency,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/:code/sell',
    name: 'SellCurrency',
    component: SellCurrency,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/calculator',
    name: 'Calculator',
    component: Calculator,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/log-in')
  } else {
    next()
  }
})

export default router
